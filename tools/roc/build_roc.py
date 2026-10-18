#!/usr/bin/env python3
"""Build the RoC-development (AUG) content files for the unified Taiwan tree.

Usage: python3 -B build_roc.py <out_dir>
Writes new files only; edits to existing files are made by apply_roc.py.
Source: upstream/RoC-development ceb1a0c1f5 (AUG, "Taiwan Focus import", August 2025).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import roc_spec as R  # noqa: E402

OUT = sys.argv[1]
HDR = "# Operation Blue Tiger: RoC-development content by AUG (upstream/RoC-development ceb1a0c1f5), integrated into the unified Taiwan tree\n"


def write(rel, text, bom=False):
    path = os.path.join(OUT, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = [l.rstrip() for l in text.split("\n")]
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write("\n".join(lines).rstrip("\n") + "\n")


def block(name, body, ind=1):
    t = "\t" * ind
    inner = "\n".join((t + "\t" + l) if l else "" for l in body.strip("\n").split("\n"))
    return f"{t}{name} = {{\n{inner}\n{t}}}"


# ---------------------------------------------------------------- national spirits (29)
LOCKED = "allowed_civil_war = { always = yes }\nremoval_cost = -1"
TAIONLY = "removal_cost = -1"
IDEAS = [
    ("TAI_cpc", "cpc_tw", "cost = 100\nremoval_cost = 10", "research_bonus = {\n\tCAT_fuel_refining = 0.35\n}"),
    ("TAI_idw", "escort_effort", LOCKED, "modifier = {\n\tindustrial_capacity_dockyard = 0.3\n\tresearch_speed_factor = 0.05\n}"),
    ("TAI_921_earthquake", "recovering_from_the_civil_war", LOCKED, "modifier = {\n\tconsumer_goods_factor = 0.05\n\tmobilization_speed = -0.2\n\tproduction_speed_arms_factory_factor = -0.2\n}"),
    ("TAI_highspeed_train", "tai_train", TAIONLY, "modifier = {\n\tproduction_speed_buildings_factor = 0.1\n\tarmy_speed_factor = 0.1\n}"),
    ("TAI_national_mob_law", "manpower_bonus", LOCKED, "modifier = {\n\tmobilization_speed = 0.2\n}"),
    ("TAI_afrc", "general_staff", LOCKED, "modifier = {\n\tdefence = 0.01\n\tdig_in_speed_factor = 0.05\n}"),
    ("TAI_expand_soldiers", "reserve_divisions", LOCKED, "modifier = {\n\tconscription = 0.02\n}"),
    ("TAI_post_kmt", "democracy", LOCKED, "modifier = {\n\tstability_weekly = 0.001\n\tdemocratic_drift = 0.05\n\tnationalist_drift = 0.01\n}"),
    ("TAI_martial_law", "fascism6", LOCKED, "modifier = {\n\tpolitical_power_factor = -0.05\n\tstability_weekly = -0.001\n\tnationalist_drift = 0.05\n}"),
    ("TAI_1st_special_force", "infantry_bonus2", LOCKED, "modifier = {\n\tspecial_forces_training_time_factor = 0.3\n\tspecial_forces_cap = 0.3\n}"),
    ("TAI_gastapo", "garrison_command", LOCKED, "modifier = {\n\tnationalist_drift = 0.02\n\tstability_weekly = 0.001\n}"),
    ("TAI_early_economy_control", "consumer_goods", LOCKED, "modifier = {\n\tconsumer_goods_factor = -0.05\n}"),
    ("TAI_total_economy_control", "consumer_goods", LOCKED, "modifier = {\n\tconsumer_goods_factor = -0.1\n}"),
    ("TAI_political_edu", "army_war_college", LOCKED, "modifier = {\n\tnationalist_drift = 0.03\n\tpolitical_power_factor = 0.05\n}"),
    ("TAI_government_controlled_union", "democratic_socialism", LOCKED, "modifier = {\n\tnationalist_drift = 0.01\n\tindustrial_capacity_factory = 0.01\n\tstability_weekly = 0.001\n}"),
    ("TAI_enforced_labor", "production_bonus", LOCKED, "modifier = {\n\tindustrial_capacity_factory = 0.1\n}"),
    ("TAI_aia", "spy_political", LOCKED, "modifier = {\n\tencryption_factor = 0.25\n\tforeign_influence_defense_modifier = 0.2\n}"),
    ("TAI_taiwan_indep", "TAI", LOCKED, "modifier = {\n\temerging_outlook_campaign_cost_modifier = -0.05\n\tnationalist_outlook_campaign_cost_modifier = -0.05\n\tforeign_influence_defense_modifier = 0.05\n\twestern_outlook_campaign_cost_modifier = 0.05\n\tpropaganda_campaign_cost_modifier = 0.05\n}"),
    ("TAI_purge_kmt", "purge_kmt", LOCKED, "modifier = {\n\tstability_weekly = -0.001\n\tdemocratic_drift = -0.01\n}"),
    ("TAI_red_rising", "revolutionary_army", "removal_cost = -1", "modifier = {\n\tcommunism_drift = 0.05\n}"),
    ("TAI_old_kmt_rise_up", "revolutionary_army", "removal_cost = -1", "modifier = {\n\tnationalist_drift = 0.05\n}"),
    ("TAI_labour_standards_law", "industrial_concern", LOCKED, "modifier = {\n\tline_change_production_efficiency_factor = 0.05\n\trepair_speed_factor = 0.05\n\tconsumer_goods_factor = 0.1\n\thealth_cost_multiplier_modifier = 0.05\n\tsocial_cost_multiplier_modifier = 0.05\n}"),
    ("TAI_military_public_educational_pension_reform", "blr_pensions_reform_govern", TAIONLY, "modifier = {\n\tconsumer_goods_factor = -0.1\n}"),
    ("TAI_gay_marriage", "lgbt", TAIONLY, "modifier = {\n\tconsumer_goods_factor = 0.05\n\tstability_factor = -0.05\n}"),
    ("TAI_renewable_energy", "dutch_windmill_idea", TAIONLY, "modifier = {\n\trenewable_energy_gain = 0.05\n\tfossil_fuel_consumption = -0.05\n}"),
    ("TAI_long_care_2", "neutrality", TAIONLY, "modifier = {\n\tconsumer_goods_factor = 0.02\n\tstability_factor = 0.05\n}"),
    ("TAI_sustainable_development_strategy", "progressivism", TAIONLY, "modifier = {\n\tindustrial_capacity_factory = -0.05\n\tmin_export = -0.05\n}"),
    ("TAI_affordable_housing_plan", "political_power_bonus", TAIONLY, "modifier = {\n\twar_support_factor = 0.05\n\tproduction_factory_max_efficiency_factor = 0.05\n}"),
    ("TAI_walfare_state_goal", "ARG_social_welfare_fund_ns", TAIONLY, "modifier = {\n\tsurrender_limit = 0.25\n\tdefensive_war_stability_factor = 0.1\n\tpolitical_power_factor = 0.1\n\tproduction_speed_buildings_factor = 0.1\n\tline_change_production_efficiency_factor = 0.05\n}"),
]
assert len(IDEAS) == 29


def ideas_file():
    out = [HDR, "ideas = {", "\tcountry = {"]
    for iid, pic, head, body in IDEAS:
        out.append(block(iid, f"picture = {pic}\n{head}\n\n{body}", 2))
        out.append("")
    out[-1] = "\t}"
    out.append("}")
    return "\n".join(out)


# ---------------------------------------------------------------- opinion modifiers
OPINION = HDR + """opinion_modifiers = {
	tai_92 = {
		value = 5
	}
	tai_ait = {
		value = 25
	}
	tai_resist = {
		value = -40
	}
}
"""

# ---------------------------------------------------------------- game rules
RULES = HDR + """TAI_southern_expansion = {
	name = "RULE_TAI_SOUTHERN_EXPANSION"
	group = "RULE_GROUP_GAMEPLAY"
	default = {
		name = DISABLED
		text = "RULE_OPTION_TAI_SEXP_DISABLED"
		desc = "RULE_OPTION_TAI_SEXP_DISABLED_DESC"
	}
	option = {
		name = PLAYER_ONLY
		text = "RULE_OPTION_TAI_SEXP_PLAYER_ONLY"
		desc = "RULE_OPTION_TAI_SEXP_PLAYER_ONLY_DESC"
	}
	option = {
		name = ENABLED
		text = "RULE_OPTION_TAI_SEXP_ENABLED"
		desc = "RULE_OPTION_TAI_SEXP_ENABLED_DESC"
	}
}

