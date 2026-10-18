# Operation Blue Tiger milestone 2: historical and focus-driven events.
# Each event: id number, title, desc (or list of (key_suffix, trigger, text)), picture,
# options: list of dicts {key, text, trigger(optional), eff(list of tokens), ai(base), aimod(list of raw lines)}
# Effect tokens reuse gen.py tokens plus: fire:N:DAYS, rawfx:<script>

NS = "blue_tiger"
EVENTS = []


def E(n, title, desc, picture, options, trigger="original_tag = TAI", sched=None):
    EVENTS.append({"n": n, "title": title, "desc": desc, "picture": picture,
                   "options": options, "trigger": trigger, "sched": sched})


def O(text, eff, ai=10, trigger=None, aimod=()):
    return {"text": text, "eff": eff, "ai": ai, "trigger": trigger, "aimod": list(aimod)}


GREEN = "TAI_pan_green_in_power = yes"
BLUE = "TAI_pan_blue_in_power = yes"
BANKRUPT = "modifier = { factor = 0.25 has_active_mission = bankruptcy_incoming_collapse }"
DEFICIT = "modifier = { factor = 0.5 ai_has_high_deficit = yes }"
LOWSTAB = "modifier = { factor = 0.2 has_stability < 0.35 }"

# ------------------------------------------------------------------ scheduled
E(1, "The Inauguration",
  [("green", GREEN, "On 20 May 2000, power passes from the Kuomintang to the Democratic Progressive Party for the first time. The new president takes the oath before a crowd that once could not have imagined it, while Beijing and Washington listen closely to every word of the inaugural address."),
   ("blue", BLUE, "On 20 May 2000, the Republic of China inaugurates its second directly elected president. The handover keeps the government in Pan-Blue hands, but the campaign showed how much the electorate has changed since 1996.")],
  "GFX_TAI_roc",
  [O("Pledge the Four Noes", ["chi:tension:-5", "var:usconf:5", "chi:trust:3", "flag:TAI_2000_camp_green", "fire:2:3"], ai=80, trigger=GREEN),
   O("Stand on our mandate", ["var:identity:5", "chi:tension:5", "var:usconf:-5", "flag:TAI_2000_camp_green", "fire:2:3"], ai=20, trigger=GREEN),
   O("Promise continuity and reconciliation", ["stab:0.03", "chi:trust:3", "flag:TAI_2000_camp_blue"], ai=100, trigger=BLUE)],
  sched=(2000, 140))

E(2, "The 2000 Transfer of Power",
  "For half a century the officer corps served a state run by the Kuomintang. Now its commander-in-chief comes from the party many senior officers were trained to distrust. How the new government handles its first appointments will shape civil-military relations for years.",
  "GFX_Military_Reform",
  [O("Reassure the commanders", ["var:milconf:10", "var:reform:-5"], ai=50),
   O("Appoint reform-minded officers", ["var:milconf:-8", "var:reform:8"], ai=25),
   O("Insist on constitutional practice", ["stab:0.02", "var:milconf:-3", "var:reform:3"], ai=25)],
  trigger="original_tag = TAI\n\t\tTAI_pan_green_in_power = yes")

E(3, "The Dot-Com Bust",
  "The collapse of global technology demand has hit our export economy hard. Factory orders are falling, unemployment is climbing above anything seen in decades, and the economy is heading for its first annual contraction since the island's industrialisation.",
  "GFX_economy_crisis",
  [O("Fund a stimulus package", ["money:-3", "rawfx:if = { limit = { has_completed_focus = TAI_su_2001_recession } add_timed_idea = { idea = TAI_dotcom_bust days = 120 } } else = { add_timed_idea = { idea = TAI_dotcom_bust days = 240 } }"], ai=10, aimod=[BANKRUPT, DEFICIT]),
   O("Let the market correct itself", ["stab:-0.02", "rawfx:if = { limit = { has_completed_focus = TAI_su_2001_recession } add_timed_idea = { idea = TAI_dotcom_bust days = 180 } } else = { add_timed_idea = { idea = TAI_dotcom_bust days = 365 } }"], ai=5, aimod=[LOWSTAB])],
  sched=(2001, 59))

E(4, "The 2001 Legislative Election",
  "Voters have redrawn the Legislative Yuan. The Kuomintang has lost its position as the largest party, James Soong's People First Party has won dozens of seats, and Lee Teng-hui's new Taiwan Solidarity Union has entered the chamber on the Pan-Green side.",
  "GFX_election_day",
  [O("The new legislature takes its seats", ["party:1:-0.05", "party:14:0.04", "party:2:0.01"], ai=100)],
  sched=(2001, 334))

E(5, "SARS Reaches Taiwan",
  "A new respiratory illness that began in Guangdong has reached our hospitals. Cases are rising, a Taipei hospital has been sealed with staff and patients inside, and we still have no direct line to the World Health Organization.",
  "GFX_hospital",
  [O("Impose strict quarantine", ["money:-1", "timed:TAI_sars_outbreak:90"], ai=15, aimod=[BANKRUPT]),
   O("Keep the economy open", ["stab:-0.03", "timed:TAI_sars_outbreak:180"], ai=5, aimod=[LOWSTAB])],
  sched=(2003, 110))

E(6, "Shots on Election Eve",
  "On the final day of the campaign, the president and vice president have been wounded by gunshots while campaigning in Tainan. Both are recovering, but with the vote tomorrow, rumour and suspicion are spreading faster than the investigators can work.",
  "GFX_election_rally",
  [O("Call for calm and let investigators work", ["stab:-0.02", "raw:TAI_campaign_for_ruling_camp = yes", "fire:7:2"], ai=100)],
  trigger="original_tag = TAI\n\t\tTAI_pan_green_in_power = yes",
  sched=(2004, 78))

E(7, "A Margin of Thousands",
  "The incumbent has won by fewer than thirty thousand votes out of thirteen million. The opposition demands a recount and has filed suit, and protesters fill the streets outside the Presidential Office.",
  "GFX_election_protests",
  [O("Accept a full recount and court review", ["stab:-0.03", "timed:TAI_disputed_result:365"], ai=70, aimod=[LOWSTAB]),
   O("Declare the result final", ["stab:-0.06", "timed:TAI_disputed_result:545", "var:usconf:-3"], ai=30, aimod=[LOWSTAB])])

