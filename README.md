# Operation Blue Tiger

Operation Blue Tiger (OBT) is a historically researched overhaul of the Republic of China (Taiwan) for the Hearts of Iron IV mod [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn). It adds a large national focus tree covering political reform, diplomacy, defense modernization, economic development and national resilience, starting from the 1 January 2000 bookmark.

The design goal is a Taiwan that is neither doomed nor invincible. The player's task is to make the island increasingly difficult to coerce at an acceptable political, military and economic price.

> **Status:** Milestones 1 to 10 complete: focus tree and spirits, historical events, the cross-Strait pressure system, AI paths, the optional Return to the Mainland path, party branches with stronger rewards, the shared Cross-Strait Tension meter, the 2001-2005 crisis events, the Defense and National Reform tab with American arms deliveries, and a historically audited January 2000 order of battle with reserve mobilization. Milestones 5, 7 and 8 are awaiting review by the Millennium Dawn team, and milestones 7 to 9 are in in-game testing. AUG's RoC-development tree is being merged into a single unified Taiwan tree on a local integration branch (see below). Built against the Millennium Dawn developer version (descriptor 2.0.0, changelog v2.0.1) for HOI4 1.19. Not an official Millennium Dawn release.

## Features

The focus tree has **310 focuses** in twelve branches, laid out in three rows: national branches on top and bottom, and a row of party branches in the middle. The unified build with AUG's RoC-development work has 368 (see below).

| Branch | Focuses | What it covers |
| --- | --- | --- |
| The 2000 Succession | 14 | The three-way 2000 election, the first peaceful transfer of power, divided government and the elections that follow |
| Kuomintang | 18 | Localizing the party, the chairman election, the 6-3-3 plan, the 1992 Consensus, the Three Links and a peace framework |
| People First Party | 18 | James Soong's personal machine, the legislative kingmaker, a joint Pan-Blue ticket and Soong's trip to Beijing |
| Democratic Progressive Party | 18 | The Middle Way, the Economic Advisory Conference, One Country on Each Side, the Defensive Referendum and judicial reform |
| Taiwan Solidarity Union | 18 | Lee Teng-hui's party as a coalition partner of a Pan-Green government: name rectification, Hand in Hand, farmers and a new constitution |
| Green Party Taiwan | 18 | The Greens as a coalition partner: a nuclear-free homeland, the Meinong Dam, wetlands, labour and indigenous rights, a Green minister |
| Democratic Fortress | 30 | Rule of law, anti-corruption, Legislative Yuan and electoral reform, media independence, information resilience |
| The National Army | 50 | Civilian control, five defense doctrines, manpower policy, procurement versus absorption |
| The Silicon Island | 37 | Semiconductors and supply chains, financial reform, infrastructure, energy and food reserves |
| Across the Strait | 29 | Cross-Strait trade and investment, the 1992 question, crisis channels, confidence-building |
| The Pacific Lifeline | 33 | The United States, Japan, Europe, India, diplomatic allies, WTO, WHO and SARS |
| Operation Blue Tiger | 27 | National strategy, continuity of government, civil defense, emergency doctrine |

Every focus takes 35 or 70 days: short focuses for the opening weeks of the 2000 succession, 70 days for everything else.

It also adds **88 national spirits**, including five starting conditions (Young Democracy, Legacy of the Party-Army, Defense-in-Depth Legacy, Large but Uneven Reserve System, and Advanced Procurement, Limited Absorption), four defense postures, and the branch and party programs below.

### Focus rewards and spirits

- **Political power on every focus:** at least 50 in the political branches (100 where a focus already granted some) and at least 25 in the national branches.
- **Branch programs:** each of the seven national branches grants a spirit at its first focus and upgrades it twice along the branch, for example *Defense Reform → A Professional Military → Joint Forces*. The upgrades sit on focuses every playthrough can reach.
- **Party programs:** each party branch grants a program spirit at its first focus, upgrades it midway, and replaces it with a capstone spirit at the end. Governing parties reach up to +25-30% political power and +10% stability; coalition partners reach +10% political power and +6% stability.
- **Military:** every National Army focus grants experience (typically 25-40), eleven focuses cut doctrine costs, and each defense posture speeds up the matching doctrine's mastery: Defence in Depth for the 1990s doctrine and Hard ROC, Combined Arms and Green Water for Active Defense, Mission Command and Jeune École for the Overall Defense Concept.