TAI_nato_request = {
	name = "RULE_TAI_NATO_REQUEST"
	group = "RULE_GROUP_GAMEPLAY"
	default = {
		name = DISABLED
		text = "RULE_OPTION_TAI_NATO_DISABLED"
		desc = "RULE_OPTION_TAI_NATO_DISABLED_DESC"
	}
	option = {
		name = PLAYER_ONLY
		text = "RULE_OPTION_TAI_NATO_PLAYER_ONLY"
		desc = "RULE_OPTION_TAI_NATO_PLAYER_ONLY_DESC"
	}
	option = {
		name = ENABLED
		text = "RULE_OPTION_TAI_NATO_ENABLED"
		desc = "RULE_OPTION_TAI_NATO_ENABLED_DESC"
	}
}
"""

TRIGGERS = HDR + """ROC_southern_expansion_allowed = {
	custom_trigger_tooltip = {
		tooltip = ROC_southern_expansion_allowed_tt
		OR = {
			has_game_rule = { rule = TAI_southern_expansion option = ENABLED }
			AND = {
				is_ai = no
				has_game_rule = { rule = TAI_southern_expansion option = PLAYER_ONLY }
			}
		}
	}
}

ROC_nato_request_allowed = {
	custom_trigger_tooltip = {
		tooltip = ROC_nato_request_allowed_tt
		OR = {
			has_game_rule = { rule = TAI_nato_request option = ENABLED }
			AND = {
				is_ai = no
				has_game_rule = { rule = TAI_nato_request option = PLAYER_ONLY }
			}
		}
	}
}
"""

# AUG's ROC_ai_behavior options merged into OBT's TAI_ai_behavior rule (options added by apply_roc.py).
ON_ACTIONS = HDR + """on_actions = {
	on_startup = {
		effect = {
			if = {
				limit = { country_exists = TAI }
				TAI = {
					if = {
						limit = { has_game_rule = { rule = TAI_ai_behavior option = PROJECT_NATIONAL_GLORY } }
						set_global_flag = TAI_PNG_FOCUS_PATH
					}
					if = {
						limit = { has_game_rule = { rule = TAI_ai_behavior option = UNITE_CHANNEL } }
						set_global_flag = TAI_UNITE_CHANNEL_FOCUS_PATH
					}
					if = {
						limit = { has_game_rule = { rule = TAI_ai_behavior option = ROAD_TO_SPLIT } }
						set_global_flag = TAI_ROAD_TO_SPLIT_FOCUS_PATH
					}
				}
			}
		}
	}
}
"""

CATEGORIES = HDR + """TAI_economy_decisions_category = {
	icon = GFX_decision_category_economic
	allowed = { original_tag = TAI }
	visible = { has_completed_focus = TAI_ss_root }
	priority = 590
}