E(8, "The Anti-Secession Law",
  "The National People's Congress has passed a law authorising \"non-peaceful means\" if Taiwan moves toward independence, if a major incident leads to separation, or if the possibility of peaceful unification is exhausted. Beijing alone will decide when those conditions are met.",
  "GFX_CHI_event_national_congress_started",
  [O("Rally in the streets", ["chi:tension:10", "var:identity:5", "ws:0.03"], ai=40),
   O("Work quietly with Washington", ["chi:tension:10", "var:usconf:5"], ai=40),
   O("Appeal to the world", ["chi:tension:13", "chi:ussupport:4"], ai=20)],
  sched=(2005, 72))

E(9, "The Journey of Peace",
  "The Kuomintang chairman has travelled to Beijing and met the General Secretary of the Communist Party, the first meeting of the two parties' leaders since the civil war. The opposition is now conducting its own cross-Strait diplomacy.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Condemn the visit", ["var:identity:3", "chi:trust:-3"], ai=40),
   O("Welcome any step toward dialogue", ["chi:trust:5", "party:1:0.01"], ai=30),
   O("Let the voters judge", ["stab:0.01"], ai=30)],
  trigger="original_tag = TAI\n\t\tTAI_pan_green_in_power = yes",
  sched=(2005, 115))

E(10, "The State Affairs Fund",
  [("audited", "OR = { has_completed_focus = TAI_df_special_funds_audit has_completed_focus = TAI_su_dpp_clean_party }", "Prosecutors are examining how the president's discretionary State Affairs Fund was spent. Because the fund was audited and our party's finances were opened earlier, the inquiry is narrow, but the opposition is eager to make the most of it."),
   ("open", "NOT = { OR = { has_completed_focus = TAI_df_special_funds_audit has_completed_focus = TAI_su_dpp_clean_party } }", "Prosecutors are examining how the president's discretionary State Affairs Fund was spent, and allegations now reach members of the first family. The case is unproven, but it is consuming the government's credibility day by day.")],
  "GFX_FRA_political_scandal",
  [O("Cooperate with the prosecutors", ["rawfx:if = { limit = { OR = { has_completed_focus = TAI_df_special_funds_audit has_completed_focus = TAI_su_dpp_clean_party } } add_stability = -0.02 } else = { add_stability = -0.05 }", "rawfx:hidden_effect = { if = { limit = { has_stability < 0.45 } country_event = { id = blue_tiger.11 days = 70 } } }"], ai=70, aimod=[LOWSTAB]),
   O("Resist the investigation", ["stab:-0.02", "rawfx:hidden_effect = { country_event = { id = blue_tiger.11 days = 70 } }"], ai=30)],
  trigger="original_tag = TAI\n\t\tTAI_pan_green_in_power = yes",
  sched=(2006, 180))

E(11, "The Red Shirts",
  "Hundreds of thousands of protesters in red have surrounded the Presidential Office, demanding the president's resignation over the corruption allegations. A recall motion is moving through the Legislative Yuan.",
  "GFX_election_protests",
  [O("Respect the right to protest", ["stab:-0.04", "raw:TAI_campaign_for_ruling_camp = yes"], ai=60, aimod=[LOWSTAB]),
   O("Call counter-rallies in the south", ["stab:-0.02", "var:identity:2", "party:1:0.01"], ai=40)])

E(12, "The 2008 Legislative Election",
  [("sntv", "has_completed_focus = TAI_df_end_sntv", "The first election under single-member districts has reshaped the Legislative Yuan. The new system rewards the largest party in each district, and the results are lopsided."),
   ("old", "NOT = { has_completed_focus = TAI_df_end_sntv }", "Voters have returned a new Legislative Yuan after a campaign dominated by the economy and fatigue with the governing party.")],
  "GFX_election_day",
  [O("The opposition sweeps the districts", ["party:1:0.05", "party:2:-0.04"], ai=100, trigger=GREEN),
   O("Our majority is renewed", ["party:1:0.02", "stab:0.02"], ai=100, trigger=BLUE)],
  sched=(2008, 11))

E(13, "Democracy's Second Test",
  "The newly elected president is inaugurated on 20 May 2008. Whatever the outcome, eight years after the first transfer of power, alternation in office has become part of ordinary politics on the island.",
  "GFX_TAI_taiwan",
  [O("A second peaceful turnover", ["stab:0.05", "pp:50"], ai=100,
     trigger="OR = { AND = { has_country_flag = TAI_2000_camp_green TAI_pan_blue_in_power = yes } AND = { has_country_flag = TAI_2000_camp_blue TAI_pan_green_in_power = yes } }"),
   O("The mandate continues", ["stab:0.02", "pp:25"], ai=100,
     trigger="NOT = { OR = { AND = { has_country_flag = TAI_2000_camp_green TAI_pan_blue_in_power = yes } AND = { has_country_flag = TAI_2000_camp_blue TAI_pan_green_in_power = yes } } }")],
  sched=(2008, 141))

# ------------------------------------------------------------------ focus-driven
E(20, "Reconciliation Talks",
  "Emissaries from Lien Chan and James Soong are meeting quietly to discuss a joint campaign. Soong's supporters left the party bitterly, and neither man wants to be the one who steps aside.",
  "GFX_TAI_roc",
  [O("Await the outcome", ["rawfx:random_list = { 35 = { add_to_variable = { party_pop_array^1 = 0.06 } add_to_variable = { party_pop_array^14 = -0.06 } recalculate_party = yes custom_effect_tooltip = TAI_reconciliation_success_tt } 65 = { add_to_variable = { party_pop_array^14 = 0.02 } recalculate_party = yes custom_effect_tooltip = TAI_reconciliation_failure_tt } }"], ai=100)])

E(21, "Choosing a Premier",
  "The president must nominate a premier who can work with the Legislative Yuan. A respected figure from across the aisle would calm the opposition and the officer corps; a trusted party colleague would push the government's programme harder.",
  "GFX_politics_talks",
  [O("Nominate a cross-party premier", ["var:milconf:5", "stab:0.02"], ai=60),
   O("Nominate a party loyalist", ["var:reform:5", "pp:50"], ai=40)])

E(22, "The Fourth Nuclear Plant Crisis",
  "The Lungmen nuclear plant is budgeted and partly built. Halting it would honour years of environmental campaigning and trigger a constitutional confrontation with the legislature; completing it would secure electricity for a growing economy.",
  "GFX_nuclear_power_plant",
  [O("Halt construction", ["stab:-0.05", "money:2"], ai=20, trigger=GREEN, aimod=[LOWSTAB]),
   O("Finish the plant", ["stab:-0.01", "raw:add_tech_bonus = { name = blue_tiger.22.b bonus = 0.5 uses = 1 category = CAT_nuclear_reactors }"], ai=50),
   O("Refer the dispute to the Grand Justices", ["stab:0.02", "pp:-25"], ai=30, aimod=[BANKRUPT])])

