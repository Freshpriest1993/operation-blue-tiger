# Taiwan focus tree: effects and completion-time audit

Status: report only. No focus rewards have been changed.
Author: Freshpriest1993
Checked against: the unified Taiwan tree with branch hiding, Silicon Island and the power stations (368 focuses).

## How to read this report

Every focus reward was read from the generator specification and sorted into one of these categories:

| Category | What it covers |
| --- | --- |
| **Generic** | Political power, stability, corruption |
| **Politics** | War support, party popularity |
| **Meters** | Taiwan's own variables (Taiwanese identity, US confidence, Reform Capacity, National Coordination, pressure to negotiate, mainland dependence, chip security, military confidence) and China's Cross-Strait variables |
| **Unique** | A national spirit, research bonus, building, event, opinion modifier, unlocked decision, units, diplomatic or war effect, or political change |

A focus counts as **"no unique reward"** if it gives only generic, politics and meter rewards. The **reward score** is a rough measure for comparing focuses, not a balance value: 50 political power, 5% stability, 5 meter points or a corruption step each count about 1; a spirit about 3; a building or a research bonus about 2 to 2.5.

## Headline findings

- **Political power is on 323 of 368 focuses (88%)**, usually 25 to 100, whether or not it fits the focus. That alone makes many focuses feel alike.
- **Stability is on 93 focuses and corruption on 18.** Corruption is concentrated in Democratic Fortress, which explains why that branch feels repetitive.
- **165 focuses (45%) have no unique reward.** 46 of them give *only* political power, stability or corruption.
- **117 focuses take 70 days but score under 3**, so their reward is small for the time they take.
- **25 sets of focuses share identical rewards** (ignoring political power), covering 78 focuses.
- **Taiwan's meters do carry most of the tree's identity**, but the same few values repeat (for example "pressure to negotiate −3" or "chip security +10"). When a meter is the only reward, the focus reads as a number change rather than a policy.
- **AUG's branches (Island Society, Southern Policy, Project National Glory) score best on uniqueness**: their rewards are mostly spirits, events, units and political changes.

## By branch

| Branch | Focuses | Political power | Stability | Corruption | No unique reward | Only generic | Weak 70-day | Average score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| The 2000 Succession | 14 | 14 | 7 | 0 | 6 | 3 | 2 | 4.2 |
| Democratic Fortress | 30 | 30 | 21 | 10 | 24 | 15 | 20 | 3.1 |
| The National Army | 53 | 50 | 2 | 0 | 9 | 0 | 6 | 4.9 |
| The Silicon Island | 41 | 37 | 6 | 0 | 12 | 3 | 14 | 3.7 |
| Across the Strait | 34 | 30 | 3 | 0 | 19 | 0 | 11 | 4.0 |
| The Pacific Lifeline | 35 | 34 | 5 | 1 | 17 | 5 | 15 | 2.7 |
| Operation Blue Tiger | 28 | 27 | 6 | 1 | 16 | 2 | 12 | 2.8 |
| Kuomintang | 19 | 19 | 6 | 1 | 10 | 1 | 3 | 4.3 |
| People First Party | 18 | 18 | 8 | 2 | 11 | 3 | 6 | 4.0 |
| Democratic Progressive Party | 19 | 18 | 7 | 3 | 8 | 2 | 2 | 5.7 |
| Taiwan Solidarity Union | 18 | 18 | 5 | 0 | 13 | 3 | 10 | 3.5 |
| Green Party Taiwan | 18 | 18 | 12 | 0 | 14 | 4 | 14 | 2.8 |
| Island Society | 10 | 5 | 2 | 0 | 2 | 2 | 0 | 4.3 |
| Southern Policy | 16 | 2 | 0 | 0 | 2 | 2 | 2 | 2.6 |
| Project National Glory | 15 | 3 | 3 | 0 | 2 | 1 | 0 | 5.1 |

Worst first, by share of focuses without a unique reward: Democratic Fortress (24 of 30), Green Party (14 of 18), TSU (13 of 18), Across the Strait (19 of 34), Operation Blue Tiger (16 of 28), Pacific Lifeline (17 of 35). This matches Droid's priority of economy and foreign policy first, then politics: Pacific Lifeline and Across the Strait are the foreign-policy core, and Democratic Fortress plus the party branches are the political core.

## 1. Focuses that rely only on political power, stability or corruption