### Historical events

22 historical events cover the period from the first transfer of power to the second: the May 2000 inauguration and the officer corps' response, the 2001 dot-com bust and legislative election, SARS in 2003, the 2004 election-eve shooting and disputed recount, the 2005 Anti-Secession Law and the KMT chairman's visit to Beijing, the 2006 State Affairs Fund inquiry and Red Shirt protests, and the 2008 elections. Party focuses open 14 more events, from the KMT chairman election and the Defensive Referendum to the founding of the Taiwan Solidarity Union. Every party focus takes 70 days, so a full party branch lasts about one presidential term. Ten other focuses also open decision events, such as the Fourth Nuclear Plant crisis, the special defense budget showdown and the HF-2E controversy.

Events follow the governing party: a Pan-Blue Taiwan does not get Pan-Green history, and contested allegations are presented as allegations.

### Crisis events, 2001-2005

Three event chains let Washington, Beijing, Tokyo and Taipei each make their own choices. Every chain stays neutral on contested facts and none of them can start a war.

- **Hainan Island Incident (April 2001).** Starts from Millennium Dawn's existing Chinese event. The United States demands its crew back or expresses regret; China holds the crew, releases them at once, or, rarely and only after honouring its pilot, puts them on trial. Washington can send the "very sorry" letter or refuse, which drags the standoff on. China then keeps the EP-3E for inspection, as happened, or returns it intact. Taiwan decides whether to back Washington quietly or stay out.
- **The 2001 arms package.** The President approves the historical package with Aegis destroyers deferred, approves everything including Aegis, or postpones it. A postponement locks Taiwan's *2001 Arms Package* focus until 1 January 2002; Aegis approval adds a naval electronics bonus to *Accept the Kidd-Class Destroyers*. The President can then say the United States will do "whatever it takes" to help Taiwan defend itself, or reaffirm strategic ambiguity. Taiwan and China each respond.
- **The 2005 U.S.-Japan "2+2" statement.** Japan chooses whether to name the Taiwan Strait among the alliance's common strategic objectives, as it did on 19 February 2005. If it does, Taiwan and China respond.

Each choice moves Strait Tension, American support, U.S. confidence in Taipei or cross-Strait trust, so the tension meter reflects the crises. Choices that did not happen are marked *(Alternate history)*.

### Defense and National Reform

A dedicated tab, separate from Cross-Strait Relations, shows nine national indicators as bars, each with a tooltip explaining what it does and how to change it, plus a tracker for American arms purchases.

| Indicator | Effect |
| --- | --- |
| Military Confidence | Division organization and planning speed |
| Reform Capacity | Research speed and army experience gain |
| National Coordination | Construction speed and stability |
| Mainland Dependence | More factory output, less war support |
| Semiconductor Security | Production efficiency growth |
| U.S. Confidence in Taipei | Washington's trust in Taipei: unlocks U.S. help and procurement steps |
| U.S. Support | Washington's own commitment: slows Pressure to Negotiate and keeps Beijing's harshest options closed |
| Pressure to Negotiate, Taiwan-Centered Identity | Unchanged: they open talks and shape public reactions |

Effects are measured from Taiwan's 2000 starting values, so the game starts balanced and the effects grow as the indicators move. U.S. Confidence (how Washington sees Taipei) and U.S. Support (how committed Washington is) stay separate.

**Arms procurement.** Approval, funding, contract or refit, delivery and crew working-up are separate steps. Completing a focus alone never produces equipment, and deliveries are never charged twice: the money comes from the Special Defense Budget and the existing focuses.