E(23, "Special Defense Budget Showdown",
  "The arms package needs a special budget, and the Legislative Yuan will decide how much of it survives. Supporters call it the minimum for deterrence; critics call it a payment to Washington for weapons we cannot crew.",
  "GFX_CAN_increase_military_spending",
  [O("Pass the budget in full", ["money:-5", "var:usconf:5", "chi:ussupport:3"], ai=40, trigger="TAI_can_pass_legislation = yes", aimod=[BANKRUPT, DEFICIT]),
   O("Accept a trimmed budget", ["money:-2", "var:usconf:2"], ai=40, aimod=[BANKRUPT]),
   O("Let the budget stall", ["var:usconf:-5", "var:milconf:-3"], ai=20)])

E(24, "The HF-2E Controversy",
  "Our engineers have a land-attack cruise missile ready for production. Beijing calls it proof of offensive intent, Washington has asked us privately to reconsider, and the opposition questions its cost.",
  "GFX_CHI_event_missiles_taiwan",
  [O("Fund full production", ["chi:tension:6", "var:usconf:-5", "var:milconf:5"], ai=40),
   O("Cap the range and numbers", ["chi:tension:2", "var:usconf:2"], ai=40),
   O("Shelve the program", ["var:usconf:5", "var:milconf:-5"], ai=20)])

E(25, "Reserve Readiness Audit",
  "The audit is in. Millions of reservists exist on paper, but few have trained since their conscription, and many units lack modern equipment. The question is what to do with the findings.",
  "GFX_Army_reforms_event",
  [O("Fund refresher training", ["money:-2", "army_xp:15"], ai=40, aimod=[BANKRUPT, DEFICIT]),
   O("Prioritise the active forces", ["army_xp:10", "var:milconf:3"], ai=40),
   O("Publish the findings", ["var:reform:5", "stab:-0.01"], ai=20, aimod=[LOWSTAB])])

E(26, "The Submarine Question",
  "Washington approved diesel submarines in 2001, but no American yard builds them and European builders fear Beijing. We can wait for a solution or begin learning to build our own.",
  "GFX_submarine",
  [O("Wait for an American solution", ["var:usconf:3"], ai=50),
   O("Plan an indigenous program", ["raw:add_tech_bonus = { name = blue_tiger.26.b bonus = 0.5 uses = 1 category = CAT_submarines }", "var:reform:3"], ai=50)])

E(27, "Washington Warns Taipei",
  "The U.S. government has publicly stated that it opposes unilateral changes to the status quo. American officials want our assurance that the latest step will go no further.",
  "GFX_USA_event_congress",
  [O("Give Washington its assurance", ["var:usconf:8", "var:identity:-2", "stab:-0.02"], ai=60, aimod=[LOWSTAB]),
   O("Proceed regardless", ["var:identity:3", "var:usconf:-8", "chi:ussupport:-3"], ai=40)])

E(28, "Deep-Green Discontent",
  "Independence activists in our own camp accuse the government of abandoning its principles to please Washington. They are threatening to sit out the next election.",
  "GFX_TAI_228_hand",
  [O("Offer symbolic gestures", ["var:identity:2", "var:usconf:-3"], ai=50),
   O("Hold the line", ["stab:-0.02", "party:2:-0.01"], ai=50, aimod=[LOWSTAB])])

IDEAS_BLOCK = '''
		# Operation Blue Tiger milestone 2: event spirits
		TAI_dotcom_bust = {
			picture = financial_crisis
			allowed_civil_war = { always = yes }
			modifier = {
				tax_gain_multiplier_modifier = -0.05
				production_factory_efficiency_gain_factor = -0.05
			}
		}

		TAI_sars_outbreak = {
			picture = political_drain
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = -0.03
				tax_gain_multiplier_modifier = -0.03
			}
		}

		TAI_disputed_result = {
			picture = disjointed_government
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = -0.05
				political_power_factor = -0.05
			}
		}
'''

IDEAS_LOC = [
    ("TAI_dotcom_bust", "Dot-Com Bust"),
    ("TAI_dotcom_bust_desc", "Falling global demand for electronics has pushed our export economy into recession.\\n§W--------------§!\\nThis national spirit is shorter if we complete the §Y$TAI_su_2001_recession$§! focus first."),
    ("TAI_sars_outbreak", "SARS Outbreak"),
    ("TAI_sars_outbreak_desc", "A new respiratory epidemic is straining our hospitals and keeping shoppers and tourists at home."),
    ("TAI_disputed_result", "Disputed Election Result"),
    ("TAI_disputed_result_desc", "Many citizens doubt the narrow result of the last presidential election.\\n§W--------------§!\\nThis national spirit will be §RRemoved§! if we complete the §Y$TAI_su_heal_divided_island$§! focus."),
    ("TAI_reconciliation_success_tt", "§G35%§!: Lien and Soong agree on a joint campaign. The §YKuomintang§! gains popularity at the expense of the §YPeople First Party§!."),
    ("TAI_reconciliation_failure_tt", "§R65%§!: The talks collapse. The §YPeople First Party§! gains popularity."),
]

# Focus changes that wire focuses to the new events (applied to spec.py by apply2).
FOCUS_EDITS = {
    "TAI_su_heal_kmt_split": ["raw:country_event = { id = blue_tiger.20 days = 1 }"],
    "TAI_su_form_cabinet": ["raw:country_event = { id = blue_tiger.21 days = 1 }", "pp:25"],
    "TAI_su_fourth_nuclear": ["raw:country_event = { id = blue_tiger.22 days = 1 }"],
    "TAI_na_special_budget": ["raw:country_event = { id = blue_tiger.23 days = 1 }"],
    "TAI_na_hf2e": ["tech:CAT_cruise_missiles:0.75:2", "raw:country_event = { id = blue_tiger.24 days = 1 }"],
    "TAI_na_reserve_audit": ["raw:country_event = { id = blue_tiger.25 days = 1 }"],
    "TAI_na_submarine_question": ["tech:CAT_submarines:0.5:1", "raw:country_event = { id = blue_tiger.26 days = 1 }"],
    "TAI_su_dpp_name_rectification": ["var:identity:10", "chi:tension:10", "var:usconf:-5", "raw:country_event = { id = blue_tiger.27 days = 3 }"],
    "TAI_su_dpp_un_bid": ["var:identity:10", "var:usconf:-5", "chi:tension:10", "raw:country_event = { id = blue_tiger.27 days = 3 }"],
    "TAI_su_dpp_status_quo": ["var:usconf:10", "chi:tension:-5", "raw:country_event = { id = blue_tiger.28 days = 30 }"],
    "TAI_su_heal_divided_island": ["stab:0.05", "var:ptn:-3", "rmidea:TAI_disputed_result"],
}

