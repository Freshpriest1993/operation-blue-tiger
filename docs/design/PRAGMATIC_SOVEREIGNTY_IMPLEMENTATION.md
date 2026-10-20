# Pragmatic Sovereignty: implementation notes

Status: built and validated locally. **Not installed, not committed.** It installs after the Judicial and Constitutional hiding commit and the N1 commit, in that order.
Author: Freshpriest1993
Design: `PRAGMATIC_SOVEREIGNTY_DESIGN.md`. Render: `ps_implemented_layout.png`.

## Changed files in Millennium Dawn (3)

| File | Change |
| --- | --- |
| `common/national_focus/05_taiwan.txt` | Two new DPP focuses, `TAI_su_dpp_roc_taiwan` and `TAI_su_dpp_pragmatic_sovereignty`. One added line in the `available` of the Project National Glory root (below) |
| `common/ideas/05_taiwan.txt` | New spirit `TAI_dpp_pragmatic_sovereignty`: stability +5%, foreign influence defence +10%, trade opinion +5% |
| `localisation/english/MD_focus_TAI_l_english.yml` | Names and descriptions for the two focuses and the spirit (6 keys) |

Nothing else changes. No existing focus moves, and no existing prerequisite, exclusion, reward or AI weight changes.

## Compatibility note for AUG (Project National Glory)

The only change inside AUG's content is one added line in the `available` block of `TAI_restart_project_national_glory`:

```
			NOT = { has_completed_focus = TAI_su_dpp_pragmatic_sovereignty }
```

- It sits with the six existing "not after a democratic capstone" lines, which were written by OBT (commit 86b7b287e0).
- It adds Pragmatic Sovereignty, OBT's new DPP capstone, to the same exclusion.
- The reverse check, "not after Project National Glory", is on Pragmatic Sovereignty itself.
- Both checks come from one entry in `DEMO_CAPS` (`tools/roc/roc_spec.py`).
- AUG's rewards, AI weights, layout, hiding and follow-up focuses are unchanged.

## Generator changes (OBT tools)

| File | Change |
| --- | --- |
| `tools/identity/identity_spec.py` | New. Defines the two focuses. Loaded from `spec.py` before the RoC integration. `OBT_SKIP_IDENTITY=1` builds without them |
| `tools/identity/apply_identity_text.py` | New. Idempotent insertion of the spirit and the text into the two existing files |
| `tools/spec.py` | Hook for `identity_spec` |
| `tools/roc/roc_spec.py` | `DEMO_CAPS` includes the capstone when it is in the tree |
| `tools/nav/nav_spec.py` | The capstone sets `TAI_democratic_capstone_completed` and refreshes branch visibility, as the other capstones do |
| `tools/layout.py` | Optional `lay_anchor` (fixed spot relative to another focus of the branch). No effect on focuses without it |
| `tools/events_spec.py` | Spirit and spirit text mirrored |

**Reproducibility:**
- `OBT_SKIP_IDENTITY=1` reproduces the N1 build byte for byte (sha256 `91eb6da8…`).
- `OBT_SKIP_IDENTITY=1 OBT_SKIP_N1=1` reproduces the current Millennium Dawn file byte for byte (`816d44f9…`).

## Validation

Generator: 370 focuses, no warnings or errors.

**Tree checks on the generated file:**

| Check | Result |
| --- | --- |
| Focus count | 370 (368 + 2) |
| Existing focuses changed | Only the Project National Glory root (the one added line) |
| Existing positions moved | 0. Grid stays 76 × 42 |
| Overlapping positions | None |
| Pragmatic Sovereignty requires | The Republic of China (Taiwan), Reaffirm the Status Quo, A New Generation, The Economic Advisory Conference |
| Taiwan's Own Path requires | Name Rectification, A New Generation, The Economic Advisory Conference (unchanged) |
| Status Quo / Name Rectification exclusion | Declared on both, unchanged. The two capstones can't both be reached |
| Project National Glory | Its `available` excludes 7 capstones, and all 7 check back. These are gameplay requirements, independent of `allow_branch`, so they hold with Show Obsolete Branches set to Show |
| Bypass in the chain | None |
| Capstone flag | Set before the visibility refresh |

**Millennium Dawn validators.** Base is the working tree with the Judicial and Constitutional hiding plus N1. Int is base plus this change. No new findings in any validator:

| Validator | Base | With change |
| --- | --- | --- |
| focus_tree | no issues | no issues |
| ideas | 36 warnings | 36 (no new) |
| localisation | 1926 errors / 382 warnings | identical |
| modifiers | 481 warnings | identical |
| gfx_references | no issues | no issues |
| standardization | 1031 warnings | identical |
| common_mistakes | no issues | no issues |
| ai_path_rules | 7 warnings | identical |
| style | no issues | no issues |
| bonus_names | no issues | no issues |
| unused_scripted | no issues | no issues |
| set_variables | 2 errors | identical |
| variables, simplifications | The validator itself crashes on both base and int | — |

**Layout:** red-line crossings 85 → 86. The one extra crossing is the new line from A New Generation, as expected from the design.

## AI

DPP focuses have no strategy-specific weights today, so every AI strategy uses the same weights:
- Reaffirm the Status Quo 3, Name Rectification 1, so the AI takes the Status Quo about three times in four;
- The Republic of China (Taiwan) 3;
- Pragmatic Sovereignty 5.

| Strategy | DPP route | Capstone reached |
| --- | --- | --- |
| Historical, Accommodation, Island Fortress, Unification Channel, Road to Separation | Usually the Status Quo route | **Pragmatic Sovereignty**. On the Name Rectification route (about one in four), no capstone: see the Join the UN issue |
| Project National Glory | Status Quo route up to The Republic of China (Taiwan) | None, by design. Pragmatic Sovereignty has `factor = 0` on this path, so the AI keeps Project National Glory open |

No existing AI weight was changed. Strategy-specific preferences, for example Historical preferring Name Rectification, are left for a separate decision. They only make sense once the Join the UN issue is fixed, otherwise they would send the Historical AI into the dead end.

## Spirits after government changes

| Question | Finding |
| --- | --- |
| Can the spirit be added twice? | No. Only Pragmatic Sovereignty adds it, and a focus completes once |
| Can it stack with Taiwan's Own Path? | No. The two capstones are on exclusive routes |
| Is programme II removed later? | Only by Taiwan's Own Path, which this route can't take. So Pragmatic Sovereignty and programme II stay together, as designed |
| After a government change or election | No script removes party spirits when the government changes. This is true for all five parties today: Taiwan's Own Path, the KMT, PFP, TSU and Green spirits also stay after their party leaves office. The other camp's party branch then opens, and its spirits are added alongside |

The persistence matches every other party, so this change doesn't introduce new stacking. Whether party spirits should end when the party leaves office is a tree-wide balance question for the later effects review with Foggy. It is not changed here.

## Text for the names and effects review

| Item | Note |
| --- | --- |
| "The Republic of China (Taiwan)" | Close to the KMT capstone "The Republic of China on Taiwan" |
| "Pragmatic Sovereignty" | Close to the PFP focus "A Pragmatic Strait" (`TAI_su_pfp_pragmatic_strait`) |
| Icons | Placeholders: `Focus_Parliament_Constitution` and `MNT_democracy` (the second is shared with Taiwan's Own Path) |
| Rewards | Provisional baseline as approved. The capstone has no political power or other one-off rewards |
