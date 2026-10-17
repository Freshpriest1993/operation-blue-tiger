# Operation Blue Tiger

Operation Blue Tiger (OBT) is a historically researched overhaul of the Republic of China (Taiwan) for the Hearts of Iron IV mod [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn). It adds a large national focus tree covering political reform, diplomacy, defense modernization, economic development and national resilience, starting from the 1 January 2000 bookmark.

The design goal is a Taiwan that is neither doomed nor invincible. The player's task is to make the island increasingly difficult to coerce at an acceptable political, military and economic price.

> **Status:** Milestone 1 of 4 (focus tree, national spirits, starting conditions). Built against the Millennium Dawn developer version (descriptor 2.0.0, changelog v2.0.1) for HOI4 1.19. Not an official Millennium Dawn release.

## Features

The focus tree has **247 focuses** in seven branches.

| Branch | Focuses | What it covers |
| --- | --- | --- |
| The 2000 Succession | 41 | The three-way 2000 election, the first peaceful transfer of power, divided government, and separate DPP, KMT and PFP paths |
| Democratic Fortress | 30 | Rule of law, anti-corruption, Legislative Yuan and electoral reform, media independence, information resilience |
| The National Army | 50 | Civilian control, five defense doctrines, manpower policy, procurement versus absorption |
| The Silicon Island | 37 | Semiconductors and supply chains, financial reform, infrastructure, energy and food reserves |
| Across the Strait | 29 | Cross-Strait trade and investment, the 1992 question, crisis channels, confidence-building |
| The Pacific Lifeline | 33 | The United States, Japan, Europe, India, diplomatic allies, WTO, WHO and SARS |
| Operation Blue Tiger | 27 | National strategy, continuity of government, civil defense, emergency doctrine |

It also adds **48 national spirits**, including five starting conditions (Young Democracy, Legacy of the Party-Army, Defense-in-Depth Legacy, Large but Uneven Reserve System, and Advanced Procurement, Limited Absorption) and four defense postures.

### Defense doctrines

Taiwan starts with the Defense-in-Depth doctrine of the 1990s and can move through:

1. **Active Defense:** engaging an invasion at sea and at its bases (from 2000).
2. **Hard ROC:** survival, denial and recovery (from 2008, or earlier under the KMT).
3. **Asymmetric Defense:** the Overall Defense Concept (from 2017).
4. **Hybrid Resilience:** combining gray-zone presence with invasion denial.

Buying equipment and absorbing it are separate steps, so purchases do not instantly become readiness.

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

**Copy the files.** Copy the contents of `mod/` into your Millennium Dawn folder, keeping the folder structure. This replaces six Taiwan files.

**Apply the patch.** From your Millennium Dawn folder, run:

```
git apply path/to/operation-blue-tiger/patches/obt-milestone1.patch
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
- [ ] **Milestone 2:** historical events (2000 inauguration, 2004 election and shooting, Anti-Secession Law, State Affairs Fund and Red Shirt protests, 2008 transition)
- [ ] **Milestone 3:** Cross-Strait Pressure System (blockade burden, stockpiles, partner support, staged negotiations with exits)
- [ ] **Milestone 4:** AI behavior, balance and polish

## Research

The content is based on the Operation Blue Tiger research series (six research passes and the original 2000-2010 grand strategy thesis), together with scholarship on Taiwan's democratization by Larry Diamond, Kharis Templeman and Yun-han Chu, and the IISS *Military Balance* for the starting military. The research documents and third-party papers are not included in this repository.

## Credits and license

Operation Blue Tiger is by Freshpriest1993.

It is built on [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn) by the Millennium Dawn team. Files in `mod/` and `patches/` are derived from Millennium Dawn, which is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). This project is released under the same license.

Hearts of Iron IV is a trademark of Paradox Interactive. This project is not affiliated with or endorsed by Paradox Interactive or the Millennium Dawn team.