# ------------------------------------------------------------------ milestone 3: negotiation, war, support
STAGE0 = "check_variable = { TAI_negotiation_stage = 0 }"
NOWAR = "NOT = { has_war_with = CHI }"
PTN_HI = "modifier = { add = 30 check_variable = { TAI_pressure_to_negotiate > 69 } }"
ID_HI = "modifier = { factor = 0.3 check_variable = { TAI_taiwanese_identity > 59 } }"
SET_STAGE = "set_variable = {{ TAI_negotiation_stage = {} }}"
REFUSE_CD = "set_country_flag = { flag = TAI_refused_terms days = 365 value = 1 }"
TELL_CHI_REJECT = "hidden_effect = { CHI = { country_event = { id = blue_tiger.46 days = 2 } } }"

E(40, "Talks with Beijing",
  "Beijing has set out terms for ending the crisis: an end to the blockade in exchange for economic arrangements now and political talks later. Entering talks commits us only to the first stage, and we can leave at any point.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Open economic talks", ["rawfx:" + SET_STAGE.format(1), "var:ptn:-10", "chi:trust:5", "rawfx:custom_effect_tooltip = TAI_talks_stage_one_tt\nhidden_effect = {\n\tCHI = { country_event = { id = blue_tiger.47 days = 2 } }\n\tcountry_event = { id = blue_tiger.41 days = 60 }\n}"], ai=10, aimod=[PTN_HI, ID_HI, "modifier = { factor = 0.3 CHI = { check_variable = { CHI_taiwan_us_support > 49 } } }", "modifier = { factor = 0.5 TAI_ai_historical_path = yes }", "modifier = { factor = 3 has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH }", "modifier = { factor = 0 has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH }"]),
   O("Refuse. The island endures", ["ws:0.05", "var:identity:3", "chi:tension:5", "rawfx:" + REFUSE_CD + "\n" + TELL_CHI_REJECT], ai=20,
     aimod=["modifier = { factor = 0.25 check_variable = { TAI_pressure_to_negotiate > 84 } }"])],
  trigger="original_tag = TAI\n\t\tcountry_exists = CHI\n\t\t" + NOWAR + "\n\t\t" + STAGE0)

E(41, "Economic Talks",
  "Negotiators have agreed on trade, investment and shipping arrangements that would end the blockade. Beijing now proposes a political conference on the island's future.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Proceed to a political conference", ["rawfx:" + SET_STAGE.format(2), "chi:trust:5", "rawfx:custom_effect_tooltip = TAI_talks_stage_two_tt\nhidden_effect = { country_event = { id = blue_tiger.42 days = 90 } }"], ai=5, aimod=[PTN_HI, ID_HI, "modifier = { factor = 0.3 CHI = { check_variable = { CHI_taiwan_us_support > 49 } } }", "modifier = { factor = 0.5 TAI_ai_historical_path = yes }", "modifier = { factor = 3 has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH }", "modifier = { factor = 0 has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH }"]),
   O("Keep the talks to trade", ["var:ptn:-5", "rawfx:hidden_effect = { country_event = { id = blue_tiger.41 days = 120 } }"], ai=10),
   O("Withdraw from the talks", ["rawfx:" + SET_STAGE.format(0) + "\n" + REFUSE_CD, "var:identity:3", "rawfx:" + TELL_CHI_REJECT], ai=5,
     aimod=["modifier = { add = 20 check_variable = { TAI_pressure_to_negotiate < 40 } }"])],
  trigger="original_tag = TAI\n\t\tcountry_exists = CHI\n\t\t" + NOWAR + "\n\t\tcheck_variable = { TAI_negotiation_stage = 1 }")

E(42, "The Political Conference",
  "Delegations are drafting a framework for the island's political future. Under our constitution and the principle of assent, no agreement can take effect unless the people of Taiwan approve it.",
  "GFX_politics_negotiations",
  [O("Put the agreement to a referendum", ["rawfx:" + SET_STAGE.format(3), "rawfx:custom_effect_tooltip = TAI_referendum_called_tt\nhidden_effect = { country_event = { id = blue_tiger.43 days = 30 } }"], ai=5,
     aimod=["modifier = { add = 30 check_variable = { TAI_pressure_to_negotiate > 79 } }", ID_HI, "modifier = { factor = 0.3 CHI = { check_variable = { CHI_taiwan_us_support > 49 } } }", "modifier = { factor = 0.5 TAI_ai_historical_path = yes }", "modifier = { factor = 3 has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH }", "modifier = { factor = 0 has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH }"]),
   O("Withdraw from the conference", ["rawfx:" + SET_STAGE.format(0) + "\n" + REFUSE_CD, "var:usconf:5", "rawfx:" + TELL_CHI_REJECT], ai=10)],
  trigger="original_tag = TAI\n\t\tcountry_exists = CHI\n\t\t" + NOWAR + "\n\t\tcheck_variable = { TAI_negotiation_stage = 2 }")

E(43, "The Settlement Referendum",
  "Voters will decide whether to accept the agreement negotiated with Beijing. The result will turn on how badly the crisis has hurt and how strongly citizens identify with the island.",
  "GFX_election_day",
  [O("Count the votes", ["rawfx:random_list = {\n\t20 = {\n\t\tmodifier = { factor = 2 check_variable = { TAI_pressure_to_negotiate > 69 } }\n\t\tmodifier = { factor = 2 check_variable = { TAI_pressure_to_negotiate > 84 } }\n\t\tmodifier = { factor = 0.5 check_variable = { TAI_taiwanese_identity > 49 } }\n\t\tmodifier = { factor = 0.5 check_variable = { TAI_taiwanese_identity > 69 } }\n\t\tcustom_effect_tooltip = TAI_referendum_approved_tt\n\t\thidden_effect = {\n\t\t\tset_variable = { TAI_negotiation_stage = 0 }\n\t\t\tCHI = { country_event = { id = china_sar.022 days = 7 } }\n\t\t}\n\t}\n\t80 = {\n\t\tcustom_effect_tooltip = TAI_referendum_rejected_tt\n\t\thidden_effect = { country_event = { id = blue_tiger.44 days = 1 } }\n\t}\n}"], ai=100)],
  trigger="original_tag = TAI\n\t\tcountry_exists = CHI\n\t\tcheck_variable = { TAI_negotiation_stage = 3 }")