| Branch | Focus | Days | Reward |
| --- | --- | --- | --- |
| The 2000 Succession | Let the Voters Decide (`TAI_su_voters_decide`) | 35 | stab:0.05, pp:100 |
| The 2000 Succession | A Unified Government (`TAI_su_unified_government`) | 35 | pp:125, stab:-0.02 |
| The 2000 Succession | Democracy's Second Test (`TAI_su_second_test`) | 70 | stab:0.06, pp:100 |
| Democratic Fortress | Professionalize the Judiciary (`TAI_df_professional_judiciary`) | 70 | stab:0.05, pp:50 |
| Democratic Fortress | Strengthen the Grand Justices (`TAI_df_grand_justices`) | 70 | stab:0.05, pp:100 |
| Democratic Fortress | A Special Investigation Division (`TAI_df_special_division`) | 70 | corr:-1, stab:-0.03, pp:50 |
| Democratic Fortress | Trust the Ordinary Prosecutors (`TAI_df_ordinary_prosecutors`) | 70 | stab:0.06, pp:50 |
| Democratic Fortress | Clean Up Black Gold (`TAI_df_black_gold`) | 70 | corr:-1, stab:-0.02, pp:50 |
| Democratic Fortress | Sunshine Laws (`TAI_df_sunshine_laws`) | 70 | corr:-1, stab:0.04, pp:50 |
| Democratic Fortress | Reform the Farmers' Associations (`TAI_df_farmers_associations`) | 70 | corr:-1, stab:-0.02, pp:50 |
| Democratic Fortress | Audit the Special Funds (`TAI_df_special_funds_audit`) | 70 | corr:-1, stab:0.05, pp:50 |
| Democratic Fortress | Settle the Executive Question (`TAI_df_settle_executive`) | 70 | stab:0.05, pp:100 |
| Democratic Fortress | Reform the Legislative Yuan (`TAI_df_legislative_reform`) | 70 | pp:100 |
| Democratic Fortress | End the SNTV System (`TAI_df_end_sntv`) | 70 | corr:-1, stab:0.04, pp:50 |
| Democratic Fortress | The National Assembly Votes Itself Out (`TAI_df_national_assembly`) | 70 | stab:0.07, pp:100 |
| Democratic Fortress | Protect the Control Yuan (`TAI_df_control_yuan`) | 70 | corr:-1, pp:50 |
| Democratic Fortress | Open the Commissions to Civil Society (`TAI_df_civil_commissions`) | 70 | stab:0.05, pp:50 |
| Democratic Fortress | Get the Parties Out of Television (`TAI_df_party_tv_exit`) | 70 | stab:0.04, pp:50 |
| The Silicon Island | The Island Trading Economy (`TAI_ss_trading_economy`) | 70 | pp:50, stab:0.02 |
| The Silicon Island | Consolidate the Banks (`TAI_ss_bank_consolidation`) | 70 | stab:0.02, pp:50 |
| The Silicon Island | Protect Farmers After the WTO (`TAI_ss_wto_farmers`) | 70 | money:-1, stab:0.03, pp:25 |
| The Pacific Lifeline | Europe's Commercial Stake (`TAI_pl_europe`) | 70 | pp:50 |
| The Pacific Lifeline | Friends in the European Parliament (`TAI_pl_european_parliament`) | 35 | stab:0.01, pp:50 |
| The Pacific Lifeline | Keep the Diplomatic Allies (`TAI_pl_keep_allies`) | 70 | money:-3, pp:50 |
| The Pacific Lifeline | End Checkbook Diplomacy (`TAI_pl_end_checkbook`) | 70 | money:2, stab:0.02, pp:25 |
| The Pacific Lifeline | Transparent Aid Diplomacy (`TAI_pl_transparent_aid`) | 70 | corr:-1, pp:50 |
| Operation Blue Tiger | Unambiguous Succession (`TAI_bt_succession`) | 35 | stab:0.03, pp:25 |
| Operation Blue Tiger | Emergency Medical Surge (`TAI_bt_medical_surge`) | 70 | money:-1, stab:0.02, pp:25 |
| Kuomintang | Settle the Party Assets (`TAI_su_kmt_party_assets`) | 70 | corr:-1, stab:0.05, pp:50 |
| People First Party | The Clean Sweep (`TAI_su_pfp_clean_sweep`) | 70 | corr:-1, stab:-0.02, pp:50 |
| People First Party | Sunshine Laws (`TAI_su_pfp_sunshine_laws`) | 70 | corr:-1, stab:0.04, pp:50 |
| People First Party | Reunite the Pan-Blue Camp (`TAI_su_pfp_reunite_blue`) | 70 | pp:100 |
| Democratic Progressive Party | A Clean Green Party (`TAI_su_dpp_clean_party`) | 70 | corr:-1, stab:0.04, pp:50 |
| Democratic Progressive Party | Judicial Reform (`TAI_su_dpp_judicial_reform`) | 70 | corr:-1, stab:0.04, pp:50 |
| Taiwan Solidarity Union | The Balance in the Legislature (`TAI_su_tsu_balance`) | 70 | pp:100 |
| Taiwan Solidarity Union | WTO Safeguards (`TAI_su_tsu_wto_safeguards`) | 70 | money:-2, stab:0.04, pp:50 |
| Taiwan Solidarity Union | Seats in the Cabinet (`TAI_su_tsu_cabinet_seats`) | 70 | stab:0.05, pp:100 |
| Green Party Taiwan | Labor Rights (`TAI_su_gpt_labor`) | 70 | stab:0.04, money:-2, pp:50 |
| Green Party Taiwan | Clean Air for the South (`TAI_su_gpt_clean_air`) | 70 | stab:0.04, money:-2, pp:50 |
| Green Party Taiwan | An Ecological Tax (`TAI_su_gpt_ecological_tax`) | 70 | money:3, stab:-0.01, pp:50 |
| Green Party Taiwan | Organic Farming (`TAI_su_gpt_organic_farming`) | 70 | stab:0.03, money:-1, pp:50 |
| Island Society | Labour Reform (`TAI_labour_reform`) | 35 | pp:150 |
| Island Society | Social Welfare Reform (`TAI_social_walfare`) | 35 | pp:150 |
| Southern Policy | Southern Policy (`TAI_southern_policy`) | 49 | pp:50 |
| Southern Policy | Road to Peace (`TAI_in_peaceful_way`) | 35 | pp:25 |
| Project National Glory | Operation Plan (`TAI_operation_plan`) | 35 | pp:125 |

