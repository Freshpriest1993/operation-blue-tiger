# Taiwan focus tree refinement: proposal

Status: proposal for review. Nothing has been changed in the game files.
Author: Freshpriest1993
Checked against: the unified 368-focus Taiwan tree on RoC-development (`86b7b287e0`), and Millennium Dawn's Poland and Algeria trees, buildings, modifiers and special projects in the same checkout.

## Summary

| Area | Proposal | New focuses |
| --- | --- | --- |
| **1. Navigation** | Use Poland's branch-hiding technique so branches the player can't or won't use disappear, starting with the five party branches. Regroup the tree into four clear sections | 0 |
| **2. Silicon Island** | Real microchip plants in the right states, a three-tier "Silicon Island" spirit built on Millennium Dawn's chip modifiers, and a stronger Silicon Shield capstone | 0 to 2 |
| **3. Military paths** | One doctrine choice (Porcupine or Conventional) at the existing "Reassess Defense-in-Depth" focus, with historical procurement and core reforms kept open to everyone | about 12 |
| **4. Mastery** | A second choice: Drone, Land or Naval mastery. Each upgrades through dates and research, and works differently depending on the path | about 9 |

**Total:** roughly 368 → 390 focuses. Because unchosen branches will be hidden, a player sees far fewer focuses on screen than today.

**Suggested order:** navigation first, since it decides where new focuses go; then Silicon Island; then military. Pass VII Phase 1 is paused and will slot into the new structure afterwards.

---

## 1. Layout and navigation

### What we have today

- **Size:** 368 focuses on an 88 × 37 grid, in 15 branches.
- **Lines:** after the last layout pass there are still 129 line crossings, and the cross-branch lines total 765 grid units.
- **Biggest problem:** all five party branches (KMT, PFP, DPP, TSU, Green), 92 focuses in all, are always on screen side by side, even though only the governing camp's branches can be taken.
- **Alternate-history branches** (Project National Glory, the Southern Policy conquest chain, the communist chain) stay visible even when a game rule or the player's path rules them out.

### How Poland does it (checked in `05_poland.txt`)

- **Two scripting tools:**
  - `allow_branch` sits on 12 of Poland's 699 focuses;
  - `mark_focus_tree_layout_dirty = yes` appears in 17 completion rewards.
- **How it works:** when `allow_branch` is false, that focus and the branch beneath it are hidden. The game re-checks the condition at game start and whenever `mark_focus_tree_layout_dirty` runs.
- **What Poland hides:**
  - the **path not taken** (for example, `POL_change_of_path` and `POL_stay_on_track` hide each other once one is completed);
  - **branches whose window has closed** (`POL_stay_on_track` also requires `date < 2005.10.1`);
  - **political branches** that only show once a matching flag is set.
- **Nothing is deleted.** Completed focuses stay completed in the save, so their rewards remain and `has_completed_focus` still works. Focus IDs don't change, so saves stay compatible.

### How Algeria does it (checked in `05_algeria.txt`)

- 718 focuses in a single tree, with no branch hiding at all.
- Almost every focus is placed relative to another focus (699 uses of `relative_position_id`).
- The branches are wide and shallow, arranged as horizontal bands, so the player scrolls sideways through clearly separated sections rather than down long chains.

### Limits we have to respect

- **Hidden space stays empty.** Focus positions are fixed, so a hidden branch leaves a gap. The layout should keep alternatives next to each other so that hiding them shrinks a section rather than leaving a hole in the middle.
- **A focus that other branches depend on can't be hidden** without hiding them as well. The 2000 Succession branch can't disappear after completion, because Democratic Fortress and every party branch hang off it. Hiding completed sections only works for self-contained chains.
- **The re-check needs a trigger.** Anything that changes the condition, such as an election, must run `mark_focus_tree_layout_dirty`.
- **To test in game:** how the engine treats a focus with two parents when only one parent is hidden.

Our generator already supports `allow_branch` (Southern Expansion uses it), so no new tooling is needed.

### Proposed hiding rules

| Branch | Visible when | Hidden when |
| --- | --- | --- |
| Party branches (KMT, PFP, DPP, TSU, Green) | That party's camp governs, or the player has already started the branch | Another camp governs and the branch was never started. Re-checked after each election |
| Project National Glory | Before any democratic capstone is completed, and the Return to the Mainland rule allows it | A democratic capstone is completed, or the rule is Blocked |
| Southern Policy conquest chain | The Southern Expansion rule allows it | The rule is Disabled (partly done already) |
| Communist chain (Mainland Threat) | Conditions to confirm (for example, communist popularity) | Otherwise |
| Military doctrine paths | Before the choice | The other path is chosen |
| Mastery doctrines | Before the choice | Another mastery is chosen |

### Proposed sections