E(44, "The Island Refuses",
  "The agreement has been rejected at the ballot box. The government has a clear mandate to keep the island's future in its own hands, and the result is being read closely in Washington and Tokyo.",
  "GFX_TAI_228_hand",
  [O("The people have spoken", ["rawfx:" + SET_STAGE.format(0) + "\nset_country_flag = { flag = TAI_refused_terms days = 730 value = 1 }", "var:identity:5", "ws:0.05", "chi:ussupport:10", "chi:tension:10", "rawfx:" + TELL_CHI_REJECT], ai=100)])

E(46, "Taipei Rejects Our Terms",
  "Taiwan has refused or abandoned the talks we offered. We can tighten the pressure again, or accept the status quo for now and wait for a better moment.",
  "GFX_CHI_event_navy_ship",
  [O("Tighten the pressure", ["chi:tension:5", "chi:trust:-5"], ai=50,
     aimod=["modifier = { factor = 0.3 check_variable = { CHI_taiwan_us_support > 69 } }"]),
   O("Accept the status quo for now", ["chi:tension:-5"], ai=50,
     aimod=["modifier = { add = 30 check_variable = { CHI_taiwan_us_support > 59 } }"])],
  trigger="original_tag = CHI\n\t\tcountry_exists = TAI")

E(47, "Taipei Opens Talks",
  "Taiwan's negotiators have accepted our invitation to economic talks. Easing the blockade would show good faith; keeping it in place would keep up the pressure on the political stage that follows.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Ease the blockade", ["rawfx:if = {\n\tlimit = { has_country_flag = CHI_TAI_full_blockade_active }\n\tclr_country_flag = CHI_TAI_full_blockade_active\n\tset_country_flag = CHI_TAI_partial_blockade_active\n\tTAI = {\n\t\tif = { limit = { has_idea = TAI_blockade_economic_crisis } remove_ideas = TAI_blockade_economic_crisis }\n\t\tif = { limit = { NOT = { has_idea = TAI_blockade_partial } } add_ideas = TAI_blockade_partial }\n\t}\n}", "chi:tension:-10", "chi:trust:3"], ai=70),
   O("Keep up the pressure", ["chi:trust:-5"], ai=30)],
  trigger="original_tag = CHI\n\t\tcountry_exists = TAI")

E(50, "War in the Strait",
  "The People's Liberation Army has opened hostilities against Taiwan. Missiles are striking airbases and ports, and the fleet is massing across the Strait. Everything prepared in peacetime will now be tested.",
  "GFX_CHI_event_missiles_taiwan",
  [O("Execute the Blue Tiger Emergency Doctrine", ["ws:0.15", "stab:0.05"], ai=100, trigger="has_idea = TAI_emergency_doctrine"),
   O("Mobilise the nation", ["ws:0.10", "stab:-0.03"], ai=100, trigger="NOT = { has_idea = TAI_emergency_doctrine }")],
  trigger="original_tag = TAI")

E(51, "War in the Taiwan Strait",
  "China has attacked Taiwan. The Taiwan Relations Act lets us provide defensive arms but does not oblige us to fight. Whether we intervene depends on how far we are committed to deterring Beijing and how much we trust Taipei.",
  "GFX_USA_event_congress",
  [O("Defend Taiwan", ["rawfx:add_to_war = {\n\ttargeted_alliance = TAI\n\tenemy = CHI\n}"], ai=0,
     aimod=["modifier = { add = 40 CHI = { check_variable = { CHI_taiwan_us_support > 69 } } }",
            "modifier = { add = 30 TAI = { check_variable = { TAI_us_confidence > 59 } } }",
            "modifier = { factor = 0 CHI = { check_variable = { CHI_taiwan_us_support < 40 } } }"]),
   O("Send arms and impose sanctions", ["rawfx:TAI = { add_timed_idea = { idea = TAI_american_assistance days = 365 } }", "rawfx:add_opinion_modifier = { target = CHI modifier = recent_actions_negative }"], ai=40),
   O("Stay out of the war", ["chi:ussupport:-10"], ai=20,
     aimod=["modifier = { add = 40 CHI = { check_variable = { CHI_taiwan_us_support < 40 } } }"])],
  trigger="original_tag = USA\n\t\tcountry_exists = TAI\n\t\tcountry_exists = CHI\n\t\tNOT = { has_war_with = TAI }\n\t\tNOT = { has_war_with = CHI }")

E(52, "Taipei Seeks Mediation",
  "Taiwan has asked third countries to broker a ceasefire. Our forces have not taken the island, and every week of war costs us at home and abroad.",
  "GFX_negotiations",
  [O("Accept a ceasefire", ["stab:-0.03", "rawfx:white_peace = TAI"], ai=10,
     aimod=["modifier = { add = 40 TAI = { controls_state = 598 } }", "modifier = { add = 30 has_war_with = USA }", "modifier = { factor = 0 controls_state = 598 }"]),
   O("Fight on", ["rawfx:hidden_effect = { TAI = { country_event = { id = blue_tiger.55 days = 1 } } }", "ws:-0.02"], ai=30)],
  trigger="original_tag = CHI\n\t\thas_war_with = TAI")

E(53, "Taipei Requests Support",
  "Taiwan is under heavy pressure from Beijing and has asked for our help. A visible response would reassure Taipei and raise tensions with China; a quiet one would do less of both.",
  "GFX_USA_event_congress",
  [O("Send a carrier group and supplies", ["chi:tension:5", "chi:ussupport:5", "rawfx:TAI = {\n\tadd_timed_idea = { idea = TAI_american_assistance days = 180 }\n\tadd_to_variable = { TAI_pressure_to_negotiate = -10 tooltip = TAI_pressure_to_negotiate_tt }\n\tclamp_variable = { var = TAI_pressure_to_negotiate min = 0 max = 100 }\n}"], ai=10,
     aimod=["modifier = { add = 30 CHI = { check_variable = { CHI_taiwan_us_support > 69 } } }", "modifier = { add = 20 TAI = { check_variable = { TAI_us_confidence > 59 } } }", "modifier = { factor = 0.2 TAI = { check_variable = { TAI_us_confidence < 30 } } }"]),
   O("Offer quiet diplomatic backing", ["chi:ussupport:2", "rawfx:TAI = {\n\tadd_to_variable = { TAI_pressure_to_negotiate = -3 tooltip = TAI_pressure_to_negotiate_tt }\n\tclamp_variable = { var = TAI_pressure_to_negotiate min = 0 max = 100 }\n}"], ai=30),
   O("Decline the request", ["chi:ussupport:-3"], ai=10,
     aimod=["modifier = { add = 30 TAI = { check_variable = { TAI_us_confidence < 30 } } }"])],
  trigger="original_tag = USA\n\t\tcountry_exists = TAI\n\t\tNOT = { has_war_with = TAI }")