TAI_png_decisions_category = {
	icon = GFX_decision_category_taiwan
	allowed = { original_tag = TAI }
	visible = { has_completed_focus = TAI_launch_our_plan }
	priority = 588
}
"""


# ---------------------------------------------------------------- decisions
def unit(state, prov, name, template, xp, eq):
    div = f'name = \\"{name}\\" division_template = \\"{template}\\" start_experience_factor = {xp} start_equipment_factor = {eq}'
    return f'create_unit = {{ division = "{div}" owner = TAI prioritize_location = {prov} }}'


def in_state(state, lines):
    grouped = []
    for l in lines:
        if grouped and grouped[-1][0] == l:
            grouped[-1][1] += 1
        else:
            grouped.append([l, 1])
    lines = [l if n == 1 else l[:-2] + f" count = {n} }}" for l, n in grouped]
    body = "\n".join("\t\t" + l for l in lines)
    return f"if = {{\n\tlimit = {{ {state} = {{ is_controlled_by = ROOT }} }}\n\t{state} = {{\n{body}\n\t}}\n}}"


def decision(did, icon, visible, available, cost, effect, ai, extra=""):
    parts = [f"icon = {icon}", ""]
    if visible:
        parts += [block("visible", visible, 0), ""]
    if available:
        parts += [block("available", available, 0), ""]
    parts += [f"cost = {cost}"]
    if extra:
        parts += extra.split("\n")
    parts += ["", block("complete_effect", f'log = "[GetDateText]: [Root.GetName]: Decision {did}"\n' + effect, 0), "", block("ai_will_do", ai, 0)]
    return block(did, "\n".join(parts), 1)


BANKRUPT = "modifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }"
ECON = [
    decision("TAI_consumer_voucher_policy", "GFX_decision_ger_mefo_bills", None, "has_stability > 0.45\nhas_war = no", 100,
             "add_stability = 0.1", "base = 1", "fire_only_once = yes"),
    decision("TAI_industrial_develop_project", "GFX_decision_ger_mefo_bills", None, "has_stability > 0.65\nhas_war = no", 75,
             "set_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nadd_offsite_building = { type = industrial_complex level = 1 }",
             "base = 1\nmodifier = { factor = 0 can_staff_an_industrial_complex = no }\n" + BANKRUPT, "days_re_enable = 180"),
    decision("TAI_construction_policy", "GFX_decision_generic_taiwan", None, "has_stability > 0.25", 20,
             "add_war_support = 0.001\nadd_stability = 0.001\nrandom_owned_controlled_state = {\n\tadd_extra_state_shared_building_slots = 4\n}", "base = 1", "days_re_enable = 360"),
    decision("TAI_weapon_self_made_program", "GFX_decision_generic_taiwan", None, "has_stability > 0.75", 75,
             "set_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nadd_offsite_building = { type = arms_factory level = 1 }",
             "base = 1\nmodifier = { factor = 0 can_staff_an_arms_industry = no }\n" + BANKRUPT, "days_re_enable = 360"),
]

THEATERS = [
    ("TAI_reserve_army_northern_district_second_level_mobilization", "TAI_mob_north_second_level", 1155, [7214, 14412]),
    ("TAI_reserve_army_central_district_second_level_mobilization", "TAI_mob_central_second_level", 1156, [14411, 11959]),
    ("TAI_reserve_army_southern_district_second_level_mobilization", "TAI_mob_south_second_level", 1157, [1091, 12027, 12068]),
]
RESERVE = []
for did, flag, state, provs in THEATERS:
    RESERVE.append(decision(
        did, "GFX_decision_armed_forces_officers", f"has_country_flag = OBT_mob_general\nNOT = {{ has_country_flag = {flag} }}",
        f"has_manpower > {3000 * len(provs)}", 25,
        f"set_country_flag = {flag}\nOBT_reserve_template = yes\ncustom_effect_tooltip = {did}_tt\n" +
        in_state(state, [unit(state, p, "", "Reserve Infantry Brigade", 0.15, 0.01).replace('name = \\"\\" ', "") for p in provs]),
        "base = 1\nmodifier = { add = 40 has_war_with = CHI }"))
MILITIA = [(430, 13275), (1109, 14608), (1158, 13274), (1015, 13326)]
RESERVE.append(decision(
    "TAI_total_mobilization_decision", "GFX_decision_armed_forces_officers", "has_country_flag = OBT_mob_general\nNOT = { has_country_flag = TAI_total_mobilized }",
    "has_country_flag = TAI_mob_north_second_level\nhas_country_flag = TAI_mob_central_second_level\n"
    "has_country_flag = TAI_mob_south_second_level\nOR = {\n\tAND = { has_war = yes has_war_support > 0.8 }\n\tAND = { has_completed_focus = TAI_mobilized_reserve_troops has_war_with = CHI }\n}", 50,
    "set_country_flag = TAI_total_mobilized\nOBT_reserve_template = yes\ncustom_effect_tooltip = TAI_total_mobilization_decision_tt\n" +
    "\n".join(in_state(s, [unit(s, p, "", "Reserve Infantry Brigade", 0.05, 0.01).replace('name = \\"\\" ', "")] * 3) for s, p in MILITIA),
    "base = 1\nmodifier = { add = 40 has_war_with = CHI }"))

SEVENTH_FLEET = decision(
    "TAI_seventh_fleet_pass_thought_strait", "GFX_decision_generic_naval",
    "has_completed_focus = TAI_pl_capitol_hill\nNOT = { has_country_flag = ROC_seventh_fleet_invited }",
    "country_exists = USA\nNOT = { has_war_with = USA }\nNOT = { AND = { country_exists = CHI has_war_with = CHI } }", 50,
    "set_country_flag = ROC_seventh_fleet_invited\nnavy_experience = 20\ncountry_event = { id = roc_dev.21 days = 3 }",
    "base = 1\nmodifier = { factor = 0 TAI_ai_historical_path = yes }", "fire_only_once = yes")

NRA = "National Revolutionary Army"


def png_template(name, regs, sup):
    return ("division_template = {\n\tname = \"" + name + "\"\n\tregiments = {\n" + "\n".join(f"\t\t{r} = {{ x = {x} y = {y} }}" for r, x, y in regs) +
            "\n\t}\n\tsupport = {\n" + "\n".join(f"\t\t{r} = {{ x = {x} y = {y} }}" for r, x, y in sup) + "\n\t}\n\tpriority = 2\n}")


PNG_TEMPLATES = "\n".join([
    png_template(f"{NRA} Special Force",
                 [("armor_Bat", 0, 0), ("armor_Bat", 0, 1), ("Mech_Inf_Bat", 1, 0), ("Mech_Inf_Bat", 2, 0), ("Mot_Inf_Bat", 1, 1), ("Mot_Inf_Bat", 1, 2), ("Mot_Inf_Bat", 2, 1), ("Mot_Inf_Bat", 2, 2)],
                 [("L_Engi_Comp", 0, 0), ("Mot_Recce_Comp", 0, 1), ("SP_AA_Battery", 0, 2), ("Arty_Battery", 0, 3), ("combat_service_support_company", 0, 4)]),
    png_template(f"{NRA} Marine Special Force",
                 [("L_Marine_Bat", 0, 0), ("L_Marine_Bat", 0, 1), ("L_Marine_Bat", 0, 2), ("L_Marine_Bat", 1, 0), ("L_Marine_Bat", 1, 1), ("L_Marine_Bat", 1, 2)],
                 [("L_Engi_Comp", 0, 0), ("L_Recce_Comp", 0, 1), ("combat_service_support_company", 0, 2)]),
    png_template(f"{NRA} Airborne Special Force",
                 [("L_Air_assault_Bat", 0, 0), ("L_Air_assault_Bat", 0, 1), ("L_Air_assault_Bat", 0, 2), ("L_Air_assault_Bat", 1, 0), ("L_Air_assault_Bat", 1, 1), ("L_Air_assault_Bat", 1, 2)],
                 [("L_Engi_Comp", 0, 0), ("L_Recce_Comp", 0, 1), ("combat_service_support_company", 0, 2)]),
])
SF, MAR, AIR = (f"{NRA} Special Force", f"{NRA} Special Force"), (f"{NRA} Marine", f"{NRA} Marine Special Force"), (f"{NRA} Airborne", f"{NRA} Airborne Special Force")
PNG_UNITS = [
    (598, [(7180, MAR), (14699, AIR), (14701, AIR), (14702, AIR)]),
    (599, [(11914, AIR), (14410, AIR), (14410, MAR)]),
    (430, [(13275, SF)] * 3),
    (600, [(4096, SF), (1175, AIR), (9955, AIR), (14698, AIR)]),
    (1109, [(14608, SF)] * 3),
    (1155, [(7214, SF), (14412, SF)]),
    (1156, [(11959, SF), (14411, SF)]),
    (1157, [(1091, SF), (12027, SF), (12068, SF)]),
    (1158, [(13274, SF)] * 3),
]
PNG_EFFECT = ("army_experience = 60\nif = {\n\tlimit = { has_country_flag = TAI_army_1sf }\n" +
              "\n".join("\t" + l for l in PNG_TEMPLATES.split("\n")) + "\n" +
              "\n".join("\t" + l for s, us in PNG_UNITS for l in in_state(s, [unit(s, p, n, t, 0.9, 1) for p, (n, t) in us]).split("\n")) +
              "\n}\nif = {\n\tlimit = { country_exists = CHI }\n\tdeclare_war_on = { target = CHI type = annex_everything }\n}\n"
              "if = {\n\tlimit = { country_exists = MON }\n\tdeclare_war_on = { target = MON type = annex_everything }\n}")
PNG_DEC = decision("TAI_png_launch", "GFX_decision_intervention_in_china", None,
                   "has_completed_focus = TAI_launch_our_plan\nTAI_reclamation_allowed = yes\nhas_war = no\nNOT = { has_country_flag = ROC_png_uprising_negotiated }", 10, PNG_EFFECT,
                   "base = 0\nmodifier = { add = 10 has_global_flag = TAI_PNG_FOCUS_PATH }", "fire_only_once = yes\nwar_with_on_complete = CHI")


def decisions_file():
    return "\n".join([
        HDR.rstrip("\n"),
        "TAI_economy_decisions_category = {", "\n\n".join(ECON), "}", "",
        "# Regional theaters and outlying-island militia from AUG's mobilization chain, merged into the OBT reserve system",
        "OBT_reserve_category = {", "\n\n".join(RESERVE), "}", "",
        "OBT_cross_strait_category = {", SEVENTH_FLEET, "}", "",
        "TAI_png_decisions_category = {", PNG_DEC, "}", ""])


# ---------------------------------------------------------------- events (namespace roc_dev, numbers kept from taiwan.18-28)
def event(n, pic, options, trigger=None):
    lines = [f"\tid = roc_dev.{n}", f"\ttitle = roc_dev.{n}.t", f"\tdesc = roc_dev.{n}.d", f"\tpicture = {pic}", "\tis_triggered_only = yes", "\tfire_only_once = yes"]
    if trigger:
        lines += ["", block("trigger", trigger, 1)]
    for key, eff, ai in options:
        ai_ind = "\n".join("\t" + l for l in ai.split("\n"))
        body = f'name = roc_dev.{n}.{key}\nlog = "[GetDateText]: [This.GetName]: roc_dev.{n}.{key} executed"\n{eff}\nai_chance = {{\n{ai_ind}\n}}'
        lines += ["", block("option", body, 1)]
    return "country_event = {\n" + "\n".join(lines) + "\n}"


def tension(v):
    return f"if = {{\n\tlimit = {{ country_exists = CHI }}\n\tCHI = {{\n\t\tadd_to_variable = {{ CHI_taiwan_strait_tension = {v} tooltip = CHI_taiwan_strait_tension_tt }}\n\t\tclamp_variable = {{ var = CHI_taiwan_strait_tension min = 0 max = 100 }}\n\t}}\n}}"


def ussupport(v):
    return f"if = {{\n\tlimit = {{ country_exists = CHI }}\n\tCHI = {{\n\t\tadd_to_variable = {{ CHI_taiwan_us_support = {v} tooltip = CHI_taiwan_us_support_tt }}\n\t\tclamp_variable = {{ var = CHI_taiwan_us_support min = 0 max = 100 }}\n\t}}\n}}"


def puppet_event(n, tags):
    yes = "\n".join(f"TAI = {{ puppet = {t} }}" if i == 0 else f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\tTAI = {{ puppet = {t} }}\n}}" for i, t in enumerate(tags))
    no = "\n".join(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\tTAI = {{ create_wargoal = {{ target = {t} type = puppet_wargoal_focus }} }}\n}}" for t in tags)
    return event(n, "GFX_TAI_roc", [("a", yes, "base = 25\nmodifier = { factor = 80 TAI = { num_divisions > 60 } }"), ("b", no, "base = 75")],
                 trigger="country_exists = TAI")


EVENTS = [
    event(18, "GFX_internal_conflict", [
        ("a", "start_civil_war = {\n\truling_party = nationalist\n\tideology = democratic\n\tsize = 0.8\n\tcapital = 598\n\tstates = { 598 599 430 1109 }\n}", "base = 50"),
        ("b", "if = { limit = { has_idea = TAI_martial_law } remove_ideas = TAI_martial_law }\nadd_stability = -0.10\nadd_political_power = -100\nset_country_flag = ROC_png_uprising_negotiated", "base = 50\nmodifier = { add = 25 has_country_flag = TAI_citizen_resist }"),
    ], trigger="original_tag = TAI"),
    event(19, "GFX_TAI_roc", [
        ("a", "if = { limit = { has_idea = TAI_legacy_of_1949 } remove_ideas = TAI_legacy_of_1949 }\nif = { limit = { NOT = { has_idea = p5_member } } add_ideas = p5_member }\n"
              "set_country_flag = TAI_roc_recover_mainland\nadd_political_power = 100\nadd_stability = 0.2", "base = 100"),
    ], trigger="original_tag = TAI\nNOT = { has_country_flag = TAI_roc_recover_mainland }"),
    event(20, "GFX_CHI_generic", [
        ("a", "custom_effect_tooltip = ROC_open_staged_talks_tt\nadd_to_variable = { TAI_pressure_to_negotiate = 25 tooltip = TAI_pressure_to_negotiate_tt }\n"
              "clamp_variable = { var = TAI_pressure_to_negotiate min = 0 max = 100 }\n"
              "if = {\n\tlimit = {\n\t\tcountry_exists = CHI\n\t\tNOT = { has_war_with = CHI }\n\t\tcheck_variable = { TAI_negotiation_stage = 0 }\n\t}\n\tcountry_event = { id = blue_tiger.40 days = 7 }\n}",
         "base = 90"),
        ("b", "add_stability = -0.05\nadd_political_power = -50", "base = 10"),
    ], trigger="original_tag = TAI"),
    event(21, "GFX_usn_seven_fleet", [("a", "add_stability = 0.05\n" + tension(8) + "\n" + ussupport(5), "base = 100")], trigger="original_tag = TAI"),
    event(22, "GFX_TAI_gay_pride", [("a", "add_ideas = TAI_gay_marriage\nadd_political_power = -25", "base = 100")], trigger="original_tag = TAI"),
    event(23, "GFX_USA_generic", [("a", "add_war_support = 0.1\nset_global_flag = usa_intervene_taiwan\n" + ussupport(5), "base = 100")], trigger="original_tag = TAI"),
    puppet_event(24, ["PHI"]),
    puppet_event(25, ["MAY", "BRU", "SIN"]),
    puppet_event(26, ["VIE", "LAO", "CBD"]),
    puppet_event(27, ["SIA"]),
    puppet_event(28, ["IND"]),
]


def events_file():
    return HDR + "add_namespace = roc_dev\n\n" + "\n\n".join(EVENTS) + "\n"


# ---------------------------------------------------------------- localisation
def L(k, v):
    return f' {k}: "{v}"'


def loc_file(focus_loc):
    A = R.AUG_LOC
    out = ["l_english:", " # Operation Blue Tiger: RoC-development content by AUG (upstream/RoC-development ceb1a0c1f5)", " # Focuses"]
    out += focus_loc
    out.append(" # National spirits")
    idea_names = {
        "TAI_highspeed_train": "Taiwan High Speed Rail", "TAI_gastapo": "Taiwan Garrison Command", "TAI_purge_kmt": "Clean Up KMT Party Assets",
        "TAI_walfare_state_goal": "Welfare State", "TAI_military_public_educational_pension_reform": "Military, Civil Service and Teacher Pension Reform",
        "TAI_labour_standards_law": "Labour Standards Act", "TAI_renewable_energy": "Leading Renewable Energy", "TAI_early_economy_control": "Early Economic Control",
        "TAI_total_economy_control": "Total Economic Control", "TAI_1st_special_force": "1st Special Forces Group", "TAI_cpc": "CPC Corporation, Taiwan",
        "TAI_taiwan_indep": "Taiwan Independence", "TAI_gay_marriage": "Marriage Equality", "TAI_red_rising": "Rising of Communism", "TAI_old_kmt_rise_up": "Rising of the Old KMT",
    }
    idea_descs = {
        "TAI_gastapo_desc": "The Taiwan Garrison Command, abolished in 1992, has been rebuilt to watch over public order and political dissent.",
        "TAI_1st_special_force_desc": "The army's elite airborne special forces are ready for the most demanding missions.",
        "TAI_old_kmt_rise_up_desc": "The old guard of the Kuomintang is returning to the centre of power.",
        "TAI_renewable_energy_desc": "Wind and solar power are becoming a growing share of the island's electricity.",
        "TAI_long_care_2_desc": "Long-term care services reach the elderly and disabled in every community.",
        "TAI_sustainable_development_strategy_desc": "Growth must now meet environmental limits, even at some cost to heavy industry and exports.",
        "TAI_affordable_housing_plan_desc": "Public housing is giving young families a stake in the island's future.",
        "TAI_walfare_state_goal_desc": "A comprehensive welfare state gives every citizen a reason to defend the island.",
        "TAI_cpc_desc": "CPC Corporation, Taiwan is the island's state-owned petroleum and petrochemical company, with refineries in Kaohsiung.",
        "TAI_purge_kmt_desc": "The government is investigating the party assets the Kuomintang accumulated during the authoritarian era.",
    }
    for iid, *_ in IDEAS:
        out.append(L(iid, idea_names.get(iid) or R._clean(A.get(iid, iid))))
        out.append(L(iid + "_desc", idea_descs.get(iid + "_desc") or R._clean(A.get(iid + "_desc", ""))))
    out.append(" # Decisions")
    dec_names = {
        "TAI_economy_decisions_category": "Economic Policy", "TAI_consumer_voucher_policy": "Consumer Vouchers", "TAI_industrial_develop_project": "Industrial Development Plan",
        "TAI_construction_policy": "Revitalize the Construction Industry", "TAI_weapon_self_made_program": "Indigenous Weapons Programme",
        "TAI_reserve_army_northern_district_second_level_mobilization": "Mobilize the Northern Theater",
        "TAI_reserve_army_central_district_second_level_mobilization": "Mobilize the Central Theater",
        "TAI_reserve_army_southern_district_second_level_mobilization": "Mobilize the Southern Theater",
        "TAI_total_mobilization_decision": "Total Mobilization of the Outlying Islands",
        "TAI_seventh_fleet_pass_thought_strait": "Invite the U.S. Seventh Fleet to Patrol the Strait",
        "TAI_png_decisions_category": "Project National Glory", "TAI_png_launch": "Launch Project National Glory",
    }
    for k, v in dec_names.items():
        out.append(L(k, v))
        d = R._clean(A.get(k + "_desc", ""))
        if k == "TAI_seventh_fleet_pass_thought_strait":
            d = "A public transit of the Taiwan Strait by the U.S. Seventh Fleet would reassure the island and anger Beijing."
        if k == "TAI_total_mobilization_decision":
            d = "Call up militia on Kinmen, Matsu, Penghu and Pratas once every theater of the island has mobilized."
        if k.startswith("TAI_reserve_army_"):
            d = "Call up additional reserve brigades in this theater during a general mobilization."
        if k == "TAI_png_launch":
            d = "The plan is ready. Every unit of Project National Glory will cross the Strait."
        out.append(L(k + "_desc", d))
    out += [
        L("TAI_reserve_army_northern_district_second_level_mobilization_tt", "Two §YReserve Infantry Brigades§! will form in §YHsinchu§!."),
        L("TAI_reserve_army_central_district_second_level_mobilization_tt", "Two §YReserve Infantry Brigades§! will form in §YTaichung§!."),
        L("TAI_reserve_army_southern_district_second_level_mobilization_tt", "Three §YReserve Infantry Brigades§! will form in §YTainan§!."),
        L("TAI_total_mobilization_decision_tt", "Three §YReserve Infantry Brigades§! will form on each of §YKinmen§!, §YMatsu§!, §YPenghu§! and §YPratas§!."),
    ]
    out.append(" # Events")
    ev = {
        "roc_dev.18.t": "The Taiwan Democratic Movement Uprising",
        "roc_dev.18.d": "Just as Project National Glory was about to be launched, the long-dormant Taiwan Democratic Rebellion Alliance rose in arms. The uprising has spread across the island and threatens to derail the plan.",
        "roc_dev.18.a": "Crush the rebellion.",
        "roc_dev.18.b": "Lift martial law and negotiate.",
        "roc_dev.19.t": "The Rise of the Republic of China",
        "roc_dev.19.d": "After more than half a century, the government that withdrew to the island has restored its authority over China and reclaimed its former place in the world.",
        "roc_dev.19.a": "Unified China under the Three Principles of the People.",
        "roc_dev.20.t": "Taiwan and the Mainland",
        "roc_dev.20.d": "The revolutionary government in Taipei has declared that the island belongs to one China and asks Beijing to open talks on its return. Under the constitution, any settlement must still be approved by the people of Taiwan.",
        "roc_dev.20.a": "Open talks with Beijing.",
        "roc_dev.20.b": "The island is not ready.",
        "roc_dev.21.t": "U.S. Seventh Fleet Transits the Taiwan Strait",
        "roc_dev.21.d": "Ships of the U.S. Seventh Fleet, based at Yokosuka in Japan, have sailed through the Taiwan Strait in a public show of support. Beijing has condemned the transit.",
        "roc_dev.21.a": "Our thanks to a great friend.",
        "roc_dev.22.t": "Constitutional Court Rules for Same-Sex Marriage",
        "roc_dev.22.d": "The Council of Grand Justices has ruled that the Civil Code's failure to allow same-sex marriage is unconstitutional and has given the Legislative Yuan two years to change the law.",
        "roc_dev.22.a": "The first in Asia to recognize same-sex marriage.",
        "roc_dev.23.t": "Washington Restates Its Taiwan Strait Policy",
        "roc_dev.23.d": "The U.S. government has again set out its Taiwan Strait policy: it opposes any unilateral change to the status quo that would undermine decades of peace, stability and development in the region.",
        "roc_dev.23.a": "Good to hear.",
    }
    for n, c in ((24, "the Philippines"), (25, "Malaysia"), (26, "Vietnam"), (27, "Thailand"), (28, "Indonesia")):
        ev[f"roc_dev.{n}.t"] = f"Taiwan Demands That {c[0].upper() + c[1:]} Submit"
        ev[f"roc_dev.{n}.d"] = f"Taiwan has issued an ultimatum to {c}: become a subordinate of the national government, or face war."
        ev[f"roc_dev.{n}.a"] = "There seems to be no other way."
        ev[f"roc_dev.{n}.b"] = "Impossible!"
    out += [L(k, v) for k, v in ev.items()]
    out.append(" # Game rules")
    out += [
        L("RULE_OPTION_TAI_PROJECT_NATIONAL_GLORY", "Project National Glory"),
        L("RULE_OPTION_TAI_PROJECT_NATIONAL_GLORY_DESC", "The AI Republic of China follows Project National Glory if the Return to the Mainland rule allows the AI to take that path."),
        L("RULE_OPTION_TAI_UNITE_CHANNEL", "Unification Channel"),
        L("RULE_OPTION_TAI_UNITE_CHANNEL_DESC", "The AI Republic of China follows the Red Infiltration path, which ends in staged talks and a referendum."),
        L("RULE_OPTION_TAI_ROAD_TO_SPLIT", "Road to Separation"),
        L("RULE_OPTION_TAI_ROAD_TO_SPLIT_DESC", "The AI Republic of China takes the alternate-history independence capstones."),
        L("RULE_TAI_SOUTHERN_EXPANSION", "Taiwan: Southern Expansion"),
        L("RULE_OPTION_TAI_SEXP_DISABLED", "Disabled"),
        L("RULE_OPTION_TAI_SEXP_DISABLED_DESC", "The alternate-history conquest of Southeast Asia is hidden from Taiwan's focus tree."),
        L("RULE_OPTION_TAI_SEXP_PLAYER_ONLY", "Player Only"),
        L("RULE_OPTION_TAI_SEXP_PLAYER_ONLY_DESC", "Only a human-controlled Taiwan can take the Southern Expansion path."),
        L("RULE_OPTION_TAI_SEXP_ENABLED", "Allowed"),
        L("RULE_OPTION_TAI_SEXP_ENABLED_DESC", "Any Taiwan can take the Southern Expansion path. The AI does so only with the Project National Glory AI behaviour."),
        L("RULE_TAI_NATO_REQUEST", "Taiwan: NATO Request"),
        L("RULE_OPTION_TAI_NATO_DISABLED", "Disabled"),
        L("RULE_OPTION_TAI_NATO_DISABLED_DESC", "Taiwan cannot request NATO membership."),
        L("RULE_OPTION_TAI_NATO_PLAYER_ONLY", "Player Only"),
        L("RULE_OPTION_TAI_NATO_PLAYER_ONLY_DESC", "Only a human-controlled Taiwan can request NATO membership."),
        L("RULE_OPTION_TAI_NATO_ENABLED", "Allowed"),
        L("RULE_OPTION_TAI_NATO_ENABLED_DESC", "Any Taiwan can request NATO membership."),
    ]
    out.append(" # Tooltips, flags, opinion modifiers and parties")
    tips = {
        "ROC_southern_expansion_allowed_tt": "The §YSouthern Expansion§! game rule allows this.",
        "ROC_nato_request_allowed_tt": "The §YNATO Request§! game rule allows this.",
        "ROC_us_support_above_59_tt": "U.S. support for Taiwan is above §Y59§!.",
        "ROC_us_support_above_79_tt": "U.S. support for Taiwan is above §Y79§!.",
        "ROC_identity_above_69_tt": "Taiwan-Centered Identity is above §Y69§!.",
        "ROC_reserve_readiness_15_tt": "§YReserve Readiness§! increases by §G15§!.",
        "ROC_reserve_readiness_20_tt": "§YReserve Readiness§! increases by §G20§!.",
        "ROC_png_mobilization_tt": "Reserve mobilization no longer requires a crisis in the Strait.",
        "ROC_open_staged_talks_tt": "Opens §YTalks with Beijing§!. Any settlement still requires a referendum.",
        "TAI_png_tt": R._clean(A["TAI_png_tt"]),
        "TAI_communist_upring_tt": "§YThe Communists will start a civil war.§!",
        "TAI_back_to_chi_tt": "§YThe division across the Strait may finally come to an end.§!",
        "TAI_second_constitution_tt": "§YThe Constitution of the Second Republic limits the state's territory to the areas it governs.§!",
        "TAI_taiwan_republic_tt": "§YThe people of Taiwan will take control of their own destiny.§!",
        "TAI_war_with_mainland_tt": "§CThis could lead to war with China!§!",
        "TAI_communism_increase_10_tt": A["TAI_communism_increase_10_tt"],
        "TAI_communism_increase_40_tt": A["TAI_communism_increase_40_tt"],
        "TAI_afrc_units_were_all_set": "Reserve units established",
        "TAI_mob_north_second_level": "Northern theater mobilized",
        "TAI_mob_central_second_level": "Central theater mobilized",
        "TAI_mob_south_second_level": "Southern theater mobilized",
        "TAI_total_mobilized": "Outlying islands mobilized",
        "TAI_public_fear": "The public fears the Garrison Command",
        "TAI_labor_resist": "Labour resists",
        "TAI_public_resist": "The public resists",
        "TAI_student_resist": "Students resist",
        "TAI_army_resist": "Parts of the army resist",
        "TAI_army_1sf": "1st Special Forces Group ready",
        "TAI_citizen_resist": "Citizens resist martial law",
        "TAI_roc_recover_mainland": "The Republic of China recovered the mainland",
        "ROC_seventh_fleet_invited": "The Seventh Fleet was invited",
        "ROC_png_uprising_negotiated": "Martial law lifted after the uprising",
        "tai_92": "1992 Consensus",
        "tai_ait": "American Institute in Taiwan",
        "tai_resist": "Resisting annexation by the mainland",
        "TAI_industry_bonus": "Focus on Internal Development",
        "TAI_liberalism_party_tdra": "TDRA",
        "TAI_liberalism_party_tdra_long": "Taiwan Democratic Rebellion Alliance",
    }
    out += [L(k, v) for k, v in tips.items()]
    return "\n".join(out) + "\n"


def main():
    write("common/ideas/99_TAI_roc_dev_ideas.txt", ideas_file())
    write("common/opinion_modifiers/99_TAI_roc_dev_opinion_modifiers.txt", OPINION)
    write("common/game_rules/99_ROC_dev_game_rules.txt", RULES)
    write("common/scripted_triggers/99_ROC_dev_scripted_triggers.txt", TRIGGERS)
    write("common/on_actions/99_ROC_dev_on_actions.txt", ON_ACTIONS)
    write("common/decisions/categories/99_ROC_dev_categories.txt", CATEGORIES)
    write("common/decisions/ROC_dev_decisions.txt", decisions_file())
    write("events/ROC_dev_events.txt", events_file())
    focus_loc_path = sys.argv[2] if len(sys.argv) > 2 else None
    focus_loc = []
    if focus_loc_path:
        ids = set(R.roc_focus_ids())
        for line in open(focus_loc_path, encoding="utf-8"):
            key = line.split(":")[0].strip()
            if key in ids or (key.endswith("_desc") and key[:-5] in ids):
                focus_loc.append(line.rstrip("\n"))
    write("localisation/english/MD_ROC_dev_l_english.yml", loc_file(focus_loc), bom=True)
    print("built", OUT)


if __name__ == "__main__":
    main()