- **Kidd-class destroyers:** funded by a trimmed or full budget, refitted after *Accept the Kidd-Class Destroyers*, and delivered as ROCS Keelung and Su Ao, then Tso Ying and Ma Kong, about a year apart, as in 2005-2006.
- **P-3C Orions:** need a full budget, which the Legislative Yuan historically blocked until 2007, then contract talks and years of refurbishment. Twelve aircraft arrive in batches of four.
- **Diesel submarines:** Taiwan must find a construction partner before 2009: an American yard, the Dutch RDM yard (before it closes in 2004) or a German license. Each partner has strict, non-random conditions. Without one, the program fails as it did historically and Taiwan turns to the Indigenous Submarine Program.
- **Aegis destroyers:** only if Washington approved them in 2001. They are built new, arrive late and raise Cross-Strait Tension.
- Expensive decisions can speed up refits, refurbishment and construction. Programs are suspended while Washington withdraws support, while Taiwan is at war with the United States, or while the Strait is closed by a war the United States is not in. Ships need a naval base to arrive.

Reform decisions in the same tab (Han Kuang exercises, joint operations drills, Pentagon assessments, civil defense and supply-chain reviews) raise the indicators, each with a cooldown. The test checklist is in [`docs/DEFENSE_REFORM_TESTING.md`](docs/DEFENSE_REFORM_TESTING.md).

### Historical order of battle and reserve mobilization

Taiwan starts with the army it had on 1 January 2000, midway through the Jingshi reorganization: 34 named combined-arms brigades and 4 unnumbered garrison brigades under the 6th, 8th and 10th Army Corps and the Kinmen, Matsu, Penghu and Hua-Tung defense commands, the 601st and 602nd Air Cavalry and 862nd Special Warfare Brigades, and the 66th and 99th Marine Divisions. The audit also corrected the destroyer names, based the fleet at Tsoying, added 61 Jin Chiang and Hai Ou missile craft, cut the F-5 fleet to about 160 and removed equipment delivered after 2000. Every change, source and open question is in [`docs/ORDER_OF_BATTLE_AUDIT.md`](docs/ORDER_OF_BATTLE_AUDIT.md).

Reserve brigades never start on the map. The **Reserve Mobilization** tab runs a peacetime readiness program and an annual refresher recall, then partial mobilization (4 brigades in a crisis) and general mobilization (up to 12 in a war with China). Brigades arrive over weeks, fill from the stockpile, gain experience from readiness, and cost political power and industrial output while they serve. Demobilizing sends them home with a one-year cooldown.

### Cross-Strait Pressure System

- **Blockade Burden** reads Beijing's actual blockade each month and is reduced by Taiwan's preparations: strategic reserves, the emergency doctrine, partner arrangements, shipping guarantees and energy rationing. The economic damage itself still comes only from China's blockade, so no loss is counted twice.
- **Pressure to Negotiate** rises while the blockade bites and falls when it lifts. A legitimate government under pressure also gains identity and American support: the coercion paradox.
- **Blue Tiger Emergency** decisions let Taiwan declare time-limited emergency powers, release or rebuild its fuel reserve, guarantee shipping, ration energy, fly in chip materials, request American or Japanese help, publicize or quietly protest incidents, and seek mediation in wartime.
- **Staged talks replace automatic annexation.** When Taiwan seeks terms, it enters economic talks, then a political conference, then a referendum. It can withdraw at every stage, and unification happens only if voters approve. Beijing can offer the talks, and an active blockade costs it political power and stability every month.
- **Defensive war.** If China attacks, Taiwan mobilizes and the United States decides whether to intervene, send aid or stay out, based on its commitment to deterring Beijing and its confidence in Taipei. Taiwan can seek mediation while it still holds Taipei. If Taiwan fires first, American support collapses.

### Cross-Strait Tension meter

China's **One China Strategy** tab and Taiwan's **Cross-Strait Relations** tab both show the same meter from 1 January 2000, in the style of Stalin's paranoia bar. It reads Millennium Dawn's existing Strait Tension value live and divides it into five stages: **Calm** (0-19), **Friction** (20-39), **Coercion** (40-59), **Crisis** (60-79) and **Brink** (80-100).

