# CLAUDE.md

Notes for working in this repo (Little Apple Aikido Curriculum, Jekyll site).

## Footwork diagrams (SVG)

Files (in `assets/figures/`, referenced from `Foundations/Footwork.md`):

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
5. Add the image to the `## Diagrams` table at the end of `Foundations/Footwork.md` (`height="200"`, caption line under it), and add a one-line record below.

### Cropping SVGs (crop-svg.sh)

All SVGs in `assets/figures/` are served with tight crops via `scripts/crop-svg.sh`. The script uses `rsvg-convert` + `magick -fuzz 5%` to find content bounds, then updates the root `<svg>` `viewBox`, `width`, and `height` attributes.

- Usage: `scripts/crop-svg.sh <input.svg> [padding_px] [output.svg]`
- The original viewBox origin may be negative or fractional (stick figures); the offset math is done in awk, not bash integers.
- All SVGs must have their white `<rect>` background removed before cropping.
- Always reference the `-cropped.svg` versions in Markdown (`NAME-cropped.svg`).
- After editing an SVG: run `scripts/crop-svg.sh assets/figures/NAME.svg 0 assets/figures/NAME-cropped.svg` to regenerate the cropped version.

Variant records:

- `tsugi-ashi.svg` — 4 footprints (2 per side). Left foot takes a SHORT step (1/4 of the stride, 55px) so the new position overlaps the old: draw the second (new) left footprint in gray (`#999999`) on top of the black one. Its arrow is much smaller (stroke 5, 12px head) and pulled to the side of the column (x offset ~30px), numbered 1. Right foot takes the full stride, numbered 2.
- `ayumi-ashi.svg` — identical layout to okuri-ashi-forward, only the numbers swapped: 1=2, 2=1, 3=4, 4=3 (left foot leads, feet alternate).
- `hiraki-ashi-right.svg` — start pair same as okuri-ashi-forward. Right foot moves 45° diagonally forward-right (same 220px distance as its okuri-ashi stride), then rotates 45° CCW about the ball pivot: local point (50,86) = top center, 25% down the foot. Final foot transform: `translate(hx-88.55 hy-110.15) scale(0.6) rotate(-45 50 86)`. Left foot placed in normal stance relative to the final right foot (okuri-ashi start offset (−133.4, 110) rotated −45° → (−16.5, 172.1)), same rotation; toes end up pointing upper-left. Curved (quadratic) arrows show the pivot, numbered 1 (right) and 2 (left).
- `hiraki-ashi-left.svg` — same start pair. Left foot moves first to the upper left: ends at the same y as the right foot's end in hiraki-ashi-right, x-moved left by the same distance the right foot moved there; rotated 45° CW about the ball pivot (transform `translate(hx+28.55 hy-110.15) scale(0.6) rotate(45 50 86)`), toes pointing upper-right. Right foot placed behind it (offset (+16.5, 172.1)) so the stance swaps to left foot forward, same rotation. Curved arrows numbered 1 (left) and 2 (right).
- `hiraki-ashi-cross-centerline.svg` — start is the end position of hiraki-ashi-right (right foot forward, both rotated −45°), end is the stance of hiraki-ashi-left (left foot forward, both rotated +45°). The back (left) foot crosses the centerline first (1), then the right foot follows (2); the two curved arrows cross in the middle of the canvas, with arrow 2 bowed the other way (toward the back) to show the right foot's rotational movement.

Foot-shape changes: update `foot-shape.svg` first, get it approved, then copy the path into all diagram files.

## Stick figure poses (kamae, ...)

In-use figures (OLD, hand-tuned 2D — leave as-is): `chudan-no-kamae.svg`, `jodan-no-kamae.svg`, `gedan-no-kamae.svg`, `hasso-no-kamae.svg`, `waki-gamae.svg` in `assets/figures/`, referenced from the "Base Poses" section of `Foundations/Sword-Stances.md`. They use the old proportions (forearm+hand = 60, no neck, no depth) — do NOT regenerate or "fix" them; new figures go through the 3D generator below.

### 3D generator (`scripts/stick-figure.py`)

Everything is computed in 3D (x, y, z); projection to screen happens only at draw time. Six orthographic projections are available (`--view`; default side). The FEET drive the construction — the head is NOT an input anymore.