E(55, "Beijing Rejects Mediation",
  "Beijing has turned down the ceasefire proposal. The war goes on, but the offer has strengthened our case abroad.",
  "GFX_UN_gen_assembly",
  [O("We will hold", ["ws:0.03", "chi:ussupport:3"], ai=100)])

IDEAS_BLOCK_M3 = '''
		# Operation Blue Tiger milestone 3: crisis spirits
		TAI_american_assistance = {
			picture = international_treaty2
			allowed_civil_war = { always = yes }
			modifier = {
				army_defence_factor = 0.05
				air_superiority_efficiency = 0.05
				stability_factor = 0.03
			}
		}
'''

IDEAS_LOC_M3 = [
    ("TAI_american_assistance", "American Assistance"),
    ("TAI_american_assistance_desc", "Arms, intelligence and supplies from the United States are reaching our forces. It is help, not an alliance."),
    ("TAI_talks_stage_one_tt", "Economic talks begin. In §Y60§! days we decide whether to move to a political conference, keep talking about trade, or withdraw."),
    ("TAI_talks_stage_two_tt", "A political conference opens. In §Y90§! days we decide whether to hold a referendum or withdraw."),
    ("TAI_referendum_called_tt", "A referendum on the agreement is held in §Y30§! days. Approval becomes likelier as §YPressure to Negotiate§! rises and less likely as §YTaiwan-Centered Identity§! rises."),
    ("TAI_referendum_approved_tt", "If voters §Rapprove§!: Taiwan accepts unification with the mainland."),
    ("TAI_referendum_rejected_tt", "If voters §Greject§!: the talks end and the government gains a mandate to resist."),
]

# ------------------------------------------------------------------ party branches
E(60, "Elect the Chairman",
  "For the first time, Kuomintang members choose their chairman directly. One candidate is a popular reformist mayor who appeals to young and urban voters; the other is a veteran legislator with deep roots in the party's local networks.",
  "GFX_election_day",
  [O("Back the reformist mayor", ["party:1:0.02", "stab:0.02"], ai=60),
   O("Back the veteran legislator", ["var:identity:2", "party:1:0.01", "pp:50"], ai=40)])

E(61, "A Forum with the Communist Party",
  "Beijing has accepted a regular forum between the Kuomintang and the Communist Party. It wants politics on the agenda; many of our own members want to keep it to trade and tourism.",
  "GFX_politics_talks",
  [O("Open the forum to every subject", ["chi:trust:8", "var:dep:3", "var:usconf:-3"], ai=40),
   O("Keep it to trade and tourism", ["chi:trust:3", "var:usconf:2"], ai=60)])

E(62, "Can the Targets Be Met?",
  "Economists doubt that six percent growth is realistic in a slowing world economy. The opposition is already quoting our promise back at us.",
  "GFX_election_rally",
  [O("Hold to the targets", ["stab:0.02", "money:-3"], ai=50, aimod=[DEFICIT, BANKRUPT]),
   O("Quietly soften them", ["pp:25", "stab:-0.01"], ai=50)])

E(63, "Active Opening, Effective Management",
  "The Economic Advisory Conference recommends replacing the policy of \"no haste, be patient\" on mainland investment with \"active opening, effective management\". Our coalition partners and the deep-green wing object.",
  "GFX_negotiations",
  [O("Adopt the new policy", ["var:dep:5", "money:3", "chi:trust:3"], ai=60),
   O("Keep the brakes on", ["var:dep:-3", "party:18:0.01", "stab:0.01"], ai=40)])

E(64, "One Country on Each Side",
  "The president's remark has made headlines across Asia. Beijing calls it a provocation, Washington asks what it means, and supporters at home cheer.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Stand by the statement", ["var:identity:3", "chi:tension:8", "var:usconf:-5"], ai=40),
   O("Clarify that nothing has changed", ["var:usconf:3", "var:identity:-1", "stab:0.01"], ai=60)])

E(65, "The Defensive Referendum",
  "Two questions will appear on the ballot: whether to buy more missile defenses if Beijing does not withdraw its missiles, and whether to open talks on a framework for peace. Washington has made clear it is uneasy.",
  "GFX_election_day",
  [O("Hold it alongside the election", ["var:identity:3", "var:usconf:-5", "chi:tension:5"], ai=50),
   O("Withdraw it under American pressure", ["var:usconf:5", "party:2:-0.01"], ai=50)])

E(66, "The Soong Machine",
  "Crowds turn out wherever James Soong goes. Party organizers warn that a party built around one man will not outlive him.",
  "GFX_election_rally",
  [O("Let Soong campaign everywhere", ["party:14:0.02", "pp:-25"], ai=50),
   O("Build institutions, not a personality", ["var:reform:3", "party:14:0.01"], ai=50)])

E(67, "Who Leads the Ticket?",
  "The Pan-Blue parties have agreed on one ticket for the presidency. They have not agreed whose name goes first.",
  "GFX_election_rally",
  [O("Our leader heads the ticket", ["party:14:0.02", "party:1:-0.01"], ai=50),
   O("Take second place for the sake of unity", ["party:1:0.02", "stab:0.02"], ai=50)])

E(68, "Soong in Beijing",
  "James Soong's talks with the Chinese leadership have produced a draft statement on peace in the Strait. Signing it would make headlines; refusing would disappoint our hosts.",
  "GFX_politics_talks",
  [O("Sign the joint statement", ["chi:trust:8", "chi:tension:-5", "var:usconf:-3"], ai=50),
   O("Return without commitments", ["chi:trust:2", "var:usconf:2"], ai=50)])

E(69, "Lee Teng-hui's New Party",
  "Supporters of former president Lee Teng-hui have founded the Taiwan Solidarity Union, and the Kuomintang has expelled its former chairman. The new party offers its votes to the government.",
  "GFX_TAI_taiwan",
  [O("Welcome it into the Pan-Green camp", ["party:18:0.02", "party:1:-0.02", "chi:tension:3"], ai=60),
   O("Keep it at arm's length", ["var:usconf:2", "party:18:0.01"], ai=40)])

E(70, "March to Rectify the Name",
  "Tens of thousands have marched through Taipei demanding that the country be called Taiwan. The organizers ask the government to join them.",
  "GFX_election_protests",
  [O("Join the march", ["var:identity:3", "chi:tension:4", "var:usconf:-3"], ai=40),
   O("Send a message of support", ["var:identity:1", "stab:0.01"], ai=60)])