**The interface.** A colour-graded bar fills from green to red with markers at 20, 40, 60 and 80. The title reads, for example, *CROSS-STRAIT TENSION: 20/100 · FRICTION*; the current stage is highlighted under the bar; a stage line shows the next thresholds; and each side sees four national indicators with last month's change in brackets. Every element has a tooltip explaining its effects and what moves it.

| Taiwan sees | China sees |
| --- | --- |
| Pressure to Negotiate | Cross-Strait Trust |
| Blockade Burden | U.S. Support for Taiwan |
| U.S. Confidence in Taipei | Taiwan Blockade Burden |
| Taiwan-Centered Identity | Taipei's Will to Negotiate (estimate) |

**Stage effects.** Each stage applies one modifier to each country, replaced at every stage change so nothing stacks. Calm is the only stage that pays both sides.

| Stage | China | Taiwan |
| --- | --- | --- |
| Calm | +2% stability, +5% political power, +5% trade, +2% factory output | the same |
| Friction | +1% political power, -2% trade | +2% war support, -2% trade |
| Coercion | -1% stability, -2% political power, -5% trade, +2% organization, +5% army and navy experience | -2% political power, -3% trade, +3% war support, +2% defense, +2% recruitable population, +5% anti-air |
| Crisis | -3% stability, -5% political power, -10% trade, +2% consumer goods, +3% organization, +10% army and navy experience | -2% stability, -4% political power, -6% trade, +2% consumer goods, +5% war support, +4% defense, +4% recruitable population, +10% anti-air |
| Brink | -5% stability, -10% political power, -15% trade, +4% consumer goods, +5% organization, +15% army and navy experience | -4% stability, -6% political power, -10% trade, +4% consumer goods, +8% war support, +5% defense, +6% recruitable population, +15% anti-air |

**Decisions.** Twelve decisions, each with a cost, a cooldown and a one-line summary of how it moves tension.

- **China:** Open the Crisis Hotline, Quiet Channel to Taipei and Issue a Stern Warning from the start; after the One China Framework focus, Surge Coast Guard Patrols, Offer Economic Incentives and, at Brink only, Prepare a Taiwan Contingency (a war goal, never a declaration of war).
- **Taiwan:** Use the Crisis Hotline, Reaffirm the Status Quo, Reopen Cross-Strait Trade Talks, Raise Readiness and Brief Washington; after the Blue Tiger root focus, a Nationwide Civil Defense Drill. Declare a Blue Tiger Emergency also opens at Crisis.

**Events and AI.** A stage change fires one event for each side, rising or falling, with a 180-day cooldown; options trade tension, trust and support rather than handing out free rewards. Both AIs de-escalate when stability is low or tension is high; China's Hegemon path leans on pressure and its Peaceful Rise path on talks, while Taiwan's Accommodation path favours talks and Island Fortress favours readiness.

**Pressure is not control.** No stage declares war, annexes Taiwan or forces it to capitulate. The meter updates monthly, at game start and after its own decisions, never daily.

Changes to Millennium Dawn's own China files are listed in [`docs/CHINA_FILE_CHANGES.md`](docs/CHINA_FILE_CHANGES.md), and the in-game test plan is in [`docs/PRESSURE_SYSTEM_TESTING.md`](docs/PRESSURE_SYSTEM_TESTING.md).

### AI behavior

A **Taiwan** AI path game rule, in Millennium Dawn's standard form, sets how an AI-controlled Taiwan plays:

| Option | AI Taiwan |
| --- | --- |
| Historical | The DPP wins in 2000, trade with the mainland opens, defense moves toward Hard ROC, and the Blue Tiger strategy guides national resilience |
| Cross-Strait Accommodation | The KMT leads, with confidence-building measures, a peace accord track and the Accommodation strategy |
| Island Fortress | Taiwan limits mainland exposure, courts India, extends conscription and builds Fortress Taiwan |
| Random Path / No Path | A random path, or unscripted AI (the default) |

AI Taiwan also prioritizes removing its starting penalties, raises defense focuses when threatened, and is much less willing to enter talks or hold a referendum under the Historical and Island Fortress paths, or while American support is strong.

