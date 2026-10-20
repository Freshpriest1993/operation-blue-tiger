# National Identity: Pragmatic Sovereignty (final design)

Status: final design for approval. Nothing has been built. The two DPP focuses stay on hold until the Project National Glory question (section 5) is decided.
Author: Freshpriest1993
Render: `ps_final_dpp_positions.png`. It replaces `d2_revised_dpp_positions.png`.

## 1. Summary

| | |
| --- | --- |
| Route | Reaffirm the Status Quo → **The Republic of China (Taiwan)** → **Pragmatic Sovereignty**, a separate DPP capstone |
| Unchanged | Name Rectification, The Council Ceases to Function, Join the UN as Taiwan, Taiwan's Own Path, and AUG's Establishment of the Republic of Taiwan |
| Exclusivity | Each capstone sits behind one side of the existing exclusion between Reaffirm the Status Quo and Name Rectification |
| Tree size | 368 → 370 focuses |
| Grid | No change (76 × 42). The DPP branch stays 9 × 10, and no existing focus moves |

## 2. The two new focuses

| | The Republic of China (Taiwan) | Pragmatic Sovereignty |
| --- | --- | --- |
| ID | `TAI_su_dpp_roc_taiwan` | `TAI_su_dpp_pragmatic_sovereignty` |
| Prerequisites | Reaffirm the Status Quo | The Republic of China (Taiwan) **and** A New Generation **and** The Economic Advisory Conference. These are three separate `prerequisite` blocks, so all three are required |
| Mutually exclusive | — (covered by the Status Quo exclusion) | — (covered by the Status Quo exclusion) |
| Available | `TAI_pan_green_in_power = yes`, `date > 2006.1.1` | `TAI_pan_green_in_power = yes`, `NOT = { has_completed_focus = TAI_restart_project_national_glory }` |
| Time | 70 days | 70 days |
| Rewards *(placeholders for Foggy)* | Taiwanese identity +5, US confidence +5, Cross-Strait tension −3, stability +3%. No political power | New spirit **Pragmatic Sovereignty** (section 4). Sets `TAI_democratic_capstone_completed` and refreshes branch visibility, as the other capstones do |
| AI weight | base 3 | base 5 (same as Taiwan's Own Path) |

**Name similarity, for Foggy's review:** "The Republic of China (Taiwan)" is close to the KMT capstone "The Republic of China on Taiwan" (`TAI_su_kmt_roc_on_taiwan`). Both phrasings are historical: the DPP used the first, and the KMT and Ma Ying-jeou used the second. Players may still confuse them in tooltips. President Tsai's "Republic of China, Taiwan" is equally close, so a clearly different name may be better. Foggy's call.

## 3. Checks

### 3a. Shared DPP prerequisites can't be bypassed

| Check | Result |
| --- | --- |
| `bypass` on any DPP focus | None |
| `complete_national_focus` or `unlock_national_focus` targeting a DPP focus, anywhere in `common/` or `events/` | None |
| Prerequisite structure | Three separate `prerequisite` blocks (AND), the same pattern as Taiwan's Own Path |
| Hiding | `allow_branch` only changes what is shown. It never completes or skips a focus |
| Chain to A New Generation | Four Noes → The Cautious Revolutionary → A Clean Green Party → Judicial Reform → Weather the Scandals → A New Generation |
| Chain to The Economic Advisory Conference | Four Noes → The Middle Way → The Economic Advisory Conference |

### 3b. AI accessibility

| Step | AI weight | Notes |
| --- | --- | --- |
| Reaffirm the Status Quo or Name Rectification | 3 or 1 | Unchanged. The AI usually takes the Status Quo |
| The Republic of China (Taiwan) | 3 | New |
| A New Generation, The Economic Advisory Conference | 3 each | Unchanged |
| Pragmatic Sovereignty | 5 | New |
| *Join the UN as Taiwan* | *0* | *Existing issue, unchanged: an AI DPP that picks Name Rectification still never reaches Taiwan's Own Path. To be raised separately* |

**Result:** an AI DPP government now reaches a capstone through the Status Quo route. No AI weight on an existing focus changes. Behaviour-specific weights (Historical prefers Name Rectification, Accommodation prefers the Status Quo route) can be added later. They aren't needed for the route to work.

### 3c. Other dependencies

| Area | Result |
| --- | --- |
| Republic of Taiwan (AUG) | Untouched. Still requires Taiwan's Own Path or the TSU capstone, so the Status Quo route can't reach it |
| Events, decisions, scripted triggers | Nothing outside the tree reads the National Identity focuses. "Deep-Green Discontent" (blue_tiger.28) still fires after the Status Quo |
| Reward mechanics | `TAI_taiwanese_identity`, `TAI_us_confidence` and `CHI_taiwan_strait_tension` are existing variables, already used by the DPP branch |
| Branch hiding | Status Quo hides Name Rectification → Taiwan's Own Path. Name Rectification hides the Status Quo and both new focuses. Establishment of the Republic of Taiwan stays visible through the TSU route (the render shows the DPP branch only) |

## 4. Spirit and balance

### 4a. Modifiers (all exist in MD)

| Modifier | Value | Used in MD ideas |
| --- | --- | --- |
| `stability_factor` | +0.05 | 118 idea files |
| `foreign_influence_defense_modifier` | +0.10 | 70 files. Defined in `influence_modifier_definitions.txt` |
| `trade_opinion_factor` | +0.05 | 74 files |
| Political power gain | none | — |

### 4b. Balance against Taiwan's Own Path

Taiwan's Own Path removes DPP programme I and II and replaces them with its own spirit. **If Pragmatic Sovereignty did the same, the capstone would be a downgrade.** Every player on this route already holds DPP programme II, because Taiwan-Centered State is on the path to the Status Quo.

| Spirit set after the capstone | Political power | Stability | Research | War support | Foreign influence defence | Trade opinion |
| --- | --- | --- | --- | --- | --- | --- |
| DPP programme II, before either capstone | +15% | +6% | +4% | — | — | — |
| Taiwan's Own Path (replaces programme II) | +25% | +10% | +5% | +5% | — | — |
| Pragmatic Sovereignty, **replacing** programme II | — | +5% | — | — | +10% | +5% |
| **Recommended:** Pragmatic Sovereignty **added alongside** programme II | +15% | +11% | +4% | — | +10% | +5% |

**Recommendation:** Pragmatic Sovereignty keeps DPP programme II and adds its own spirit beside it.
- The spirit itself has no political power gain, as approved.
- Compared with Own Path, the route is a little weaker at home (political power +15% against +25%, research +4% against +5%, no war support). It is stronger abroad (foreign influence defence, trade opinion) and gives slightly more stability.
- The Republic of China (Taiwan) adds less identity than the Name Rectification chain, and lowers tension where that chain raises it.

**Decision A.** If programme II should be replaced instead, the spirit needs some political power gain, for example +10%, so the capstone isn't a net loss.

## 5. Project National Glory compatibility

### 5a. Who owns what

| Part | Owner |
| --- | --- |
| The PNG root focus (`TAI_restart_project_national_glory`) | AUG |
| The six `NOT = { has_completed_focus = <democratic capstone> }` lines in its `available` | Written by OBT. They came in with commit 86b7b287e0 (Freshpriest1993), the unified tree layout, and are already on RoC-development. They are generated from `DEMO_CAPS` in `tools/roc/roc_spec.py` |
| `TAI_reclamation_allowed`, also in that `available` | OBT (`99_TAI_scripted_triggers.txt`) |

### 5b. Options checked

| Option | Touches AUG's focus? | Reliable? | Verdict |
| --- | --- | --- | --- |
| **1. Add the capstone to `TAI_reclamation_allowed`** | No | Blocks PNG, but the trigger also controls three other things: the visibility of the Return to the Mainland decision category, the Taiwan balance of power (`common/bop/TAI.txt` uses that category), and AUG's `TAI_png_launch` decision. A Pragmatic Sovereignty Taiwan would lose Return to the Mainland when China collapses, while players of the other five capstones keep it. The tooltip text describes the game rule, so the reason shown would also be wrong | **Rejected:** too broad |
| **2. Mutual exclusion on Pragmatic Sovereignty's side only** | No | MD declares `mutually_exclusive` on both focuses. A one-sided declaration isn't the documented behaviour and would need an engine test before relying on it | **Rejected:** not reliable |
| **3. Visibility hiding only** | No | PNG could still be taken with "Show Obsolete Branches" set to Show | **Rejected,** per your instruction |
| **4. One-way check in Pragmatic Sovereignty's own `available`** | No | Blocks Pragmatic Sovereignty after PNG. It doesn't block PNG after Pragmatic Sovereignty | **Included,** but only covers half the exclusion |
| **5. One line in the PNG root's `available`, the same OBT-written list** | One added line, beside the six existing OBT lines | Reliable. The same mechanism as the other six capstones | **Recommended** |

**Conclusion:** no reliable OBT-only route exists. Every OBT-owned trigger already in the PNG root's `available` is shared with other systems.

### 5c. Exact change required in AUG's focus

File: `common/national_focus/05_taiwan.txt`, focus `TAI_restart_project_national_glory`, inside `available`. Add one line after `NOT = { has_completed_focus = TAI_df_political_dna }`:

```
			NOT = { has_completed_focus = TAI_su_dpp_pragmatic_sovereignty }
```

- **Generator:** add `"TAI_su_dpp_pragmatic_sovereignty"` to `DEMO_CAPS` in `tools/roc/roc_spec.py`. The same list already adds the PNG check to each listed capstone's own `available` (option 4), so both directions would come from one entry.
- **Nothing else changes in AUG's focus.** Its rewards, layout, hiding and follow-up focuses stay as they are. AUG's later PNG focuses all require the root, so blocking the root is enough.
- **Commit:** this line would go in the same commit as the two new focuses, because a capstone without its PNG exclusion shouldn't exist on its own. The message would mention the PNG line, so AUG can see it.

### 5d. Alternative to avoid future edits (not recommended now)

Replace the six OBT lines plus the new one with a single OBT trigger, `TAI_democratic_capstone_taken`. Future capstones would then never touch AUG's focus. This edits seven lines in AUG's focus instead of adding one, so it's better proposed to AUG later than done now.

## 6. Positions (revised)

| Focus | Position | Reason |
| --- | --- | --- |
| The Republic of China (Taiwan) | Directly below Reaffirm the Status Quo | Automatic spot. No line passes through another focus |
| Pragmatic Sovereignty | **Capstone row, same row as Taiwan's Own Path, three columns left of the Status Quo (under The Economic Advisory Conference side)** | Replaces the earlier "one column right" suggestion |

**Why the change:** I checked every free cell in the DPP branch for lines running through another focus, under two line-drawing models, and for line crossings.
- The earlier spot (one row down, one column right) still sent the line from A New Generation through The Council Ceases to Function.
- The automatic spot sent lines through the Status Quo and The Republic of China (Taiwan).
- The new spot is clean under both models, with one crossing.
- It also puts the two DPP capstones on the same row, one on each side of the branch.

No existing focus moves, and the branch stays 9 × 10.

## 7. Decisions needed

1. **PNG compatibility:** approve the one added line in the PNG root's `available` (5c), generated from `DEMO_CAPS`, to be shown to AUG?
2. **Spirit (Decision A):** keep DPP programme II alongside Pragmatic Sovereignty (recommended), or replace it and add some political power gain?
3. **Position:** approve Pragmatic Sovereignty on the capstone row?
4. **Name:** pass "The Republic of China (Taiwan)" to Foggy with the similarity flag?
