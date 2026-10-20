# Validation report: 370-focus milestone

Date: 2026-10-19
Author: Freshpriest1993
Millennium Dawn branch: `obt/navigation`, local only. HEAD `cc5ee661f9`.

## Millennium Dawn commits in this milestone

| Commit | Change |
| --- | --- |
| `c6283e54f7` | Hide party branches for parties not in government, and Project National Glory once ruled out |
| `957986377c` | Silicon Island rework |
| `0cc86c0bd7` | Two power stations from Energy Security Review |
| `75b7822855` | Section layout, positions only (tag `obt-layout-tested`) |
| `a02b74e02d` | Hide the unchosen side of the Judicial Reform and Constitutional Reform choices |
| `6858805cbc` | N1: Green Party route after the Maanshan expansion |
| `cc5ee661f9` | Pragmatic Sovereignty (370 focuses) |

## Generator reproducibility

All builds use the backup repo's `tools/`, run against the Millennium Dawn working copy.

| Build | Output | Matches |
| --- | --- | --- |
| Default | `05_taiwan.txt`, 370 focuses, no warnings | `cc5ee661f9` |
| `OBT_SKIP_IDENTITY=1` | `05_taiwan.txt` | `6858805cbc` (N1) |
| `OBT_SKIP_IDENTITY=1 OBT_SKIP_N1=1` | `05_taiwan.txt` | `a02b74e02d` |
| `nav/build_nav.py` | Navigation scripted effects and on_actions | HEAD |
| `silicon/build_silicon.py` | Silicon decisions, effects, triggers, localisation | HEAD |
| `identity/apply_identity_text.py` on the N1 files | `common/ideas/05_taiwan.txt`, `MD_focus_TAI_l_english.yml` | HEAD |

## Validators (Millennium Dawn's `tools/validation`)

Each change was validated against the commit before it. **No change in this milestone added a finding.**

The remaining findings are pre-existing:

| Validator | Findings | Taiwan or OBT? |
| --- | --- | --- |
| focus_tree, gfx_references, common_mistakes, style, bonus_names, unused_scripted | None | — |
| localisation | 1926 errors, 382 warnings in 170 files | None in Taiwan or OBT files |
| ideas | 36 warnings | None in Taiwan or OBT files |
| modifiers | 481 warnings in 87 files | None in Taiwan or OBT files |
| standardization | 1031 warnings | None in Taiwan or OBT files |
| ai_path_rules | 7 warnings: no AI behaviour rule for NKR, KOS, LIC, SMA, SOO, TAJ, ERI | None |
| set_variables | 2 errors | **Yes**, OBT: `OBT_pk_n` and `OBT_pa_n` in `99_OBT_defense_scripted_effects.txt` are counted (Kidd and PAC-3 deliveries) but never read. Harmless. Maintenance item: remove them or use them |
| variables, simplifications | Validator crashes, with and without our changes | Not ours. `re.error: multiple repeat` in Python 3.10.12. The validators probably use regular-expression syntax that needs Python 3.11 or later. Maintenance item: confirm Millennium Dawn's required Python version and rerun on 3.11+ |

## Tests passed in game

| Change | Result |
| --- | --- |
| Section layout | Passed |
| Party-branch hiding, including Sustainable Development (a focus with two possible prerequisites) | Passed |
| Judicial Reform and Constitutional Reform hiding | Passed |
| N1, including the Green route after Maanshan | Passed |
| Pragmatic Sovereignty | **Pending final in-game test** |
