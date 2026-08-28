# LANGUAGE.md

Language references for this repo: kanji for budō terms, romanization rules, where each definition was found, and known variances. Check this file before adding or verifying any Japanese term, and update it here when you learn something new.

## Romanization (Full Hepburn with macrons)

Use full Hepburn romanization with macrons: `ō` for long o, `ū` for long u.

### Key terms

| term | romanization | notes |
|---|---|---|
| 正面 / 正面打ち | shōmen / shōmen-uchi | never `shomenuchi` (one word) |
| 横面打ち | yokomen-uchi | hyphenate; never `yokomenuchi` or `Yōkumenuchi` |
| 面打ち | men-uchi | hyphenate; never `menuchi` |
| 中段の構え | chūdan-no-kamae | |
| 上段の構え | jōdan-no-kamae | |
| 肩取り面打ち | katatori-men-uchi | hyphenated in glossary entry |

### Hints

- Always hyphenate compound strikes: `shōmen-uchi`, `yokomen-uchi`, `men-uchi`. The `-uchi` suffix means "strike" and should be separated.
- When `-uchi` is dropped in context (e.g. "shōmen cut"), keep `shōmen` as the level descriptor.
- Check Glossary.md as the canonical reference — other files should match it.
- When in doubt, verify Japanese terms on jisho.org.
- Run `grep -r 'shomenuchi\|Shomenuchi\|menuchi\|Yokomenuchi'` to catch old-style romanization (missing hyphens).

## Sword waza terms (`Foundations/Sword-Waza.md`)

| term | kanji | where found |
|---|---|---|
| suriage | 摺上げ | pre-existing in this repo (`摺上げ面`); kendo writes 刷り上げ — see variances below |
| kaeshi | 返し | Glossary.md (`小手返し` kotegaeshi) |
| kiriotoshi | 切落し | jisho.org — listed variant of `切り落とし` (verb 切落す / 切落とす, "to cut off") |
| makiotoshi | 巻落し | derived — stem of 巻落す, same `X落し` pattern; no direct jisho entry |
| uchiotoshi | 撃落し | Wikipedia "Kendo" — `Uchiotoshi-waza (撃落し技)` |
| suriotoshi | 摺落し | derived — this repo's `摺` + the kendo `X落し` pattern; no standard entry found |
| kote | 小手 | Glossary.md |
| ukenagashi | 受流し | jisho.org — stem of `受流す / 受け流す` (uke-nagasu, "to parry"); matches Glossary.md `下段受流し` |
| tsuki | 突き | in use throughout the repo |
| uchikomi | 打ち込み | jisho.org — common word; `打ち込み稽古` = "training performed by an attacker and a defender, involving intentional openings" |
| shikodachi | 仕込太刀 | user-confirmed — 仕込 (stem of 仕込む shikomu, "to train/prepare", jisho.org) + 太刀 (tachi "sword", reads -dachi in compounds) |
| uchidachi / shidachi | 打太刀 / 仕太刀 | Wikipedia "Kendo" — the two kata roles; pages spell them "Uchitachi" / "Shitachi" (u dropped) |

## Variances and differences

- **suri — 摺 vs 刷**: 摺る (to slide) and 刷る (to brush/sweep) are homophones (suru). Kendo standard (Wikipedia) writes suriage 刷り上げ; this repo established 摺上げ (pre-existing `摺上げ面`) — keep 摺 across this site for consistency.
- **otoshi — 落し vs 落とし**: 落とす (otosu, transitive "to drop") has stem 落とし; the kendo family of deflection techniques uses `X落し` instead (撃落し per Wikipedia; jisho lists 切落し alongside 切落とし as a variant of 切り落とし). This repo uses `X落し` throughout: 切落し, 巻落し, 撃落し, 摺落し.
- **uchi — 撃 vs 打ち**: kendo writes uchiotoshi 撃落し (撃 "to strike"), not 打ち落とし.
- **ukenagashi — 受流し vs 受け流し**: jisho lists both (受流す / 受け流す). This repo uses the compressed 受流し throughout (Sword-Waza.md `受流し`, Glossary.md `下段受流し` and the `Uke-nagashi` entry). Romaji: hyphenate as `uke-nagashi` (one word `ukenagashi` in running prose); the Glossary previously spelled the entry `Uke-Nagashi 受け流し` / rows `Uke Nagashi` — standardized 2026-08.
- **kirikaeshi**: Sword-Waza.md had `kirikeashi`; correct Hepburn for 切返(し) is `kirikaeshi` (切り返し; Wikipedia "Kendo": Kirikaeshi 切り返し). Fixed in the Uchikomi link labels.
- **shidachi**: pages use "Shitachi"; standard romanization is `shidachi` (仕太刀).

## Sources

- **jisho.org** (JMdict) — first stop for term verification: 切落し (variant of 切り落とし; 切落す/切落とす), 受流す/受け流す, 仕込む (shikomu), 打ち込み/打ち込み稽古, kanji 切/落/巻/受/流/木/立. Note: 木立 on jisho is "cluster of trees" — NOT the martial-arts word.
- **Wikipedia "Kendo"** (en.wikipedia.org/wiki/Kendo) — kendo standard: 撃落し技, 刷り上げ技, 返し技, 仕掛け技, Kirikaeshi 切り返し, practice types (waza-geiko 技稽古, kakari-geiko 掛稽古, ji-geiko 地稽古, gokaku-geiko 互角稽古, hikitate-geiko 引立稽古, shiai-geiko 試合稽古), kata roles 打太刀 / 仕太刀 (kata 8-10: shidachi uses 小太刀 kodachi, a shorter sword).
- **Glossary.md** — canonical in-repo reference: 小手 kote, 小手返し kotegaeshi, 下段受流し soto gedan uke nagashi.
- **ALC 英辞郎** — 0 hits for しこだち (not in general dictionaries).
- **User** — 仕込太刀 shikodachi (partner practice taking turns striking; Chiba system).
