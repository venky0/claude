#!/usr/bin/env python3
"""Automated first-pass YouTube edit.

Pipeline (each step optional):
  1. Detect silences and jump-cut them out (with breathing-room padding).
  2. Transcribe with faster-whisper (word timestamps) and also cut filler words.
  3. Normalize loudness to YouTube's -14 LUFS target.
  4. Export captions (.srt for upload, styled .ass burned into the video).
  5. Export a 9:16 vertical cut for Shorts/Reels.
  6. Write transcript.txt + edit_report.json for chapters/title/description.

Usage:
  python3 autoedit.py raw.mp4 -o out/ --transcribe --short
  python3 autoedit.py raw.mp4 -o out/ --srt raw.srt     # bring your own captions
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

FILLERS = {"um", "uh", "erm", "uhm", "hmm", "mm", "ah", "er"}


def run(cmd, capture=False):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{res.stderr[-2000:]}")
    return res.stderr if capture else res.stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json",
               "-show_format", "-show_streams", str(path)])
    info = json.loads(out)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    return float(info["format"]["duration"]), video


# ---------- 1. silence detection ----------

def detect_silences(path, noise_db, min_silence):
    log = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
               f"silencedetect=n={noise_db}dB:d={min_silence}", "-f", "null", "-"],
              capture=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def keep_segments(duration, removals, pad, min_keep):
    """Complement of `removals` within [0, duration], padded and merged."""
    keeps, cursor = [], 0.0
    for start, end in sorted(removals):
        end = duration if end is None else end
        if start > cursor:
            keeps.append([cursor, start])
        cursor = max(cursor, end)
    if cursor < duration:
        keeps.append([cursor, duration])
    padded = [[max(0.0, s - pad), min(duration, e + pad)] for s, e in keeps]
    merged = []
    for s, e in padded:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [seg for seg in merged if seg[1] - seg[0] >= min_keep]


# ---------- 2. transcription ----------

def transcribe(path, model_size):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("--transcribe needs: pip install faster-whisper")
    model = WhisperModel(model_size, compute_type="int8")
    segments, _ = model.transcribe(str(path), word_timestamps=True, vad_filter=True)
    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"start": w.start, "end": w.end, "text": w.word.strip()})
    return words


def read_srt(path):
    """Parse an .srt into caption cues (no word timing)."""
    cues = []
    blocks = re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8").strip())
    ts = r"(\d+):(\d+):(\d+)[,.](\d+)"
    for block in blocks:
        m = re.search(ts + r"\s*-->\s*" + ts, block)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = " ".join(block[m.end():].strip().splitlines())
        cues.append({"start": start, "end": end, "text": text})
    return cues


def subtract(keeps, removals, min_keep):
    """Cut exact intervals (no padding) out of already-padded keep segments."""
    for rs, re_ in sorted(removals):
        nxt = []
        for s, e in keeps:
            if re_ <= s or rs >= e:
                nxt.append([s, e])
                continue
            if rs > s:
                nxt.append([s, rs])
            if re_ < e:
                nxt.append([re_, e])
        keeps = nxt
    return [seg for seg in keeps if seg[1] - seg[0] >= min_keep]


def filler_removals(words):
    return [(w["start"], w["end"]) for w in words
            if re.sub(r"[^\w]", "", w["text"].lower()) in FILLERS]


# ---------- timeline remapping ----------

def remap(t, keeps):
    """Map a time on the original timeline onto the cut timeline."""
    offset = 0.0
    for s, e in keeps:
        if t < s:
            return offset
        if t <= e:
            return offset + (t - s)
        offset += e - s
    return offset


def remap_cues(cues, keeps):
    out = []
    for c in cues:
        s, e = remap(c["start"], keeps), remap(c["end"], keeps)
        if e - s > 0.05 and c["text"]:
            out.append({"start": s, "end": e, "text": c["text"]})
    return out


def chunk_words(words, max_words=3, max_gap=0.6):
    """Group word-level timings into short punchy caption chunks."""
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > max_gap):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return [{"start": c[0]["start"], "end": c[-1]["end"],
             "text": " ".join(w["text"] for w in c)} for c in chunks]


# ---------- 4. caption files ----------

def fmt_srt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def fmt_ass(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def write_srt(cues, path):
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{fmt_srt(c['start'])} --> {fmt_srt(c['end'])}", c["text"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_ass(cues, path, width, height, vertical):
    size = int(height * (0.055 if vertical else 0.065))
    margin_v = int(height * (0.35 if vertical else 0.08))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,{size},&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{max(2, size // 12)},2,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [f"Dialogue: 0,{fmt_ass(c['start'])},{fmt_ass(c['end'])},Cap,,0,0,0,,"
              "{\\fad(60,40)}" + c["text"].upper().replace("\n", " ")
              for c in cues]
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


# ---------- render ----------

def render_cut(src, keeps, has_video, lufs, out_path, workdir):
    parts, labels = [], []
    for i, (s, e) in enumerate(keeps):
        if has_video:
            parts.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}];")
            labels.append(f"[v{i}]")
        parts.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}];")
        labels.append(f"[a{i}]")
    v = 1 if has_video else 0
    graph = "".join(parts) + "".join(labels) + f"concat=n={len(keeps)}:v={v}:a=1"
    graph += ("[vc][ac];" if has_video else "[ac];")
    graph += f"[ac]loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000[ao]"
    script = workdir / "cut.filtergraph"
    script.write_text(graph)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
           "-filter_complex_script", str(script), "-map", "[ao]"]
    if has_video:
        cmd += ["-map", "[vc]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-pix_fmt", "yuv420p"]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out_path)]
    run(cmd)


def escape_filter_path(p):
    return str(p).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")


def burn(src, ass, out_path, vf_prefix=""):
    vf = f"{vf_prefix}ass='{escape_filter_path(ass)}'" if ass else vf_prefix.rstrip(",")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out_path)])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--out", default="autoedit_out")
    ap.add_argument("--silence-db", type=float, default=-35,
                    help="below this level counts as silence (default -35 dB)")
    ap.add_argument("--min-silence", type=float, default=0.5,
                    help="shortest pause to cut, seconds (default 0.5)")
    ap.add_argument("--pad", type=float, default=0.12,
                    help="breathing room kept around speech, seconds (default 0.12)")
    ap.add_argument("--no-cut", action="store_true", help="skip jump cuts")
    ap.add_argument("--transcribe", action="store_true",
                    help="transcribe with faster-whisper and cut filler words")
    ap.add_argument("--keep-fillers", action="store_true")
    ap.add_argument("--model", default="small", help="whisper model size (default small)")
    ap.add_argument("--srt", help="existing captions for the raw video (original timeline)")
    ap.add_argument("--lufs", type=float, default=-14, help="loudness target (default -14)")
    ap.add_argument("--short", action="store_true", help="also export a 9:16 vertical cut")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH")
    src = Path(args.input).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    duration, video = probe(src)

    words, cues = [], []
    if args.transcribe:
        print("transcribing…")
        words = transcribe(src, args.model)
    elif args.srt:
        cues = read_srt(args.srt)

    removals = [] if args.no_cut else detect_silences(src, args.silence_db, args.min_silence)
    fillers = filler_removals(words) if words and not args.keep_fillers else []
    keeps = keep_segments(duration, removals, 0 if args.no_cut else args.pad, 0.15)
    keeps = subtract(keeps, fillers, 0.15)
    print(f"{len(removals)} pauses, {len(fillers)} filler words -> {len(keeps)} segments")

    cut = out / "cut.mp4"
    render_cut(src, keeps, video is not None, args.lufs, cut, out)
    cut_duration, _ = probe(cut)

    if words:
        spoken = [w for w in words if not (fillers and
                  re.sub(r"[^\w]", "", w["text"].lower()) in FILLERS)]
        cues = chunk_words(remap_cues(spoken, keeps))
        (out / "transcript.txt").write_text(" ".join(w["text"] for w in spoken) + "\n")
    elif cues:
        cues = remap_cues(cues, keeps)
        (out / "transcript.txt").write_text("\n".join(c["text"] for c in cues) + "\n")

    outputs = {"cut": str(cut)}
    if cues:
        write_srt(cues, out / "captions.srt")
        outputs["srt"] = str(out / "captions.srt")
    if video is not None:
        w, h = int(video["width"]), int(video["height"])
        ass = None
        if cues:
            ass = out / "captions.ass"
            write_ass(cues, ass, w, h, vertical=False)
            burn(cut, ass, out / "final.mp4")
            outputs["final"] = str(out / "final.mp4")
        if args.short:
            vass = None
            if cues:
                vass = out / "captions_vertical.ass"
                write_ass(cues, vass, 1080, 1920, vertical=True)
            crop = "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920,setsar=1,"
            burn(cut, vass, out / "short_9x16.mp4", crop)
            outputs["short"] = str(out / "short_9x16.mp4")

    report = {
        "input": str(src),
        "original_seconds": round(duration, 2),
        "edited_seconds": round(cut_duration, 2),
        "seconds_removed": round(duration - cut_duration, 2),
        "pauses_cut": len(removals),
        "fillers_cut": len(fillers),
        "segments_kept": [[round(s, 3), round(e, 3)] for s, e in keeps],
        "loudness_target_lufs": args.lufs,
        "outputs": outputs,
    }
    (out / "edit_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in
                      ("original_seconds", "edited_seconds", "seconds_removed")}))
    for name, path in outputs.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