## 2. Identical rewards

Political power is ignored when comparing. Bracketed items are scripted effects (for example *[building]* or *[event]*).

| Shared reward | Focuses |
| --- | --- |
| diplomacy/war | Southeast Asia Regional Defense Treaty (Southern Policy); ROC Forces Guard Southeast Asia (Southern Policy); Declaration of War on the Philippines (Southern Policy); Declaration of War on Malaysia (Southern Policy); Declaration of War on Vietnam (Southern Policy); Declaration of War on Thailand (Southern Policy); Declaration of War on Indonesia (Southern Policy) |
| stab:0.05 | Let the Voters Decide (The 2000 Succession); Professionalize the Judiciary (Democratic Fortress); Strengthen the Grand Justices (Democratic Fortress); Settle the Executive Question (Democratic Fortress); Open the Commissions to Civil Society (Democratic Fortress); Seats in the Cabinet (Taiwan Solidarity Union) |
| event, other | Return to One China (Across the Strait); Demand the surrender of the Philippines (Southern Policy); Demand the surrender of Malaysia (Southern Policy); Demand the surrender of Vietnam (Southern Policy); Demand the surrender of Thailand (Southern Policy); Demand the surrender of Indonesia (Southern Policy) |
| corr:-1, stab:0.04 | Sunshine Laws (Democratic Fortress); End the SNTV System (Democratic Fortress); Sunshine Laws (People First Party); A Clean Green Party (Democratic Progressive Party); Judicial Reform (Democratic Progressive Party) |
| opinion | Consult Tokyo: The Geographic Anchor (The Pacific Lifeline); Look West to New Delhi (The Pacific Lifeline); Make APEC Count (The Pacific Lifeline); Establish Unofficial Diplomatic Relations (Southern Policy); Road to War (Southern Policy) |
| var:ptn:-5 | Media Literacy for All (Democratic Fortress); Pre-Arranged U.S. Credit Facility (The Pacific Lifeline); Japanese Credit Guarantees (The Pacific Lifeline); Publish the Reserve Levels (Operation Blue Tiger) |
| var:ptn:-3 | A Defined Reserve Facility (The Silicon Island); Emergency Shipping Arrangements (The Silicon Island); Rationing Without Panic (Operation Blue Tiger); Keep the Ports Open (Operation Blue Tiger) |
| event | Heal the KMT Split (The 2000 Succession); The Fourth Nuclear Plant Question (The 2000 Succession); Elect the Chairman (Kuomintang) |
| corr:-1, stab:-0.02 | Clean Up Black Gold (Democratic Fortress); Reform the Farmers' Associations (Democratic Fortress); The Clean Sweep (People First Party) |
| spirit | Experts, Not Loyalists (Democratic Fortress); Lessons of SARS (The Pacific Lifeline); Expand Representative Offices (The Pacific Lifeline) |
| var:chips:10 | Protect Critical Supply Chains (The Silicon Island); Japanese Materials Alliance (The Silicon Island); Semiconductor Continuity Pact (Operation Blue Tiger) |
| money:-2, stab:0.04 | WTO Safeguards (Taiwan Solidarity Union); Labor Rights (Green Party Taiwan); Clean Air for the South (Green Party Taiwan) |
| stab:0.06 | Democracy's Second Test (The 2000 Succession); Trust the Ordinary Prosecutors (Democratic Fortress) |
| corr:-1, stab:0.05 | Audit the Special Funds (Democratic Fortress); Settle the Party Assets (Kuomintang) |
| corr:-1 | Protect the Control Yuan (Democratic Fortress); Transparent Aid Diplomacy (The Pacific Lifeline) |
| money:-1, var:ptn:-3 | Expand Public Broadcasting (Democratic Fortress); National Food Reserve (The Silicon Island) |
| stab:0.02 | The Island Trading Economy (The Silicon Island); Consolidate the Banks (The Silicon Island) |
| money:-3, spirit | Clear the Bad Loans (The Silicon Island); Strategic Petroleum Reserve (The Silicon Island) |
| stab:0.02, var:ptn:-3 | National Marine Insurance Pool (The Silicon Island); Financial Continuity Plan (Operation Blue Tiger) |
| money:-1, stab:0.03 | Protect Farmers After the WTO (The Silicon Island); Organic Farming (Green Party Taiwan) |
| chi:tension:-3, chi:trust:5 | Restore the Spirit of the 1992 Talks (Across the Strait); Revive the SEF-ARATS Channel (Across the Strait) |
| chi:trust:5, event | A Party-to-Party Platform (Kuomintang); Soong Goes to Beijing (People First Party) |
| var:identity:3, event | The Defensive Referendum (Democratic Progressive Party); March to Rectify the Name (Taiwan Solidarity Union) |
| chi:tension:10, var:identity:10, var:usconf:-5, event | Name Rectification (Democratic Progressive Party); Join the UN as Taiwan (Democratic Progressive Party) |
| party:17:0.01, stab:0.03 | Save the Qigu Wetlands (Green Party Taiwan); Protect the East Coast (Green Party Taiwan) |

**Most repeated reward patterns** (same kinds of reward, different numbers):

