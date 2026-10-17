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
  "GFX_TAI_roc_flag",
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
  "GFX_HKG_SARS",
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
   ("open", "NOT = { has_completed_focus = TAI_df_special_funds_audit has_completed_focus = TAI_su_dpp_clean_party }", "Prosecutors are examining how the president's discretionary State Affairs Fund was spent, and allegations now reach members of the first family. The case is unproven, but it is consuming the government's credibility day by day.")],
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
  "GFX_TAI_roc_flag",
  [O("Nominate a cross-party premier", ["var:milconf:5", "stab:0.02"], ai=60),
   O("Nominate a party loyalist", ["var:reform:5", "pp:50"], ai=40)])

E(22, "The Fourth Nuclear Plant Crisis",
  "The Lungmen nuclear plant is budgeted and partly built. Halting it would honour years of environmental campaigning and trigger a constitutional confrontation with the legislature; completing it would secure electricity for a growing economy.",
  "GFX_SIN_singapore_builds_first_nuclear_reactor",
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
  "GFX_NKO_Submarine_1",
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
