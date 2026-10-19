# Research Pass VII: matrix against the unified tree

Status: planning document for review (AUG, FoggyBottom). Nothing here is implemented.
Author: Freshpriest1993
Checked against: the unified 368-focus Taiwan tree on RoC-development (`86b7b287e0`).

## Summary

Research Pass VII proposed roughly 60 new focuses for 2009–2026. This matrix sorts every proposal by how it can be added. The rule: **extend first, add a focus last**. Most of the content attaches to focuses that already exist, or arrives as events and decisions.

| Treatment | Meaning | Count |
| --- | --- | --- |
| **Covered** | Already in the tree; at most a small date-gated addition | 9 |
| **Extend** | An existing focus gets an era-gated or condition-gated reward | 12 |
| **Event** | An event or event chain, fired by date and political conditions or by an existing focus | 18 |
| **Decision** | A decision or reusable mechanic | 4 |
| **New focus** | Only where nothing exists to attach to | 3 |

Rows are counted by their main treatment; several combine two (for example Event + Decision).

**Result:** about 3 new focuses instead of about 60, so the tree goes from 368 to 371. The layout keeps its current branches; the three new focuses go in open space in Island Society and The National Army.

## Design rules for extending

1. **Two gates on every historical addition:** a date window and a political condition, for example `date > 2014.3.1` *and* the KMT governs *and* Cross-Strait dependence is high. Nothing fires just because the calendar reached it.
2. **One growing spirit per party, not a pile of new ones.** Each party branch already follows the pattern program I → program II → capstone spirit (for example `TAI_dpp_program_1` → `TAI_dpp_program_2` → `TAI_dpp_own_path`). Post-2008 content upgrades the capstone spirit to a later-era version instead of adding more spirits.
3. **Every gain has a cost,** as the real policy did. Pension reform saves money and costs stability; conscription adds manpower and costs the economy.
4. **Use the systems Taiwan already has:** Taiwanese identity, US confidence, Cross-Strait trust, dependence and tension, National Coordination, Reform Capacity, and the Postwar Vision balance of power.
5. **Pressure is not control.** No crisis chain leads to war, annexation or capitulation automatically.

## I. 2009–2015: Reconciliation and resistance

| # | Proposal | Year | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- | --- |
| 1 | Rebuild Southern Taiwan (Typhoon Morakot) | 2009 | Event + Decision | `TAI_bt_local_emergency`, `TAI_bt_medical_surge` | Date event in August 2009. The government's response is judged on National Coordination and whether the emergency focuses are done; a relief decision follows |
| 2 | The Cross-Strait Economic Framework (ECFA) | 2010 | Covered | `TAI_as_economic_framework` (from 2009) | Already in the tree. Its completion becomes the trigger for #3 |
| 3 | The Price of Integration (services trade agreement) | 2013 | Event | Fired after `TAI_as_economic_framework`, from 2013 | Negotiate, delay, or push through without full review. The choice decides whether #4 fires |
| 4 | The Sunflower Occupation | 2014 | Event chain (4) | Follows #3 | A Controversial Agreement → Students Occupy the Legislature → The Government Must Respond → A Generation Politicised. Lasting effects on identity, Reform Capacity, Cross-Strait trust and party popularity |
| 5 | The Singapore Encounter (Ma–Xi meeting) | 2015 | Extend | `TAI_su_kmt_peace_framework` | After 2015, with the KMT governing, high Cross-Strait trust and no war, the focus also fires a summit event |

## II. 2016–2019: A new political direction