### Defense doctrines

Taiwan starts with the Defense-in-Depth doctrine of the 1990s and can move through:

1. **Active Defense:** engaging an invasion at sea and at its bases (from 2000).
2. **Hard ROC:** survival, denial and recovery (from 2008, or earlier under the KMT).
3. **Asymmetric Defense:** the Overall Defense Concept (from 2017).
4. **Hybrid Resilience:** combining gray-zone presence with invasion denial.

Buying equipment and absorbing it are separate steps, so purchases do not instantly become readiness.

### Unified tree with AUG's RoC-development work (integration branch)

At TheGeneral's request, Operation Blue Tiger and AUG's RoC-development focus tree are being combined so Taiwan has one tree. The work is on the local branch `integration/obt-roc-unified` and has not been pushed or merged.

- **368 focuses.** 58 of AUG's focuses keep their IDs in the unified tree, including three new branches in the bottom band: **Island Society** (921 reconstruction, labour and welfare reform), **Southern Policy** (Southeast Asia, with the conquest chain hidden behind the off-by-default *Taiwan: Southern Expansion* rule) and **Project National Glory** (a KMT restoration path behind the Return to the Mainland rule).
- **Nothing is deleted.** AUG's other 34 focuses fold their rewards into the OBT focus that covers the same event, or into decisions; his 29 spirits, events, opinion modifiers, portrait and AI options are kept. Every one of the 92 focus IDs is mapped in [`docs/roc_dev/ROC_DEV_MAPPING.md`](docs/roc_dev/ROC_DEV_MAPPING.md).
- **One system for each job.** AUG's regional mobilization theaters run inside the OBT reserve system, his Seventh Fleet invitation is a Cross-Strait decision, and his Red Infiltration path ends in OBT's staged talks and referendum instead of an instant annexation.
- **Layout.** The tree is 88 by 36 cells. Southern Policy and Project National Glory sit under Across the Strait, in the Pacific Lifeline column; Island Society sits under Democratic Fortress with the domestic branches; Operation Blue Tiger sits under Pacific Lifeline, which it depends on. National Glory's exclusion with the democratic capstones is written as a completed-focus check on both sides, so no exclusion lines cross the tree.
- **Originals preserved.** AUG's files are archived byte-exact on the integration branch, and [`docs/roc_dev/INTEGRATION_CHANGELOG.md`](docs/roc_dev/INTEGRATION_CHANGELOG.md) lists every change, fix and balance adjustment for his review.

The `mod/` folder holds the unified build. To build the Operation Blue Tiger tree without AUG's focuses, set `OBT_SKIP_ROC=1` before running `gen.py`.

### Return to the Mainland (alternate history)

An optional path, behind the **Taiwan: Return to the Mainland** game rule (Player Only by default, or Allowed, or Disabled). It is labelled alternate history throughout, because in 1991 Taiwan renounced force against the mainland.

- **The Reclamation Pact.** During a war with China, or while Beijing is in crisis, Taiwan can convene a pact and pledge a postwar referendum, guaranteed autonomy, or no concessions. Each pledge changes mobilization, domestic support and Chinese backlash.
- **Two ways in.** *Carry the War Across the Strait* after holding off an invasion for 60 days (American commitment holds, confidence dips), or *Strike While Beijing Is Divided* (a war of choice that collapses American confidence).
- **Postwar Vision.** A balance-of-power bar runs from ROC Restoration to Taiwanese Self-Determination. Mobilizing pushes it one way, pledges and reassurance the other, and it decides the referendum odds and how badly a broken pledge hurts.
- **Victory is not automatic.** When Beijing capitulates, full restoration needs Beijing, Nanjing, Shanghai, Guangdong, Hubei and Chongqing under Taiwan's control, at least 75% of the mainland's states, an army of 60 or more divisions, 40% stability and 50% war support. Otherwise Taiwan accepts an armistice, keeps the provinces it holds, and can resume the war a year later.
- **The settlement.** Honor the referendum, negotiate continued association, repudiate the pledge (with protests, a general strike and a broken-pact penalty), or rule from Taipei if no pledge was made.
- **Two republics.** If Taiwan votes for its own state, or a federal union is chosen, the mainland becomes a separate Republic of China and the player chooses which country to lead.
- **Provisional Administration.** Whoever holds the mainland starts with heavy penalties and lifts them region by region through five decisions and administrative reforms. The mainland republic gets its own 32-focus reconstruction tree.

