#!/usr/bin/env python3
"""Generate ElevenLabs voice-overs for blog posts.

Walks ``content/posts/*.md``, strips markdown to plain prose, and writes an
MP3 per post to ``static/audio/<slug>.mp3``. A sidecar ``<slug>.mp3.hash``
records the SHA-256 of the synthesized text plus voice/model so re-runs skip
unchanged posts. Requires ``ELEVENLABS_API_KEY`` in the environment.

Usage:
    python3 scripts/generate_audio.py [--force] [--post <slug>]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
AUDIO_DIR = ROOT / "static" / "audio"
CACHE_DIR = ROOT / ".audio-cache"

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
VOICE_NAME = "Sarah"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"
CHUNK_CHAR_LIMIT = 4000
MAX_RETRIES = 5
RETRY_BASE_DELAY = 4.0

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip()
    body = text[end + 4 :].lstrip()
    fm: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, body


def markdown_to_speech(md: str) -> str:
    md = re.sub(r"```[\s\S]*?```", "", md)
    md = re.sub(r"(?m)^( {4,}|\t).*$", "", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    md = re.sub(r"\*(.+?)\*", r"\1", md)
    md = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", md)
    md = re.sub(r"`([^`]+)`", r"\1", md)
    md = re.sub(r"(?m)^#{1,6}\s+(.*)$", r"\1.", md)
    md = re.sub(r"(?m)^>\s?", "", md)
    md = re.sub(r"(?m)^-{3,}$", "", md)
    md = re.sub(r"(?m)^\s*[-*]\s+", "", md)
    md = re.sub(r"(?m)^\s*\d+\.\s+", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def chunk_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks: list[str] = []
    cur = ""
    for paragraph in text.split("\n\n"):
        if len(paragraph) > limit:
            if cur:
                chunks.append(cur)
                cur = ""
            sentence_buf = ""
            for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
                if len(sentence_buf) + len(sentence) + 1 <= limit:
                    sentence_buf = f"{sentence_buf} {sentence}".strip()
                else:
                    if sentence_buf:
                        chunks.append(sentence_buf)
                    sentence_buf = sentence
            if sentence_buf:
                cur = sentence_buf
            continue
        candidate = f"{cur}\n\n{paragraph}" if cur else paragraph
        if len(candidate) <= limit:
            cur = candidate
        else:
            chunks.append(cur)
            cur = paragraph
    if cur:
        chunks.append(cur)
    return chunks


def synthesize_chunk(
    text: str, api_key: str, previous_request_ids: list[str]
) -> tuple[bytes, str]:
    url = API_URL.format(voice_id=VOICE_ID) + f"?output_format={OUTPUT_FORMAT}"
    payload: dict[str, object] = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    if previous_request_ids:
        payload["previous_request_ids"] = previous_request_ids[-3:]
    for attempt in range(1, MAX_RETRIES + 1):
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.read(), response.headers.get("request-id", "")
        except urllib.error.HTTPError as err:
            body = err.read().decode(errors="replace")
            transient = err.code in (429, 500, 502, 503, 504)
            if not transient or attempt == MAX_RETRIES:
                raise SystemExit(f"ElevenLabs API error {err.code}: {body}") from err
            retry_after = err.headers.get("retry-after")
            try:
                delay = float(retry_after) if retry_after else RETRY_BASE_DELAY * (2 ** (attempt - 1))
            except ValueError:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
            print(f"    transient {err.code}, retrying in {delay:.1f}s ({attempt}/{MAX_RETRIES - 1})")
            time.sleep(delay)
        except urllib.error.URLError as err:
            if attempt == MAX_RETRIES:
                raise SystemExit(f"ElevenLabs network error: {err}") from err
            delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
            print(f"    network error, retrying in {delay:.1f}s ({attempt}/{MAX_RETRIES - 1})")
            time.sleep(delay)
    raise SystemExit("ElevenLabs: exhausted retries")


def generate_for_post(post_path: Path, api_key: str, force: bool) -> None:
    raw = post_path.read_text(encoding="utf-8")
    frontmatter, body = strip_frontmatter(raw)

    if frontmatter.get("draft", "").lower() == "true":
        print(f"skip {post_path.name} (draft)")
        return
    if frontmatter.get("audio", "").lower() == "false":
        print(f"skip {post_path.name} (audio: false)")
        return

    title = frontmatter.get("title", post_path.stem)
    speech = markdown_to_speech(body)
    speech = f"{title}.\n\n{speech}"

    digest = hashlib.sha256(
        f"{VOICE_ID}|{MODEL_ID}|{speech}".encode()
    ).hexdigest()

    slug = post_path.stem
    out_mp3 = AUDIO_DIR / f"{slug}.mp3"
    out_hash = AUDIO_DIR / f"{slug}.mp3.hash"

    if (
        not force
        and out_mp3.exists()
        and out_hash.exists()
        and out_hash.read_text().strip() == digest
    ):
        print(f"skip {slug} (up-to-date)")
        return

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    chunks = chunk_text(speech, CHUNK_CHAR_LIMIT)
    print(f"generate {slug} ({len(speech):,} chars, {len(chunks)} chunk{'s' if len(chunks) != 1 else ''})")

    audio = bytearray()
    request_ids: list[str] = []
    for index, chunk in enumerate(chunks, 1):
        chunk_digest = hashlib.sha256(
            f"{VOICE_ID}|{MODEL_ID}|{chunk}".encode()
        ).hexdigest()
        cache_file = CACHE_DIR / f"{chunk_digest}.mp3"
        if cache_file.exists():
            print(f"  chunk {index}/{len(chunks)} ({len(chunk):,} chars) — cached")
            audio.extend(cache_file.read_bytes())
            continue
        print(f"  chunk {index}/{len(chunks)} ({len(chunk):,} chars)")
        data, request_id = synthesize_chunk(chunk, api_key, request_ids)
        cache_file.write_bytes(data)
        audio.extend(data)
        if request_id:
            request_ids.append(request_id)

    out_mp3.write_bytes(bytes(audio))
    out_hash.write_text(digest)
    print(f"  wrote {out_mp3.relative_to(ROOT)} ({len(audio):,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate ElevenLabs voice-overs for blog posts."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even when the content hash matches.",
    )
    parser.add_argument(
        "--post",
        help="Generate only for this post slug (filename without .md).",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("error: ELEVENLABS_API_KEY env var not set", file=sys.stderr)
        return 1

    posts = sorted(p for p in POSTS_DIR.glob("*.md") if p.name != "_index.md")
    if args.post:
        posts = [p for p in posts if p.stem == args.post]
        if not posts:
            print(f"error: no post matching slug '{args.post}'", file=sys.stderr)
            return 1

    print(f"voice: {VOICE_NAME} ({VOICE_ID})  model: {MODEL_ID}")
    for post in posts:
        generate_for_post(post, api_key, args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