| # | Proposal | Year | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- | --- |
| 6 | The 2016 Political Transition | 2016 | Event + Extend | Election events; `TAI_su_dpp_own_path` | The result depends on party popularity, not history. A DPP win upgrades `TAI_dpp_own_path` to a 2016-era version; a KMT win does the same for `TAI_kmt_roc_on_taiwan` |
| 7 | A New Southbound Policy | 2016 | Extend | `TAI_as_go_south` | After 2016 the focus gives the larger New Southbound version: ASEAN trade, education and investment, less dependence. Kept separate from AUG's Southern Policy |
| 8 | The Taiping Island Question | 2016 | Event | `TAI_na_gray_zone` | Date event after the July 2016 arbitration ruling: reject the ruling, patrol, or keep quiet, with regional relations at stake |
| 9 | Open New Channels with Washington (Taiwan Travel Act) | 2018 | Extend | `TAI_pl_capitol_hill` | After March 2018 the focus adds US confidence and a higher-level contacts event, at a cost in Cross-Strait tension |
| 10 | Two Visions Across the Strait | 2019 | Event | Date event, January 2019 | Beijing's proposal against Taipei's answer. Options depend on the governing party; reads identity and Cross-Strait trust |
| 11 | Marriage Equality | 2019 | Covered | `TAI_act_748` | Already in the tree |
| 12 | Safeguard Democratic Institutions (Anti-Infiltration Act) | 2019 | Covered | `TAI_df_influence_transparency` | Already grants `TAI_aia` after 2019 |

## III. 2020–2023: The Silicon Shield under pressure

| # | Proposal | Year | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- | --- |
| 13 | Taiwan Can Help | 2020 | Extend | `TAI_pl_sars`, `TAI_pl_wha` | If the 2003 SARS lessons focus is done, the 2020 pandemic response is stronger; mask-diplomacy event. *Check whether Millennium Dawn has a pandemic system to hook into* |
| 14 | The Global Chip Shortage | 2021 | Event | `TAI_ss_supply_chain`, chip security | Demand spike event; choices between domestic supply, allied customers and price |
| 15 | Water for the Silicon Shield | 2021 | Event + Decision | `TAI_ss_materials_inventory` | Drought event; a decision rations water between fabs, farms and cities |
| 16 | The 2022 Strait Crisis (working title) | 2022 | Event chain (4) | Cross-Strait tension | A Delegation Requests a Visit → Exercises Across the Strait → The Median Line Under Pressure → A New Regional Status Quo? Taiwan, the United States and China each get options. Never leads to war on its own |
| 17 | Rebuild the Conscription System / A Year of Service | 2022–2024 | Extend | `TAI_na_extended_conscription`, `TAI_na_professional_force` | After December 2022 a decision restores one-year service: manpower and training against economic cost. Covers #22 too |
| 18 | Launch the Indigenous Submarine | 2023 | Extend + Decision | `TAI_na_indigenous_submarine` | Already in the tree (from 2010). Add the four milestones (development, construction, launch, acceptance trials) as procurement decisions with delay risk |
| 19 | The Twenty-First-Century Trade Initiative | 2023 | Extend | `TAI_pl_tifa` | After June 2023 the focus also signs the first agreement: US confidence, investment, less dependence |

## IV. 2024–2026: Deterrence and democratic resilience

| # | Proposal | Year | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- | --- |
| 20 | A Divided Legislature: Legislative Negotiations | 2024 | Decision (mechanic) | `TAI_su_minority_government`, `TAI_divided_government` | Reusable decisions whenever the government lacks a majority: negotiate, revise procurement, prioritise social spending, cross-party defence deal. Works for 2000–2008 too |
| 21 | The Bluebird Movement | 2024 | Event chain | Follows #20 | Uses the same template as the Sunflower chain, triggered by a clash over legislative powers |
| 22 | A Year of Service | 2024 | Covered | #17 | Merged into #17 |
| 23 | Encirclement Exercises (Joint Sword) | 2024 | Event | Cross-Strait tension | One reusable "PLA exercise" event family covering #23 and #26, scaled by tension |
| 24 | Whole-of-Society Resilience | 2024 | Covered + Extend | `TAI_na_whole_of_society`, Han Kuang decision | After 2024 the focus also creates the resilience committee: National Coordination and faster mobilisation |
| 25 | A New Generation of Armour (M1A2T) | 2024 | Decision | Procurement pipeline | Staged delivery: arrival, training, battalion in service |
| 26 | Strait Thunder | 2025 | Event | #23 | Same event family as #23, with a blockade-rehearsal variant |
| 27 | The Great Recall | 2025 | Event | Party popularity | A civic campaign whose result depends on public mood, party organisation and earlier choices. Never guaranteed |
| 28 | Modernise the Fighter Fleet (F-16V Block 70) | 2026 | Extend + Decision | `TAI_na_fighter_fleet` | Staged deliveries as procurement decisions, with long delays possible |

