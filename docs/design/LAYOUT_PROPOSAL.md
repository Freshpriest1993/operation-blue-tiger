# Taiwan focus tree: revised layout and progressive hiding

Status: proposal for review. Nothing in the tree has been moved yet.
Author: Freshpriest1993
Renders: `proposed_layout_overview.png` (whole tree) and `proposed_layout_defence.png` (defence section with focus names).

## Summary

| | Today | Today + planned military | **Proposed** |
| --- | --- | --- | --- |
| Focuses | 368 | 389 | 389 |
| Grid (width × height) | 88 × 37 | 100 × 37 | **85 × 41** |
| Length of lines between branches | 765 | 829 | 844 |
| Line crossings | 94 | 98 | 100 |
| Shown mid-game (example on the render) | 316 | 337 | **286** |

1. **Sections.** The tree is regrouped into readable areas:
   - left: **Diplomacy**;
   - centre: **Politics**, with **Domestic** reform underneath;
   - right: **Economy** on top and **Defence** below.
2. **The military branch fits inside the tree.** I split the National Army into two blocks: **core** (civil-military reform, manpower, procurement) and **doctrine** (paths and mastery), placed one under the other. With the 21 planned focuses, the tree ends up 3 columns *narrower* than today, instead of 12 columns wider.
3. **Progressive hiding** goes much further than the party branches. Once a choice is made, the alternative disappears, using the same mechanism Poland uses. In the example game, 103 of 389 focuses are hidden.
4. **Line lengths and crossings stay about where they are today.** The gain is organisation and room for the military, not shorter lines. Further line improvements come from tuning positions inside a few branches after you approve the overall structure.

Every focus ID, prerequisite, completion state, decision, event and AUG contribution is kept. Hidden focuses are never deleted.

## 1. What Poland and Algeria do (checked in the files)

| | Poland | Algeria |
| --- | --- | --- |
| Size | 699 focuses | 718 focuses |
| Hiding | `allow_branch` on 12 focuses; `mark_focus_tree_layout_dirty` 17 times. Hides the path not taken and windows that have closed | None |
| Layout | Deep, with sections stacked downward | Wide, shallow horizontal bands |

Millennium Dawn also has a shared effect for this (`update_focus_tree_obsolete_branches`), controlled by the **"Show Obsolete Branches in Focus Tree"** game rule. Taiwan already uses it for the party branches and Project National Glory. Greece uses a conditional `offset` to move focuses sideways once a branch is hidden. We can use that to close gaps.

## 2. Proposed sections

| Section | Branches | Where |
| --- | --- | --- |
| **Diplomacy** | Pacific Lifeline; Across the Strait, with Southern Policy and Project National Glory beneath it | Left |
| **Politics** | 2000 Succession, with the five party branches below it | Centre, upper |
| **Domestic** | Democratic Fortress, Island Society | Centre, lower |
| **Economy** | Silicon Island | Right, upper |
| **Defence** | Operation Blue Tiger; National Army core; National Army doctrine and mastery | Right, lower |

**Why it keeps this overall shape.** I scored eight arrangements. A pure column layout (one column per section) made the tree 122 to 147 columns wide and nearly doubled the line length. The reason is that the 2000 Succession focus unlocks Democratic Fortress, the party branches, Across the Strait and the National Army, so it has to stay central. The proposed layout keeps it central and puts each section in its own area around it.

## 3. The military branch inside the tree

See `proposed_layout_defence.png`.

**National Army core** keeps everything that stays open to every player:
- civil-military reform;
- manpower;
- procurement;
- the Chungshan Institute;
- the gray zone;
- AUG's arsenal and shipbuilding chain.

**National Army doctrine** sits directly below the core and starts at Reassess Defense-in-Depth:

| Part | Contents |
| --- | --- |
| Left | **The Porcupine Strategy** and its focuses (Harden the Island, Mine the Approaches and the 5 new Porcupine focuses) |
| Right | **A Modern Conventional Force** and its focuses (Decisive Campaign Outside the Territory, Effective Deterrence and the 5 new Conventional focuses) |
| Centre | The **three masteries**, which open from either path's third focus, and the **shared historical chain** (Unmanned Systems → Overall Defense Concept → Hybrid Resilience → Whole-of-Society Defense → Fortress Taiwan) |

Once a path and a mastery are chosen, the other path and the other two masteries disappear. The lower half of the render shows this.

