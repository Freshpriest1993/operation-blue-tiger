# Changes to Millennium Dawn's China files

Operation Blue Tiger keeps its content in its own files wherever it can. These are the only edits to files owned by Millennium Dawn's China content, listed for developer review.

## Milestone 3: staged talks instead of automatic annexation

| File | Change |
| --- | --- |
| `events/05_china.txt` | `china_sar.017` option b and `china_sar.020` option b now fire `blue_tiger.40` (staged talks) instead of annexing Taiwan. `china_sar.018` (the annexation event) is removed. `china_sar.022` clears the three blockade flags when it annexes. |
| `common/decisions/05_CHI_decisions.txt` | New decision `CHI_TAI_offer_settlement`, inserted before `CHI_TAI_lift_full_blockade`. |
| `localisation/english/MD_focus_CHI_l_english.yml` | `china_sar.018` keys removed; `china_sar.020.b` reworded to "Open talks on Beijing's terms." |

## Milestone 7: Cross-Strait Tension meter

| File | Change |
| --- | --- |
| `common/decisions/categories/99_CHI_decision_categories.txt` | `CHI_SAR_decisions_category` ("One China Strategy") is visible from the start and shows the meter (`scripted_gui = OBT_CHI_strait_meter`). Its old `visible = { has_completed_focus = CHI_SAR_one_china_framework }` is removed. |
| `common/decisions/05_CHI_decisions.txt` | To keep every existing decision exactly as reachable as before, `has_completed_focus = CHI_SAR_one_china_framework` is added to the `visible` block of each decision in `CHI_SAR_decisions_category` (55 decisions; 6 already had it). `CHI_TAI_pro_china_party_networks_mission` is left unchanged because missions ignore `visible`. Hong Kong, Macau, Tibet, Xinjiang, Inner Mongolia and Mongolia conditions are untouched. |

New China decisions for the meter live in Operation Blue Tiger's own file, `common/decisions/OBT_strait_decisions.txt`, under the same category key.

## Shared files touched outside China

| File | Change |
| --- | --- |
| `common/game_rules/00_game_rules.txt`, `localisation/english/MD_game_rules_l_english.yml` | `TAI_ai_behavior` and `TAI_return_to_mainland` rules. |
| `common/on_actions/999_game_rules_on_actions.txt` | Taiwan AI path flags. |
| `common/scripted_effects/00_yearly_effects.txt` | Schedules Taiwan's historical events. |
| `common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt` | KMT party names for the restored mainland republic (flag-gated) and the Taiwan Solidarity Union name from August 2001. |
| `localisation/english/MD_politics_view_parties_l_english.yml` | Taiwan Solidarity Union party name and description. |
| `Changelog.txt` | One Operation Blue Tiger line. |
