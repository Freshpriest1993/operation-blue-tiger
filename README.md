# Operation Blue Tiger

Operation Blue Tiger (OBT) is a historically researched overhaul of the Republic of China (Taiwan) for the Hearts of Iron IV mod [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn). It adds a large national focus tree covering political reform, diplomacy, defense modernization, economic development and national resilience, starting from the 1 January 2000 bookmark.

The design goal is a Taiwan that is neither doomed nor invincible. The player's task is to make the island increasingly difficult to coerce at an acceptable political, military and economic price.

> **Status:** Milestones 1 to 5 complete (focus tree, national spirits, historical events, cross-Strait pressure system, AI paths, and the optional Return to the Mainland path). Milestone 5 is awaiting review by the Millennium Dawn team. Built against the Millennium Dawn developer version (descriptor 2.0.0, changelog v2.0.1) for HOI4 1.19. Not an official Millennium Dawn release.

## Features

The focus tree has **310 focuses** in twelve branches, laid out in three rows: national branches on top and bottom, and a row of party branches in the middle.

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

It also adds **52 national spirits**, including five starting conditions (Young Democracy, Legacy of the Party-Army, Defense-in-Depth Legacy, Large but Uneven Reserve System, and Advanced Procurement, Limited Absorption) and four defense postures.

### Historical events

22 historical events cover the period from the first transfer of power to the second: the May 2000 inauguration and the officer corps' response, the 2001 dot-com bust and legislative election, SARS in 2003, the 2004 election-eve shooting and disputed recount, the 2005 Anti-Secession Law and the KMT chairman's visit to Beijing, the 2006 State Affairs Fund inquiry and Red Shirt protests, and the 2008 elections. Party focuses open 14 more events, from the KMT chairman election and the Defensive Referendum to the founding of the Taiwan Solidarity Union. Every party focus takes 70 days, so a full party branch lasts about one presidential term. Ten other focuses also open decision events, such as the Fourth Nuclear Plant crisis, the special defense budget showdown and the HF-2E controversy.

Events follow the governing party: a Pan-Blue Taiwan does not get Pan-Green history, and contested allegations are presented as allegations.

### Cross-Strait Pressure System

- **Blockade Burden** reads Beijing's actual blockade each month and is reduced by Taiwan's preparations: strategic reserves, the emergency doctrine, partner arrangements, shipping guarantees and energy rationing. The economic damage itself still comes only from China's blockade, so no loss is counted twice.
- **Pressure to Negotiate** rises while the blockade bites and falls when it lifts. A legitimate government under pressure also gains identity and American support: the coercion paradox.
- **Blue Tiger Emergency** decisions let Taiwan declare time-limited emergency powers, release or rebuild its fuel reserve, guarantee shipping, ration energy, fly in chip materials, request American or Japanese help, publicize or quietly protest incidents, and seek mediation in wartime.
- **Staged talks replace automatic annexation.** When Taiwan seeks terms, it enters economic talks, then a political conference, then a referendum. It can withdraw at every stage, and unification happens only if voters approve. Beijing can offer the talks, and an active blockade costs it political power and stability every month.
- **Defensive war.** If China attacks, Taiwan mobilizes and the United States decides whether to intervene, send aid or stay out, based on its commitment to deterring Beijing and its confidence in Taipei. Taiwan can seek mediation while it still holds Taipei. If Taiwan fires first, American support collapses.

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
- **No anachronisms at the start.** Taiwan begins in 2000 with an existing semiconductor industry, no WTO seat and no 2017-era doctrine. Later policies unlock on historically appropriate dates.
- **Alternate history is labelled.** Counterfactual content, such as the U.S.-Taiwan Semiconductor Compact and the India partnership tiers, says so in its description.

OBT reuses Millennium Dawn's existing cross-Strait systems (Strait Tension, Cross-Strait Trust and U.S. Support for Taiwan) instead of duplicating them.

## Installation

You need a local copy of Millennium Dawn (the developer version from its GitHub repository). Choose one method.

**Copy the files.** Copy the contents of `mod/` into your Millennium Dawn folder, keeping the folder structure. This replaces the Taiwan files, adds the Blue Tiger events, decisions and monthly update, and replaces shared Millennium Dawn files: `00_yearly_effects.txt` (schedules the historical events), China's `05_china.txt`, `05_CHI_decisions.txt` and `MD_focus_CHI_l_english.yml` (staged talks in place of automatic annexation), `00_game_rules.txt`, `999_game_rules_on_actions.txt` and `MD_game_rules_l_english.yml` (the Taiwan game rules), and `00_MD_politicsview_scripted_localisation.txt` (Kuomintang party names for the mainland republic).

**Apply the patch.** From your Millennium Dawn folder, run:

```
git apply path/to/operation-blue-tiger/patches/obt-milestones-1-4.patch
```

The patch also adds a line to Millennium Dawn's `Changelog.txt`. If it does not apply cleanly, your Millennium Dawn version has changed those files; use the copy method or regenerate with the tools below.

Then start a game as Taiwan on the 2000 bookmark.

## Repository layout

| Path | Contents |
| --- | --- |
| `mod/` | The Taiwan files in Millennium Dawn's folder structure |
| `patches/` | The milestone as a Git patch for a Millennium Dawn checkout |
| `tools/` | The generator: `spec.py` defines every focus, `gen.py` builds the script and localisation, `apply.py` writes them into a Millennium Dawn checkout |
| `docs/` | Milestone handoff notes and a spreadsheet of every focus, spirit and variable |

### Regenerating the files

Requires Python 3.10 or later.

```
python tools/gen.py <millennium-dawn-folder> <output-folder>
python tools/apply.py <millennium-dawn-folder> <output-folder> tools/blocks --dry-run
```

Remove `--dry-run` to write the files. `apply.py` checks for duplicate IDs and localisation keys first and only adds content, so running it twice changes nothing.

## Roadmap

- [x] **Milestone 1:** focus tree, national spirits, starting conditions, localisation
- [x] **Milestone 2:** historical events (2000 inauguration, 2004 election and shooting, Anti-Secession Law, State Affairs Fund and Red Shirt protests, 2008 transition)
- [x] **Milestone 3:** Cross-Strait Pressure System (blockade burden, stockpiles, partner support, staged negotiations with exits)
- [x] **Milestone 4:** AI behavior, balance and polish
- [x] **Milestone 5:** Return to the Mainland (alternate history): reclamation pact, postwar settlement, successor states and the mainland Republic of China

## Research

The content is based on the Operation Blue Tiger research series (six research passes and the original 2000-2010 grand strategy thesis), together with scholarship on Taiwan's democratization by Larry Diamond, Kharis Templeman and Yun-han Chu, and the IISS *Military Balance* for the starting military. The research documents and third-party papers are not included in this repository.

## Special Contributions

Special contributions to the project were made by **Samilou**, **Quaza** and **Chairman Mao Zedong**. Without their contributions I would not have been able to make this focus tree. From the bottom of my heart, thank you, contributors!

## Credits and license

Operation Blue Tiger is by Freshpriest1993.

It is built on [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn) by the Millennium Dawn team. Files in `mod/` and `patches/` are derived from Millennium Dawn, which is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). This project is released under the same license.

Hearts of Iron IV is a trademark of Paradox Interactive. This project is not affiliated with or endorsed by Paradox Interactive or the Millennium Dawn team.
