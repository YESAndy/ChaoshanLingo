#!/usr/bin/env bash
# Ingest syllable-bank recordings (for future "speak any Peng'im text" TTS).
#
# Usage:
#   1. Open tools/audio/syllable-bank.csv (sorted by frequency — record from
#      the top; the top ~800 rows cover ~80% of running text).
#      Record each row's `syllable` as `record_as` (s0001.m4a, ...).
#   2. bash tools/audio/ingest-syllables.sh <recordings-dir>
#
# Output: apps/web/static/voice-bank/<syllable>.mp3 (e.g. voice-bank/gai5.mp3)
# ~10 KB each; the full 2,215-syllable bank is roughly 20-25 MB.
set -euo pipefail

RECDIR="${1:?usage: ingest-syllables.sh <recordings-dir>}"
cd "$(dirname "$0")/../.."
OUT="apps/web/static/voice-bank"
MANIFEST="tools/audio/syllable-bank.csv"
mkdir -p "$OUT"

count=0
# columns: nr,syllable,freq,cumulative_coverage,record_as,target_file
while IFS=, read -r nr syllable freq cov record_as target_file; do
  [ "$nr" = "nr" ] && continue
  base="${record_as%.*}"
  src=""
  for ext in m4a wav mp3 aac ogg flac; do
    [ -f "$RECDIR/$base.$ext" ] && src="$RECDIR/$base.$ext" && break
    [ -f "$RECDIR/$syllable.$ext" ] && src="$RECDIR/$syllable.$ext" && break
  done
  [ -z "$src" ] && continue
  ffmpeg -y -loglevel error -i "$src" -ac 1 -ar 32000 -b:a 32k "$OUT/$target_file"
  count=$((count+1))
done < "$MANIFEST"

echo "Done: $count syllables ingested into $OUT ($(du -sh "$OUT" | cut -f1))"