## V. Domestic subjects

| # | Proposal | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- |
| 29 | Expand Offshore Wind | Extend | `TAI_ss_renewables` | After 2016 the focus adds offshore wind: energy supply, more resistant to blockade |
| 30 | Reconsider Nuclear Power | Event | `TAI_maanshan_nuclear_power_military_expansion`, `TAI_su_gpt_nuclear_free` | 2025 shutdown, referendum and licence renewal. Outcome depends on earlier nuclear choices and the Greens' influence |
| 31 | Protect the National Grid | Covered | `TAI_bt_restore_grid`, `TAI_ss_coal_stocks` | Already in the tree |
| 32 | An Aging Republic / Family Support Reform | **New focus** | Island Society, after `TAI_long_term_care` | Island Society has only 10 focuses, so there is room. Spending against workforce and recruitment |
| 33 | Resilient Infrastructure (Hualien 2024) | Event + Decision | `TAI_bt_local_emergency` | A reusable earthquake event; a "Reinforce Critical Facilities" decision |
| 34 | Secure Government Networks | Extend | `TAI_na_info_warfare` | After 2016 the focus adds network defence against cyber intrusion events |
| 35 | Protect the Undersea Cables | **New focus** | The National Army, near `TAI_na_gray_zone` | Nothing covers this today. Links to the 2023 Matsu cable cuts and the gray-zone events |
| 36 | Counter Foreign Interference | Covered | `TAI_df_counter_disinfo` | Already in the tree |
| 37 | Build Digital Resilience | Extend | `TAI_bt_redundant_comms` | After 2020 adds satellite and backup links |

## VI. Late-game chains and other gaps

| # | Proposal | Treatment | Attaches to | How it works |
| --- | --- | --- | --- | --- |
| 38 | The Silicon Shield Goes Global | Decision | `TAI_ss_silicon_shield` | Choose domestic capacity, overseas fabs or partnerships; each carries a different risk |
| 39 | The Gray-Zone Challenge | Covered + Event | `TAI_na_gray_zone` | Recurring coast-guard incidents with protest, monitoring or hotline responses |
| 40 | National Resilience Exercises | Covered | Han Kuang decision | Scales with date (longer exercises, more reservists) |
| 41 | The Battle for Diplomatic Recognition | Decision | `TAI_pl_keep_allies`, `TAI_pl_end_checkbook` | Recurring aid and engagement decisions; losses depend on conditions |
| 42 | Advanced semiconductors and AI-era investment | Extend | `TAI_ss_advanced_process` | After 2018 the focus gives a leading-edge version |
| 43 | The 2018 local elections and referendums | Event | Party popularity | Midterm event; referendum results read identity and earlier choices |
| 44 | The rise of the Taiwan People's Party | Event | Party names | Activates the existing TPP party name (`TAI.neutral_Social_1`) from 2019 |
| 45 | The 2020 presidential election | Event | Election events | Shares the election framework with #6 |
| 46 | A third new focus (reserve) | **New focus** | To decide | Held in reserve for whichever gap testing shows is most visible. Candidate: a Silicon Island energy-transition hub |

## Order of work (unchanged from Pass VII)

1. **2009–2015:** #1–5, plus the Legislative Negotiations mechanic (#20), since it also improves the 2000–2008 content.
2. **2016–2023:** #6–19.
3. **2024–2026:** #21–28.
4. **Domestic subjects and late-game chains:** #29–46.

## To check by hand before building

- Whether Millennium Dawn has a pandemic system for #13.
- How Millennium Dawn runs Taiwan's elections after 2004, so #6 and #45 hook into it rather than duplicate it.
- The real dates for every date gate, against the Pass VII references.
- Balance for the era-upgraded spirits, which should not make the late game easier than the early game.
