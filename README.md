[![Netlify Status](https://api.netlify.com/api/v1/badges/809e5527-4c5d-4afc-a95b-e6816789bd3f/deploy-status)](https://app.netlify.com/sites/dazzling-hamilton-bbc66b/deploys)

## Voice-overs

Each post can have an ElevenLabs-generated MP3 rendered as a player at the top of the page.

Generate them locally before pushing:

```sh
export ELEVENLABS_API_KEY=...     # paid ElevenLabs key
make audio                        # only regenerates posts whose text has changed
make audio-force                  # regenerate everything
python3 scripts/generate_audio.py --post <slug>   # one post by filename (no .md)
```

MP3s land in `static/audio/<slug>.mp3` with a `<slug>.mp3.hash` sidecar — both are committed so Netlify serves them directly. Skip a post by adding `audio: false` to its front matter; drafts are skipped automatically.

Voice and model are configured at the top of `scripts/generate_audio.py` (default: Sarah, `eleven_multilingual_v2`). v2 chains `previous_request_ids` between chunks for consistent prosody across long posts.