The branches would be regrouped into four bands, keeping every ID and prerequisite:

1. **Politics:** 2000 Succession, the party row (now mostly hidden), Democratic Fortress, Island Society.
2. **Economy:** Silicon Island, plus AUG's development focuses.
3. **Foreign and Cross-Strait:** Pacific Lifeline, Across the Strait, Southern Policy, Project National Glory.
4. **Defence:** the reorganised National Army, its doctrine and mastery paths, and Operation Blue Tiger.

I'll render the new layout and send it for review before building it, as with the last layout pass.

---

## 2. Silicon Island and the semiconductor economy

### What Millennium Dawn already provides (checked)

| Mechanic | Detail |
| --- | --- |
| `microchip_plant` building | Produces 20 microchips locally, up to 5 per state, shares building slots, costs $10.50, and consumes tungsten (3) and chromium (2) |
| `one_random_microchip_plant` | A ready-made effect that builds one plant in a state with a free slot and charges the treasury |
| `can_staff_an_microchip_plant` | A workforce check, so we don't build plants Taiwan can't staff |
| Chip modifiers | `production_speed_microchip_plant_factor`, `local_resources_microchips_factor`, `microchip_plant_productivity_modifier` (income), `microchip_export_multiplier_modifier` (export revenue), `industry_chip_consumption_modifier` |
| Microchip special project | `sp_microchip_production` is already completed for Taiwan at the 2000 start |
| Existing Taiwan chip content | Millennium Dawn's GPU development events and the TSMC and Foxconn corporate history events already fire for Taiwan |

### What Taiwan has today

- **Starting plants:** 9 microchip plants (Taipei 3, Kaohsiung 2, Taichung 2, Tainan 2) and **none in Hsinchu**, the historical home of the industry.
- **Silicon Island rewards:** mostly research bonuses, generic civilian factories ("Deepen Hsinchu Science Park" builds a civilian factory in a random state), and points of Semiconductor Security.
- **Spirit:** the branch already has a three-step spirit (`TAI_ss_program_1` → `2` → `3`), but its modifiers aren't chip-specific.

### Proposal

1. **Microchip plants where the history happened**, built with a staffing check and a fallback when slots or workers run out:
   - "Deepen Hsinchu Science Park" builds plants in Hsinchu;
   - "Expand the Southern Science Park" builds plants in Tainan;
   - "Found the Central Taiwan Science Park" builds plants in Taichung.
2. **Silicon Island I → II → III:** turn the existing three-step spirit into the chip spirit the brief asks for. It grows with plant build speed, microchip output, plant income and export revenue at each tier, at the same three focuses that upgrade it today.
3. **A stronger Silicon Shield capstone:**
   - higher chip export revenue and plant income;
   - linked to Semiconductor Security and to US support, which it already raises.
4. **Built-in limits that come from history:**
   - Taiwan has to import tungsten and chromium, so plants raise exposure to blockade;
   - workforce and building slots cap how far the industry can grow;
   - the materials focuses (the Japanese Materials Alliance, the Strategic Materials Inventory) offset these limits.
