# Implementation plan: Silicon Island rework and military paths

Status: plan for approval. Nothing has been changed yet.
Author: Freshpriest1993
Based on: `TREE_REFINEMENT_PROPOSAL.md` (hybrid military option chosen) and the current tree on RoC-development plus branch hiding.

Everything below goes through our generators (`spec.py` and friends) as before. Every existing focus ID, event, decision and national spirit is kept. Numbers marked *(balance)* are first values for testing.

---

## Part 1: Silicon Island

### 1a. The three-tier spirit: "Silicon Island I / II / III"

The branch already upgrades one spirit at the same three focuses (`TAI_ss_program_1` → `_2` → `_3`). I keep the IDs and the upgrade points, rename them, and give them chip modifiers that already exist in Millennium Dawn.

| Tier | Granted by | Today | After the rework *(balance)* |
| --- | --- | --- | --- |
| **Silicon Island I** | The Silicon Island (root) | +3% factory efficiency growth, +2% research speed | Same, **plus** +10% microchip plant build speed, +5% microchip output |
| **Silicon Island II** | The 12-Inch Transition | +5% factory efficiency growth, +3% research speed | Same, **plus** +15% plant build speed, +8% microchip output, +5% plant income, +5% chip export revenue |
| **Silicon Island III** | Protect the Crown Jewels | +8% factory efficiency growth, +5% research speed | Same, **plus** +20% plant build speed, +12% microchip output, +10% plant income, +8% chip export revenue |

Modifiers used (all checked in Millennium Dawn): `production_speed_microchip_plant_factor`, `local_resources_microchips_factor`, `microchip_plant_productivity_modifier`, `microchip_export_multiplier_modifier`.

For scale: Millennium Dawn's strongest existing chip spirits give up to +14% output and +15% export revenue, and MD's own TSMC-era GPU spirit gives +5% to each. Tier III puts Taiwan at the top of that range without passing it.

### 1b. A stronger Silicon Shield (capstone)

| | Today | After *(balance)* |
| --- | --- | --- |
| **The Silicon Shield** spirit | +5% microchip output, +10% trade opinion, +10% foreign influence defence | Same, **plus** +7% chip export revenue, +5% plant income |

It still adds US support (unchanged). With Silicon Island III, Taiwan reaches +17% microchip output, the highest in the mod. That's deliberate, but flagged for balance review.

### 1c. Microchip plants instead of generic factories

