# -*- coding: utf-8 -*-
"""
Extract course audio from the Teochew-Wild corpus (real native speech).

Pipeline
  1. Download the gated dataset (accept conditions on the HF page first):
       https://huggingface.co/datasets/panlr/teochew_wild
  2. Parse its annotation files (`wav|speaker|hanzi|pinyin` format).
  3. For each row in tools/audio/manifest.csv, find clips whose Peng'im
     token sequence contains the item's tokens (contiguously).
  4. Exact whole-clip matches are copied directly. For words inside longer
     utterances, word timestamps from panlr/whisper-finetune-teochew are
     used to cut the segment (with padding).
  5. Output goes to tools/audio/extracted/<record_as>.wav — review by ear,
     delete bad ones, then run:  bash tools/audio/ingest.sh tools/audio/extracted

Setup (once):
  pip install "huggingface_hub" "transformers" "torch" "torchaudio" "librosa" "soundfile"
  huggingface-cli login        # then accept dataset conditions in browser

License note: Teochew-Wild is CC BY-NC-4.0 (non-commercial only) and the
underlying audio comes from public broadcasts. Keep the app non-commercial
and credit Teochew-Wild. Prefer replacing these clips with your own
recordings over time.
"""
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tools/audio/manifest.csv"
OUTDIR = ROOT / "tools/audio/extracted"
DATA_DIR = Path.home() / "teochew_wild"  # where the dataset gets downloaded

TONE = re.compile(r"\(\d\)|\d")


def norm_tokens(pinyin: str, keep_tone=True):
    toks = pinyin.strip().lower().split()
    if keep_tone:
        return [re.sub(r"\(\d\)", "", t) for t in toks]
    return [TONE.sub("", t) for t in toks]


def download():
    from huggingface_hub import snapshot_download

    path = snapshot_download(
        repo_id="panlr/teochew_wild", repo_type="dataset", local_dir=DATA_DIR
    )
    print("dataset at", path)
    # unzip any archives
    for z in Path(path).rglob("*.zip"):
        subprocess.run(["unzip", "-n", "-q", str(z), "-d", str(z.parent)], check=False)
    return Path(path)


def load_annotations(data_dir: Path):
    """Find annotation lines of the form  wav|speaker|hanzi|pinyin  (or raw format)."""
    rows = []
    for f in data_dir.rglob("*.txt"):
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.strip().split("|")
            if len(parts) == 4 and parts[0].endswith(".wav"):
                rows.append({"wav": parts[0], "hanzi": parts[2], "pinyin": parts[3]})
            elif len(parts) == 2 and parts[0].endswith(".wav") and "@" in parts[1]:
                # raw format: 伊@i1 祇@zi2 ...
                toks = [seg.split("@")[1] for seg in parts[1].split() if "@" in seg]
                rows.append({"wav": parts[0], "hanzi": "", "pinyin": " ".join(toks)})
    print(f"{len(rows)} annotated clips found")
    return rows


def find_wav(data_dir: Path, rel: str):
    p = data_dir / rel
    if p.exists():
        return p
    hits = list(data_dir.rglob(Path(rel).name))
    return hits[0] if hits else None


def contains(haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i : i + len(needle)] == needle:
            return i
    return -1


def cut_with_whisper(wav_path: Path, target_tokens, out_path: Path):
    """Use word timestamps from the Teochew whisper model to cut the segment."""
    global _asr
    if "_asr" not in globals():
        from transformers import pipeline

        _asr = pipeline(
            "automatic-speech-recognition",
            model="panlr/whisper-finetune-teochew",
            return_timestamps="word",
        )
    result = _asr(str(wav_path))
    words = result.get("chunks") or []
    # match against hanzi sequence is unreliable; match count of syllables:
    # take a window of len(target_tokens) words with the best overlap in time order
    if not words:
        return False
    n = len(target_tokens)
    if len(words) < n:
        return False
    # heuristic: pick the window whose recognized text length best matches
    best = None
    for i in range(len(words) - n + 1):
        start = words[i]["timestamp"][0]
        end = words[i + n - 1]["timestamp"][1]
        if start is None or end is None:
            continue
        dur = end - start
        if 0.15 * n <= dur <= 1.2 * n:  # plausible syllable pacing
            best = (max(0, start - 0.05), end + 0.08)
            break
    if not best:
        return False
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
         "-ss", f"{best[0]:.2f}", "-to", f"{best[1]:.2f}", str(out_path)],
        check=True,
    )
    return True


def main():
    data_dir = DATA_DIR if DATA_DIR.exists() else download()
    annotations = load_annotations(data_dir)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    stats = {"exact": 0, "cut": 0, "missing": 0}
    with open(MANIFEST) as f:
        for row in csv.DictReader(f):
            # strip hanzi/punctuation from course text -> peng'im tokens
            latin = re.sub(r"[^\w\sê()]", " ", row["text"].lower())
            target = norm_tokens(latin)
            target = [t for t in target if t]
            if not target:
                continue
            out = OUTDIR / (Path(row["record_as"]).stem + ".wav")
            if out.exists():
                continue
            exact, partial = None, None
            for ann in annotations:
                toks = norm_tokens(ann["pinyin"])
                if toks == target:
                    exact = ann
                    break
                if partial is None and contains(toks, target) >= 0 and len(toks) <= len(target) + 12:
                    partial = ann
            if exact:
                src = find_wav(data_dir, exact["wav"])
                if src:
                    shutil.copy(src, out)
                    stats["exact"] += 1
                    print(f"[exact] {row['text']}  <-  {exact['wav']}")
                    continue
            if partial:
                src = find_wav(data_dir, partial["wav"])
                if src and cut_with_whisper(src, target, out):
                    stats["cut"] += 1
                    print(f"[cut]   {row['text']}  <-  {partial['wav']}")
                    continue
            stats["missing"] += 1
            print(f"[miss]  {row['text']}")

    print("\nsummary:", stats)
    print(f"Listen to the clips in {OUTDIR}, delete any bad ones, then run:")
    print("  bash tools/audio/ingest.sh tools/audio/extracted")


if __name__ == "__main__":
    main()