| Pattern | Focuses |
| --- | --- |
| political power + stability | 20 |
| political power | 19 |
| corruption + political power + stability | 11 |
| treasury + political power + stability | 9 |
| political power + stability + pressure to negotiate | 8 |
| political power + pressure to negotiate | 8 |
| party popularity + political power | 8 |
| spirit + political power | 7 |
| spirit + political power + spirit swap | 7 |
| treasury | 6 |
| political power + chip security | 6 |

## 3. Weak focuses (70 days, score under 3)

These are the first candidates either for a stronger, more specific reward or for a shorter 35-day completion time (see section 5).

| Branch | Focus | Score | Reward |
| --- | --- | --- | --- |
| The 2000 Succession | Seek a Second Mandate (`TAI_su_second_mandate`) | 2.8 | [scripted], stab:0.04, pp:50 |
| The 2000 Succession | Healing a Divided Island (`TAI_su_heal_divided_island`) | 2.9 | stab:0.07, var:ptn:-3, pp:50 |
| Democratic Fortress | Expand Public Broadcasting (`TAI_df_public_broadcasting`) | 1.5 | money:-1, var:ptn:-3, pp:50 |
| Democratic Fortress | Get the Parties Out of Television (`TAI_df_party_tv_exit`) | 1.8 | stab:0.04, pp:50 |
| Democratic Fortress | Media Literacy for All (`TAI_df_media_literacy`) | 1.8 | var:ptn:-5, pp:50 |
| Democratic Fortress | Professionalize the Judiciary (`TAI_df_professional_judiciary`) | 2.0 | stab:0.05, pp:50 |
| Democratic Fortress | Reform the Legislative Yuan (`TAI_df_legislative_reform`) | 2.0 | pp:100 |
| Democratic Fortress | Protect the Control Yuan (`TAI_df_control_yuan`) | 2.0 | corr:-1, pp:50 |
| Democratic Fortress | Open the Commissions to Civil Society (`TAI_df_civil_commissions`) | 2.0 | stab:0.05, pp:50 |
| Democratic Fortress | Trust the Ordinary Prosecutors (`TAI_df_ordinary_prosecutors`) | 2.2 | stab:0.06, pp:50 |
| Democratic Fortress | Voices of Every Community (`TAI_df_every_community`) | 2.3 | var:identity:3, stab:0.04, pp:50 |
| Democratic Fortress | Rapid Factual Communication (`TAI_df_rapid_facts`) | 2.3 | var:ptn:-3, stab:0.04, pp:50 |
| Democratic Fortress | Clean Up Black Gold (`TAI_df_black_gold`) | 2.4 | corr:-1, stab:-0.02, pp:50 |
| Democratic Fortress | Reform the Farmers' Associations (`TAI_df_farmers_associations`) | 2.4 | corr:-1, stab:-0.02, pp:50 |
| Democratic Fortress | End the Vote-Buying Economy (`TAI_df_vote_buying`) | 2.5 | corr:-1, party:1:-0.01, pp:50 |
| Democratic Fortress | A Special Investigation Division (`TAI_df_special_division`) | 2.6 | corr:-1, stab:-0.03, pp:50 |
| Democratic Fortress | A Neutral Civil Service (`TAI_df_civil_service`) | 2.6 | var:coord:5, var:reform:5, pp:50 |
| Democratic Fortress | Counter-Disinformation Center (`TAI_df_counter_disinfo`) | 2.7 | var:ptn:-8, stab:-0.02, pp:50 |
| Democratic Fortress | A Reformist Justice Minister (`TAI_df_justice_minister`) | 2.8 | var:reform:5, corr:-1, pp:50 |
| Democratic Fortress | Sunshine Laws (`TAI_df_sunshine_laws`) | 2.8 | corr:-1, stab:0.04, pp:50 |
| Democratic Fortress | End the SNTV System (`TAI_df_end_sntv`) | 2.8 | corr:-1, stab:0.04, pp:50 |
| Democratic Fortress | Confront the Martial-Law Past (`TAI_df_martial_law_past`) | 2.8 | stab:0.05, var:milconf:-5, pp:50 |
| The National Army | Effective Deterrence, Resolute Defense (`TAI_na_effective_deterrence`) | 1.7 | navy_xp:30, air_xp:30, pp:25 |
| The National Army | Secure U.S. Defense Links (`TAI_na_us_links`) | 2.0 | chi:ussupport:3, var:usconf:3, pp:25, air_xp:25 |
| The National Army | Contest the Gray Zone (`TAI_na_gray_zone`) | 2.0 | navy_xp:25, air_xp:25, var:ptn:-3, pp:25 |
| The National Army | Reform the Political Warfare Department (`TAI_na_political_warfare`) | 2.2 | stab:0.02, var:milconf:5, pp:25, army_xp:25 |
| The National Army | Interoperability Without Alliance (`TAI_na_interoperability`) | 2.3 | var:reform:5, army_xp:25, air_xp:25, pp:25 |
| The National Army | Empower the Chungshan Institute (`TAI_na_csist`) | 2.9 | tech:CAT_missiles:0.5:2, money:-2, pp:25, army_xp:20 |
| The Silicon Island | Coal Stockpiles for the Grid (`TAI_ss_coal_stocks`) | 0.8 | var:ptn:-2, money:-1, pp:25 |
| The Silicon Island | National Food Reserve (`TAI_ss_food_reserve`) | 1.0 | money:-1, var:ptn:-3, pp:25 |
| The Silicon Island | Emergency Shipping Arrangements (`TAI_ss_emergency_shipping`) | 1.0 | var:ptn:-3, pp:25 |
| The Silicon Island | Protect Farmers After the WTO (`TAI_ss_wto_farmers`) | 1.1 | money:-1, stab:0.03, pp:25 |
| The Silicon Island | The Island Trading Economy (`TAI_ss_trading_economy`) | 1.4 | pp:50, stab:0.02 |
| The Silicon Island | Consolidate the Banks (`TAI_ss_bank_consolidation`) | 1.4 | stab:0.02, pp:50 |
| The Silicon Island | National Marine Insurance Pool (`TAI_ss_marine_insurance`) | 1.4 | var:ptn:-3, stab:0.02, pp:25 |
| The Silicon Island | A Defined Reserve Facility (`TAI_ss_fx_facility`) | 1.5 | pp:50, var:ptn:-3 |
| The Silicon Island | Expand the Southern Science Park (`TAI_ss_southern_park`) | 1.9 | [scripted], stab:0.02, pp:25 |
| The Silicon Island | Protect Critical Supply Chains (`TAI_ss_supply_chain`) | 2.1 | var:chips:10, pp:25 |
| The Silicon Island | Strategic Materials Inventory (`TAI_ss_materials_inventory`) | 2.1 | var:chips:10, money:-2, pp:25 |
| The Silicon Island | Japanese Materials Alliance (`TAI_ss_japan_materials`) | 2.1 | var:chips:10, pp:25 |
| The Silicon Island | Biotech Takeoff (`TAI_ss_biotech`) | 2.5 | tech:CAT_genetics:0.5:2, pp:25 |
| The Silicon Island | U.S.-Taiwan Semiconductor Compact (`TAI_ss_us_compact`) | 2.9 | chi:ussupport:5, var:usconf:5, var:chips:5, money:5, pp:25 |
| Across the Strait | The Taishang Question (`TAI_as_taishang`) | 1.5 | var:dep:3, pp:50 |
| Across the Strait | Sector Investment Caps (`TAI_as_investment_caps`) | 1.8 | var:dep:-5, var:ptn:-3, pp:25 |
| Across the Strait | Active Management, Effective Opening (`TAI_as_tighten_management`) | 1.8 | var:dep:-5, chi:trust:-3, pp:25 |
| Across the Strait | Mainland Tourists (`TAI_as_mainland_tourists`) | 1.8 | var:dep:5, chi:trust:3, pp:25 |
| Across the Strait | Restore the Spirit of the 1992 Talks (`TAI_as_restore_1992_spirit`) | 1.8 | chi:trust:5, chi:tension:-3, pp:25 |
| Across the Strait | Revive the SEF-ARATS Channel (`TAI_as_sef_arats`) | 1.8 | chi:trust:5, chi:tension:-3, pp:25 |
| Across the Strait | Answer the Anti-Secession Law (`TAI_as_anti_secession`) | 1.9 | var:identity:3, chi:ussupport:3, stab:0.02, pp:25 |
| Across the Strait | Structured Restraint (`TAI_as_structured_restraint`) | 2.1 | chi:ussupport:5, var:usconf:5, pp:25 |
| Across the Strait | Military Confidence-Building Measures (`TAI_as_cbms`) | 2.3 | chi:tension:-8, var:milconf:-3, pp:25 |
| Across the Strait | The Assent of the People of Taiwan (`TAI_as_assent`) | 2.5 | var:ptn:-10, stab:0.02, pp:25 |
| Across the Strait | The Journey of Peace (`TAI_as_journey_of_peace`) | 2.9 | chi:trust:10, chi:tension:-5, pp:25 |
| The Pacific Lifeline | End Checkbook Diplomacy (`TAI_pl_end_checkbook`) | 0.9 | money:2, stab:0.02, pp:25 |
| The Pacific Lifeline | Coast Guard Talks with Japan (`TAI_pl_japan_coast_guard`) | 1.0 | navy_xp:10, var:ptn:-2, pp:25 |
| The Pacific Lifeline | Europe's Commercial Stake (`TAI_pl_europe`) | 1.0 | pp:50 |
| The Pacific Lifeline | Tier II: Controlled Licensing (`TAI_pl_india_tier2`) | 1.0 | money:3, var:dep:-3, pp:25 |
| The Pacific Lifeline | Keep the Diplomatic Allies (`TAI_pl_keep_allies`) | 1.0 | money:-3, pp:50 |
| The Pacific Lifeline | Unofficial Security Dialogue with Japan (`TAI_pl_japan_dialogue`) | 1.1 | chi:ussupport:2, chi:tension:2, pp:25 |
| The Pacific Lifeline | Pre-Arranged U.S. Credit Facility (`TAI_pl_us_credit`) | 1.3 | var:ptn:-5, pp:25 |
| The Pacific Lifeline | Japanese Credit Guarantees (`TAI_pl_japan_credit`) | 1.3 | var:ptn:-5, pp:25 |
| The Pacific Lifeline | Indian Market Diversification (`TAI_pl_india_market`) | 1.3 | var:dep:-5, pp:25 |
| The Pacific Lifeline | Bid for the World Health Assembly (`TAI_pl_wha`) | 1.3 | pp:50, chi:tension:2 |
| The Pacific Lifeline | Strategic Partnership with New Delhi (`TAI_pl_india_partnership`) | 1.5 | var:ptn:-3, chi:tension:3, pp:25 |
| The Pacific Lifeline | Prepare to Document Coercion (`TAI_pl_document_coercion`) | 1.5 | chi:ussupport:3, var:ptn:-3, pp:25 |
| The Pacific Lifeline | Crisis Communication with Washington (`TAI_pl_us_crisis_comms`) | 1.8 | chi:ussupport:3, var:usconf:5, pp:25 |
| The Pacific Lifeline | European Industrial Supply Network (`TAI_pl_eu_supply`) | 1.8 | var:chips:5, var:ptn:-3, pp:25 |
| The Pacific Lifeline | Transparent Aid Diplomacy (`TAI_pl_transparent_aid`) | 2.0 | corr:-1, pp:50 |
| Operation Blue Tiger | Emergency Medical Surge (`TAI_bt_medical_surge`) | 0.9 | money:-1, stab:0.02, pp:25 |
| Operation Blue Tiger | Rationing Without Panic (`TAI_bt_rationing`) | 1.0 | var:ptn:-3, pp:25 |
| Operation Blue Tiger | Keep the Ports Open (`TAI_bt_ports_open`) | 1.0 | var:ptn:-3, pp:25 |
| Operation Blue Tiger | High-Value Airlift (`TAI_bt_airlift`) | 1.3 | var:chips:5, pp:25 |
| Operation Blue Tiger | Financial Continuity Plan (`TAI_bt_financial_continuity`) | 1.4 | var:ptn:-3, stab:0.02, pp:25 |
| Operation Blue Tiger | Economic Adaptation Office (`TAI_bt_adaptation_office`) | 1.5 | var:dep:-3, var:ptn:-3, pp:25 |
| Operation Blue Tiger | The Counterweapon (`TAI_bt_counterweapon`) | 1.5 | pp:50, chi:tension:3 |
| Operation Blue Tiger | Emergency Powers With Limits (`TAI_bt_emergency_limits`) | 1.6 | stab:0.03, var:ptn:-3, pp:25 |
| Operation Blue Tiger | Local Emergency Administration (`TAI_bt_local_emergency`) | 1.7 | var:coord:5, ws:0.02, pp:25 |
| Operation Blue Tiger | Emergency Procurement Networks (`TAI_bt_emergency_procurement`) | 2.0 | var:ptn:-3, corr:-1, pp:25 |
| Operation Blue Tiger | Semiconductor Continuity Pact (`TAI_bt_semiconductor_continuity`) | 2.1 | var:chips:10, pp:25 |
| Operation Blue Tiger | The Island Can Endure (`TAI_bt_island_endures`) | 2.7 | var:ptn:-10, ws:0.03, pp:25 |
| Kuomintang | We Are All New Taiwanese (`TAI_su_kmt_new_taiwanese`) | 2.6 | var:identity:4, stab:0.05, pp:50 |
| Kuomintang | The Three Links (`TAI_su_kmt_three_links`) | 2.6 | var:dep:5, chi:trust:5, money:3, pp:50 |
| Kuomintang | Keep Washington Close (`TAI_su_kmt_us_ties`) | 2.8 | var:usconf:8, chi:ussupport:3, pp:50 |
| People First Party | Reunite the Pan-Blue Camp (`TAI_su_pfp_reunite_blue`) | 2.0 | pp:100 |
| People First Party | Reassure Washington (`TAI_su_pfp_washington`) | 2.3 | var:usconf:8, pp:50 |
| People First Party | The Clean Sweep (`TAI_su_pfp_clean_sweep`) | 2.4 | corr:-1, stab:-0.02, pp:50 |
| People First Party | Welfare for Every Family (`TAI_su_pfp_welfare`) | 2.7 | money:-4, stab:0.06, party:14:0.01, pp:50 |
| People First Party | Sunshine Laws (`TAI_su_pfp_sunshine_laws`) | 2.8 | corr:-1, stab:0.04, pp:50 |
| People First Party | A Blue Legislature (`TAI_su_pfp_blue_legislature`) | 2.8 | party:1:0.01, party:14:0.01, stab:0.04, pp:50 |
| Democratic Progressive Party | A Clean Green Party (`TAI_su_dpp_clean_party`) | 2.8 | corr:-1, stab:0.04, pp:50 |
| Democratic Progressive Party | Judicial Reform (`TAI_su_dpp_judicial_reform`) | 2.8 | corr:-1, stab:0.04, pp:50 |
| Taiwan Solidarity Union | Rooted in Taiwan (`TAI_su_tsu_rooted_in_taiwan`) | 1.8 | var:chips:3, var:dep:-2, pp:50 |
| Taiwan Solidarity Union | Young Taiwan (`TAI_su_tsu_young_taiwan`) | 1.8 | party:18:0.01, var:identity:2, pp:50 |
| Taiwan Solidarity Union | WTO Safeguards (`TAI_su_tsu_wto_safeguards`) | 1.8 | money:-2, stab:0.04, pp:50 |
| Taiwan Solidarity Union | The Balance in the Legislature (`TAI_su_tsu_balance`) | 2.0 | pp:100 |
| Taiwan Solidarity Union | Mother Tongue in the Classroom (`TAI_su_tsu_mother_tongue`) | 2.1 | var:identity:3, stab:0.03, pp:50 |
| Taiwan Solidarity Union | Hold the Line on China Trade (`TAI_su_tsu_hold_the_line`) | 2.3 | var:dep:-5, chi:trust:-3, money:-2, pp:50 |
| Taiwan Solidarity Union | Farmers and Fishermen (`TAI_su_tsu_farmers`) | 2.3 | money:-3, stab:0.04, party:18:0.01, pp:50 |
| Taiwan Solidarity Union | Lee's Brain Trust (`TAI_su_tsu_brain_trust`) | 2.5 | var:reform:3, pp:100 |
| Taiwan Solidarity Union | A Southern Base (`TAI_su_tsu_southern_base`) | 2.6 | party:18:0.02, stab:0.03, pp:50 |
| Taiwan Solidarity Union | Answer the Anti-Secession Law (`TAI_su_tsu_against_anti_secession`) | 2.6 | var:identity:3, ws:0.03, chi:tension:3, pp:50 |
| Green Party Taiwan | An Ecological Tax (`TAI_su_gpt_ecological_tax`) | 1.2 | money:3, stab:-0.01, pp:50 |
| Green Party Taiwan | Ecological Tax Reform (`TAI_su_gpt_eco_reform`) | 1.5 | var:reform:3, money:2, pp:50 |
| Green Party Taiwan | Organic Farming (`TAI_su_gpt_organic_farming`) | 1.6 | stab:0.03, money:-1, pp:50 |
| Green Party Taiwan | Labor Rights (`TAI_su_gpt_labor`) | 1.8 | stab:0.04, money:-2, pp:50 |
| Green Party Taiwan | Wind and Sun (`TAI_su_gpt_wind_and_sun`) | 1.8 | var:chips:2, party:17:0.01, pp:50 |
| Green Party Taiwan | Clean Air for the South (`TAI_su_gpt_clean_air`) | 1.8 | stab:0.04, money:-2, pp:50 |
| Green Party Taiwan | Indigenous Land Rights (`TAI_su_gpt_indigenous`) | 2.0 | stab:0.04, var:identity:1, pp:50 |
| Green Party Taiwan | Seats on the City Councils (`TAI_su_gpt_council_seats`) | 2.0 | party:17:0.02, pp:50 |
| Green Party Taiwan | Save the Qigu Wetlands (`TAI_su_gpt_qigu_wetlands`) | 2.1 | stab:0.03, party:17:0.01, pp:50 |
| Green Party Taiwan | Protect the East Coast (`TAI_su_gpt_east_coast`) | 2.1 | party:17:0.01, stab:0.03, pp:50 |
| Green Party Taiwan | Cancel the Meinong Dam (`TAI_su_gpt_meinong_dam`) | 2.3 | party:17:0.01, stab:0.04, money:1, pp:50 |
| Green Party Taiwan | Environmental Impact Assessment (`TAI_su_gpt_impact_assessment`) | 2.3 | stab:0.04, var:reform:3, pp:50 |
| Green Party Taiwan | Let the People Decide on Nuclear Power (`TAI_su_gpt_nuclear_referendum`) | 2.3 | stab:0.03, var:identity:1, party:17:0.01, pp:50 |
| Green Party Taiwan | The Civil Society Alliance (`TAI_su_gpt_civil_society`) | 2.3 | stab:0.04, var:coord:3, pp:50 |
| Southern Policy | Establish Unofficial Diplomatic Relations (`TAI_establish_unoffical_diplomatic_relationships`) | 2.5 | [opinion] |
| Southern Policy | Southeast Asia Regional Defense Treaty (`TAI_south_east_nations_sign_regional_security_treaty`) | 2.5 | [diplomacy/war] |