| Focus | Today | After |
| --- | --- | --- |
| **Deepen Hsinchu Science Park** | 1 civilian factory in a random state | **1 microchip plant in Hsinchu** (state 1155), with one building slot added first |
| **Expand the Southern Science Park** | 1 civilian factory in a random state | **1 microchip plant in Tainan** (state 1157), with one slot added first |
| **Found the Central Taiwan Science Park** (AUG's grant) | 2 civilian factories each in Hsinchu and Taichung | **Unchanged**, plus **1 microchip plant in Taichung** (state 1156) with one more slot |
| **Advanced Process R&D** | Research bonus, Semiconductor Security | Same, **plus 1 microchip plant** in a random Taiwanese state with a free slot (Millennium Dawn's `one_random_microchip_plant`) |

**How each plant is built:**
- **Workforce check:** if Taiwan can't staff the plant (`can_staff_an_microchip_plant`), the focus gives +15% microchip plant build speed for a year instead, so it never builds an empty plant.
- **Cost:** each plant charges the treasury $10.50, Millennium Dawn's standard price.
- **Result:** Taiwan goes from 9 plants to as many as 13.
- **Cost of the plants themselves:** each plant needs tungsten and chromium, which Taiwan must import. That ties the chip industry to the blockade and materials focuses already in the branch.

### 1d. Not changed

- Millennium Dawn's GPU development and TSMC/Foxconn corporate history events.
- AUG's civilian factories.
- Hsinchu's starting buildings. That needs Millennium Dawn team approval and stays a separate proposal.

---

## Part 2: Military paths (hybrid)

### 2a. What stays open to everyone

These keep their prerequisites and rewards:
- civil-military reform (7 focuses);
- manpower (8);
- procurement (14, plus AUG's 3);
- Reassess Defense-in-Depth, Lessons of the Missile Crisis, Layered Air and Missile Defense;
- Unmanned Systems, Overall Defense Concept, Hybrid Resilience, Whole-of-Society Defense, Fortress Taiwan.

### 2b. The decision point

**Reassess Defense-in-Depth** (existing) opens two **new, mutually exclusive** roots:

| New focus | ID | Prerequisite |
| --- | --- | --- |
| **The Porcupine Strategy** | `TAI_na_porcupine_strategy` | Reassess Defense-in-Depth |
| **A Modern Conventional Force** | `TAI_na_conventional_force` | Reassess Defense-in-Depth |

Once one is taken, the other path is hidden, using the same branch hiding as the party branches.

### 2c. Existing focuses that move into a path

This is the only prerequisite change to existing content.

| Path | Existing focuses that move | Prerequisite change |
| --- | --- | --- |
| **Porcupine** | Harden the Island → Repair the Runways, Mine the Approaches → Rapid Internal Redeployment, Hard ROC, Mobile Coastal Fires → Disperse and Survive | **Harden the Island** now requires The Porcupine Strategy instead of Lessons of the Missile Crisis. The rest follow as before |
| **Conventional** | Decisive Campaign Outside the Territory → Effective Deterrence → Air-Sea Interdiction, the HF-2E chain, Information and Electronic Warfare Command | **Decisive Campaign Outside the Territory** now requires A Modern Conventional Force instead of Lessons of the Missile Crisis. The rest follow as before |
| Shared | **Unmanned Systems** | Requires Disperse and Survive **or** Information and Electronic Warfare Command, so it stays reachable on both paths |

Mobile Coastal Fires and Hybrid Resilience already accept prerequisites from either side and stay as they are.

### 2d. New focuses per path (5 each)

**Path A: The Porcupine Strategy.** Survive, deny, and make an invasion too costly.

| # | New focus | ID | Reward *(balance)* |
| --- | --- | --- | --- |
| A0 | The Porcupine Strategy (root) | `TAI_na_porcupine_strategy` | Spirit **Porcupine Doctrine I**: +5% division defence, +10% dig-in speed, +1 max dig-in, −5% division attack |
| A1 | Mission Command | `TAI_na_mission_command` | Land doctrine cost −20% (1 use), +3% army organisation (added to the spirit) |
| A2 | Mobile Air Defence Battalions | `TAI_na_mobile_air_defense` | Surface-to-air missile research bonus (+75%, 2 uses), 1 anti-air building |
| A3 | Coastal Missile Production | `TAI_na_coastal_missile_production` | Anti-ship missile research bonus (+75%, 2 uses), cruise missile research bonus (+50%, 1 use), 1 military factory |
| A4 | Fortify the Beaches | `TAI_na_fortify_beaches` | Coastal bunkers on Taiwan's invasion beaches (Taoyuan, Taichung, Tainan, Kaohsiung coasts), +5% defence |
| A5 | Too Costly to Swallow (capstone) | `TAI_na_porcupine_capstone` | Upgrades to **Porcupine Doctrine II**: +10% defence, +15% dig-in speed, +2 max dig-in, −10% supply use, −5% division attack |

**Path B: A Modern Conventional Force.** Larger, heavier forces able to sustain high-intensity operations.

| # | New focus | ID | Reward *(balance)* |
| --- | --- | --- | --- |
| B0 | A Modern Conventional Force (root) | `TAI_na_conventional_force` | Spirit **Conventional Force I**: +5% division attack, +5% military factory build speed, +5% conscription. Costs $3 from the treasury |
| B1 | Modernize the Armored Corps | `TAI_na_armored_modernization` | Main battle tank and armoured vehicle research bonuses (+75%, 2 uses each), army experience |
| B2 | Expand the Air Force | `TAI_na_air_force_expansion` | Aircraft research bonus (+75%, 2 uses), 2 air bases, air experience |
| B3 | A Blue-Water Squadron | `TAI_na_blue_water_squadron` | Destroyer and submarine research bonuses, 1 dockyard, navy experience |
| B4 | Military Industrial Expansion | `TAI_na_military_industry` | 2 military factories, +10% military factory build speed (added to the spirit), costs $8 |
| B5 | Fight and Win (capstone) | `TAI_na_conventional_capstone` | Upgrades to **Conventional Force II**: +10% division attack, +5% organisation, +5% production efficiency cap, +5% military factory output |

**How they balance:**

| | Porcupine | Conventional |
| --- | --- | --- |
| Good at | Defence, anti-air, coastal defence, cheaper missiles, survival under blockade | Offence, more equipment, air and naval strength, Return to the Mainland |
| Costs | Weaker in offensives | Money and manpower; more exposed to a long blockade |
| Works with | Island Fortress strategy, Overall Defense Concept (+50% bigger reward on this path) | Blue Tiger strategy, Project National Glory, the reclamation war |

The Overall Defense Concept, Whole-of-Society Defense and Fortress Taiwan stay open to both paths, but give extra rewards on the Porcupine path (for example, Fortress Taiwan adds coastal bunkers). That keeps the historical 2017 doctrine available to everyone.

### 2e. Mastery: the second choice (9 new focuses)

Mastery opens after the **third** focus of either path: Coastal Missile Production (A3) or A Blue-Water Squadron (B3). The player picks one of three mutually exclusive roots, and the others are hidden.

| Mastery | Focuses (ID) | Date gate | Grows the spirit… | With Porcupine | With Conventional |
| --- | --- | --- | --- | --- | --- |
| **Drone Warfare** | Drone Reconnaissance (`TAI_na_drone_mastery`) → Tactical Drones (`TAI_na_drone_tactical`) → Swarms and Loitering Munitions (`TAI_na_drone_swarms`) | 2005 / 2012 / 2017 | **Drone Warfare I → II → III**: research speed on drone categories (`CAT_air_drones`, `CAT_land_drones`, `CAT_naval_recon_drones`), recon and air superiority support | Anti-ship drones, drone torpedoes, naval drone swarms | Helicopter drones, drone artillery ammunition, reconnaissance for armour |
| **Land Warfare** | Land Warfare Mastery (`TAI_na_land_mastery`) → Combined Arms Doctrine (`TAI_na_land_doctrine`) → Elite Ground Forces (`TAI_na_land_elite`) | none | **Land Warfare I → II → III**: land doctrine cost, army organisation, army experience | Infantry and territorial brigades: defence, entrenchment | Armoured brigades: breakthrough, armour speed |
| **Naval Warfare** | Naval Warfare Mastery (`TAI_na_naval_mastery`) → Littoral Doctrine (`TAI_na_naval_doctrine`) → Fleet in Being (`TAI_na_naval_elite`) | none | **Naval Warfare I → II → III**: naval doctrine cost, naval production, ship organisation | Mines, fast attack craft, coastal missile boats | Destroyers, submarines, blue-water operations |

The difference between paths comes from `if` blocks in each mastery focus that read which path was taken. Each mastery has its own focus rewards, not just a list of stat bonuses.

### 2f. AI behaviour

| Taiwan AI Behavior rule | Path | Mastery |
| --- | --- | --- |
| Historical, Island Fortress | Porcupine | Drone (after 2012), otherwise Naval |
| Project National Glory, Unification Channel, Road to Separation | Conventional | Land |
| Accommodation, No Path, Random | Weighted, about 60% Porcupine and 40% Conventional | Weighted |

### 2g. Size and layout

- **New focuses:** 2 roots + 10 path focuses + 9 mastery focuses = **21**, taking the tree from **368 to 389**.
- **Layout:** the National Army branch gets wider. I'll render the new layout and send it for review before building it.
- **Branch hiding:** the unchosen path and masteries are hidden, so a player sees about 12 fewer focuses on screen once committed.

---

## Part 3: How I'll build and check it

1. Silicon Island changes (spirits, plants, capstone) through the generator.
2. Military: new focuses and spirits, the three prerequisite changes, AI weights, localisation, and branch hiding for the unchosen path and masteries.
3. A layout render for your review.
4. Validators against the same baselines, plus a check that a build without these changes reproduces the current tree exactly.
5. Copy into your Millennium Dawn folder, uncommitted, for your in-game test.

## Things that need hands-on checking during the build

- That each state ID (1155 Hsinchu, 1156 Taichung, 1157 Tainan) has a free slot after the extra one is added.
- The exact beach states for Fortify the Beaches, and whether coastal bunkers there can be targeted by province.
- Which drone combat modifiers exist beyond research bonuses. If there are none, Drone Warfare uses research and air and recon bonuses only.
- That −5% division attack on Porcupine doesn't make Return to the Mainland impossible. It shouldn't, because the Conventional path exists for that.