5. **No double rewards:** the focuses read the flags from Millennium Dawn's GPU and TSMC events rather than repeating them.
6. **Possible later additions (1 or 2 focuses):** leading-edge process nodes and AI-era demand (Pass VII matrix #42).

### Needs Millennium Dawn team approval

- **Hsinchu starting plants:** giving Hsinchu its historical plants means editing a state history file outside our Taiwan files.
- I'd propose it separately and log it in `docs/CHINA_FILE_CHANGES.md` rather than change it quietly.

---

## 3. Military: two strategic paths

### What we have today

- **Size:** The National Army has 53 focuses in four tracks:
  - civil-military reform (7);
  - doctrine (21);
  - manpower (8);
  - procurement (17, including AUG's arsenal and shipbuilding chain).
- **Choices that already exist:**
  - manpower is already a three-way choice: Volunteer/Reserve Split, Professional Force, or Extended Conscription;
  - Operation Blue Tiger has its own grand strategy choice: Accommodation, Blue Tiger or Island Fortress.
- **Doctrine track is history, not a choice:** it follows real doctrine changes in order ("Decisive Campaign Outside the Territory" in 2000, "Hard ROC" in 2008, the Overall Defense Concept in 2017), and everything is compatible.

### Proposed structure

**Stays open to everyone (the shared core):**
- civil-military reform;
- manpower;
- the Chungshan Institute;
- US defence links;
- the gray-zone focus;
- the historical procurement focuses (the 2001 arms package, the Kidd destroyers, fighters, submarines).

These are historical events rather than doctrines, so every player keeps them, along with basic development in land, sea and air.

**Decision point: "Reassess Defense-in-Depth"** (an existing focus) opens two mutually exclusive new roots.

| | **Path A: The Porcupine Strategy** | **Path B: A Modern Conventional Force** |
| --- | --- | --- |
| Idea | Survive and deny: dispersed, cheap, hard to destroy | Fight and win: larger, heavier forces that can sustain high-intensity operations |
| Focuses it takes over | Harden the Island, Mine the Approaches, Mobile Coastal Fires, Disperse and Survive, Unmanned Systems, Layered Air Defense, the HF-2E counterstrike chain | Decisive Campaign Outside the Territory, Effective Deterrence, Air-Sea Interdiction, Hard ROC, AUG's arsenal and shipbuilding chain |
| New focuses (about 5 each) | Decentralised command, mobile air defence, coastal missile production, territorial defence networks, electronic warfare | Armoured and mechanised modernisation, air force expansion, surface fleet and submarines, military industry, logistics |
| Strengths | Defence, entrenchment, anti-air, coastal defence, cheaper equipment, lower manpower cost | More divisions, armour, air and naval production, arms factories and dockyards, offensive capability |
| Weaknesses | Weak in offensives; little help for Return to the Mainland | Expensive in money and manpower; vulnerable to a long blockade |
| Fits with | Island Fortress strategy, survival under the Cross-Strait Pressure System | Blue Tiger strategy, Return to the Mainland |

**Where the Overall Defense Concept goes:** it is history (2017) and is the Porcupine doctrine. I suggest it stays available to both paths but gives much more on Path A. The same applies to Whole-of-Society Defense and Fortress Taiwan. That way the historical content stays open while the choice still matters.

**Three ways to build it.** One question for you:

1. **Re-parent existing focuses** into the paths. About 12 new focuses, the strongest sense of choice, but some prerequisites change.
2. **Add new exclusive blocks only** and leave the existing doctrine track shared. About 20 new focuses, and no prerequisite changes.
3. **Hybrid (recommended):** move only the clearly doctrinal focuses listed above, keep the historical milestones shared with path-dependent rewards, and add about 5 new focuses per path.

---

## 4. Mastery: a second specialisation

After the third focus of either path, the player picks one of three mutually exclusive masteries. Each one is a root plus two follow-up focuses, and it upgrades a mastery spirit over time instead of granting modern capabilities at once.

| Mastery | Grows through | With Porcupine | With Conventional |
| --- | --- | --- | --- |
| **Drone Warfare** | Reconnaissance drones (from about 2005), tactical drones (2012), loitering munitions and swarms (2017), mass production (2022). Gated by date and research | Cheap swarms, coastal and anti-ship drones, survivability | Reconnaissance and strike support for armour and the fleet |
| **Land Warfare** | Army organisation, land doctrine research, ground combat | Territorial defence brigades, infantry, defensive bonuses | Armoured brigades, breakthrough, mechanised logistics |
| **Naval Warfare** | Naval doctrine, maritime defence, naval production | Mines, fast attack craft, coastal missile boats | Destroyers, submarines, blue-water presence |

**What Millennium Dawn already has for this (checked):** drone research categories for air, land, naval, anti-ship, drone torpedoes, naval swarms, naval reconnaissance and helicopter drones (`CAT_air_drones`, `CAT_land_drones`, `CAT_naval_drone_swarms` and others). The exact combat modifiers for drone equipment still need checking before I set values.

**AI behaviour:**
- Historical Taiwan takes Porcupine and builds toward drones over time.
- Each existing AI behaviour option gets a matching preference: Island Fortress → Porcupine; Project National Glory and Return to the Mainland → Conventional.

---

## 5. Compatibility checklist

- Every existing focus ID, event, spirit and decision is kept. Hidden is not deleted.
- The Cross-Strait Pressure System, the procurement and delivery decisions, AUG's reserve theaters and mobilisation decisions, and the game rules for Southern Expansion, NATO Request and Return to the Mainland are unchanged.
- Any shared-file change is logged in `docs/CHINA_FILE_CHANGES.md`.
- Before you test each step in game: validators against the same baselines as before, plus a prerequisite and exclusivity audit.

## 6. Decisions needed from you

1. **Military build approach:** re-parent, add only, or hybrid (recommended)?
2. **Party branches:** hide branches for parties that haven't governed, as proposed?
3. **Hsinchu starting plants:** propose the state history change to the Millennium Dawn team?
4. **Order:** navigation → Silicon Island → military, with Pass VII Phase 1 afterwards?

## 7. Estimated effort

| Step | What it covers | Estimate |
| --- | --- | --- |
| Navigation | Hiding rules, regrouped layout, render for review, build, validators | 3–5 hours, plus your in-game test |
| Silicon Island | Plant rewards, tiered spirit, capstone, balance | 2–3 hours, plus test |
| Military paths and mastery | About 21 focuses, spirits, AI weights, localisation | 5–8 hours across sessions, plus test |