## 4. The same subject in two places

Four subjects appear as two separate focuses with the same name in different branches. Either one should become the other's prerequisite or follow-up, or their rewards should be clearly different:

| Subject | Focuses |
| --- | --- |
| Sunshine Laws | Democratic Fortress (`TAI_df_sunshine_laws`) and PFP (`TAI_su_pfp_sunshine_laws`): both give −1 corruption and +4% stability |
| The Three Links | Across the Strait (`TAI_as_three_links`) and KMT (`TAI_su_kmt_three_links`) |
| One Country on Each Side | Across the Strait (`TAI_as_one_country_each_side`) and DPP (`TAI_su_dpp_one_country_each_side`) |
| Answer the Anti-Secession Law | Across the Strait (`TAI_as_anti_secession`) and TSU (`TAI_su_tsu_against_anti_secession`) |

There are also near-repeats in meaning: "Consult Washington" (Pacific Lifeline), "Keep Washington Close" (KMT), "Reassure Washington" (PFP) and "Secure U.S. Defense Links" (National Army) all mainly raise US confidence or US support.

## 5. Rewards that could use Millennium Dawn's own systems

These systems were all checked in the Millennium Dawn files. They are suggestions for the names-and-rewards pass with Foggy, not changes.

| System in Millennium Dawn | What it offers | Where it fits in the Taiwan tree |
| --- | --- | --- |
| **Buildings**: `offices`, `internet_station`, `agriculture_district`, `renewable_energy_infra`, `nuclear_reactor`, `microchip_plant`, `fossil_powerplant`, research facilities | Real economic output instead of political power | Silicon Island services and e-Taiwan focuses (offices, network infrastructure), WTO farmers (agriculture), the energy chain (renewables, Maanshan nuclear), Biotech and ITRI (a research facility) |
| **Chip modifiers**: plant build speed, microchip output, plant income, chip export revenue | Specialised economic identity | Already used by Silicon Island I/II/III. More Silicon focuses could add timed versions |
| **Energy system**: energy deficit, fossil fuel use, renewables | A real constraint to manage | Energy chain, the blockade focuses, and Foggy's planned nuclear-versus-green paths |
| **Treasury and money system** | Costs and income that matter | Many focuses already cost money; few earn it. Trade and services focuses could raise income or lower interest |
| **Influence** (`influence_array`) and **recognition** (`Granted_Recognition`, the UN screen) | Real diplomacy | Pacific Lifeline: influence in partner countries, recognition campaigns, keeping diplomatic allies |
| **Opinion modifiers** | Relations with specific countries | Already used by AUG's focuses (`tai_ait`, `tai_92`). Pacific Lifeline and Across the Strait could use them instead of political power |
| **Internal factions** (for example `change_fossil_fuel_industry_opinion`) | Domestic interest groups | Energy, labour, farmers and business focuses |
| **Dynamic modifiers that grow** (as in Greece's land-forces modifier) | One clean, upgradeable tooltip per branch | Party agendas (one per party), Democratic Fortress (institutional strength), Pacific Lifeline (partnership network) |
| **Decisions and categories** | Player choices outside the tree | Deferred fabs and power stations already use this; legislative negotiations (Pass VII) and recognition campaigns would too |
| **Party popularity** (`party_pop_array`) | Political consequences | Already used by the party branches; could replace generic political power in many political focuses |

## 6. Completion times

**Current in-game times.** Our generator caps every focus at 70 days, so nothing in the tree takes longer:

| In-game time | Focuses |
| --- | --- |
| 70 days | 302 |
| 35 to 56 days | 55 + 7 |
| Under 30 days (7 to 21 days, AUG's Southern Policy, Project National Glory and the communist chain) | 4 |

No focus is excessively long. The main issue is the reverse: **most focuses take the maximum 70 days whatever they give.**

**Recommendations:**
1. **Move weak 70-day focuses to 35 days.** These are the 117 focuses in section 3 that score under 3. This makes the tree play faster without adding focuses, and nothing is split.
2. **Keep 70 days for real policy steps and programmes:** spirits, buildings, research packages, events with choices.
3. **Longer than 70 days, for major programmes only.** The specification already marks 40 focuses as 105 or 140 days, but the cap reduces them to 70. If you want some major programmes to take longer, the cap can be raised for a short, approved list. Candidates:

| Branch | Focus | Intended days |
| --- | --- | --- |
| The National Army | Joint Command Reform (`TAI_na_joint_command`) | 105 |
| The National Army | Extended-Range Countermeasures (`TAI_na_hf2e_extended`) | 140 |
| The National Army | Overall Defense Concept (`TAI_na_odc`) | 105 |
| The National Army | Fortress Taiwan (`TAI_na_fortress_taiwan`) | 140 |
| The National Army | Indigenous Submarine Program (`TAI_na_indigenous_submarine`) | 140 |
| The Silicon Island | The 12-Inch Transition (`TAI_ss_twelve_inch`) | 105 |
| The Silicon Island | U.S.-Taiwan Semiconductor Compact (`TAI_ss_us_compact`) | 140 |
| The Silicon Island | The Silicon Shield (`TAI_ss_silicon_shield`) | 140 |
| The Silicon Island | Finish the High-Speed Rail (`TAI_ss_high_speed_rail`) | 105 |
| Across the Strait | A Cross-Strait Economic Framework (`TAI_as_economic_framework`) | 140 |
| Across the Strait | A Cross-Strait Peace Accord? (`TAI_as_peace_accord`) | 140 |
| The Pacific Lifeline | The Lifeline Holds (`TAI_pl_lifeline_holds`) | 140 |
| Operation Blue Tiger | Impossible to Coerce at an Acceptable Price (`TAI_bt_capstone`) | 140 |

The full list of 40 is in the spreadsheet. My suggestion is to keep the 70-day cap and allow 105 days only for capstones and genuine multi-year programmes, such as the Silicon Shield, the indigenous submarine and Fortress Taiwan.

4. **Splitting 70-day focuses into two 35-day focuses** should be rare, as you said: only where both halves are real choices. No split candidates are proposed here; that decision belongs in the rewards pass with Foggy.

## 7. Suggested order for the rewards pass

1. **Pacific Lifeline and Across the Strait** (foreign policy core): replace political power with influence, recognition, opinion and trade rewards.
2. **Democratic Fortress, then the party branches:** cut repeated corruption and stability rewards, and give each party a growing agenda modifier.
3. **Operation Blue Tiger:** turn meter-only rewards into decisions and mechanics (rationing, ports, reserves).
4. **Silicon Island** (already improved) and **the National Army** (rebalanced with the doctrine paths).
5. **Completion times** alongside each branch: weak focuses move to 35 days as their rewards are revised.

A spreadsheet with every focus (branch, ID, name, days, score, flags and rewards) accompanies this report: `focus_audit.csv`.
