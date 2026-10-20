# National Identity: revised D2 (Pragmatic Sovereignty)

Status: proposal for approval. Nothing has been built.
Author: Freshpriest1993
Diagrams: `deps_national_identity_revised.png` (dependencies), `d2_revised_dpp_positions.png` (positions and hiding).

## Design

**Path A: Pragmatic Sovereignty (new, OBT)**
Reaffirm the Status Quo → **The Republic of China (Taiwan)** → **Pragmatic Sovereignty** (a separate DPP capstone).

**Path B: Name Rectification (unchanged)**
Name Rectification → The Council Ceases to Function → Join the UN as Taiwan → Taiwan's Own Path.

The two paths stay mutually exclusive through the existing exclusion between Reaffirm the Status Quo and Name Rectification. A player can't reach both capstones, because each sits behind one side of that choice.

## Comparison with the original D2

| | Original D2 | **Revised (Pragmatic Sovereignty)** |
| --- | --- | --- |
| New focuses | 1 | 2 |
| Taiwan's Own Path | Gains an "either" prerequisite | **Unchanged** |
| AUG's Republic of Taiwan | Would become reachable after the Status Quo, so it needed a guard on AUG's focus | **Untouched**, and it can't be reached through Path A, because it still requires Taiwan's Own Path or the TSU capstone |
| Status-quo capstone | Shared with Name Rectification | Its own capstone and spirit, closer to the status-quo politics it represents |

## The two new focuses (names, descriptions and rewards to be confirmed with Foggy)

| | The Republic of China (Taiwan) | Pragmatic Sovereignty |
| --- | --- | --- |
| ID | `TAI_su_dpp_roc_taiwan` | `TAI_su_dpp_pragmatic_sovereignty` |
| Prerequisites | Reaffirm the Status Quo | The Republic of China (Taiwan) **and** A New Generation **and** The Economic Advisory Conference (the same other two as Taiwan's Own Path) |
| Available | Pan-Green government, from 2006 | Pan-Green government; not after Project National Glory (same check as the other capstones) |
| Time | 70 days | 70 days |
| Theme | Taiwan is already a sovereign state under its current constitution and name, so no formal change is needed; partners abroad are reassured | De facto sovereignty, democratic institutions and international partnership, without needless escalation |
| Proposed rewards *(placeholders)* | Taiwanese identity +5, US confidence +5, Cross-Strait tension −3, stability +3% (no political power, per the audit) | Replaces DPP programme I/II with a new spirit, **Pragmatic Sovereignty**: stability +8%, political power gain +15%, foreign influence defence +10%, trade opinion +10%. Also US confidence +10, Cross-Strait tension −5 |
| Compared with Taiwan's Own Path | — | Own Path spirit: political power gain +25%, stability +10%, research +5%, war support +5%. Pragmatic Sovereignty is a little weaker at home and stronger abroad |

## Recommended positions (inside the DPP branch, no other focus moves)

| Focus | Position in the DPP branch | Notes |
| --- | --- | --- |
| The Republic of China (Taiwan) | Directly below Reaffirm the Status Quo | The layout tool places it there automatically |
| Pragmatic Sovereignty | One row below and one column right of The Republic of China (Taiwan), beside Join the UN as Taiwan | The automatic spot is directly below, where the lines from A New Generation would run through The Republic of China (Taiwan). Moving it one column avoids that |

The DPP branch stays the same size (9 × 10). No existing focus moves, and nothing overlaps the TSU branch.

## Dependency check

| Area | Finding |
| --- | --- |
| **Republic of Taiwan (AUG)** | Untouched. Path A can't reach it |
| **Project National Glory (AUG focus, exclusion written by OBT)** | PNG is exclusive with every democratic capstone through availability checks that our integration added to both sides. For Pragmatic Sovereignty to be exclusive too, **one line would be added to the PNG root's availability** ("not after Pragmatic Sovereignty"). That line sits in AUG's focus but belongs to the OBT-written exclusion list. **Decision 3.** Without it, PNG would still be hidden after Pragmatic Sovereignty by our hiding system, but it could still be taken with "Show Obsolete Branches" set to Show |
| **Branch hiding** | Pragmatic Sovereignty sets the same flag as the other capstones, so PNG hides as usual. National Identity hiding then behaves well: Status Quo hides Name Rectification, The Council Ceases to Function, Join the UN as Taiwan and Taiwan's Own Path; Name Rectification hides Status Quo and the two new focuses. Republic of Taiwan stays visible through the TSU |
| **Events and scripted triggers** | No event, decision or scripted trigger refers to Taiwan's Own Path or the national identity choice except the focus tree itself, its spirit and its text. "Deep-Green Discontent" still fires after the Status Quo, as now |
| **Elections and party progression** | Nothing reads these focuses. Party popularity is unaffected |
| **AI** | Today the AI prefers the Status Quo (weight 3 against 1) and **never takes Join the UN as Taiwan** (weight 0), so an AI DPP never reaches a capstone. With Path A, an AI DPP would reach Pragmatic Sovereignty. Proposed weights: Historical prefers Name Rectification as history did; Accommodation prefers Path A. The UN bid weight of 0 is an existing issue to look at separately |
| **Tree size** | 368 → 370 focuses |

## Decisions needed

1. Approve the revised design: two OBT focuses, with Taiwan's Own Path unchanged?
2. Approve the positions and the placeholder rewards for Foggy to review?
3. Add Pragmatic Sovereignty to the OBT-written exclusion check on the Project National Glory root (one line in AUG's focus)? Or leave it to the hiding system?
