#!/usr/bin/env python3
"""OBT milestone 10: Reserve Mobilization (peacetime preparation, partial and general mobilization, demobilization).

Usage: python3 mob10.py <out_dir>
"""
import os
import sys

OUT = sys.argv[1]
LOC = []


def L(k, v):
    assert "—" not in v
    LOC.append(f' {k}: "{v}"')


def w(rel, text, bom=False):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)


TEMPLATE = "Reserve Infantry Brigade"
SPAWN_PROVS = [7186, 11959, 14410, 12068, 14699, 14411, 7214, 4096]
SPAWN_STATES = [598, 1156, 599, 1157, 598, 1156, 1155, 600]
PARTIAL_MAX, GENERAL_MAX = 4, 12

effects = f'''# Operation Blue Tiger milestone 10: reserve mobilization

OBT_reserve_init = {{
	if = {{
		limit = {{ NOT = {{ has_country_flag = OBT_reserve_initialized }} }}
		set_country_flag = OBT_reserve_initialized
		set_variable = {{ OBT_reserve_readiness = 15 }}
		set_variable = {{ OBT_mob_spawned = 0 }}
	}}
}}

OBT_reserve_monthly = {{
	OBT_reserve_init = yes
	if = {{
		limit = {{ has_country_flag = OBT_reserve_program }}
		add_to_variable = {{ OBT_reserve_readiness = 2 }}
	}}
	else_if = {{
		limit = {{ check_variable = {{ OBT_reserve_readiness > 10 }} }}
		subtract_from_variable = {{ OBT_reserve_readiness = 1 }}
	}}
	clamp_variable = {{ var = OBT_reserve_readiness min = 0 max = 100 }}
}}

OBT_reserve_template = {{
	if = {{
		limit = {{ NOT = {{ has_country_flag = OBT_reserve_template_made }} }}
		set_country_flag = OBT_reserve_template_made
		division_template = {{
			name = "{TEMPLATE}"
			division_names_group = TAI_RES
			is_locked = yes
			regiments = {{
				Militia_Bat = {{ x = 0 y = 0 }}
				Militia_Bat = {{ x = 0 y = 1 }}
				Militia_Bat = {{ x = 0 y = 2 }}
			}}
			support = {{
				H_Engi_Comp = {{ x = 0 y = 0 }}
			}}
		}}
	}}
}}

# Spawns one reserve brigade if the cap for the current stage allows it. Experience follows Reserve Readiness.
OBT_reserve_spawn_one = {{
	OBT_reserve_template = yes
	set_temp_variable = {{ OBT_mob_cap = {PARTIAL_MAX} }}
	if = {{ limit = {{ has_country_flag = OBT_mob_general }} set_temp_variable = {{ OBT_mob_cap = {GENERAL_MAX} }} }}
	if = {{
		limit = {{
			OR = {{ has_country_flag = OBT_mob_partial has_country_flag = OBT_mob_general }}
			check_variable = {{ OBT_mob_spawned < OBT_mob_cap }}
		}}
		set_temp_variable = {{ OBT_mob_slot = OBT_mob_spawned }}
		modulo_temp_variable = {{ OBT_mob_slot = {len(SPAWN_PROVS)} }}
'''
TIERS = (("check_variable = { OBT_reserve_readiness > 69 }", 0.25), ("check_variable = { OBT_reserve_readiness > 39 }", 0.18), (None, 0.1))
for i, prov in enumerate(SPAWN_PROVS):
    kw = "if" if i == 0 else "else_if"
    effects += f"\t\t{kw} = {{\n\t\t\tlimit = {{ check_variable = {{ OBT_mob_slot = {i} }} }}\n"
    for tier, (cond, xp) in enumerate(TIERS):
        tk = "if" if tier == 0 else ("else_if" if cond else "else")
        lim = f"limit = {{ {cond} }} " if cond else ""
        cu = (f'create_unit = {{ division = "division_template = \\"{TEMPLATE}\\" start_experience_factor = {xp} start_equipment_factor = 0.01" '
              f"owner = TAI prioritize_location = {prov} }}")
        st = SPAWN_STATES[i]
        effects += (f"\t\t\t{tk} = {{\n\t\t\t\t{lim}\n\t\t\t\tif = {{ limit = {{ {st} = {{ is_controlled_by = TAI }} }} {st} = {{ {cu} }} }}\n"
                    f"\t\t\t\telse = {{ capital_scope = {{ {cu} }} }}\n\t\t\t}}\n")
    effects += "\t\t}\n"