The planned focus positions come from our layout tool and will be tuned when the military part is built.

## 4. Progressive hiding plan

| Level | What is hidden | When | Status |
| --- | --- | --- | --- |
| 1 | **Party branches** of the camp not in government (unless already started) | After Form the Cabinet; re-checked monthly | Done, tested |
| 1 | **Project National Glory** | After a democratic capstone, or with Return to the Mainland set to Blocked | Done |
| 2 | **The unchosen side of every mutually exclusive choice**: 22 pairs in the tree today, for example the three Operation Blue Tiger strategies, the three manpower models, Go Slow or Active Opening, the two 1992 Consensus focuses, Keep Allies or End Checkbook Diplomacy, and Southern Policy war or surrender | As soon as one side is completed | Proposed |
| 2 | **Military paths and masteries** | When chosen | Proposed, with the military build |
| 3 | **Windows that have closed**, for example Heal the KMT Split once the 18 March 2000 election has passed. Only one focus has an end date today; Pass VII will add more | When the date passes | Proposed |
| 4 | **A completed political path**: a party branch collapses once its capstone is done, as in Poland | After the capstone | Optional, needs your decision |
| 5 | **Closing the gaps.** When the Pan-Blue branches are hidden, the Pan-Green branches move left with a conditional `offset` (as Greece does), and the reverse | With level 1 | Prototype first |

**Rules for all of it:**
- **Only alternatives and finished paths are hidden.** Ordinary economic and military chains stay visible as a record of what the player has built.
- **Follows the game rule.** Everything obeys "Show Obsolete Branches in Focus Tree". Set to Show, nothing is hidden.
- **Nothing is lost.** Completed focuses stay completed and keep their rewards, and every other condition that checks a focus still works.

**One thing I still need your in-game check on:** whether a focus with two possible prerequisites stays visible when one of them is hidden. Island Society's "Sustainable Development" is the test case: its second prerequisite is in the Green branch, so it should still show under a Pan-Blue government. Level 2 depends on the answer, because several choices have shared follow-up focuses.

## 5. Military design fixes (planning only)

### 5a. The AI picking a mastery and then trying another

**The cause:** the AI could take Naval mastery before 2005, when Drone mastery isn't available yet. After that it would keep wanting Drone mastery, which the Naval choice now excludes.

**The fix:** the AI decides once, when mastery opens, and never wants a mastery it can't have.
- Under **Historical** and **Island Fortress**, the AI won't take Land or Naval mastery at all, so it waits for Drone mastery. It unlocks in 2005, and mastery only opens after the third Porcupine focus, which in practice is later than that.
- Under **Project National Glory, Unification Channel and Road to Separation**, the AI takes Land mastery and never Drone.
- Every other option uses weights with no conflicting preferences.
- Once any mastery is taken, the AI weight for the others is 0. The exclusivity and hiding already enforce that for players.

### 5b. A narrower Porcupine penalty

Instead of −5% division attack everywhere, the penalty would apply only to the things a porcupine doesn't do:

| Option | Effect | Assessment |
| --- | --- | --- |
| **Recommended:** −10% breakthrough and a −15% amphibious invasion penalty | Hurts offensives and landings, especially a Return to the Mainland invasion, and leaves defence untouched | Fits the doctrine. The defence bonuses stay full value |
| −5% division attack (original) | Hurts every attack, including counter-attacks on Taiwan itself | Too broad |
| No penalty | — | Makes Porcupine strictly better for defence |

Both modifiers (`breakthrough_factor`, `amphibious_invasion`) are standard Hearts of Iron IV modifiers. I'll confirm how Millennium Dawn uses them when building.

## 6. Order of work after approval

Each step is a separate commit, and the current tree stays reproducible at every step.

1. **Layout:** new section placement and the National Army core/doctrine split, with no reward changes. Render, validate, then your in-game check.
2. **Level 2 hiding** for the existing 22 choices, once the two-prerequisite behaviour is confirmed.
3. **Level 3 hiding** for closed windows.
4. **A gap-closing prototype** for the party camps (level 5).
5. **The military build** (paths, masteries, AI fix, narrower penalty) into the doctrine block, after you approve it.

## 7. Decisions needed

1. Approve the section layout as rendered?
2. Hide the unchosen side of all 22 existing choices (level 2)?
3. Collapse a party branch once its capstone is done (level 4)?
4. Use the narrower Porcupine penalty (breakthrough and amphibious)?
