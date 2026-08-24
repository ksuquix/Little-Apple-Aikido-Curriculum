# CLAUDE.md

Notes for working in this repo (Little Apple Aikido Curriculum, Jekyll site).

## Footwork diagrams (SVG)

Files (in `assets/figures/`, referenced from `Additional-Foundations.md`):

- `foot-shape.svg` — the footprint silhouette alone (right + left foot, black). Iterate on the shape here first, then sync the path into the diagrams.
- `okuri-ashi-forward.svg` / `okuri-ashi-backward.svg` — the step diagrams.

### Foot shape

One right-foot footprint defined in `<defs>` as `#foot-r` in a local 100x230 box (toes up, heel bottom at y=224, big toe on the left/medial side):

- Sole: single closed bezier path. Ball of foot ~65 units wide, narrow heel (~46 units), subtle concave arch on the medial (left) edge.
- The outside (lateral/right) edge must stay near-straight: slight bulge at the ball, then a gentle taper to the heel. No S-wave.
- Toes: 5 separate ellipses above the sole, fanned along the ball arc, big toe longest. Keep visible gaps between toes.
- Left foot is a mirror: `<use href="#foot-r" transform="translate(100 0) scale(-1 1)"/>` wrapped in `#foot-l`.
- In diagrams both feet are black (`#111111`) on white — no colors, no shadows.

### Okuri-ashi layout (user-approved rules; reference layout — other diagrams may use a different canvas)

- Canvas 420x780, viewBox `0 0 420 780`.
- Two columns 133px apart (centered): right foot at x=276.7, left foot at x=143.3. Big toes face each other (top-down view of your own feet).
- Feet are placed with `transform="translate(colX-30, heelY-134.4) scale(0.6)"` (local point (50,224) = heel center).
- Positions form ONE continuous interlocking sequence, not pairs: the back of every foot's heel is level with the toes of the foot adjacent to it in the other column. Consequence: same-foot spacing = 2x foot length, column stagger = 1 foot length.
- Foot length (heel to toe tip at scale 0.6) = 110px. Current heel y's: right 170/390/610, left 280/500/720.
- Arrows: one per transition, in the gap between consecutive same-foot positions, pointing in the direction of travel, 6px inset from the feet. Stroke 7, round cap, 16px arrowhead marker.
- Numbers: circles (r=17, white fill, black stroke 2.5) with bold 20px sans-serif digits, placed right next to (outside of) the arrow they label. Numbers number the MOVEMENT, not the foot positions:
  - Forward: right foot 1 (starts) and 3 (lands); left foot 2 (starts) and 4 (lands). Arrows point up.
  - Backward: identical foot positions; arrows reversed (point down); numbers remapped 4=1, 3=2, 2=3, 1=4.

### Making a new diagram (recipe)

Decision rules first (from user corrections — follow them):

1. Do exactly what the user says, literally. Never derive geometry from body mechanics or "how the movement really works" — the user's words override physics (e.g. in hiraki-ashi-right the toes end up pointing upper-left; that is correct, not a mistake to "fix").
2. Copy the closest existing diagram and edit it. Specs are always "same as X, but ...".
3. If a spec is ambiguous, pick the simplest literal reading and write the file. Once the user has answered a question, do not re-litigate it. One pass, then hand over the filename.
4. No chrome/headless rendering, no self-verification loops. The user opens the files directly; just hand over filenames.

Steps:

1. Copy the base diagram (usually `okuri-ashi-forward.svg`) to the new name; keep its `<defs>` (self-contained files).
2. Place feet by heel position (heel = local (50,224); ball pivot = local (50,86) = top center, 25% down):
   - unrotated: `translate(hx-30, hy-134.4) scale(0.6)`
   - 45° CCW: `translate(hx-88.55, hy-110.15) scale(0.6) rotate(-45 50 86)`
   - 45° CW: `translate(hx+28.55, hy-110.15) scale(0.6) rotate(45 50 86)`
3. Arrows: straight in the gap between consecutive same-foot positions (6px inset, stroke 7, 16px head) for slides; quadratic curves for pivot movements. Number circle (r=17, white fill, black 2.5 stroke, bold 20px digit) right next to the arrow it labels; the digit is the movement number.
4. If a new position overlaps the old one: draw the new footprint in gray (`#999999`) on top of the black one, and make its arrow smaller (stroke 5, 12px head) pulled to the side of the column.
5. Add `<img src="../assets/figures/NAME-cropped.svg" width="200" alt="...">` under the matching bullet in `Additional-Foundations.md`, and add a one-line record below.

### Cropping SVGs (crop-svg.sh)

All SVGs in `assets/figures/` are served with tight crops via `scripts/crop-svg.sh`. The script uses `rsvg-convert` + `magick -fuzz 5%` to find content bounds, then updates the root `<svg>` `viewBox`, `width`, and `height` attributes.

- Usage: `scripts/crop-svg.sh <input.svg> [padding_px] [output.svg]`
- All SVGs must have their white `<rect>` background removed before cropping.
- Always reference the `-cropped.svg` versions in Markdown (`NAME-cropped.svg`).
- After editing an SVG: run `scripts/crop-svg.sh assets/figures/NAME.svg 0 assets/figures/NAME-cropped.svg` to regenerate the cropped version.

Variant records:

- `tsugi-ashi.svg` — 4 footprints (2 per side). Left foot takes a SHORT step (1/4 of the stride, 55px) so the new position overlaps the old: draw the second (new) left footprint in gray (`#999999`) on top of the black one. Its arrow is much smaller (stroke 5, 12px head) and pulled to the side of the column (x offset ~30px), numbered 1. Right foot takes the full stride, numbered 2.
- `ayumi-ashi.svg` — identical layout to okuri-ashi-forward, only the numbers swapped: 1=2, 2=1, 3=4, 4=3 (left foot leads, feet alternate).
- `hiraki-ashi-right.svg` — start pair same as okuri-ashi-forward. Right foot moves 45° diagonally forward-right (same 220px distance as its okuri-ashi stride), then rotates 45° CCW about the ball pivot: local point (50,86) = top center, 25% down the foot. Final foot transform: `translate(hx-88.55 hy-110.15) scale(0.6) rotate(-45 50 86)`. Left foot placed in normal stance relative to the final right foot (okuri-ashi start offset (−133.4, 110) rotated −45° → (−16.5, 172.1)), same rotation; toes end up pointing upper-left. Curved (quadratic) arrows show the pivot, numbered 1 (right) and 2 (left).
- `hiraki-ashi-left.svg` — same start pair. Left foot moves first to the upper left: ends at the same y as the right foot's end in hiraki-ashi-right, x-moved left by the same distance the right foot moved there; rotated 45° CW about the ball pivot (transform `translate(hx+28.55 hy-110.15) scale(0.6) rotate(45 50 86)`), toes pointing upper-right. Right foot placed behind it (offset (+16.5, 172.1)) so the stance swaps to left foot forward, same rotation. Curved arrows numbered 1 (left) and 2 (right).

Foot-shape changes: update `foot-shape.svg` first, get it approved, then copy the path into all diagram files.

## Stick figure poses (kamae, ...)

Files: `chudan-no-kamae.svg`, `jodan-no-kamae.svg` in `assets/figures/`, referenced from the "Base Poses" section of `Additional-Foundations.md`.

### Conventions

- Side view facing right, black (`#222`) on white, round caps/joins; stroke 5 for limbs, 4 for blade; head = white-filled circle r=20; no title, no ground line.
- No part labels (e.g. "kissaki") unless the user asks for one on a specific diagram.
- Grip: right hand near the tsuba, left hand at the midpoint of the tsuka. Tsuka ~36px; tsuba short (~11px), perpendicular to the blade.
- Arms are RIGID: upper arm = forearm = 60px. When a hand moves, recompute the elbow (two-circle intersection) — never stretch a segment.

### Proportions (artistic, in heads; head = 40px)

| part | heads | px |
|---|---|---|
| head (circle diameter) | 1 | 40 (r=20) |
| upper arm | 1.5 | 60 |
| forearm + hand | 1.5 | 60 |
| torso (shoulder → crotch) | 3 | 120 |
| thigh | 2 | 80 |
| shin | 2 | 80 |

### Shared skeleton

Copy these coordinates, then only change the arms/sword per pose:

- head: circle (191,205) r=20
- torso: (190,225) → (178,345)
- front leg: (178,345) → (218,415) → (226,495); foot (226,495) → (248,495)
- back leg: (178,345) → (138,414) → (124,493); foot (124,493) → (146,493)
- arm shoulders: right/near (192,232), left/far (187,240)

### Pose values

- Chudan: sword line 20° up toward opponent's eye line (direction (0.940,-0.342)), grip at belly level — tsuba (262,304), tsuka back to (220,319), blade to kissaki (370,265); tsuba (260,299)→(264,309). Right hand (256,306), elbow (198,292); left hand (241,312), elbow (182,300) (left upper arm runs along/behind the torso — expected, far-side arm).
- Jodan: sword raised above head, hilt above the front of the face (face front x=211) — tsuba (214,158), blade 45° up-back to kissaki (133,77); tsuka back to (246,190); tsuba (218,154)→(210,162). Right hand (224,168), elbow (251,222); left hand (230,174), elbow (247,232).

### Embedding in Markdown

`<img src="../assets/figures/NAME-cropped.svg" width="200" alt="...">` under the pose heading (see image-path gotcha below).

## Image paths in Markdown (gotcha)

Pages are served as DIRECTORIES (clean URLs, e.g. `.../Additional-Foundations/`), so image `src` paths in the Markdown must be `../assets/figures/...`:

- `assets/figures/...` is broken (resolves to `Additional-Foundations/assets/...`) — kramdown also rewrites it to `/assets/...` (domain root) in the built HTML, which is broken too.
- `../assets/figures/...` passes through kramdown unchanged and resolves correctly on the live site.
- Verify after editing: `jekyll build`, then `grep -o 'src="[^"]*"' _site/Additional-Foundations.html` — every figure should show `src="../assets/figures/..."`.

## Romanization (Hepburn Wāpuro)

Use Wāpuro-style Hepburn: `ou` instead of `ō`, no diacritical marks.

### Key terms

| term | romanization | notes |
|---|---|---|
| 正面 / 正面打ち | shoumen / shoumen-uchi | never `shomenuchi` (one word), never `shōmen` (macron) |
| 横面打ち | yokomen-uchi | hyphenate; never `yokomenuchi` or `Yokumenuchi` |
| 面打ち | men-uchi | hyphenate; never `menuchi` |
| 中段の構え | chuudan-no-kamae | |
| 上段の構え | joudan-no-kamae | |
| 肩取り面打ち | katatori men-uchi | hyphenate in glossary entry |

### Hints

- Always hyphenate compound strikes: `shoumen-uchi`, `yokomen-uchi`, `men-uchi`. The `-uchi` suffix means "strike" and should be separated.
- When `-uchi` is dropped in context (e.g. "shoumen cut"), keep `shoumen` as the level descriptor.
- Check Glossary.md as the canonical reference — other files should match it.
- When in doubt, verify Japanese terms on jisho.org.
- Run `grep -r 'shomenuchi\|Shomenuchi\|Shōmen\|menuchi\|Yokumenuchi'` to catch old-style romanization.
