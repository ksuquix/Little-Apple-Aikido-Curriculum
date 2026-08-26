#!/usr/bin/env python3
"""Publish verified side-view stances from examples/ to the site.

Pipeline (run this AFTER rendering and human verification):
  1. python3 scripts/stick-figure.py --render-all --view side
  2. verify the renders in assets/figures/examples/ as a human
  3. python3 scripts/update-stance-figures.py

This script:
  - copies examples/{pose}-side.svg into assets/figures/stance/
  - crops each with scripts/crop-svg.sh (-> {pose}-side-cropped.svg)
  - rebuilds the `## Diagrams` table in Foundations/Sword-Stances.md,
    keeping one common px-per-unit scale: the tallest figure gets
    height="200", the others scale by cropped viewBox height.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "assets" / "figures" / "examples"
STANCE = ROOT / "assets" / "figures" / "stance"
DATA = ROOT / "assets" / "data"
CROP = ROOT / "scripts" / "crop-svg.sh"
MD = ROOT / "Foundations" / "Sword-Stances.md"
VIEW = "side"
REF_HEIGHT = 200

# (pose data name, romaji caption, kanji caption) — table order
POSES = [
    ("chudan", "Chūdan-no-kamae", "中段の構え"),
    ("jodan", "Jōdan-no-kamae", "上段の構え"),
    ("gedan", "Gedan-no-kamae", "下段の構え"),
    ("hasso", "Hassō-no-kamae", "八相の構え"),
    ("waki", "Waki-gamae", "脇構え"),
]


def viewBox_height(path: Path) -> float:
    m = re.search(r'viewBox="([^"]+)"', path.read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"no viewBox in {path}")
    return float(m.group(1).split()[3])


def main() -> None:
    for pose, _, _ in POSES:
        pose_data = json.loads((DATA / f"{pose}.json").read_text(encoding="utf-8"))
        if pose_data.get("stance", "hanmi") != "forward":
            sys.exit(f"{pose}.json is not a forward stance; table expects forward")

    missing = [f"{p}-{VIEW}.svg" for p, _, _ in POSES if not (EXAMPLES / f"{p}-{VIEW}.svg").is_file()]
    if missing:
        sys.exit(
            "missing from "
            f"{EXAMPLES}:\n  " + "\n  ".join(missing)
            + "\nRender first: python3 scripts/stick-figure.py --render-all --view side\n"
            + "and verify the renders before publishing."
        )

    STANCE.mkdir(parents=True, exist_ok=True)
    heights = {}
    for pose, _, _ in POSES:
        dst = STANCE / f"{pose}-{VIEW}.svg"
        cropped = STANCE / f"{pose}-{VIEW}-cropped.svg"
        shutil.copy2(EXAMPLES / f"{pose}-{VIEW}.svg", dst)
        subprocess.run([str(CROP), str(dst), "0", str(cropped)], check=True)
        heights[pose] = viewBox_height(cropped)

    ref = max(heights, key=heights.get)
    px = {p: round(REF_HEIGHT * h / heights[ref]) for p, h in heights.items()}

    cells = [
        '<td style="text-align:center; vertical-align:bottom">\n'
        f'<img src="../../assets/figures/stance/{pose}-{VIEW}-cropped.svg" '
        f'height="{px[pose]}" alt="{romaji}">\n'
        f"<br>{romaji}<br>{kanji}\n"
        "</td>"
        for pose, romaji, kanji in POSES
    ]
    table = "<table>\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"

    text = MD.read_text(encoding="utf-8")
    start = text.index("## Diagrams")
    t0 = text.index("<table>", start)
    t1 = text.index("</table>", t0) + len("</table>")
    MD.write_text(text[:t0] + table + text[t1:], encoding="utf-8")

    for pose, romaji, _ in POSES:
        print(f"{pose:8} viewBox {heights[pose]:7.1f}  height={px[pose]}  {romaji}")


if __name__ == "__main__":
    main()