E(71, "Hand in Hand for Taiwan",
  "Some two million people have joined hands in a human chain running the length of the island, on the anniversary of the 1947 massacre.",
  "GFX_TAI_228_hand",
  [O("The island stands together", ["var:identity:4", "stab:0.02", "chi:tension:3"], ai=50),
   O("Turn it into a campaign rally", ["party:2:0.02", "party:18:0.01"], ai=50)])

E(72, "A Nuclear-Free Homeland",
  "The bill commits Taiwan to becoming nuclear-free. The Greens want a firm timetable; the chipmakers warn about power supply.",
  "GFX_nuclear_power_plant",
  [O("Set a firm timetable", ["party:17:0.02", "var:chips:-2", "stab:0.01"], ai=40),
   O("Make it a long-term goal", ["party:17:0.01"], ai=60)])

E(73, "A Green Minister",
  "Green Party Taiwan's leaders are divided over whether to enter the cabinet. Joining would bring influence and the burden of the government's compromises.",
  "GFX_politics_negotiations",
  [O("Offer the environment ministry", ["party:17:0.02", "stab:0.02", "var:reform:3"], ai=50),
   O("Offer an advisory council instead", ["pp:25", "party:17:-0.01"], ai=50)])

IDEAS_BLOCK_M6 = '''
		# Operation Blue Tiger: branch and party programs
		TAI_su_program_1 = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.05
				stability_factor = 0.02
			}
		}
		TAI_su_program_2 = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.1
				stability_factor = 0.04
			}
		}
		TAI_su_program_3 = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.15
				stability_factor = 0.06
			}
		}
		TAI_df_program_1 = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.03
				political_power_factor = 0.03
			}
		}
		TAI_df_program_2 = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.05
				political_power_factor = 0.05
			}
		}
		TAI_df_program_3 = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.08
				political_power_factor = 0.08
			}
		}
		TAI_na_program_1 = {
			picture = army_war_college
			allowed_civil_war = { always = yes }
			modifier = {
				army_org_factor = 0.03
				training_time_army_factor = -0.03
			}
		}
		TAI_na_program_2 = {
			picture = army_war_college
			allowed_civil_war = { always = yes }
			modifier = {
				army_org_factor = 0.05
				training_time_army_factor = -0.05
				army_defence_factor = 0.03
			}
		}
		TAI_na_program_3 = {
			picture = army_war_college
			allowed_civil_war = { always = yes }
			modifier = {
				army_org_factor = 0.08
				training_time_army_factor = -0.08
				army_defence_factor = 0.05
			}
		}
		TAI_ss_program_1 = {
			picture = research_bonus
			allowed_civil_war = { always = yes }
			modifier = {
				production_factory_efficiency_gain_factor = 0.03
				research_speed_factor = 0.02
			}
		}
		TAI_ss_program_2 = {
			picture = research_bonus
			allowed_civil_war = { always = yes }
			modifier = {
				production_factory_efficiency_gain_factor = 0.05
				research_speed_factor = 0.03
			}
		}
		TAI_ss_program_3 = {
			picture = research_bonus
			allowed_civil_war = { always = yes }
			modifier = {
				production_factory_efficiency_gain_factor = 0.08
				research_speed_factor = 0.05
			}
		}
		TAI_as_program_1 = {
			picture = trade
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.02
				trade_opinion_factor = 0.05
			}
		}
		TAI_as_program_2 = {
			picture = trade
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.03
				trade_opinion_factor = 0.1
			}
		}
		TAI_as_program_3 = {
			picture = trade
			allowed_civil_war = { always = yes }
			modifier = {
				stability_factor = 0.05
				trade_opinion_factor = 0.15
			}
		}
		TAI_pl_program_1 = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.03
				trade_opinion_factor = 0.05
			}
		}
		TAI_pl_program_2 = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.05
				trade_opinion_factor = 0.1
			}
		}
		TAI_pl_program_3 = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.08
				trade_opinion_factor = 0.15
			}
		}
		TAI_bt_program_1 = {
			picture = national_mobilization
			allowed_civil_war = { always = yes }
			modifier = {
				war_support_factor = 0.03
				army_defence_factor = 0.03
			}
		}
		TAI_bt_program_2 = {
			picture = national_mobilization
			allowed_civil_war = { always = yes }
			modifier = {
				war_support_factor = 0.05
				army_defence_factor = 0.05
				stability_factor = 0.02
			}
		}
		TAI_bt_program_3 = {
			picture = national_mobilization
			allowed_civil_war = { always = yes }
			modifier = {
				war_support_factor = 0.08
				army_defence_factor = 0.08
				stability_factor = 0.03
			}
		}
		TAI_kmt_program_1 = {
			picture = political_support
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.1
				stability_factor = 0.03
				production_speed_buildings_factor = 0.03
			}
		}
		TAI_kmt_program_2 = {
			picture = political_support
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.15
				stability_factor = 0.06
				production_speed_buildings_factor = 0.06
			}
		}
		TAI_kmt_roc_on_taiwan = {
			picture = political_support
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.25
				stability_factor = 0.1
				production_speed_buildings_factor = 0.08
				trade_opinion_factor = 0.15
			}
		}
		TAI_dpp_program_1 = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.1
				stability_factor = 0.03
				research_speed_factor = 0.02
			}
		}
		TAI_dpp_program_2 = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.15
				stability_factor = 0.06
				research_speed_factor = 0.04
			}
		}
		TAI_dpp_own_path = {
			picture = democracy
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.25
				stability_factor = 0.1
				research_speed_factor = 0.05
				war_support_factor = 0.05
			}
		}
		TAI_pfp_program_1 = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.12
				stability_factor = 0.04
			}
		}
		TAI_pfp_program_2 = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.2
				stability_factor = 0.07
			}
		}
		TAI_pfp_third_force = {
			picture = political_reform
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.3
				stability_factor = 0.1
				political_power_factor = 0.1
			}
		}
		TAI_tsu_program_1 = {
			picture = national_unity
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.05
				stability_factor = 0.02
			}
		}
		TAI_tsu_program_2 = {
			picture = national_unity
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.08
				stability_factor = 0.04
				war_support_factor = 0.03
			}
		}
		TAI_tsu_taiwan_consensus = {
			picture = national_unity
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.1
				stability_factor = 0.06
				war_support_factor = 0.08
			}
		}
		TAI_gpt_program_1 = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.05
				stability_factor = 0.02
			}
		}
		TAI_gpt_program_2 = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.08
				stability_factor = 0.04
				research_speed_factor = 0.02
			}
		}
		TAI_gpt_green_conscience = {
			picture = international_treaty
			allowed_civil_war = { always = yes }
			modifier = {
				political_power_gain = 0.1
				stability_factor = 0.06
				research_speed_factor = 0.03
			}
		}
'''