The restored mainland republic reuses China's tag with a Republic of China name, flag and parties, so some of China's own decision tabs may still appear for it.

## Design principles

- **More than independence versus unification.** Democracy, identity, the economy, defense and foreign relations move separately.
- **U.S. commitment and U.S. confidence are different.** Washington can protect Taiwan while disapproving of a Taiwanese action. The Taiwan Relations Act is not treated as a war guarantee.
- **Trade and trust are different.** Cross-Strait commerce can grow while political trust falls.
- **Pressure is not control.** No threshold annexes Taiwan or starts a war on its own.
- **Pressure is a dilemma.** Escalation costs Beijing, Taiwan's defensive gains cost it trade and political capital, and only calm pays both sides.
- **No anachronisms at the start.** Taiwan begins in 2000 with an existing semiconductor industry, no WTO seat and no 2017-era doctrine. Later policies unlock on historically appropriate dates.
- **Alternate history is labelled.** Counterfactual content, such as the U.S.-Taiwan Semiconductor Compact and the India partnership tiers, says so in its description.

OBT reuses Millennium Dawn's existing cross-Strait systems (Strait Tension, Cross-Strait Trust and U.S. Support for Taiwan) instead of duplicating them.

## Installation

You need a local copy of Millennium Dawn (the developer version from its GitHub repository).

**Copy the files.** Copy the contents of `mod/` into your Millennium Dawn folder, keeping the folder structure. Most of Operation Blue Tiger lives in its own files, but these shared Millennium Dawn files are replaced:

- `00_yearly_effects.txt`: schedules Taiwan's historical events and the 2001 and 2005 crisis events.
- China's `05_china.txt` (also starts the Hainan chain), `05_CHI_decisions.txt`, `99_CHI_decision_categories.txt` and `MD_focus_CHI_l_english.yml`: staged talks instead of automatic annexation, and the One China Strategy tab visible from the start with the tension meter.
- `00_game_rules.txt`, `999_game_rules_on_actions.txt` and `MD_game_rules_l_english.yml`: the Taiwan AI path and Return to the Mainland game rules.
- `00_MD_politicsview_scripted_localisation.txt` and `MD_politics_view_parties_l_english.yml`: the Taiwan Solidarity Union and the mainland republic's party names.
- `TAI_names_divisions.txt`: researched names for new Taiwanese brigades, such as the 542nd Armored Brigade 'Xunlei' - 6th Army Corps, and a separate reserve pool.
- `TAI - Taiwan.txt` and Taiwan's six `TAI_2000_*` unit files: the audited January 2000 order of battle and two missile boat designs.

Every change to China's files is listed in [`docs/CHINA_FILE_CHANGES.md`](docs/CHINA_FILE_CHANGES.md).

**The patch file** in `patches/` covers milestones 1 to 4 only and predates the later work, so use the copy method for now.

Then start a game as Taiwan, or as China to see the pressure system from Beijing's side, on the 2000 bookmark.

## Repository layout