effects += '''		add_to_variable = { OBT_mob_spawned = 1 }
	}
}

OBT_reserve_spawn_two = {
	OBT_reserve_spawn_one = yes
	OBT_reserve_spawn_one = yes
}

OBT_reserve_demobilize = {
	delete_unit = { division_template = "Reserve Infantry Brigade" disband = yes }
	clr_country_flag = OBT_mob_partial
	clr_country_flag = OBT_mob_general
	set_variable = { OBT_mob_spawned = 0 }
	if = { limit = { has_dynamic_modifier = { modifier = OBT_partial_mobilization } } remove_dynamic_modifier = { modifier = OBT_partial_mobilization } }
	if = { limit = { has_dynamic_modifier = { modifier = OBT_general_mobilization } } remove_dynamic_modifier = { modifier = OBT_general_mobilization } }
	set_country_flag = { flag = OBT_mob_cooldown days = 365 value = 1 }
}
'''

triggers = '''# Operation Blue Tiger milestone 10: reserve mobilization

OBT_mob_crisis_condition = {
	custom_trigger_tooltip = {
		tooltip = OBT_mob_crisis_condition_tt
		OR = {
			OBT_strait_at_least_crisis = yes
			AND = { country_exists = CHI has_war_with = CHI }
			check_variable = { TAI_blockade_burden > 0 }
		}
	}
}

OBT_mob_war_condition = {
	custom_trigger_tooltip = {
		tooltip = OBT_mob_war_condition_tt
		OR = {
			AND = { country_exists = CHI has_war_with = CHI }
			AND = { country_exists = CHI CHI = { check_variable = { CHI_taiwan_strait_tension > 79 } } }
		}
	}
}

OBT_reserve_readiness_at_least_20 = {
	custom_trigger_tooltip = {
		tooltip = OBT_reserve_readiness_at_least_20_tt
		check_variable = { OBT_reserve_readiness > 19 }
	}
}
'''
L("OBT_mob_crisis_condition_tt", "Cross-Strait Tension is at §YCrisis§! or higher, Taiwan is under blockade, or Taiwan is at war with China")
L("OBT_mob_war_condition_tt", "Taiwan is at war with China, or Cross-Strait Tension is at §YBrink§! (80 or higher)")
L("OBT_reserve_readiness_at_least_20_tt", "Reserve Readiness is at least §Y20§!")
L("OBT_mob_partial", "Partial mobilization is active")
L("OBT_mob_general", "General mobilization is active")
L("OBT_mob_cooldown", "Taiwan demobilized less than a year ago")
L("OBT_reserve_program", "The Reserve Readiness Program is running")

dynmod = '''OBT_reserve_program_cost = {
	icon = GFX_idea_national_unity
	political_power_gain = -0.1
}

OBT_partial_mobilization = {
	icon = GFX_idea_national_unity
	industrial_capacity_factory = -0.05
	industrial_capacity_dockyard = -0.05
	stability_factor = -0.03
	war_support_factor = 0.05
}

OBT_general_mobilization = {
	icon = GFX_idea_national_unity
	industrial_capacity_factory = -0.15
	industrial_capacity_dockyard = -0.10
	stability_factor = -0.08
	war_support_factor = 0.10
	political_power_gain = -0.25
}
'''
L("OBT_reserve_program_cost", "Reserve Readiness Program")
L("OBT_partial_mobilization", "Partial Mobilization")
L("OBT_general_mobilization", "General Mobilization")

DEC = []


def D(key, name, desc, icon, visible, available, cost, eff, ai, extra=()):
    d = [f"\t{key} = {{", f"\t\ticon = {icon}", "", "\t\tvisible = {"] + [f"\t\t\t{l}" for l in visible] + ["\t\t}", ""]
    if available:
        d += ["\t\tavailable = {"] + [f"\t\t\t{l}" for l in available] + ["\t\t}", ""]
    d += [f"\t\tcost = {cost}"] + list(extra) + ["", "\t\tcomplete_effect = {", f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision {key}"'] + \
         [f"\t\t\t{l}" for l in eff] + ["\t\t}", "", "\t\tai_will_do = {"] + [f"\t\t\t{l}" for l in ai] + ["\t\t}", "\t}", ""]
    DEC.append("\n".join(d))
    L(key, name)
    L(key + "_desc", desc)


