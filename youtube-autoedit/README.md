# YouTube auto-edit

A first-pass edit of a raw talking-head recording, done in one command and using only ffmpeg
(plus optional local Whisper for transcription).

| Step | What it does | Why it matters |
|---|---|---|
| Jump cuts | Finds pauses with `silencedetect` and cuts them out, keeping 0.12 s of breathing room on each side | Gets rid of most dead air, the most tedious part of editing by hand |
| Filler-word cuts | Uses Whisper word timestamps to cut "um / uh / er" exactly | Tighter pacing without trimming words by hand |
| Loudness | Normalizes with `loudnorm` to -14 LUFS, true peak -1.5 dB | Matches YouTube's playback target, so the video isn't turned down or left quiet |
| Captions | `captions.srt` for upload, plus bold 3-word animated captions burned into `final.mp4` | Uploaded captions help search; burned captions help retention on mobile |
| Shorts | `short_9x16.mp4`: a 1080×1920 center crop with captions placed mid-screen | One recording gives you both a long-form and a vertical cut |
| Report | `edit_report.json` and `transcript.txt` | Hand the transcript to Claude to draft chapters, a title, a description and tags |

## Install

```bash
# ffmpeg 6+ with libass (apt install ffmpeg / brew install ffmpeg)
pip install faster-whisper   # only needed for --transcribe
```

## Use

```bash
# Full pass: jump cuts + filler removal + captions + Shorts version
python3 autoedit.py raw.mp4 -o out/ --transcribe --short

# Already have captions (e.g. from YouTube Studio)? Pass them in; they're re-timed to the cut
python3 autoedit.py raw.mp4 -o out/ --srt raw.srt --short

# Tune for your voice and room
python3 autoedit.py raw.mp4 --silence-db -40 --min-silence 0.35 --pad 0.08
```

Main options: `--silence-db` (lower it in a noisy room), `--min-silence` (shortest pause that gets cut),
`--pad` (how much air to keep around speech), `--no-cut`, `--keep-fillers`,
`--model` (Whisper size: tiny/base/small/medium/large-v3), `--lufs`.

## Outputs (in `-o` dir)

- `cut.mp4`: jump-cut and loudness-normalized, no captions burned in
- `final.mp4`: `cut.mp4` with styled captions burned in
- `short_9x16.mp4`: vertical version (with `--short`)
- `captions.srt`, `transcript.txt`, `edit_report.json`

## After the edit

Ask Claude Code: *"Read out/transcript.txt and out/edit_report.json, then write YouTube chapters,
3 title options, a description and tags."*