IDEAS_LOC_M6 = [
    ("TAI_su_program_1", "The Peaceful Transition"),
    ("TAI_su_program_1_desc", "Power has changed hands by the ballot, and the institutions are adjusting to it."),
    ("TAI_su_program_2", "Constitutional Government"),
    ("TAI_su_program_2_desc", "Power has changed hands by the ballot, and the institutions are adjusting to it."),
    ("TAI_su_program_3", "A Mature Democracy"),
    ("TAI_su_program_3_desc", "Power has changed hands by the ballot, and the institutions are adjusting to it."),
    ("TAI_df_program_1", "Democratic Consolidation"),
    ("TAI_df_program_1_desc", "Courts, prosecutors, the civil service and the media are becoming independent of any party."),
    ("TAI_df_program_2", "The Rule of Law"),
    ("TAI_df_program_2_desc", "Courts, prosecutors, the civil service and the media are becoming independent of any party."),
    ("TAI_df_program_3", "A Democratic Fortress"),
    ("TAI_df_program_3_desc", "Courts, prosecutors, the civil service and the media are becoming independent of any party."),
    ("TAI_na_program_1", "Defense Reform"),
    ("TAI_na_program_1_desc", "A national army under civilian control, trained and commanded for the defense of the island."),
    ("TAI_na_program_2", "A Professional Military"),
    ("TAI_na_program_2_desc", "A national army under civilian control, trained and commanded for the defense of the island."),
    ("TAI_na_program_3", "Joint Forces"),
    ("TAI_na_program_3_desc", "A national army under civilian control, trained and commanded for the defense of the island."),
    ("TAI_ss_program_1", "The Silicon Island"),
    ("TAI_ss_program_1_desc", "Fabs, science parks and research institutes are the engine of the island's prosperity."),
    ("TAI_ss_program_2", "The 12-Inch Economy"),
    ("TAI_ss_program_2_desc", "Fabs, science parks and research institutes are the engine of the island's prosperity."),
    ("TAI_ss_program_3", "The Silicon Shield Economy"),
    ("TAI_ss_program_3_desc", "Fabs, science parks and research institutes are the engine of the island's prosperity."),
    ("TAI_as_program_1", "Cross-Strait Management"),
    ("TAI_as_program_1_desc", "Trade, tourism and quiet channels across the Strait are managed rather than left to chance."),
    ("TAI_as_program_2", "A Channel Across the Strait"),
    ("TAI_as_program_2_desc", "Trade, tourism and quiet channels across the Strait are managed rather than left to chance."),
    ("TAI_as_program_3", "The Status Quo Dividend"),
    ("TAI_as_program_3_desc", "Trade, tourism and quiet channels across the Strait are managed rather than left to chance."),
    ("TAI_pl_program_1", "Pacific Partnerships"),
    ("TAI_pl_program_1_desc", "Washington, Tokyo, Europe and new partners know where Taipei stands and what it needs."),
    ("TAI_pl_program_2", "No Surprises"),
    ("TAI_pl_program_2_desc", "Washington, Tokyo, Europe and new partners know where Taipei stands and what it needs."),
    ("TAI_pl_program_3", "Seats at the Table"),
    ("TAI_pl_program_3_desc", "Washington, Tokyo, Europe and new partners know where Taipei stands and what it needs."),
    ("TAI_bt_program_1", "National Resilience"),
    ("TAI_bt_program_1_desc", "The whole of government, and the whole of society, is preparing to endure."),
    ("TAI_bt_program_2", "A Coordinated Nation"),
    ("TAI_bt_program_2_desc", "The whole of government, and the whole of society, is preparing to endure."),
    ("TAI_bt_program_3", "Continuity of Government"),
    ("TAI_bt_program_3_desc", "The whole of government, and the whole of society, is preparing to endure."),
    ("TAI_kmt_program_1", "A Renewed Kuomintang"),
    ("TAI_kmt_program_1_desc", "The party of government has new faces, a local base and a program voters can measure."),
    ("TAI_kmt_program_2", "The Kuomintang Restored"),
    ("TAI_kmt_program_2_desc", "The Kuomintang governs with confidence again, and its technocrats are building."),
    ("TAI_dpp_program_1", "The Green Administration"),
    ("TAI_dpp_program_1_desc", "The first opposition party ever to govern is learning the machinery of the state."),
    ("TAI_dpp_program_2", "Reform in Government"),
    ("TAI_dpp_program_2_desc", "The administration has found its footing and its own agenda."),
    ("TAI_pfp_program_1", "People First"),
    ("TAI_pfp_program_1_desc", "James Soong's network reaches every township, and the new government means to use it."),
    ("TAI_pfp_program_2", "The People First Program"),
    ("TAI_pfp_program_2_desc", "The party's discipline in the legislature turns promises into law."),
    ("TAI_tsu_program_1", "Solidarity Union Partnership"),
    ("TAI_tsu_program_1_desc", "Lee Teng-hui's party votes with the government in the Legislative Yuan."),
    ("TAI_tsu_program_2", "Solidarity in Government"),
    ("TAI_tsu_program_2_desc", "Our partner's voters and Lee Teng-hui's prestige stand behind the government."),
    ("TAI_gpt_program_1", "Green Partnership"),
    ("TAI_gpt_program_1_desc", "Green Party Taiwan lends the government the credibility of the environmental movement."),
    ("TAI_gpt_program_2", "The Green Alliance"),
    ("TAI_gpt_program_2_desc", "Environmental, labor and indigenous groups work with the government rather than against it."),
    ("TAI_kmt_roc_on_taiwan", "The Republic of China on Taiwan"),
    ("TAI_kmt_roc_on_taiwan_desc", "The Republic founded in 1912 governs Taiwan by consent and keeps the door to the mainland open on its own terms."),
    ("TAI_dpp_own_path", "Taiwan's Own Path"),
    ("TAI_dpp_own_path_desc", "A democracy that chose its own government and decides its own future."),
    ("TAI_pfp_third_force", "The Third Force"),
    ("TAI_pfp_third_force_desc", "A party born of a split now governs, and its discipline in the legislature has become the government's strength."),
    ("TAI_tsu_taiwan_consensus", "The Taiwan Consensus"),
    ("TAI_tsu_taiwan_consensus_desc", "A majority of the island agrees that its future belongs to its own people."),
    ("TAI_gpt_green_conscience", "The Green Conscience"),
    ("TAI_gpt_green_conscience_desc", "Environmental and social movements have become partners in government."),
]