| Path | Contents |
| --- | --- |
| `mod/` | All Operation Blue Tiger files in Millennium Dawn's folder structure |
| `patches/` | A Git patch of milestones 1 to 4 |
| `tools/` | The generators: `spec.py` defines every Taiwan focus, `layout.py` arranges the tree, `gen.py` builds the focus tree and localisation, and `events_gen.py` builds the events and spirits from `events_spec.py` |
| `tools/m3`, `m4`, `m5`, `m7`, `m8`, `m9`, `m10` | Sources and apply scripts for the pressure system, AI paths, Return to the Mainland, the tension meter, the crisis events and Defense and National Reform, and the order of battle and reserve mobilization |
| `tools/roc` | The RoC-development integration: `roc_spec.py` (AUG's focuses and the 92-row mapping), `build_roc.py` (his spirits, decisions, events and text), `apply_roc.py` and `rebuild.sh` |
| `docs/` | Handoff notes, a focus spreadsheet, the China change log and the tension meter test plan |
| `docs/roc_dev/` | The RoC-development archive notes, focus mapping and integration changelog |

### Regenerating the files

Requires Python 3.10 or later.

```
python tools/gen.py <millennium-dawn-folder> <output-folder>
python tools/events_gen.py <millennium-dawn-folder> <output-folder>
python tools/m7/build7.py tools/m7
python tools/m8/build8.py tools/m8
python tools/m9/build9.py tools/m9/out
python tools/m10/oob10.py <millennium-dawn-folder> tools/m10/out
python tools/m10/mob10.py tools/m10/out
bash tools/roc/rebuild.sh <millennium-dawn-folder> <work-folder>
```

The apply scripts (`apply.py` to `apply10.py`) write the output into a Millennium Dawn checkout. Run them with `--dry-run` first; they refuse to overwrite files that have changed and only add what is missing, so running them twice changes nothing.

## Roadmap

- [x] **Milestone 1:** focus tree, national spirits, starting conditions, localisation
- [x] **Milestone 2:** historical events (2000 inauguration, 2004 election and shooting, Anti-Secession Law, State Affairs Fund and Red Shirt protests, 2008 transition)
- [x] **Milestone 3:** Cross-Strait Pressure System (blockade burden, stockpiles, partner support, staged negotiations with exits)
- [x] **Milestone 4:** AI behavior, balance and polish
- [x] **Milestone 5:** Return to the Mainland (alternate history): reclamation pact, postwar settlement, successor states and the mainland Republic of China
- [x] **Milestone 6:** party branches (KMT, DPP, PFP, Taiwan Solidarity Union, Green Party), a two-row tree layout, stronger rewards, branch and party programs, and military experience and doctrine bonuses
- [x] **Milestone 7:** the shared Cross-Strait Tension meter for China and Taiwan, with five stages, stage effects, decisions, events and AI
- [x] **Milestone 8:** crisis events: the Hainan Island Incident, the 2001 arms package and the 2005 U.S.-Japan statement
- [x] **Milestone 9:** Defense and National Reform tab, real indicator effects, the procurement tracker and American arms deliveries
- [x] **Milestone 10:** audited January 2000 order of battle (army, air, navy, equipment) and reserve mobilization
- [x] **RoC-development integration:** AUG's 92 focuses mapped and merged into one unified tree on `integration/obt-roc-unified` (awaiting AUG's review)
- [ ] Confirm the 373rd and 395th Armored Infantry Brigades' 2000 organization and equipment
- [ ] In-game testing of the tension meter, crisis events, Defense and National Reform and the new order of battle
- [ ] Update to Millennium Dawn 2.0.2
- [ ] Review by the Millennium Dawn team

## Research

The content is based on the Operation Blue Tiger research series (six research passes and the original 2000-2010 grand strategy thesis), together with scholarship on Taiwan's democratization by Larry Diamond, Kharis Templeman and Yun-han Chu, and the IISS *Military Balance* for the starting military. The research documents and third-party papers are not included in this repository.

## Special Contributions

Special contributions to the project were made by **FoggyBottom**,**Samilou**, **Quaza** and **Chairman Mao Zedong**. Without their contributions I would not have been able to make this focus tree. From the bottom of my heart, thank you, contributors!

## Credits and license

Operation Blue Tiger is by Freshpriest1993.

The Island Society, Southern Policy and Project National Glory branches, and the RoC-development spirits, decisions and events in the unified build, are by **AUG**.

It is built on [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn) by the Millennium Dawn team. Files in `mod/` and `patches/` are derived from Millennium Dawn, which is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). This project is released under the same license.

Hearts of Iron IV is a trademark of Paradox Interactive. This project is not affiliated with or endorsed by Paradox Interactive or the Millennium Dawn team.