- Pose data: `assets/data/*.json` — `chudan`, `jodan`, `gedan`, `hasso`, `waki`, `chudan-nosword` (forward stance), plus a `-hanmi` variant of each of the first five (hanmi) → rendered to `assets/figures/examples/`.
- Usage:
  - `python3 scripts/stick-figure.py assets/data/NAME.json -o out.svg` — one pose
  - `python3 scripts/stick-figure.py --render-all` — every `assets/data/*.json`; failing files are skipped with a message, exit 1 if any skipped. With `--view`, the view name is appended to the output filenames (`chudan-front.svg`); without it, names are unchanged (`chudan.svg`).
  - `--view {side,left,front,back,top,bottom}` — orthographic projection (screen_x, screen_y): side `x, y`; left `-x, y`; front `z, y`; back `-z, y`; top `z, -x` (figure faces up/away); bottom `-z, x` (figure faces down/toward). In the top/bottom views the figure's right side stays on the right, as in the front view. Default: `side` if `--skew` is given, else `front` (single pose); `side` for `--render-all`.
  - `--skew K` — depth skew, side views only: screen_x = base + K·z (0 = flat; the user views with `--skew -0.2`)
  - `--export-3mf` — also write a 3MF of the 3D wireframe (next to the SVG with a `.3mf` suffix; with `--render-all`, all poses). See "3MF export" below.
  - `--dump` — print the computed skeleton as JSON, nested by coordinate frame (ground / spine / per-shoulder arm / sword)
  - Build trace (always, stderr): every computed location, printed in its own frame — ground (ankles, toes, knees, hips, hip center), spine (hips, shoulder base, shoulders, neck, head), per shoulder (hand, elbow), sword (tsuba / tsuka end / kissaki from the right hand) — followed by summary diagnostics (stance, leg bends, equidistant deviation, arm reach).

3D conventions:

- x = forward (screen right), y = down (SVG), z = toward the viewer. The figure faces +x, so its RIGHT side = +z = NEAR, left side = −z = FAR.

Coordinate frames (nothing is specified as a plain absolute coordinate):

- **ground** — origin: the FRONT foot's ankle, declared in the pose file (`"front_foot"`), at (0, 0, 0); y = 0 at ground level. Foot points, knees and hips live here. The back foot's ground level (`"feet": {"back_y": ...}`; 0 = level ground, the default, so the key is omittable) is the only foot input; its x is computed (forward) or the whole foot (hanmi).
- **spine** — origin: the base of the spine (the hip center). Hip points, the shoulder base, the shoulder points, the neck and the head live here.
- **shoulder** — origin: each shoulder. That arm's hand and elbow live here; the sword's points (tsuba / tsuka end / kissaki) live relative to the right hand (its grip). The hand's z is addressed from the shoulder; a 4th element `a` (default false) addresses it from the body centerline (the shoulder base's z) instead — a hand on the centerline is `[x, y, 0, true]` (even though the spine level sits at z ≠ 0 in the ground frame).
- Draw order by depth (far parts first): side/left/front/back views sort by z; top/bottom views sort by y (the projection functions return the depth value — top negates it so higher y = closer = draws first). The derived left hand sits exactly on the sword axis in 3D and draws at its own depth (no depth hack needed).
- Depth shading: near side (right arm/leg) and middle (torso, neck, head, sword, shoulder/hip bars) = `#222`; far side (left arm, left leg, their hands) = medium gray `#888`.
- With non-zero skew, shoulder/hip connector bars are drawn (tie the limbs to the torso; invisible when flat). In forward stance the hips share x and y, so the hip bar projects to a point at 0 skew.

Proportions (head = 40px):

| part | heads | px |
|---|---|---|
| head (circle diameter) | 1 | 40 (r=20) |
| neck (head → shoulder gap) | 0.5 | 20 |
| torso (shoulder → hip) | 3 | 120 |
| shoulder width (z) | 2 | 80 (±40) |
| hip width (z) | 1.5 | 60 (±30) |
| upper arm | 1.5 | 60 |
| forearm | 1.25 | 50 |
| open hand (oval, long × wide) | 0.5 × 0.125 | 20 × 5 |
| closed hand (dot) | 0.375 | 15 (r=7.5) |
| thigh / shin | 2 | 80 / 80 |
| foot (side view) | 0.75 | 30 |
| tsuka / tsuba / blade | — | 45 / 11 / 115 |

