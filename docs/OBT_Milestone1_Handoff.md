# Operation Blue Tiger: Milestone 1 Handoff

Branch `obt-taiwan-overhaul` (base `f198c6c8db`), Millennium Dawn `D:\Projects\Millennium-Dawn`. All changes are uncommitted working-tree edits: 1 new file, 6 files with insertions only (0 lines deleted).

## Implemented

| File | Change |
| --- | --- |
| `common/national_focus/05_taiwan.txt` | New. `taiwan_focus` tree, 247 focuses in 7 branches (Succession 41, Democratic Fortress 30, National Army 50, Silicon Island 37, Across the Strait 29, Pacific Lifeline 33, Operation Blue Tiger 27). |
| `common/ideas/05_taiwan.txt` | +48 national spirits: 5 starting conditions, 4 defense postures, politics, defense, economy, cross-Strait, strategy and resilience spirits. |
| `common/scripted_triggers/99_TAI_scripted_triggers.txt` | +7 triggers: KMT / PFP / Pan-Blue / Pan-Green in power, Legislative Yuan majority, can pass legislation, Blue Tiger roots ready. |
| `common/scripted_effects/99_TAI_scripted_effects.txt` | +3 effects: party-army legacy steps, Defense-in-Depth joint penalty removal, ruling-camp campaign. |
| `history/countries/TAI - Taiwan.txt` | +5 starting spirits; +9 Blue Tiger state variables. |
| `localisation/english/MD_focus_TAI_l_english.yml` | +611 lines: every focus, spirit, variable and tooltip key. |
| `Changelog.txt` | One BLUF line under v2.0.1 Content. |

## Research mapping

| Research | Represented by |
| --- | --- |
| Directive: no separate PLA Pressure meter | Not created. Cross-Strait effects use MD's existing `CHI_taiwan_strait_tension`, `CHI_TAI_trust` and `CHI_taiwan_us_support`. |
| U.S. commitment vs confidence (Pass VI) | Commitment = existing `CHI_taiwan_us_support`; confidence = new `TAI_us_confidence`. Focuses move them independently. |
| Trade vs trust (Pass VI) | `TAI_mainland_dependence` separate from `CHI_TAI_trust`; Chen-era focuses raise one while lowering the other. |
| Phase I Silicon Shield | Silicon Island semiconductor track; Silicon Shield spirit framed as interest, not guarantee. |
| Phase II Strait Stabilization | Across the Strait political track (labelled alternate history). |
| Phase III India | Pacific Lifeline India tiers, gated by Protect the Crown Jewels (labelled alternate history). |
| Phase IV Democratic Fortress | Democratic Fortress branch; LY-gated focuses use `TAI_can_pass_legislation`. |
| Phase V Blue Tiger Emergency | Operation Blue Tiger branch (strategy, continuity of government, emergency doctrine). Crisis decisions come in milestone 3. |
| Pass IV doctrine | Defense-in-Depth start; Active Defense; early hardening; Hard ROC (2008 or KMT); ODC (2017); Hybrid. Procurement and absorption are separate focuses. |
| 1999/2000 IISS reference | Starting OOB already matches the IISS-era inventory (F-16A/B, Mirage 2000-5, IDF, Knox, Cheng Kung, Kang Ding). No free units granted; the 2001 package offer is not a delivery. |
| Historical timing | Date gates: Mini Three Links 2001, WTO after Nov 2001, SARS lessons 2003, SNTV reform 2004, National Assembly 2005, Anti-Secession answer after 14 Mar 2005, HSR after mid-2006, Hard ROC 2008, ODC 2017. |

## Checks run (on a local copy of the repo)

Passed with no findings in Blue Tiger files: `validate_focus_tree` (with `--missing-icons`), `validate_ideas`, `validate_modifiers`, `validate_tech_categories`, `validate_building_guards`, `validate_common_mistakes`, `validate_history`, `validate_scripted_params`, `validate_unused_scripted`, `validate_localisation`, `validate_style`, `validate_variables`, `validate_set_variables`, `validate_simplifications`, `validate_dynamic_modifier_guards`, `validate_bonus_names`, `validate_standardization`, `fix_loc_yaml`, `check_common_mistakes`. Pre-flight: no duplicate focus, idea, trigger, effect or localisation keys anywhere in the repo.

Fixed during validation: AI factory-staffing guards on 6 building focuses; removed 5 political power penalties; tooltips for 2 `check_variable` requirements.

`validate_variables` and `validate_simplifications` use Python 3.11 regex syntax; the workspace has 3.10, so they ran from a locally patched copy. The repo's own files were not modified.

## Not tested

- No in-game load. Needs: game launch error log, focus tree layout (115 columns wide), tooltip rendering, election path flow.
- Focus layout is generated; branch roots and cross-branch prerequisite lines need a visual pass.
- AI path weights are basic `ai_will_do` values only.

## Known limitations

- The 9 Blue Tiger variables are set and moved by focuses but nothing reads them yet except tooltips. Milestone 3's Pressure System consumes them.
- Legislative Yuan majority is approximated from Pan-Blue vs Pan-Green party popularity.
- Existing China content can still annex Taiwan through `china_sar.017` to `.018` (full blockade plus low U.S. support). This conflicts with Pass VI; fix proposed for milestone 3, needs approval.
- `feature-operation-blue-tiger` holds a malformed `taiwan.327`; that ID is reserved and unused here.

## Next

1. In-game smoke test of milestone 1.
2. Milestone 2: historical events (2000 inauguration, 2004 election and shooting, Anti-Secession Law, State Affairs Fund and Red Shirts, 2008 transition), wired to existing `taiwan.3`.
3. Milestone 3: Pressure System decisions and China-side staged negotiation in place of automatic annexation.

Generator: `D:\Projects\Operation-Blue-Tiger\tools\` (`spec.py` → `gen.py` → `apply.py`, guarded and re-runnable).
