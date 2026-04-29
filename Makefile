.PHONY: audio audio-force serve build

audio:
	@python3 scripts/generate_audio.py

audio-force:
	@python3 scripts/generate_audio.py --force

serve:
	@hugo server -D

build:
	@hugo --minify