Construction order (the feet drive everything):

1. Feet: the pose declares the front foot (`"front_foot"`); its ankle is the ground-frame origin (0, 0, 0) at ground level. The only foot input is the back foot's ground level (`"feet": {"back_y": ...}`, 0 = level, default/omittable); the back foot's x is computed (forward) or the whole foot (hanmi), one hip-width away in z. The toe is 30px ahead of the ankle along the foot direction.
2. Stance (`"stance"`: `"hanmi"` default, or `"forward"`) sets the defaults:
   - **forward**: hips level AND even (both hips share x and y; only z differs), both feet point straight forward. The front leg places the hip: knee `front_knee_offset` (default 7px) along the foot from the heel, straight up the shin; thigh leaves the knee `front_thigh_angle` (default 45) below horizontal, up-and-back. The hip is fully derived — NOT centered over the stride. The back foot's x is COMPUTED from the back hip and the back leg (5° bend default, knee in front of the foot); only the back foot's y comes from the input.
   - **hanmi**: hips rotated 45° about the vertical axis (`hip_rot` default ±45 by front side; the forward hip sits on the forward foot's side), front foot 0°, back foot 45° out. The front leg derives the hip exactly as in forward. The back foot is then COMPUTED: behind the back hip by the back leg's span (15° bend default), on the front foot's ground, at the side z one hip-width from the front foot. The deviation of the hip center from being equidistant from both feet is printed (18.7px with the current hasso data — see review list).
   - Overrides: `hip_rot`, per-foot `foot_rot`, per-leg `knee_bend` (back leg only: 5° forward / 15° hanmi default), per-knee `knee_dir` (pick vector, default the foot direction), `front_knee_offset`, `front_thigh_angle`.
3. Knees: the front knee is placed (offset above the foot); the back knee is two-circle IK (80/80) with the pick in the foot direction.
4. Spine, neck, head go straight up from the hip center.
5. Shoulders rotate by the same angle as the hips (±40 along the rotated axis).
6. Hands: one is given as `[x, y]`, `[x, y, z]` or `[x, y, z, a]` **relative to the shoulder on the same side**; z is from the shoulder by default (0 = the shoulder's depth), or from the body centerline when `a` is true (the forward-stance grip is on the centerline: `[x, y, 0, true]`). The other hand is derived from the sword; without a sword both must be given.
7. Sword: fixed parts tsuka 45 / tsuba 11 / blade 115. The fist (r 7.5) touches the back edge of the tsuba with its center on the axis; the left hand sits halfway between the right hand and the tsuka end. Both distances are computed once from the parts and stored: right hand → kissaki 133.5, right hand → left hand −18.75.
8. Sword input: `angle_from_horizontal` (required; positive up) + `angle_from_center` (default 0) — an azimuth about the vertical axis from straight forward (+x); positive swings toward the viewer (+z). If the left hand is given instead of the right, the right hand is derived the same way.
9. Elbows: two-sphere IK (60/50); the solutions form a circle in 3D, take the point on it whose shoulder→elbow direction is closest to a supplied vector (default straight down); `elbow_dir` overrides per elbow.
10. **No stretching**: a hand farther than 110px from its shoulder, or a foot farther than 160px from its hip, is a hard error — no SVG is written, non-zero exit.

Pose JSON:

```json
{
  "stance": "forward",
  "front_foot": "right",
  "feet": {"back_y": -2},
  "hands": {"right": [67.6, 67.3, 0, true]},
  "sword": {"angle_from_horizontal": 20, "angle_from_center": 0}
}
```

Optional keys: `hip_rot`, `foot_rot`, `knee_bend`, `knee_dir`, `elbow_dir`, `front_knee_offset`, `front_thigh_angle`, a z and centerline flag `a` on the given hand, `hand_style` (open|closed), `hand_dir`.

Example notes:

- Right foot forward: chudan, chudan-hanmi, chudan-nosword, gedan, gedan-hanmi, jodan, jodan-hanmi. Left foot forward: hasso, hasso-hanmi, waki, waki-hanmi.
- hasso (user-tuned): right hand `[7.5, 31.3, 0]` relative to the right shoulder, `elbow_dir` right `[-1, 0, 0]` (elbow trails back), left `[.25, 1, 0]` (hasso) / `[1, 1, 0]` (hasso-hanmi) (down, slightly forward), sword 90°/0.
- jodan/jodan-hanmi: the given hand is the RIGHT, on the centerline — `[20, -65.7, 0, true]` (jodan) / `[-8.3, -65.7, 0, true]` (jodan-hanmi); `elbow_dir` right `[1, 0, 1]`, left `[1, 0, -1]` (elbows lead forward and out — the default DOWN pick would trail the right elbow back). waki/waki-hanmi: `elbow_dir` right `[-1, 0, 0]`, left `[1, 0, 0]`.
- Sword angles were converted from the old right-hand→kissaki axes: chudan 20/0, gedan −34/0, jodan 45/180, hasso 90/0, waki −45/155.

### 3MF export (`--export-3mf`)

Writes the 3D wireframe as a 3MF (triangle mesh) for viewing/3D-printing in any 3MF viewer. Structure matches the official lib3MF writer: `3D/3dmodel.model` part + root `_rels/.rels` + content types (a missing root rels or wrong `unit`/`objectid` attribute names makes every viewer reject the file).

- Geometry: every bone is a capped 12-gon cylinder (beam radius 2mm, sword beams 0.8×), feet are ankle→toe beams, the head (r 20) and hands (fist r 7.5, open hand r 10) are UV spheres, and the tsuba is a thin square disk (r 10.5, thickness 3.0; 8 vertices, 12 triangles) perpendicular to the blade axis at the tsuba point: the two square faces are pure TRANSLATIONS of each other (offset ±h along the sword axis, never a point reflection or a y-only offset — both made the side quads non-planar/twisted), so the four side quads are planar parallelograms.
- Coordinates: skeleton space is converted to 3MF's right-handed Z-up space via (x, y, z) → (x, −z, −y), so the figure stands upright on z = 0 in viewers.
- Winding: all triangles outward-facing (mesh is manifold and consistently oriented; verify with signed volume > 0 — the winding was determined numerically, the interleaved cylinder vertex layout `[A0, B0, A1, B1, ...]` makes the winding easy to get wrong).
- Material: one `<basematerials id="1">` group with a single `<base name="Blue" displaycolor="#0099FF"/>`, referenced from the object (`<object id="2" ... pid="1" pindex="0">`) — the 3MF core spec's object-level property assignment, so no triangle carries a `pid`. Resource ids share one namespace across all resources, so the object id (2) must not collide with the materials-group id (1).
- Verified against the official 3D Printing Consortium library (`pip install py-lib3mf`, reader in strict mode: zero errors/warnings, `ismanifoldandoriented` true) for all eleven poses.

### Publishing verified renders (`scripts/update-stance-figures.py`)

After `--render-all --view side` and human verification of `assets/figures/examples/`: `python3 scripts/update-stance-figures.py` copies the side views of the five forward-stance poses into `assets/figures/stance/`, crops each via `scripts/crop-svg.sh` (`{pose}-side-cropped.svg`), and rebuilds the `## Diagrams` table in `Foundations/Sword-Stances.md` — one common px-per-unit scale: tallest figure = `height="200"`, others rounded by cropped viewBox height. (Forward-stance side views only, for now.)

**NEEDS FIX** (script was edited in a later session without updating this file — keep CLAUDE.md in sync when touching the script):

- The script emits a **bare** `<table>` with `<img ... height=...>` cells. The committed `Foundations/Sword-Stances.md` table has since been hand-tuned (commits `d7ad929`, `737e8f3`) to `<table class="stance-table">` + `<img class="stance-figure" style="--sw:NN%">`, and `assets/css/style.scss` (`@media (max-width: 42em)`) depends on those `class`es and the `--sw` var to give each figure a proportional column share on phones. **Re-running the script silently drops all of that and orphans the CSS.** Fix the script to re-emit `class="stance-table"` / `class="stance-figure"` and to compute each `--sw` = `round(100 × croppedViewBoxWidth / widestCroppedViewBoxWidth, 2)%` (the widest figure omits `--sw`). Until then, do NOT re-run it — hand-edit the table.
- The §"Embedding in Markdown" heights below and Review-list item 4 are stale: the current committed table is chūdan 153 / jōdan 200 / gedan 153 / hassō 172 / waki 153 (ref jōdan, cropped viewBox height 421), and `--sw` chūdan 100% (omitted) / gedan 93.97% / jōdan 59.93% / hassō 59.93% / waki 63.12% (widest chūdan 282). These match the current `assets/figures/stance/*-side-cropped.svg` and are correct — the swap in Review-list item 5 already happened; the old `assets/figures/*-no-kamae*.svg` / `waki-gamae*.svg` are now orphaned.

### Review list (next session)

1. **Hanmi equidistant deviation is 18.7px** (hip center 155.0 from the front foot vs 173.7 from the computed back foot, with the hasso data). The front-knee-offset + 45°-thigh derivation and the 15° back bend do not currently satisfy "hip midpoint equidistant from both feet" — decide whether to adjust (offset, thigh angle, back bend) or accept the deviation.
2. **`chudan-hanmi`** — user's experiment file; the given hand is the LEFT `[50.0, 73.7, 0, true]` (right hand computed from the sword; left reaches 93.4/110); decide if it stays in `assets/data/`.
3. **`waki` sword angle** (−45°/155, converted from the old axis) — verify visually (its hand is retuned: `[-7.5, 75, 5]`).
4. **Embedding heights are stale** — the `## Diagrams` table heights in `Foundations/Sword-Stances.md` (jōdan 200 / chūdan 149 / …) were computed from the OLD viewBoxes; re-derive them when the new figures are embedded (rule: reference pose `height="200"`, others `200 × viewBoxHeight/viewBoxHeight_ref`).
5. **Swap decision** — the in-use figures in `assets/figures/` (`chudan-no-kamae.svg` etc.) are still the old hand-tuned 2D ones referenced by `Foundations/Sword-Stances.md`; the `examples/` versions are the new geometry. Decide when/whether to replace the in-use figures with generator output (and re-crop via `scripts/crop-svg.sh` — the examples are not cropped).

Done this session: the 3MF tsuba became a thin square disk (r 10.5 — 75% of the first r 14 —, thickness 3.0) perpendicular to the blade axis: offset along the sword axis (not y), back square a pure translation of the front (negated corners made the side quads twisted), all 12 triangle windings determined numerically and verified outward for all eleven poses; `hasso.json` got a JSON syntax fix (`[.25,1,0]` → `[0.25,1,0]`, which is why `--render-all` was skipping it). Earlier: elbow IK moved from two-circle (planar pick) to two-sphere (the 3D solution circle; the point whose shoulder→elbow direction is closest to `elbow_dir` is taken) — off-plane picks like a forward elbow now work; 3MF export gained a single Blue basematerial (object-level `pid`, no per-triangle `pid`); jodan/jodan-hanmi's given hand moved to the right on the centerline (`[20, -65.7, 0, true]` / `[-8.3, -65.7, 0, true]`) with `elbow_dir` `[1, 0, 1]` / `[1, 0, -1]`, and hasso/hasso-hanmi got a left `elbow_dir` (`[.25, 1, 0]` / `[1, 1, 0]`). Earlier: added `--view` (six orthographic projections; `--render-all` appends the view to filenames when `--view` is given), top/bottom depth sorting by y, and `--export-3mf` (capped-tube wireframe + head/hand spheres, validated against the official lib3MF in strict mode for all eleven poses). Earlier still: the three out-of-reach hands were retuned (gedan right `[65.6, 74.3, 0, true]`, waki right `[-7.5, 75, 5]`, chudan-hanmi left `[50.0, 73.7, 0, true]` — all now ≤ 107/110); the pose format moved to the hierarchical coordinate frames above.

### Embedding in Markdown

Poses go in the `## Diagrams` table under Base Poses in `Foundations/Sword-Stances.md` (see image-path gotcha below).

- Cells: `<td style="text-align:center; vertical-align:bottom">` — row height is set by the tallest figure; `vertical-align:bottom` aligns image bottoms so the feet sit on the same line.
- Caption: two lines under the image, romaji over kanji: `<br>Chūdan-no-kamae<br>中段の構え`.
- Heights: keep every figure at the SAME scale (px per local unit). Each pose's viewBox height differs (a raised sword extends it above the head), so give the reference pose `height="200"` and scale the others by viewBox height: `height = 200 × (viewBoxHeight / viewBoxHeight_ref)`. Currently: jōdan 200 (viewBox 423), chūdan 149 (316 → 200×316/423 ≈ 149.4), gedan 149 (316, same as chūdan), hassō 174 (368 → 200×368/423 ≈ 174), waki 149 (316, same as chūdan). STALE — these are the old-geometry numbers; re-derive when the new figures are embedded (review list item 5).

## Relative paths in Markdown (gotcha)

The live site is the PROJECT PAGE `https://ksuquix.github.io/Little-Apple-Aikido-Curriculum/` — the domain root (`ksuquix.github.io/`) is not this site and 404s; every live URL carries the `/Little-Apple-Aikido-Curriculum` subpath. `_config.yml` sets `url`/`baseurl` to match (canonical/og tags and theme links come out correct), and `permalink: /:path/` makes every page a DIRECTORY page (`Foundations/Footwork/index.html`) whose canonical URL ends in `/` (the no-slash form 301s to the slash form).

That trailing slash is load-bearing: a document URL without it resolves relative paths one level too high — `../../assets/...` climbs out of the subpath to the domain root and 404s. So image `src` paths stay relative to the page's own directory — one `../` per level below the repo root:

- Root page → `../assets/figures/...`; page in `Foundations/` → `../../assets/figures/...`.
- The same rule governs content links, which resolve from the page's directory URL, one level BELOW its source file: a root page (`Jo.md` → `Jo/`) needs `../` to reach repo-root level (`../Jo%20Weapons/31%20Jo` — `./...` would nest under `Jo/` and 404); a one-deep page (`Jo Weapons/31 Jo.md` → `Jo Weapons/31 Jo/`) needs `../../` (`../../Jo` for its parent, `../../Foundations/Footwork` cross-tree, bare `../../` for the top page).
- Every content page starts with a back-link above its H1 pointing at the page it is linked from: root pages `[← Back to top](../)`, Foundations `[← Back to top](../../)`, Bokken Weapons `[← Bokken](../../Bokken)`, Jo Weapons `[← Jo](../../Jo)`.
- Paths with `../` pass through kramdown unchanged and resolve correctly on the live site. Bare `assets/figures/...` (no `../`) now rewrites under the subpath too (baseurl is set) — correct, but keep the `../` form.
- Verify after editing: `jekyll build`, then `grep -o 'src="[^"]*"' _site/Foundations/Footwork/index.html` — every figure should show the correct relative path.

## Branding / theme (gotchas)

- Palette (taken from littleappledojo.com): `--aka #b22222` firebrick red (links, headings, table headers), `--midori #008000` leaf green, `--sumi #161616` header/text, white page. The apple mark IS the ensō — do not add separate ensō graphics.
- Brand assets in `assets/images/`: `apple.png` (header mark), `favicon-16x16.png` / `favicon-32x32.png`, `apple-touch-icon.png`. Fonts: Open Sans (theme) + Zen Old Mincho (the header line ちさいりんご合気道 — hiragana, not katakana).
- **Custom CSS lives in `assets/css/style.scss`, NOT `style.css`**: the cayman theme also ships `assets/css/style.scss` (front matter + `@import 'jekyll-theme-cayman'`), which compiles to the same output `assets/css/style.css`, and in that collision the THEME file wins — a user `style.css` is never emitted (built file is pure theme CSS, no error). Naming the user file `style.scss` shadows the theme file at the source path, so there is no collision.
- `scripts/rebuild.sh` — stop the server (`.jekyll-serve.pid`, then `pkill -f 'jekyll[s]erve'`; the bracket trick keeps pkill from matching the script's own cmdline), clean `jekyll build`, detached `jekyll serve` (setsid, log `.jekyll-serve.log`), curl-verify the subpath URL. Config changes need a restart; `.md`/layout edits hot-reload.
- CSS `?v=` cache buster: `site.github.build_revision` on GH Pages, build time locally (via a Liquid `assign` tag — Liquid cannot take pipes inside filter-argument parens).
- CLAUDE.md is itself a rendered page: Liquid tags written literally in it are rendered (a stray one fails the GH Pages build, while local jekyll 4 only warns). Avoid them, or wrap such text in a raw block.

## Language (check LANGUAGE.md)

All language references live in `LANGUAGE.md`: romanization rules (full Hepburn with macrons), kanji for terms with the sources where each was found, and known variances. Check it before adding or verifying any Japanese term, and update it there when you learn something new.

## Content consistency backlog (from the 2026-08-27 sweep)

Open items found in a full consistency pass. `Glossary.md` was fixed in that pass; the rest are still open. Fresh `jekyll build` is clean and every internal link/image path resolves.

### Decisions needed (not clear-cut)

- **Are the weapons text pages in scope for the macron standard?** `Jo Weapons/*.md`, `Bokken Weapons/*.md`, `Weapons.md`, `Bokken.md`, `local-weapons-testing.md` are wholesale ASCII (`Jodan`, `Shomen`, `Hasso`, `Happo Giri`, `Tsuki Jodan Gaeshi`, …). LANGUAGE.md says "other files should match Glossary" + macrons everywhere. Either bring them up to standard (a sweep) or carve out an explicit "informal notes, ASCII OK" exception in LANGUAGE.md.
- **`Gemfile` and `Gemfile.lock` are git-ignored and untracked** (`.gitignore` lines 6–7) — no committed build config. GitHub Pages builds fine (its own `github-pages` gem), but a fresh clone and `scripts/rebuild.sh` depend on a `Gemfile` that isn't in the repo. Gitignoring `Gemfile` itself is unusual; consider committing at least it.
- **`Sword-Stances.md` heading hierarchy**: jumps `#` → `###` (stances), no `##`. `Footwork.md` / `Sword-Waza.md` use `##`. Adding `## Base Poses` above the stance list would fix this *and* make CLAUDE.md's two "Base Poses section" references (this file, §"Stick figure poses" intro and §"Embedding in Markdown") accurate — that section name is referenced but does not exist.

### Clear-cut fixes

- **`Foundations/Sword-Waza.md`** (in scope for macrons):
  - line 9: `peform` typo; `menuchi` → `men-uchi` (LANGUAGE.md: "never `menuchi`").
  - line 41: `moves the attach offline` → `attack`.
  - heading spacing inconsistent within the file: `## Suri Otoshi` / `## Uchi Otoshi` (two words) vs `## Kiriotoshi Tsuki` / `## Makiotoshi Men` (one word). LANGUAGE.md treats them as one word.
- **Typos in the weapons pages** (regardless of the macron decision):
  - `Geidan` → `Gedan`: `Jo Weapons/31 Jo.md:14`; `Jo Weapons/Jo Awase (8).md:11,13`.
  - `Yokumen` → `Yokomen`: `Jo Weapons/31 Jo.md:11,13,16,36` (`Jo Suburi (20).md` has `Yokomen` right).
  - `guided attach` → `attack`: `Bokken Weapons/Ken Awase (7).md:5`.
  - `Two cities` → `Twin Cities`: `Bokken Weapons/Kumitachi (7).md:15,23,29` (`Weaponsconsideration.md` has it right).
  - `Wakagamen` (`Bokken Weapons/Ken Suburi.md:7`; `Kumitachi (7).md:17`) — term used but defined nowhere (not in Glossary or LANGUAGE.md). Gloss it or correct it.

### Incompleteness (not errors, just stubs)

- `Tanto.md` is title-only; `Weapons.md` "### Tanto" section is empty; README still lists Tanto.
- `Bokken Weapons/Kumitachi (7).md` has prose for forms 1–4 only (5–7 are just the one-line summary list).
- `Weaponsconsideration.md` lower half is raw pasted notes (its own commit message says "still needs massive cleaning up").
- `Foundations/Sword-Waza.md` `## Partner striking drill (name TODO)` — was mis-titled "Shikodachi 仕込太刀"; that word is 四股立ち (horse stance, now a Glossary term). The drill (Chiba, via Davinder Bath t=451s) still needs its real name.

### Cosmetic (low priority)

- `Footwork.md` §Diagrams: 3-col table with a single-cell middle row (3+1+3 for 7 figures).
- `Footwork.md` cells are `<td style="text-align:center">`; `Sword-Stances.md` cells add `vertical-align:bottom`. Different diagram types, so maybe fine.
- `Weapons.md` uses trailing-double-space hard breaks on some list items, not others.