def money(n):
    return [f"set_temp_variable = {{ treasury_change = {n} }}", "modify_treasury_effect = yes"]


def tt(k, v):
    L(k, v)
    return f"custom_effect_tooltip = {k}"


D("OBT_start_reserve_program", "Launch the Reserve Readiness Program",
  "Keep reserve rosters current, store equipment where units will gather, and train the cadres who will lead them. The program costs political capital every day it runs.",
  "generic_army_support", ["NOT = { has_country_flag = OBT_reserve_program }"], [], 25,
  ["set_country_flag = OBT_reserve_program", "add_dynamic_modifier = { modifier = OBT_reserve_program_cost }",
   tt("OBT_start_reserve_program_tt", "Reserve Readiness rises by §G2§! a month while the program runs (otherwise it falls by 1 a month, to no lower than 10).")],
  ["base = 3", "modifier = { factor = 3 OBT_strait_at_least_coercion = yes }", "modifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }"])
D("OBT_end_reserve_program", "End the Reserve Readiness Program",
  "Stop the program and save its political cost. Readiness will slowly decline.",
  "generic_army_support", ["has_country_flag = OBT_reserve_program"], [], 0,
  ["clr_country_flag = OBT_reserve_program", "if = { limit = { has_dynamic_modifier = { modifier = OBT_reserve_program_cost } } remove_dynamic_modifier = { modifier = OBT_reserve_program_cost } }"],
  ["base = 0", "modifier = { add = 2 OBT_strait_at_most_coercion = yes check_variable = { OBT_reserve_readiness > 60 } }"])
D("OBT_reserve_refresher_recall", "Annual Reserve Refresher Recall",
  "Call reservists back for five to seven days of refresher training, as the armed forces did each year in the late 1990s. Employers and families notice.",
  "generic_army_support", ["always = yes"], [], 25,
  money(-0.3) + ["add_stability = -0.01", "add_to_variable = { OBT_reserve_readiness = 8 }", "clamp_variable = { var = OBT_reserve_readiness min = 0 max = 100 }",
                 tt("OBT_reserve_refresher_recall_tt", "Reserve Readiness §G+8§!.")],
  ["base = 2", "modifier = { factor = 3 OBT_strait_at_least_coercion = yes }"], extra=["\t\tdays_re_enable = 365"])
D("OBT_partial_mobilization_dec", "Partial Mobilization",
  "Call up the first reserve brigades. They gather over the next month with whatever equipment the depots hold, and they will be far less trained than the regular army.",
  "generic_military", ["NOT = { has_country_flag = OBT_mob_partial }", "NOT = { has_country_flag = OBT_mob_general }"],
  ["OBT_mob_crisis_condition = yes", "OBT_reserve_readiness_at_least_20 = yes", "has_manpower > 12000", "NOT = { has_country_flag = OBT_mob_cooldown }"], 100,
  ["set_country_flag = OBT_mob_partial", "add_dynamic_modifier = { modifier = OBT_partial_mobilization }", "add_stability = -0.02",
   "country_event = { id = obt_mob.1 days = 15 }", "country_event = { id = obt_mob.1 days = 30 }",
   tt("OBT_partial_mobilization_dec_tt", "§Y4§! reserve infantry brigades arrive in two groups, after §Y15§! and §Y30§! days. They draw equipment and manpower from the stockpile as they fill.")],
  ["base = 1", "modifier = { add = 20 OBT_strait_at_least_crisis = yes }", "modifier = { add = 40 has_war_with = CHI }"])
