#!/usr/bin/env bash
# crop-svg.sh - Crop SVG to content bounds using rsvg-convert + ImageMagick
# Usage: ./crop-svg.sh <input.svg> [padding_px] [output.svg]

set -euo pipefail

INPUT="${1:?Usage: $0 <input.svg> [padding_px] [output.svg]}"
PADDING="${2:-0}"
OUTPUT="${3:-}"

if [ -z "$OUTPUT" ]; then
  BASENAME=$(basename "$INPUT" .svg)
  OUTPUT="${BASENAME}-cropped.svg"
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

PNG="$TMPDIR/input.png"

# 1. Convert SVG to PNG
rsvg-convert "$INPUT" -o "$PNG"

# 2. Trim and get geometry
GEOMETRY=$(magick "$PNG" -fuzz 5% +repage -format "%@" info:)
read -r DIMS <<< "$GEOMETRY"
IFS='x+' read -r NEW_W NEW_H OFFSET_X OFFSET_Y <<< "$DIMS"

# 2.5. Add original SVG viewBox offset
ORIG_VB=$(sed -n 's/.*viewBox="\([^"]*\)".*/\1/p' "$INPUT" | head -1)
if [ -n "$ORIG_VB" ]; then
  ORIG_X=$(echo "$ORIG_VB" | cut -d' ' -f1)
  ORIG_Y=$(echo "$ORIG_VB" | cut -d' ' -f2)
  OFFSET_X=$((OFFSET_X + ORIG_X))
  OFFSET_Y=$((OFFSET_Y + ORIG_Y))
fi

# 3. Apply padding
PADDING=$((PADDING < 0 ? 0 : PADDING))
NEW_X=$((OFFSET_X - PADDING))
NEW_Y=$((OFFSET_Y - PADDING))
FINAL_W=$((NEW_W + 2 * PADDING))
FINAL_H=$((NEW_H + 2 * PADDING))

echo "Original: $INPUT"
echo "Trimmed: ${NEW_W}x${NEW_H} at (${OFFSET_X}, ${OFFSET_Y})"
echo "Padding: ${PADDING}px"
echo "New viewBox: ${NEW_X} ${NEW_Y} ${FINAL_W} ${FINAL_H}"

# 4. Create cropped SVG
# Replace only the root <svg> viewBox, width, height, and <rect> dimensions
sed -E \
  -e '0,/^<svg.*viewBox="[^"]*"/{s/viewBox="[^"]*"/viewBox="'"${NEW_X} ${NEW_Y} ${FINAL_W} ${FINAL_H}"'"/; s/width="[^"]*"/width="'"${FINAL_W}"'"/; s/height="[^"]*"/height="'"${FINAL_H}"'"/}' \
  -e 's/<rect width="[^"]*" height="[^"]*"/<rect width="'"${FINAL_W}"'" height="'"${FINAL_H}"'"/' \
  "$INPUT" > "$OUTPUT"

# Ensure trailing newline
[[ -s "$OUTPUT" ]] && [[ "$(tail -c1 "$OUTPUT" | wc -l)" -eq 0 ]] && echo "" >> "$OUTPUT"

echo "Written: $OUTPUT"
