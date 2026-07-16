#!/usr/bin/env bash
# Ingest native-speaker recordings into the app.
#
# Usage:
#   1. Open tools/audio/manifest.csv — record each row's `text` (see `hanzi`),
#      saving files named 001.m4a, 002.m4a, ... (wav/mp3/m4a all fine)
#      into a folder, e.g. tools/audio/recordings/
#   2. Run:  bash tools/audio/ingest.sh tools/audio/recordings
#   3. Commit. Files are converted to ~32kbps mono mp3 (~10-20 KB each) and
#      renamed to the hash filenames the app expects.
#
# Requires: ffmpeg  (brew install ffmpeg)
set -euo pipefail

RECDIR="${1:?usage: ingest.sh <recordings-dir>}"
cd "$(dirname "$0")/../.."
OUT="apps/web/static/voice"
MANIFEST="tools/audio/manifest.csv"

count=0
# columns: nr,skill,text,hanzi,record_as,target_hash
while IFS=, read -r nr skill text hanzi record_as target_hash; do
  [ "$nr" = "nr" ] && continue
  base="${record_as%.*}"
  src=""
  for ext in m4a wav mp3 aac ogg flac; do
    [ -f "$RECDIR/$base.$ext" ] && src="$RECDIR/$base.$ext" && break
  done
  [ -z "$src" ] && continue
  ffmpeg -y -loglevel error -i "$src" -ac 1 -ar 32000 -b:a 32k "$OUT/$target_hash.mp3"
  count=$((count+1))
  echo "[$count] $base -> $text"
done < "$MANIFEST"

echo
echo "Done: $count recordings ingested into $OUT"
echo "Tip: run 'du -sh $OUT' to see total size (should stay well under a few MB)."