D("OBT_general_mobilization_dec", "General Mobilization",
  "Call up every reserve brigade the system can form. The economy will slow sharply while factories lose their workers.",
  "generic_military", ["has_country_flag = OBT_mob_partial", "NOT = { has_country_flag = OBT_mob_general }"],
  ["OBT_mob_war_condition = yes", "has_manpower > 24000"], 150,
  ["set_country_flag = OBT_mob_general", "if = { limit = { has_dynamic_modifier = { modifier = OBT_partial_mobilization } } remove_dynamic_modifier = { modifier = OBT_partial_mobilization } }", "add_dynamic_modifier = { modifier = OBT_general_mobilization }",
   "add_stability = -0.04", "country_event = { id = obt_mob.1 days = 15 }", "country_event = { id = obt_mob.1 days = 30 }",
   "country_event = { id = obt_mob.1 days = 45 }", "country_event = { id = obt_mob.1 days = 60 }",
   tt("OBT_general_mobilization_dec_tt", "Up to §Y8§! more reserve infantry brigades arrive in pairs every §Y15§! days, §Y12§! in total.")],
  ["base = 1", "modifier = { add = 50 has_war_with = CHI }"])
D("OBT_demobilize_reserves", "Demobilize the Reserves",
  "Send the reserve brigades home. Their men and equipment return to the pool, and the economy recovers. Mobilizing again will not be possible for a year.",
  "generic_military", ["OR = { has_country_flag = OBT_mob_partial has_country_flag = OBT_mob_general }"],
  ["NOT = { AND = { country_exists = CHI has_war_with = CHI } }", "OBT_strait_below_crisis = yes"], 0,
  ["OBT_reserve_demobilize = yes", tt("OBT_demobilize_reserves_tt", "Every mobilized reserve brigade is disbanded. Their manpower and equipment return to the pool.")],
  ["base = 0", "modifier = { add = 10 OBT_strait_at_most_coercion = yes NOT = { has_war_with = CHI } }"])

category = '''# Operation Blue Tiger milestone 10: reserve mobilization
OBT_reserve_category = {
	allowed = { original_tag = TAI }
	icon = GFX_decision_generic_taiwan
	priority = 589
	visible_when_empty = yes
}
'''
L("OBT_reserve_category", "Reserve Mobilization")
L("OBT_reserve_category_desc", "Reserve Readiness: §Y[?TAI.OBT_reserve_readiness|0]§! / 100. Mobilized brigades: §Y[?TAI.OBT_mob_spawned|0]§!.\\n\\nReserve formations do not exist in peacetime. Preparation raises readiness, which decides how experienced the brigades are when they are called up. Partial mobilization raises §Y4§! brigades in a crisis; general mobilization raises up to §Y12§! in a war with China. Brigades fill from the equipment stockpile, the economy pays while they serve, and demobilization sends them home with a one-year cooldown.")

events = f'''add_namespace = obt_mob

# Hidden: a reserve group reports for duty
country_event = {{
	id = obt_mob.1
	is_triggered_only = yes
	hidden = yes

	trigger = {{
		original_tag = TAI
		OR = {{ has_country_flag = OBT_mob_partial has_country_flag = OBT_mob_general }}
	}}

	immediate = {{
		log = "[GetDateText]: [This.GetName]: obt_mob.1 executed"
		OBT_reserve_spawn_two = yes
	}}
}}
'''

on_actions = '''# Operation Blue Tiger milestone 10: reserve mobilization
on_actions = {
	on_monthly_TAI = {
		effect = {
			OBT_reserve_monthly = yes
		}
	}
	on_startup = {
		effect = {
			if = {
				limit = { country_exists = TAI }
				TAI = { OBT_reserve_init = yes }
			}
		}
	}
}
'''
w("common/scripted_effects/99_OBT_reserve_scripted_effects.txt", effects)
w("common/scripted_triggers/99_OBT_reserve_scripted_triggers.txt", triggers)
w("common/dynamic_modifiers/99_OBT_reserve_dynamic_modifiers.txt", dynmod)
w("common/decisions/OBT_reserve_decisions.txt", "OBT_reserve_category = {\n" + "\n".join(DEC) + "}\n")
w("common/decisions/categories/99_OBT_reserve_categories.txt", category)
w("events/OBT_mobilization_events.txt", events)
w("common/on_actions/99_OBT_reserve_on_actions.txt", on_actions)
w("localisation/english/MD_OBT_reserve_l_english.yml", "l_english:\n # Operation Blue Tiger milestone 10: reserve mobilization\n" + "\n".join(LOC) + "\n", bom=True)
print(len(DEC), "decisions,", len(LOC), "loc")
