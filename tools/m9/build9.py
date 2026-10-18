#!/usr/bin/env python3
"""Operation Blue Tiger milestone 9: Defense and National Reform tab, national indicators,
procurement tracker and American arms deliveries.

Usage: python3 build9.py <out_dir>
Stage 1: dashboard, indicator effects, procurement tracking and funding.
Stage 2: refit and construction timers, deliveries, acceleration, the submarine route and Aegis.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LOC = []


def w(name, text, bom=False):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)


def L(key, text):
    assert "—" not in text, key
    LOC.append(f' {key}: "{text}"')


def ind(lines, n):
    return ["\t" * n + l if l else "" for l in lines]


# ---------------------------------------------------------------- indicators
# key, variable, owner, short label, full name, start value, negative bar, effects [(var, modifier, per-point, pct label)]
INDICATORS = [
    ("milconf", "TAI_military_confidence", "TAI", "Mil. Confidence", "Military Confidence", 55, False,
     [("OBT_ni_org", "army_org_factor", 0.001, "Division organization"), ("OBT_ni_plan", "planning_speed", 0.002, "Planning speed")],
     "How far the officer corps trusts the elected government and believes the forces can fight.",
     "Raised by the National Defense Act, reassuring the commanders, Han Kuang exercises, deliveries entering service and some events. Lowered by abrupt purges of the old guard, scandals and a stalled defense budget."),
    ("reform", "TAI_reform_capacity", "TAI", "Reform Capacity", "Reform Capacity", 50, False,
     [("OBT_ni_research", "research_speed_factor", 0.0006, "Research speed"), ("OBT_ni_xp", "experience_gain_army_factor", 0.002, "Army experience gain")],
     "The state's ability to change how it buys, trains and organizes: trained staff, honest procurement and the patience to absorb new equipment.",
     "Raised by the absorption, service-rivalry and interoperability focuses, technocratic and judicial reforms, joint operations drills and Pentagon assessments."),
    ("coord", "TAI_national_coordination", "TAI", "Coordination", "National Coordination Capacity", 40, False,
     [("OBT_ni_build", "production_speed_buildings_factor", 0.001, "Construction speed"), ("OBT_ni_stab", "stability_factor", 0.0005, "Stability")],
     "Whether ministries, local governments and the armed forces can act as one in a crisis.",
     "Raised by the Operation Blue Tiger branch, the National Security Council, local emergency administration, a neutral civil service and civil defense coordination."),
    ("usconf", "TAI_us_confidence", "TAI", "U.S. Confidence", "U.S. Confidence in Taipei", 60, False, [],
     "How much Washington trusts Taipei: that it will not provoke Beijing, will fund its own defense and can use what it buys. This is Taipei's standing in Washington, not America's commitment.",
     "Raised by funding defense budgets, hosting Pentagon assessments, reassuring Washington and avoiding unilateral moves. Lowered by stalled budgets, surprise steps toward independence and ignoring American advice."),
    ("ussupport", "CHI_taiwan_us_support", "CHI", "U.S. Support", "U.S. Support (Washington's commitment)", 85, False, [],
     "How committed the United States is to deterring Beijing. Washington decides this, and Beijing watches it. Taipei can influence it but not control it.",
     "Raised by arms sales, Japanese and American statements, coercion that looks unprovoked and Pacific Lifeline diplomacy. Lowered by American distraction, Chinese influence campaigns and moves Washington sees as provocative."),
    ("ptn", "TAI_pressure_to_negotiate", "TAI", "Pressure", "Pressure to Negotiate", 5, True, [],
     "How strongly the public and the economy push the government to accept talks on Beijing's terms.",
     "Rises while a Chinese blockade bites and falls by 2 a month without one. Reduced by stability above 60%, Impossible to Coerce, U.S. Support above 60, strategic reserves and Blue Tiger decisions."),
    ("identity", "TAI_taiwanese_identity", "TAI", "Identity", "Taiwan-Centered Identity", 40, False, [],
     "How strongly citizens see themselves as Taiwanese first. It is neither good nor bad in itself: it changes which paths are open.",
     "Raised by Pan-Green focuses, coercion against a stable Taiwan and name-rectification policies. Lowered by reassurances to Beijing and some Pan-Blue focuses."),
    ("dep", "TAI_mainland_dependence", "TAI", "Mainland Dep.", "Mainland Economic Dependence", 30, True,
     [("OBT_ni_ic", "industrial_capacity_factory", 0.0005, "Factory output"), ("OBT_ni_ws", "war_support_factor", -0.001, "War support")],
     "How much of Taiwan's trade, investment and jobs depend on the mainland. It pays, and it gives Beijing leverage.",
     "Raised by the Three Links, opening investment and mainland tourists. Lowered by Go South, diversifying export markets, sector investment caps and supply-chain reviews."),
    ("chips", "TAI_semiconductor_security", "TAI", "Chip Security", "Semiconductor Supply Security", 85, False,
     [("OBT_ni_eff", "production_factory_efficiency_gain_factor", 0.0015, "Production efficiency growth")],
     "Whether Taiwan's chip industry can keep running: materials, tools, energy and skilled engineers.",
     "Raised by the Silicon Island branch, the Japanese and Dutch supply partnerships, strategic materials inventories and supply-chain reviews. A few events lower it, and it can only be rebuilt through partners and reserves."),
]

EXTRA_EFFECT_TEXT = {
    "usconf": "§YEffects:§! Requesting U.S. support needs at least 40. In a war with China, 60 or more makes American intervention or aid more likely; below 30 Washington is more likely to stay out. Arms procurement steps need 55-75 (see the tracker).",
    "ussupport": "§YEffects:§! Above 60 it slows the growth of Pressure to Negotiate. Beijing's harshest options open as it falls: missile tests below 50, a maritime zone below 40, a partial blockade below 30 and a full blockade below 20.",
    "ptn": "§YEffects:§! At 50 or more Taiwan can seek terms and Beijing can offer talks. At 70 or more under blockade, Beijing presents terms.",
    "identity": "§YEffects:§! Shapes how the public reacts to talks with Beijing and, on the Return to the Mainland path, the balance between restoration and self-determination.",
}


def indicator_effects_block():
    out = ["OBT_dash_update = {"]
    for key, var, owner, _s, _n, start, _neg, effs, _d, _r in INDICATORS:
        if not effs:
            continue
        for v, _m, k, _lbl in effs:
            out += [f"\tset_variable = {{ {v} = {var} }}", f"\tsubtract_from_variable = {{ {v} = {start} }}",
                    f"\tmultiply_variable = {{ {v} = {k} }}",
                    f"\tset_variable = {{ {v}_p = {v} }}", f"\tmultiply_variable = {{ {v}_p = 100 }}"]
    out += ["\tif = {", "\t\tlimit = { NOT = { has_dynamic_modifier = { modifier = OBT_TAI_national_indicators } } }",
            "\t\tadd_dynamic_modifier = { modifier = OBT_TAI_national_indicators }", "\t}"]
    out += ["\tOBT_proc_months = yes", "}"]
    return out


def dynmod():
    lines = ["OBT_TAI_national_indicators = {", "\ticon = GFX_idea_national_unity", ""]
    for key, var, *_rest in INDICATORS:
        for v, m, _k, _l in _rest[5]:
            lines.append(f"\t{m} = {v}")
    lines.append("}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- procurement data
PROJ = {
    "kidd": ("OBT_pk", "Kidd-class destroyers", 4),
    "p3c": ("OBT_pp", "P-3C patrol aircraft", 12),
    "sub": ("OBT_ps", "Diesel submarines", 8),
    "aegis": ("OBT_pa", "Aegis destroyers", 4),
}
STATUS = {
    "kidd": [(0, "Not offered"), (1, "Approved by Washington, awaiting the special budget"), (2, "Funded, awaiting the transfer agreement (Accept the Kidd-Class Destroyers)"),
             (3, "Refit in Charleston: first pair in about [?TAI.OBT_pk_months|0] months"), (4, "2 of 4 delivered: second pair in about [?TAI.OBT_pk_months|0] months"),
             (5, "4 of 4 delivered, crews working up: ready in about [?TAI.OBT_pk_months|0] months"), (6, "In service (4 of 4)"), (99, "Cancelled")],
    "p3c": [(0, "Not offered"), (1, "Approved by Washington, awaiting a full special budget"), (2, "Funded, awaiting procurement (Maritime Patrol Aircraft)"),
            (3, "Negotiating the refurbishment contract: about [?TAI.OBT_pp_months|0] months"), (4, "Airframes in refurbishment: first 4 in about [?TAI.OBT_pp_months|0] months"),
            (5, "[?TAI.OBT_pp_n|0] of 12 delivered: next 4 in about [?TAI.OBT_pp_months|0] months"), (6, "12 of 12 delivered, crews training: ready in about [?TAI.OBT_pp_months|0] months"),
            (7, "In service (12 of 12)"), (99, "Cancelled")],
    "sub": [(0, "Not offered"), (1, "Approved by Washington, awaiting a full special budget"), (2, "Funded for design work, awaiting The Submarine Question"),
            (3, "No builder found: seeking a construction partner before 1 January 2009"), (4, "Builder secured ([OBT_sub_partner_name]), awaiting the construction appropriation"),
            (5, "Under construction ([OBT_sub_partner_name]): first pair in about [?TAI.OBT_ps_months|0] months"), (6, "[?TAI.OBT_ps_n|0] of 8 commissioned: next pair in about [?TAI.OBT_ps_months|0] months"),
            (7, "8 of 8 commissioned, crews working up: ready in about [?TAI.OBT_ps_months|0] months"), (8, "In service (8 of 8)"),
            (98, "Failed: no foreign yard would build them. The Indigenous Submarine Program is the way forward"), (99, "Cancelled")],
    "aegis": [(0, "Not offered"), (1, "Approved by Washington, awaiting funding"), (2, "Under construction: first pair in about [?TAI.OBT_pa_months|0] months"),
              (3, "2 of 4 delivered: second pair in about [?TAI.OBT_pa_months|0] months"), (4, "4 of 4 delivered, crews working up: ready in about [?TAI.OBT_pa_months|0] months"),
              (5, "In service (4 of 4)"), (99, "Cancelled")],
}


def stage_is(p, *vals):
    v = PROJ[p][0]
    if len(vals) == 1:
        return f"check_variable = {{ {v}_stage = {vals[0]} }}"
    return "OR = { " + " ".join(f"check_variable = {{ {v}_stage = {x} }}" for x in vals) + " }"


def set_stage(p, n, days=None):
    v = PROJ[p][0]
    out = [f"set_variable = {{ {v}_stage = {n} }}"]
    if days is not None:
        out.append(f"set_variable = {{ {v}_days = {days} }}")
    return out


def addvar(var, n, owner=None):
    body = [f"add_to_variable = {{ {var} = {n} tooltip = {var}_tt }}", f"clamp_variable = {{ var = {var} min = 0 max = 100 }}"]
    if owner:
        return ["if = {", f"\tlimit = {{ country_exists = {owner} }}", f"\t{owner} = {{"] + ind(body, 2) + ["\t}", "}"]
    return body


def tension(n):
    return addvar("CHI_taiwan_strait_tension", n, "CHI") + ["OBT_strait_update = yes"]


def money(n):
    return [f"set_temp_variable = {{ treasury_change = {n} }}", "modify_treasury_effect = yes"]


# ---------------------------------------------------------------- variants and deliveries
KIDD_MODULES = {
    "fixed_ship_engine_slot": "module_surface_jet_turbine_power",
    "fixed_ship_fire_control_system_slot": "module_screen_digital_integrated_fire_control",
    "fixed_ship_radar_slot": "module_radar_3",
    "fixed_ship_auxillary_slot_3": "module_torpedoes_2",
    "fixed_ship_auxillary_slot_2": "module_naval_missile_mount_quad",
    "fixed_ship_auxillary_slot": "module_127mm_guns_2",
    "fixed_ship_battery_slot": "module_127mm_guns_2",
    "front_1_custom_slot": "module_naval_missile_mount_twin",
    "mid_1_custom_slot": "module_ciws_2",
    "mid_2_custom_slot": "module_ciws_2",
    "rear_1_custom_slot": "module_naval_missile_mount_twin",
    "fixed_ship_missile_ammo_slot": "module_naval_ammo_air_defense_1",
}
AEGIS_MODULES = {
    "fixed_ship_engine_slot": "module_surface_jet_turbine_power",
    "fixed_ship_fire_control_system_slot": "module_screen_digital_integrated_fire_control",
    "fixed_ship_radar_slot": "module_radar_4",
    "fixed_ship_auxillary_slot_3": "module_naval_vls_cells_64",
    "fixed_ship_auxillary_slot_2": "module_torpedoes_2",
    "fixed_ship_auxillary_slot": "module_esm_1",
    "fixed_ship_battery_slot": "module_127mm_guns_2",
    "front_1_custom_slot": "module_naval_vls_cells_64",
    "mid_1_custom_slot": "module_naval_vls_cells_32",
    "mid_2_custom_slot": "module_ciws_3",
    "rear_1_custom_slot": "module_light_helipad_1",
    "fixed_ship_missile_ammo_slot": "module_naval_ammo_balanced_3",
}
SUB_MODULES = {
    "fixed_ship_engine_slot": "module_sub_diesel_electric_power2",
    "fixed_ship_radar_slot": "module_sonar_3",
    "fixed_ship_auxillary_slot_3": "module_fuel_tank",
    "fixed_ship_auxillary_slot_2": "module_sub_esm_2",
    "fixed_ship_auxillary_slot_1": "module_torpedoes_3",
    "fixed_ship_auxillary_slot": "module_torpedoes_3",
    "fixed_ship_battery_slot": "module_anti_ship_torpedoes_3",
}
SUB_VARIANTS = [(1, "ROC Diesel Submarine (U.S. design)"), (2, "Improved Hai Lung Class"), (3, "Type 209/1400 Class (ROC)")]


def variant(flag, name, typ, modules):
    return ["if = {", f"\tlimit = {{ NOT = {{ has_country_flag = {flag} }} }}", f"\tset_country_flag = {flag}",
            "\tcreate_equipment_variant = {", f'\t\tname = "{name}"', f"\t\ttype = {typ}", "\t\tparent_version = 0", "\t\tmodules = {"] + \
        [f"\t\t\t{k} = {v}" for k, v in modules.items()] + ["\t\t}", "\t}", "}"]


def ship(typ, var_name, name=None):
    n = f' name = "{name}"' if name else ""
    return f'create_ship = {{ type = {typ} equipment_variant = "{var_name}" creator = TAI{n} }}'


def effects():
    E = []
    E += ["# Operation Blue Tiger milestone 9: Defense and National Reform, procurement and deliveries", ""]
    E += indicator_effects_block() + [""]
    # months for display
    E.append("OBT_proc_months = {")
    for p, (v, _n, _t) in PROJ.items():
        E += [f"\tset_variable = {{ {v}_months = {v}_days }}", f"\tdivide_variable = {{ {v}_months = 30 }}", f"\tround_variable = {v}_months",
              f"\tif = {{ limit = {{ check_variable = {{ {v}_months < 1 }} }} set_variable = {{ {v}_months = 1 }} }}"]
    E += ["}", ""]
    # deliveries
    E.append("OBT_deliver_kidd_pair_1 = {")
    E += ind(variant("OBT_kidd_variant", "Kidd Class (Keelung)", "destroyer_hull_1", KIDD_MODULES), 1)
    E += ["\t" + ship("destroyer_hull_1", "Kidd Class (Keelung)", "ROCS Keelung (DDG-1801)"), "\t" + ship("destroyer_hull_1", "Kidd Class (Keelung)", "ROCS Su Ao (DDG-1802)"),
          "\tadd_to_variable = { OBT_pk_n = 2 }", "}", ""]
    E.append("OBT_deliver_kidd_pair_2 = {")
    E += ind(variant("OBT_kidd_variant", "Kidd Class (Keelung)", "destroyer_hull_1", KIDD_MODULES), 1)
    E += ["\t" + ship("destroyer_hull_1", "Kidd Class (Keelung)", "ROCS Tso Ying (DDG-1803)"), "\t" + ship("destroyer_hull_1", "Kidd Class (Keelung)", "ROCS Ma Kong (DDG-1805)"),
          "\tadd_to_variable = { OBT_pk_n = 2 }", "}", ""]
    E += ["OBT_deliver_p3c_batch = {", "\tif = {", '\t\tlimit = { has_dlc = "By Blood Alone" }', "\t\tif = {", "\t\t\tlimit = { country_exists = USA }",
          '\t\t\tadd_equipment_to_stockpile = { type = large_plane_maritime_patrol_airframe_1 variant_name = "P-3 Orion" amount = 4 producer = USA }',
          "\t\t}", "\t\telse = {", "\t\t\tadd_equipment_to_stockpile = { type = large_plane_maritime_patrol_airframe_1 amount = 4 }", "\t\t}", "\t}", "\telse = {",
          "\t\tadd_equipment_to_stockpile = { type = naval_plane2 amount = 4 }", "\t}", "\tadd_to_variable = { OBT_pp_n = 4 }", "}", ""]
    E.append("OBT_deliver_sub_pair = {")
    for pid, name in SUB_VARIANTS:
        E += [f"\tif = {{", f"\t\tlimit = {{ check_variable = {{ OBT_ps_partner = {pid} }} }}"]
        E += ind(variant(f"OBT_sub_variant_{pid}", name, "attack_submarine_hull_3", SUB_MODULES), 2)
        E += ["\t\t" + ship("attack_submarine_hull_3", name), "\t\t" + ship("attack_submarine_hull_3", name), "\t}"]
    E += ["\tadd_to_variable = { OBT_ps_n = 2 }", "}", ""]
    E.append("OBT_deliver_aegis_pair = {")
    E += ind(variant("OBT_aegis_variant", "Arleigh Burke Class (ROC)", "destroyer_hull_3", AEGIS_MODULES), 1)
    E += ["\t" + ship("destroyer_hull_3", "Arleigh Burke Class (ROC)"), "\t" + ship("destroyer_hull_3", "Arleigh Burke Class (ROC)"),
          "\tadd_to_variable = { OBT_pa_n = 2 }"] + ind(tension(5), 1) + ["}", ""]

    # monthly update
    U = ["OBT_proc_update = {"]
    U += ["\t# hold reasons: 1 relationship broken, 2 war with the United States, 3 Strait closed by war",
          "\tset_variable = { OBT_proc_hold = 0 }",
          "\tif = { limit = { OBT_proc_us_channel_closed = yes } set_variable = { OBT_proc_hold = 1 } }",
          "\telse_if = { limit = { country_exists = USA has_war_with = USA } set_variable = { OBT_proc_hold = 2 } }",
          "\telse_if = { limit = { OBT_proc_strait_closed = yes } set_variable = { OBT_proc_hold = 3 } }",
          "",
          "\t# approvals"]
    for p in ("kidd", "p3c", "sub"):
        U += [f"\tif = {{ limit = {{ {stage_is(p, 0)} OBT_proc_package_approved = yes }} set_variable = {{ {PROJ[p][0]}_stage = 1 }} }}"]
    U += ["\tif = { limit = { " + stage_is("aegis", 0) + " has_global_flag = OBT_2001_aegis } set_variable = { OBT_pa_stage = 1 } }", ""]

    def timer(v):
        return [f"if = {{ limit = {{ check_variable = {{ OBT_proc_hold = 0 }} }} subtract_from_variable = {{ {v}_days = 30 }} }}"]

    def due(v, port=True):
        c = f"check_variable = {{ {v}_days < 1 }}"
        return c + (" OBT_proc_has_port = yes" if port else "")

    # Kidd
    U += ["\t# Kidd-class destroyers", "\tif = {", f"\t\tlimit = {{ {stage_is('kidd', 1)} has_country_flag = OBT_budget_kidd }}"] + ind(set_stage("kidd", 2), 2) + ["\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('kidd', 2)} has_completed_focus = TAI_na_kidd_destroyers }}"] + ind(set_stage("kidd", 3, 930), 2) + ["\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('kidd', 3, 4)} }}"] + ind(timer("OBT_pk"), 2) + [
          "\t\tif = {", f"\t\t\tlimit = {{ {stage_is('kidd', 3)} {due('OBT_pk')} }}", "\t\t\tOBT_deliver_kidd_pair_1 = yes"] + ind(set_stage("kidd", 4, 320), 3) + [
          "\t\t\tcountry_event = { id = obt_proc.1 days = 1 }", "\t\t}",
          "\t\telse_if = {", f"\t\t\tlimit = {{ {stage_is('kidd', 4)} {due('OBT_pk')} }}", "\t\t\tOBT_deliver_kidd_pair_2 = yes"] + ind(set_stage("kidd", 5, 180), 3) + [
          "\t\t\tcountry_event = { id = obt_proc.2 days = 1 }", "\t\t}", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('kidd', 5)} }}", "\t\tsubtract_from_variable = { OBT_pk_days = 30 }",
          "\t\tif = {", "\t\t\tlimit = { check_variable = { OBT_pk_days < 1 } }"] + ind(set_stage("kidd", 6), 3) + ind(addvar("TAI_military_confidence", 5), 3) + [
          "\t\t\tnavy_experience = 25", "\t\t}", "\t}", ""]
    # P-3C
    U += ["\t# P-3C Orion maritime patrol aircraft", "\tif = {", f"\t\tlimit = {{ {stage_is('p3c', 1)} has_country_flag = OBT_budget_full }}"] + ind(set_stage("p3c", 2), 2) + ["\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('p3c', 2)} has_completed_focus = TAI_na_maritime_patrol }}"] + ind(set_stage("p3c", 3, 600), 2) + ["\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('p3c', 3, 4, 5)} }}"] + ind(timer("OBT_pp"), 2) + [
          "\t\tif = {", f"\t\t\tlimit = {{ {stage_is('p3c', 3)} {due('OBT_pp', False)} }}"] + ind(set_stage("p3c", 4, 1500), 3) + [
          "\t\t\tcountry_event = { id = obt_proc.10 days = 1 }", "\t\t}",
          "\t\telse_if = {", f"\t\t\tlimit = {{ {stage_is('p3c', 4, 5)} {due('OBT_pp', False)} }}", "\t\t\tOBT_deliver_p3c_batch = yes",
          "\t\t\tif = {", "\t\t\t\tlimit = { check_variable = { OBT_pp_n > 11 } }"] + ind(set_stage("p3c", 6, 180), 4) + [
          "\t\t\t\tcountry_event = { id = obt_proc.12 days = 1 }", "\t\t\t}", "\t\t\telse = {"] + ind(set_stage("p3c", 5, 540), 4) + [
          "\t\t\t\tif = { limit = { has_country_flag = OBT_pp_second_line } set_variable = { OBT_pp_days = 270 } }",
          "\t\t\t\tcountry_event = { id = obt_proc.11 days = 1 }", "\t\t\t}", "\t\t}", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('p3c', 6)} }}", "\t\tsubtract_from_variable = { OBT_pp_days = 30 }",
          "\t\tif = {", "\t\t\tlimit = { check_variable = { OBT_pp_days < 1 } }"] + ind(set_stage("p3c", 7), 3) + ind(addvar("TAI_military_confidence", 3), 3) + [
          "\t\t\tair_experience = 20", "\t\t}", "\t}", ""]
    # Submarines
    U += ["\t# Diesel-electric submarines", "\tif = {", f"\t\tlimit = {{ {stage_is('sub', 1)} has_country_flag = OBT_budget_full }}"] + ind(set_stage("sub", 2), 2) + ["\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('sub', 2)} has_completed_focus = TAI_na_submarine_question }}"] + ind(set_stage("sub", 3), 2) + [
          "\t\tcountry_event = { id = obt_proc.20 days = 1 }", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('sub', 3)} date > 2009.1.1 NOT = {{ has_country_flag = OBT_ps_negotiating }} }}"] + ind(set_stage("sub", 98), 2) + [
          "\t\tcountry_event = { id = obt_proc.21 days = 1 }", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('sub', 5, 6)} }}"] + ind(timer("OBT_ps"), 2) + [
          "\t\tif = {", f"\t\t\tlimit = {{ {due('OBT_ps')} }}", "\t\t\tOBT_deliver_sub_pair = yes",
          "\t\t\tif = {", "\t\t\t\tlimit = { check_variable = { OBT_ps_n > 7 } }"] + ind(set_stage("sub", 7, 180), 4) + [
          "\t\t\t\tcountry_event = { id = obt_proc.25 days = 1 }", "\t\t\t}", "\t\t\telse = {"] + ind(set_stage("sub", 6, 365), 4) + [
          "\t\t\t\tif = { limit = { has_country_flag = OBT_ps_second_line } set_variable = { OBT_ps_days = 180 } }",
          "\t\t\t\tcountry_event = { id = obt_proc.24 days = 1 }", "\t\t\t}", "\t\t}", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('sub', 7)} }}", "\t\tsubtract_from_variable = { OBT_ps_days = 30 }",
          "\t\tif = {", "\t\t\tlimit = { check_variable = { OBT_ps_days < 1 } }"] + ind(set_stage("sub", 8), 3) + ind(addvar("TAI_military_confidence", 5), 3) + [
          "\t\t\tnavy_experience = 30", "\t\t}", "\t}", ""]
    # Aegis
    U += ["\t# Aegis destroyers (alternate history)", "\tif = {", f"\t\tlimit = {{ {stage_is('aegis', 2, 3)} }}"] + ind(timer("OBT_pa"), 2) + [
          "\t\tif = {", f"\t\t\tlimit = {{ {due('OBT_pa')} }}", "\t\t\tOBT_deliver_aegis_pair = yes",
          "\t\t\tif = {", f"\t\t\t\tlimit = {{ {stage_is('aegis', 3)} }}"] + ind(set_stage("aegis", 4, 180), 4) + ["\t\t\t}", "\t\t\telse = {"] + ind(set_stage("aegis", 3, 365), 4) + ["\t\t\t}",
          "\t\t\tcountry_event = { id = obt_proc.30 days = 1 }", "\t\t}", "\t}",
          "\telse_if = {", f"\t\tlimit = {{ {stage_is('aegis', 4)} }}", "\t\tsubtract_from_variable = { OBT_pa_days = 30 }",
          "\t\tif = {", "\t\t\tlimit = { check_variable = { OBT_pa_days < 1 } }"] + ind(set_stage("aegis", 5), 3) + ind(addvar("TAI_military_confidence", 5), 3) + ["\t\t}", "\t}"]
    U += ["\tOBT_proc_months = yes", "}"]
    E += U
    return "\n".join(E) + "\n"


def triggers():
    T = ["# Operation Blue Tiger milestone 9: procurement conditions", "",
         "OBT_proc_package_approved = {", "\tOR = {", "\t\thas_global_flag = OBT_2001_package_approved", "\t\thas_completed_focus = TAI_na_2001_package", "\t}", "}", "",
         "OBT_proc_us_channel_closed = {", "\tOR = {", "\t\tNOT = { country_exists = USA }", "\t\tUSA = { has_country_flag = USA_withdrew_support_TAI }", "\t}", "}", "",
         "OBT_proc_strait_closed = {", "\tcountry_exists = CHI", "\thas_war_with = CHI", "\tNOT = { USA = { has_war_with = CHI } }", "}", "",
         "OBT_proc_has_port = {", "\tcustom_trigger_tooltip = {", "\t\ttooltip = OBT_proc_has_port_tt", "\t\tany_controlled_state = { naval_base > 0 }", "\t}", "}", "",
         "OBT_proc_channel_open = {", "\tcustom_trigger_tooltip = {", "\t\ttooltip = OBT_proc_channel_open_tt", "\t\tcheck_variable = { OBT_proc_hold = 0 }", "\t}", "}", ""]
    for n in (1, 2, 3, 4, 5, 6):
        T += [f"OBT_treasury_{n} = {{", "\tcustom_trigger_tooltip = {", f"\t\ttooltip = OBT_treasury_{n}_tt", f"\t\tcheck_variable = {{ treasury > {n - 0.01} }}", "\t}", "}", ""]
        L(f"OBT_treasury_{n}_tt", f"The treasury holds at least §Y${n} billion§!")
    T += ["OBT_strait_below_friction = {", "\tcustom_trigger_tooltip = {", "\t\ttooltip = OBT_strait_below_friction_tt", "\t\tOR = {", "\t\t\tNOT = { country_exists = CHI }",
          "\t\t\tCHI = { check_variable = { CHI_taiwan_strait_tension < 40 } }", "\t\t}", "\t}", "}", "",
          "OBT_strait_below_crisis = {", "\tcustom_trigger_tooltip = {", "\t\ttooltip = OBT_strait_below_crisis_tt", "\t\tOR = {", "\t\t\tNOT = { country_exists = CHI }",
          "\t\t\tCHI = { check_variable = { CHI_taiwan_strait_tension < 60 } }", "\t\t}", "\t}", "}", "",
          "OBT_strait_below_brink = {", "\tcustom_trigger_tooltip = {", "\t\ttooltip = OBT_strait_below_brink_tt", "\t\tOR = {", "\t\t\tNOT = { country_exists = CHI }",
          "\t\t\tCHI = { check_variable = { CHI_taiwan_strait_tension < 80 } }", "\t\t}", "\t}", "}", ""]
    # submarine partner requirements
    T += ["OBT_sub_partner_usa_ready = {", "\tcountry_exists = USA", "\t" + req("TAI_us_confidence", 74),
          "\t" + req("CHI_taiwan_us_support", 64, "CHI"), "\t" + req("TAI_military_confidence", 54),
          "\t" + req("TAI_reform_capacity", 54), "\tOBT_strait_below_brink = yes", "}", "",
          "OBT_sub_partner_hol_ready = {", "\tcountry_exists = HOL", "\tNOT = { has_war_with = HOL }", "\tdate < 2004.1.1",
          "\tOR = {", "\t\thas_completed_focus = TAI_pl_europe", "\t\thas_completed_focus = TAI_ss_dutch_litho", "\t}",
          "\tHOL = { has_opinion = { target = TAI value > 19 } }", "\t" + req("TAI_us_confidence", 59),
          "\t" + req("TAI_military_confidence", 44), "\tOBT_strait_below_crisis = yes", "}", "",
          "OBT_sub_partner_ger_ready = {", "\tcountry_exists = GER", "\tNOT = { has_war_with = GER }", "\thas_completed_focus = TAI_ss_court_berlin",
          "\tGER = { has_opinion = { target = TAI value > 39 } }", "\t" + req("TAI_us_confidence", 64),
          "\t" + req("TAI_military_confidence", 49), "\tOBT_strait_below_friction = yes", "}", ""]
    L("OBT_proc_has_port_tt", "Taiwan controls a §Ynaval base§!")
    L("OBT_proc_channel_open_tt", "The American supply channel is open (no procurement hold)")
    L("OBT_strait_below_friction_tt", "Cross-Strait Tension is below §Y40§! (Calm or Friction)")
    L("OBT_strait_below_crisis_tt", "Cross-Strait Tension is below §Y60§! (no Crisis)")
    L("OBT_strait_below_brink_tt", "Cross-Strait Tension is below §Y80§! (no Brink)")
    return "\n".join(T) + "\n"


REQ_NAMES = {"TAI_us_confidence": "U.S. Confidence in Taipei", "TAI_military_confidence": "Military Confidence", "TAI_reform_capacity": "Reform Capacity",
             "TAI_national_coordination": "National Coordination", "TAI_semiconductor_security": "Semiconductor Security", "CHI_taiwan_us_support": "U.S. Support"}
REQ_DONE = set()


def req(var, more_than, owner=None):
    """Requirement with a readable tooltip: var > more_than (shown as at least more_than + 1)."""
    key = f"OBT_req_{var}_{more_than + 1}"
    if key not in REQ_DONE:
        REQ_DONE.add(key)
        L(key, f"{REQ_NAMES[var]} is at least §Y{more_than + 1}§!")
    inner = f"check_variable = {{ {var} > {more_than} }}"
    if owner:
        inner = f"{owner} = {{ {inner} }}"
    return f"custom_trigger_tooltip = {{ tooltip = {key} {inner} }}"


# ---------------------------------------------------------------- decisions
DEC = []


def D(key, name, desc, icon, visible, available, cost, eff, ai, days_re=None, days_remove=None, remove=None, extra=()):
    d = [f"\t{key} = {{", f"\t\ticon = {icon}", "", "\t\tvisible = {"] + ind(visible, 3) + ["\t\t}", ""]
    if available:
        d += ["\t\tavailable = {"] + ind(available, 3) + ["\t\t}", ""]
    d += [f"\t\tcost = {cost}"]
    if days_re:
        d.append(f"\t\tdays_re_enable = {days_re}")
    if days_remove:
        d.append(f"\t\tdays_remove = {days_remove}")
    d += list(extra)
    d += ["", "\t\tcomplete_effect = {", f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision {key}"'] + ind(eff, 3) + ["\t\t}"]
    if remove:
        d += ["", "\t\tremove_effect = {", f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision {key} resolved"'] + ind(remove, 3) + ["\t\t}"]
    d += ["", "\t\tai_will_do = {"] + ind(ai, 3) + ["\t\t}", "\t}", ""]
    DEC.append("\n".join(d))
    L(key, name)
    L(key + "_desc", desc)


BANKRUPT = ["modifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }"]
HIST = ["modifier = { factor = 0 is_historical_focus_on = yes }"]


def tt(key, text):
    L(key, text)
    return f"custom_effect_tooltip = {key}"


def decisions():
    # --- funding
    D("OBT_fund_kidd_transfer", "Fund the Kidd Transfer",
      "The Legislative Yuan stalled the special budget. A narrower bill covering only the Kidd-class destroyers may pass where the full package failed.",
      "generic_fundraising",
      ["has_country_flag = OBT_budget_vote_held", "NOT = { has_country_flag = OBT_budget_kidd }", stage_is("kidd", 1)],
      ["TAI_can_pass_legislation = yes", "OBT_treasury_2 = yes"], 50,
      money(-2) + ["set_country_flag = OBT_budget_kidd", tt("OBT_fund_kidd_tt", "Funds the §YKidd-class destroyers§!.")] + addvar("TAI_us_confidence", 2),
      ["base = 10"] + BANKRUPT, days_re=180)
    D("OBT_fund_full_package", "Pass the Remaining Special Budget",
      "The rest of the 2001 package, the patrol aircraft and the submarines, still waits for money. Historically the Legislative Yuan blocked it from 2004 to 2007.",
      "generic_fundraising",
      ["has_country_flag = OBT_budget_vote_held", "NOT = { has_country_flag = OBT_budget_full }"],
      ["TAI_can_pass_legislation = yes", "OBT_treasury_3 = yes"], 75,
      money(-3) + ["set_country_flag = OBT_budget_kidd", "set_country_flag = OBT_budget_full",
                   tt("OBT_fund_full_tt", "Funds the §YP-3C patrol aircraft§! and design work on the §Ydiesel submarines§!.")] + addvar("TAI_us_confidence", 3),
      ["base = 8", "modifier = { factor = 2 has_country_flag = OBT_budget_kidd }"] + BANKRUPT, days_re=365)
    # --- acceleration
    D("OBT_expedite_kidd", "Expedite the Kidd Refit",
      "Paying for extra shifts in the Charleston yard and sending crews early can bring the destroyers home sooner.",
      "generic_naval",
      [stage_is("kidd", 3, 4), "NOT = { has_country_flag = OBT_pk_expedited }"],
      ["OBT_proc_channel_open = yes", req("TAI_us_confidence", 54), req("TAI_military_confidence", 44), "OBT_treasury_1 = yes"], 50,
      money(-1) + ["set_country_flag = OBT_pk_expedited", "multiply_variable = { OBT_pk_days = 0.6 }", "OBT_proc_months = yes",
                   tt("OBT_expedite_kidd_tt", "The remaining refit time is cut by §G40%§!.")],
      ["base = 3", "modifier = { factor = 0 NOT = { OBT_treasury_4 = yes } }"] + BANKRUPT)
    D("OBT_p3c_priority", "Negotiate Priority Delivery",
      "If Washington will move Taiwan up the queue at Lockheed's refurbishment line, the patrol aircraft could arrive years earlier. It will cost money and goodwill.",
      "generic_air",
      [stage_is("p3c", 3, 4), "NOT = { has_country_flag = OBT_pp_priority }"],
      ["OBT_proc_channel_open = yes", req("TAI_us_confidence", 64), req("CHI_taiwan_us_support", 59, "CHI"), "OBT_treasury_2 = yes"], 75,
      money(-2) + ["set_country_flag = OBT_pp_priority", "multiply_variable = { OBT_pp_days = 0.5 }", "OBT_proc_months = yes",
                   tt("OBT_p3c_priority_tt", "The current contract or refurbishment stage is cut by §G50%§!.")],
      ["base = 3", "modifier = { factor = 0 NOT = { OBT_treasury_5 = yes } }"] + BANKRUPT)
    D("OBT_p3c_second_line", "Fund a Second Refurbishment Line",
      "A second line would refurbish airframes in parallel, if our own maintenance crews are ready to take them.",
      "generic_air",
      [stage_is("p3c", 4, 5), "NOT = { has_country_flag = OBT_pp_second_line }"],
      ["OBT_proc_channel_open = yes", req("TAI_reform_capacity", 54), "OBT_treasury_2 = yes"], 50,
      money(-2) + ["set_country_flag = OBT_pp_second_line", "multiply_variable = { OBT_pp_days = 0.75 }", "OBT_proc_months = yes",
                   tt("OBT_p3c_second_line_tt", "The current stage is cut by §G25%§! and later batches arrive every §G9§! months instead of 18.")],
      ["base = 2", "modifier = { factor = 0 NOT = { OBT_treasury_5 = yes } }"] + BANKRUPT)
    # --- submarine route
    talks = [("usa", 1, "Ask Washington to Reopen a Diesel Line",
              "No American yard has built a diesel submarine since the 1950s. A new line is possible only if Washington trusts us completely and is willing to spend its own political capital.",
              "OBT_sub_partner_usa_ready"),
             ("hol", 2, "Approach the Hai Lung Builders",
              "Rotterdam's RDM built our two Hai Lung boats in the 1980s. The yard is struggling and could build an improved design, if The Hague accepts Beijing's anger before RDM closes in 2004.",
              "OBT_sub_partner_hol_ready"),
             ("ger", 3, "Negotiate a German License",
              "Germany's HDW designs the world's best-selling diesel submarines. Berlin has always refused Taipei. Only close relations and a calm Strait could change that.",
              "OBT_sub_partner_ger_ready")]
    for key, pid, name, desc, trig in talks:
        D(f"OBT_sub_talks_{key}", name, desc + " Talks take 180 days. If the conditions still hold when they end, the contract is signed. If not, the talks fail.",
          "generic_naval",
          [stage_is("sub", 3)],
          ["NOT = { has_country_flag = OBT_ps_negotiating }", f"NOT = {{ has_country_flag = OBT_ps_talks_failed_{key} }}", trig + " = yes"], 100,
          ["set_country_flag = OBT_ps_negotiating", tt(f"OBT_sub_talks_{key}_tt", "Talks begin. They succeed only if every condition above still holds in §Y180§! days.")],
          ["base = 5", "modifier = { factor = 3 date > 2006.1.1 }"] + HIST, days_remove=180,
          remove=["clr_country_flag = OBT_ps_negotiating", "if = {", f"\tlimit = {{ {trig} = yes {stage_is('sub', 3)} }}",
                  f"\tset_variable = {{ OBT_ps_partner = {pid} }}"] + ind(set_stage("sub", 4), 1) + ["\tcountry_event = { id = obt_proc.22 days = 1 }", "}",
                  "else_if = {", f"\tlimit = {{ {stage_is('sub', 3)} }}", f"\tset_country_flag = {{ flag = OBT_ps_talks_failed_{key} days = 365 value = 1 }}",
                  f"\tset_variable = {{ OBT_ps_failed_partner = {pid} }}", "\tcountry_event = { id = obt_proc.23 days = 1 }", "}"])
    D("OBT_sub_appropriation", "Appropriate the Submarine Construction Funds",
      "A builder is ready, but construction needs its own appropriation, the largest single defense bill in our history, and a navy ready to crew eight new boats.",
      "generic_fundraising",
      [stage_is("sub", 4)],
      ["TAI_can_pass_legislation = yes", req("TAI_military_confidence", 49), "OBT_proc_has_port = yes", "OBT_treasury_4 = yes"], 100,
      money(-4) + set_stage("sub", 5, 2190) + ["OBT_proc_months = yes"] + addvar("TAI_us_confidence", 3) + tension(4) +
      [tt("OBT_sub_appropriation_tt", "Construction begins. The first pair is due in about §Y6 years§!, then a pair every year.")],
      ["base = 10"] + BANKRUPT)
    D("OBT_sub_second_line", "Open a Second Building Slip",
      "A second slip would halve the gap between pairs, if our engineers can supervise two hulls at once.",
      "generic_naval",
      [stage_is("sub", 5, 6), "NOT = { has_country_flag = OBT_ps_second_line }"],
      ["OBT_proc_channel_open = yes", req("TAI_reform_capacity", 59), req("TAI_military_confidence", 54), "OBT_treasury_3 = yes"], 100,
      money(-3) + ["set_country_flag = OBT_ps_second_line", "multiply_variable = { OBT_ps_days = 0.75 }", "OBT_proc_months = yes",
                   tt("OBT_sub_second_line_tt", "The current stage is cut by §G25%§! and later pairs arrive every §G6§! months instead of 12.")],
      ["base = 2", "modifier = { factor = 0 NOT = { OBT_treasury_6 = yes } }"] + BANKRUPT)
    D("OBT_fund_aegis", "Fund the Aegis Destroyers",
      "Washington agreed to sell Aegis destroyers. They would be the most capable warships in the region outside the U.S. and Japanese navies, built new, and very expensive.",
      "generic_naval",
      [stage_is("aegis", 1)],
      ["TAI_can_pass_legislation = yes", req("TAI_us_confidence", 59), "OBT_treasury_5 = yes"], 100,
      money(-5) + set_stage("aegis", 2, 2555) + ["OBT_proc_months = yes"] + tension(5) +
      [tt("OBT_fund_aegis_tt", "Construction begins. The first pair is due in about §Y7 years§!, the second a year later.")],
      ["base = 5", "modifier = { factor = 0 NOT = { OBT_treasury_6 = yes } }"] + BANKRUPT + HIST)
    # --- cancellations
    for p, stages, label in (("kidd", (1, 2, 3, 4), "Kidd Transfer"), ("p3c", (1, 2, 3, 4, 5), "P-3C Purchase"),
                             ("sub", (1, 2, 3, 4, 5, 6), "Submarine Program"), ("aegis", (1, 2, 3), "Aegis Purchase")):
        D(f"OBT_cancel_{p}", f"Cancel the {label}",
          "Money already spent is not returned. Washington will remember the cancellation, and anything already delivered stays in service.",
          "generic_break_treaty", [stage_is(p, *stages)], ["NOT = { has_country_flag = OBT_ps_negotiating }"] if p == "sub" else [], 25,
          set_stage(p, 99) + addvar("TAI_us_confidence", -5) + addvar("TAI_military_confidence", -2),
          ["base = 0", "modifier = { add = 5 has_active_mission = bankruptcy_incoming_collapse }"])
    # --- reform and U.S. decisions
    D("OBT_han_kuang", "Hold the Han Kuang Exercise",
      "Our annual joint exercise tests whether the services can defend the island together. Holding it seriously, rather than as a scripted show, builds real confidence.",
      "generic_army_support", ["always = yes"], ["OBT_treasury_1 = yes"], 50,
      money(-0.5) + addvar("TAI_military_confidence", 4) + addvar("TAI_national_coordination", 1) + ["army_experience = 10", "add_war_support = 0.05"] + tension(1),
      ["base = 3", "modifier = { factor = 3 check_variable = { TAI_military_confidence < 50 } }"] + BANKRUPT, days_re=365)
    D("OBT_joint_drill", "Joint Operations Drill",
      "The army, navy and air force still plan separately. A joint command drill exposes the gaps before a crisis does.",
      "generic_army_support", ["always = yes"], [req("TAI_reform_capacity", 39)], 50,
      addvar("TAI_reform_capacity", 3) + addvar("TAI_national_coordination", 2),
      ["base = 2", "modifier = { factor = 2 check_variable = { TAI_reform_capacity < 50 } }"], days_re=240)
    D("OBT_pentagon_assessment", "Host a Pentagon Assessment Team",
      "American assessors will tell us candidly what does not work. Their report will embarrass some commanders, and it will reassure Washington that we take defense seriously.",
      "generic_political_discourse", ["country_exists = USA", "NOT = { has_war_with = USA }"], ["OBT_proc_channel_open = yes"], 50,
      addvar("TAI_us_confidence", 4) + addvar("TAI_reform_capacity", 2) + addvar("TAI_military_confidence", -2),
      ["base = 2", "modifier = { factor = 3 check_variable = { TAI_us_confidence < 55 } }"], days_re=365)
    D("OBT_civil_defense_review", "Civil Defense Coordination Review",
      "City governments, ministries and the armed forces rehearse who does what when the power, ports or networks fail.",
      "generic_civil_support", ["always = yes"], [], 35,
      addvar("TAI_national_coordination", 3),
      ["base = 2", "modifier = { factor = 2 check_variable = { TAI_national_coordination < 40 } }"], days_re=180)
    D("OBT_supply_chain_review", "Semiconductor Supply-Chain Review",
      "A review of materials, tools and energy for the fabs shows where a single supplier, often on the mainland, could stop production.",
      "generic_factory", ["always = yes"], [], 50,
      addvar("TAI_semiconductor_security", 3) + addvar("TAI_mainland_dependence", -2),
      ["base = 2", "modifier = { factor = 2 check_variable = { TAI_semiconductor_security < 80 } }"], days_re=365)
    return "OBT_defense_reform_category = {\n" + "\n".join(DEC) + "}\n"


# ---------------------------------------------------------------- events
EV = []


def EVT(n, title, desc, pic, opts, trig=(), once=False):
    eid = f"obt_proc.{n}"
    out = ["country_event = {", f"\tid = {eid}", f"\ttitle = {eid}.t"]
    L(f"{eid}.t", title)
    if isinstance(desc, str):
        out.append(f"\tdesc = {eid}.d")
        L(f"{eid}.d", desc)
    else:
        for suf, trg, text in desc:
            out.append(f"\tdesc = {{ text = {eid}.d_{suf} trigger = {{ {trg} }} }}")
            L(f"{eid}.d_{suf}", text)
    out += [f"\tpicture = {pic}", "\tis_triggered_only = yes"] + (["\tfire_only_once = yes"] if once else [])
    out += ["", "\ttrigger = {", "\t\toriginal_tag = TAI"] + ["\t\t" + t for t in trig] + ["\t}", ""]
    for i, (text, eff, ai) in enumerate(opts):
        key = f"{eid}.{'abce'[i]}"
        L(key, text)
        out += ["\toption = {", f"\t\tname = {key}", f'\t\tlog = "[GetDateText]: [This.GetName]: {key} executed"'] + ind(eff, 2) + \
               ["\t\tai_chance = {"] + ind(ai, 3) + ["\t\t}", "\t}", ""]
    out[-1] = "}"
    EV.append("\n".join(out) + "\n")


def events():
    L("obt_proc.21", "No One Will Build Them")
    L("OBT_ps_negotiating", "Submarine talks are under way")
    for k, n in (("usa", "Washington"), ("hol", "the Netherlands"), ("ger", "Germany")):
        L(f"OBT_ps_talks_failed_{k}", f"Talks with {n} failed less than a year ago")
    EVT(1, "The Keelung and the Su Ao", "The first two Kidd-class destroyers have arrived from Charleston as ROCS Keelung and ROCS Su Ao. Their area air defense is unmatched in our navy, and so are their maintenance needs.",
        "GFX_submarine", [("Commission them.", addvar("TAI_military_confidence", 2), ["base = 1"])])
    EVT(2, "The Kidd-Class Destroyers Complete", "ROCS Tso Ying and ROCS Ma Kong have joined their sister ships. The crews will need several months of training before the four destroyers are fully ready.",
        "GFX_submarine", [("Begin working up.", ["navy_experience = 10"], ["base = 1"])])
    EVT(10, "The P-3C Contract", "Washington and Lockheed have agreed to refurbish twelve P-3C Orion aircraft from storage for us. The airframes need years of work before they fly again.",
        "GFX_politics_negotiations", [("Good. Train the crews now.", addvar("TAI_reform_capacity", 1), ["base = 1"])])
    EVT(11, "Orions Arrive", "Another four refurbished P-3C Orions have landed at Pingtung. Submarine hunting in the Strait is becoming a real capability.",
        "GFX_submarine", [("Assign them to the patrol squadron.", ["air_experience = 5"], ["base = 1"])])
    EVT(12, "The Last Orions", "All twelve P-3C Orions have been delivered. The new squadron needs a few months to reach full readiness.",
        "GFX_submarine", [("Begin training.", ["air_experience = 10"], ["base = 1"])])
    EVT(20, "Seeking a Submarine Builder",
        "The submarines are funded for design work, but no American yard builds diesel boats and European builders fear Beijing. Unless we find a builder before 1 January 2009, the foreign program will be over. Each option has its own conditions in the Defense and National Reform tab.",
        "GFX_submarine", [("Open the talks.", addvar("TAI_reform_capacity", 1), ["base = 1"])], once=True)
    EVT(21, "No One Will Build Them",
        "Eight years after Washington approved the submarines, no shipyard has agreed to build them. If Taiwan wants submarines, it will have to learn to build them itself.",
        "GFX_submarine",
        [("Build our own.", ["add_tech_bonus = { name = obt_proc.21 bonus = 0.5 uses = 2 category = CAT_submarines }"] + addvar("TAI_reform_capacity", 3) +
          [tt("OBT_sub_indigenous_tt", "The §YIndigenous Submarine Program§! focus is the way forward.")], ["base = 1"])], once=True)
    EVT(22, "A Builder Is Found",
        [("usa", "check_variable = { OBT_ps_partner = 1 }", "Washington has agreed to have an American yard build a new diesel design for us. It is an extraordinary sign of trust."),
         ("hol", "check_variable = { OBT_ps_partner = 2 }", "The Netherlands has agreed to let RDM build an improved Hai Lung design for us, despite protests from Beijing."),
         ("ger", "check_variable = { OBT_ps_partner = 3 }", "Berlin has approved a license for a Type 209 design built with German help, despite protests from Beijing.")],
        "GFX_submarine", [("Prepare the appropriation.", addvar("TAI_us_confidence", 2) + tension(5), ["base = 1"])], once=True)
    EVT(23, "Submarine Talks Fail",
        [("usa", "check_variable = { OBT_ps_failed_partner = 1 }", "Washington has decided not to reopen a diesel submarine line. Our standing in Washington, America's commitment or our readiness fell short when it mattered."),
         ("hol", "check_variable = { OBT_ps_failed_partner = 2 }", "The Dutch government has withdrawn RDM's export license. The Strait looked too dangerous, or our partnership too thin, for The Hague to accept Beijing's anger."),
         ("ger", "check_variable = { OBT_ps_failed_partner = 3 }", "Berlin has turned us down again. Without a calmer Strait and closer relations, it will not risk its trade with China.")],
        "GFX_submarine", [("We can try again in a year.", addvar("TAI_military_confidence", -1), ["base = 1"])])
    EVT(24, "Two Submarines Commissioned", "Another pair of new submarines has been commissioned into the fleet.",
        "GFX_submarine", [("Welcome them.", ["navy_experience = 5"], ["base = 1"])])
    EVT(25, "The Submarine Fleet Complete", "All eight submarines have been commissioned. Their crews need months of training before they are ready for war patrols.",
        "GFX_submarine", [("Begin working up.", ["navy_experience = 10"], ["base = 1"])], once=True)
    EVT(30, "Aegis Destroyers Arrive", "A pair of new Aegis destroyers has arrived. Beijing calls their delivery a grave provocation.",
        "GFX_submarine", [("Commission them.", addvar("TAI_military_confidence", 2), ["base = 1"])])
    return "add_namespace = obt_proc\n\n" + "\n".join(EV)


# ---------------------------------------------------------------- scripted localisation
def scripted_loc():
    S = []
    for p, rows in STATUS.items():
        v = PROJ[p][0]
        S += ["defined_text = {", f"\tname = OBT_proc_{p}_status"]
        for n, text in rows:
            key = f"OBT_proc_{p}_s{n}"
            L(key, text)
            S += ["\ttext = {", f"\t\ttrigger = {{ check_variable = {{ {v}_stage = {n} }} }}", f"\t\tlocalization_key = {key}", "\t}"]
        S += ["}", ""]
    S += ["defined_text = {", "\tname = OBT_sub_partner_name"]
    for pid, key, text in ((1, "OBT_partner_usa", "an American yard"), (2, "OBT_partner_hol", "RDM, Netherlands"), (3, "OBT_partner_ger", "HDW license, Germany")):
        L(key, text)
        S += ["\ttext = {", f"\t\ttrigger = {{ check_variable = {{ OBT_ps_partner = {pid} }} }}", f"\t\tlocalization_key = {key}", "\t}"]
    S += ["\ttext = {", "\t\tlocalization_key = OBT_partner_none", "\t}", "}", ""]
    L("OBT_partner_none", "no builder")
    S += ["defined_text = {", "\tname = OBT_proc_hold_note"]
    for n, key, text in ((1, "OBT_hold_1", " §R(Suspended: Washington has withdrawn support)§!"), (2, "OBT_hold_2", " §R(Suspended: at war with the United States)§!"),
                         (3, "OBT_hold_3", " §R(Suspended: the Strait is closed by war)§!")):
        L(key, text)
        S += ["\ttext = {", f"\t\ttrigger = {{ check_variable = {{ OBT_proc_hold = {n} }} }}", f"\t\tlocalization_key = {key}", "\t}"]
    S += ["\ttext = {", "\t\tlocalization_key = OBT_hold_0", "\t}", "}", ""]
    L("OBT_hold_0", "")
    return "\n".join(S)


# ---------------------------------------------------------------- GUI
COLS = [8, 153, 298]
ROWS = [("OBT_dash_row_military", "MILITARY REFORM", ["milconf", "reform", "coord"]),
        ("OBT_dash_row_us", "WASHINGTON AND THE STRAIT", ["usconf", "ussupport", "ptn"]),
        ("OBT_dash_row_home", "HOME FRONT", ["identity", "dep", "chips"])]
BY = {i[0]: i for i in INDICATORS}


def gui():
    g = ["guiTypes = {", "\tcontainerWindowType = {", "\t\tname = \"OBT_TAI_defense_dashboard_window\"", "\t\tsize = { width = 440 height = 300 }", "\t\tposition = { x = 0 y = 0 }", ""]

    def text(name, x, y, key, width, font="hoi_16mbs", tip=None, fmt="left"):
        t = ["\t\tinstantTextBoxType = {", f'\t\t\tname = "{name}"', f"\t\t\tposition = {{ x = {x} y = {y} }}", f'\t\t\tfont = "{font}"', f'\t\t\ttext = "{key}"',
             f"\t\t\tmaxWidth = {width}", "\t\t\tmaxHeight = 20", f"\t\t\tformat = {fmt}"]
        if tip:
            t.append(f'\t\t\tpdx_tooltip = "{tip}"')
        return t + ["\t\t}"]
    g += text("OBT_dash_title", 8, 0, "OBT_dash_title", 430, "hoi_20bs", "OBT_dash_title_tt")
    y = 26
    for rk, rtitle, keys in ROWS:
        g += text(rk, 8, y, rk, 430)
        L(rk, f"§Y{rtitle}§!")
        for col, k in zip(COLS, keys):
            g += text(f"OBT_dash_{k}_label", col, y + 18, f"OBT_dash_{k}_label", 140, tip=f"OBT_dash_{k}_tt")
            sprite = "GFX_OBT_ind_bar_neg" if BY[k][6] else "GFX_OBT_ind_bar"
            g += ["\t\ticonType = {", f'\t\t\tname = "OBT_dash_{k}_bar"', f'\t\t\tquadTextureSprite = "{sprite}"', f"\t\t\tposition = {{ x = {col} y = {y + 38} }}",
                  f'\t\t\tpdx_tooltip = "OBT_dash_{k}_tt"', "\t\t}"]
        y += 56
    g += text("OBT_dash_proc_title", 8, y, "OBT_dash_proc_title", 430, tip="OBT_dash_proc_tt")
    L("OBT_dash_proc_title", "§YU.S. ARMS PROCUREMENT§![OBT_proc_hold_note]")
    y += 20
    for p in ("kidd", "p3c", "sub", "aegis"):
        g += text(f"OBT_dash_proc_{p}", 8, y, f"OBT_dash_proc_{p}", 430, tip=f"OBT_dash_proc_{p}_tt")
        y += 19
    g += ["\t}", "}"]
    assert y <= 300, y
    return "\n".join(g) + "\n"


def gfx():
    return """spriteTypes = {
	progressbartype = {
		name = "GFX_OBT_ind_bar"
		texturefile1 = "gfx/interface/scripted_gui/countries/TAI/obt_ind_fill.dds"
		texturefile2 = "gfx/interface/scripted_gui/countries/TAI/obt_ind_empty.dds"
		size = { x = 136 y = 10 }
		effectfile = "gfx/FX/progress.lua"
	}
	progressbartype = {
		name = "GFX_OBT_ind_bar_neg"
		texturefile1 = "gfx/interface/scripted_gui/countries/TAI/obt_ind_fill_neg.dds"
		texturefile2 = "gfx/interface/scripted_gui/countries/TAI/obt_ind_empty.dds"
		size = { x = 136 y = 10 }
		effectfile = "gfx/FX/progress.lua"
	}
}
"""


def sgui():
    props = []
    for i in INDICATORS:
        props.append(f"\t\t\tOBT_dash_{i[0]}_bar = {{ frame = {i[2]}.{i[1]} }}")
    return ("scripted_gui = {\n\tOBT_TAI_defense_dashboard = {\n\t\twindow_name = \"OBT_TAI_defense_dashboard_window\"\n\t\tcontext_type = decision_category\n\n"
            "\t\tproperties = {\n" + "\n".join(props) + "\n\t\t}\n\t}\n}\n")


def dashboard_loc():
    L("OBT_defense_reform_category", "Defense and National Reform")
    L("OBT_defense_reform_category_desc", "Taiwan's reform, military, economic and diplomatic indicators, and the progress of American arms purchases. Hover over any indicator to see what it does and how to raise it.")
    L("OBT_dash_title", "DEFENSE AND NATIONAL REFORM")
    L("OBT_dash_title_tt", "Each indicator runs from 0 to 100. Effects are measured from Taiwan's 2000 starting value, so a stat that has not moved has no effect.")
    for key, var, owner, short, full, start, neg, effs, desc, raise_ in INDICATORS:
        L(f"OBT_dash_{key}_label", f"{short}: §Y[?{owner}.{var}|0]§!")
        lines = [f"§Y{full}§!: [?{owner}.{var}|0] / 100", "", desc, ""]
        if effs:
            lines.append(f"§YEffects§! (measured from the starting value of {start}):")
            for v, _m, k, lbl in effs:
                lines.append(f"  {lbl}: [?TAI.{v}_p|+=1]% (changes by {abs(k) * 100:g}% per point)")
        else:
            lines.append(EXTRA_EFFECT_TEXT[key])
        if key == "usconf":
            lines += ["", "U.S. Confidence is how Washington sees §YTaipei§!. U.S. Support is how committed §YWashington§! is. They move separately."]
        if key == "ussupport":
            lines += ["", "U.S. Support is Washington's own commitment. U.S. Confidence is how Washington sees Taipei. They move separately."]
        lines += ["", f"§YHow to change it:§! {raise_}"]
        L(f"OBT_dash_{key}_tt", "\\n".join(lines))
    L("OBT_dash_proc_tt", "Procurement has separate steps: §YWashington approves§!, the §YLegislative Yuan funds§!, a §Ycontract or refit§! runs, the equipment is §Ydelivered§!, and the crews §Ywork up§! before it counts as in service.\\n\\nTimers stop while the program is suspended: if Washington withdraws support, if Taiwan is at war with the United States, or if Taiwan is at war with China while the United States is not. Ships also need a naval base to arrive.")
    tips = {
        "kidd": "§YKidd-class destroyers (4)§!: approved in April 2001 and refitted in Charleston. Historically the first pair, Keelung and Su Ao, arrived in December 2005 and the second, Tso Ying and Ma Kong, in November 2006.\\n\\nFunded by a trimmed or full special budget. The refit starts when §YAccept the Kidd-Class Destroyers§! is complete: about 31 months to the first pair, 11 more to the second, then 6 months of working up.\\n\\n§YExpedite the Kidd Refit§! cuts the remaining refit time by 40%.",
        "p3c": "§YP-3C Orion patrol aircraft (12)§!: approved in 2001, funded only in 2007, contracted in 2009 and delivered from 2013.\\n\\nNeeds a full special budget and §YMaritime Patrol Aircraft§!. Then about 20 months of contract talks, 50 months of refurbishment, and batches of 4 every 18 months.\\n\\n§YNegotiate Priority Delivery§! and §YFund a Second Refurbishment Line§! can each speed this up.",
        "sub": "§YDiesel-electric submarines (8)§!: approved in 2001, but no shipyard ever agreed to build them.\\n\\nNeeds a full special budget and §YThe Submarine Question§!. Then Taiwan must secure a construction partner before 1 January 2009. Each partner has strict conditions; talks take 180 days and succeed only if the conditions still hold. A partner is followed by a construction appropriation, about 6 years to the first pair, and a pair a year after that.\\n\\nWithout a partner the program fails, as it did historically, and Taiwan turns to the Indigenous Submarine Program.",
        "aegis": "§YAegis destroyers (4)§!: alternate history. Only available if Washington approved Aegis in April 2001. New construction takes about 7 years to the first pair, and each delivery raises Cross-Strait Tension.",
    }
    for p, (v, name, total) in PROJ.items():
        L(f"OBT_dash_proc_{p}", f"{name}: [OBT_proc_{p}_status]")
        L(f"OBT_dash_proc_{p}_tt", tips[p])
    L("OBT_TAI_national_indicators", "National Indicators")
    L("OBT_budget_full_tt", "Funds the §YKidd destroyers§!, the §YP-3C patrol aircraft§! and design work on the §Ydiesel submarines§!.")
    L("OBT_budget_trim_tt", "Funds the §YKidd destroyers§! only. The rest of the package waits for another vote.")
    L("OBT_budget_stall_tt", "Funds nothing. The package can be resubmitted from the §YDefense and National Reform§! tab.")


def categories():
    return """# Operation Blue Tiger milestone 9: Defense and National Reform
OBT_defense_reform_category = {
	allowed = { original_tag = TAI }
	icon = GFX_decision_generic_taiwan
	scripted_gui = OBT_TAI_defense_dashboard
	priority = 590
	visible_when_empty = yes
}
"""


def on_actions():
    return """# Operation Blue Tiger milestone 9: indicators and procurement
on_actions = {
	on_monthly_TAI = {
		effect = {
			OBT_dash_update = yes
			OBT_proc_update = yes
		}
	}
	on_startup = {
		effect = {
			if = {
				limit = { country_exists = TAI }
				TAI = { OBT_dash_update = yes }
			}
		}
	}
}
"""


def textures():
    from PIL import Image
    d = os.path.join(OUT, "gfx")
    os.makedirs(d, exist_ok=True)

    def bar(path, top, bottom, edge=None):
        im = Image.new("RGBA", (136, 10))
        for y in range(10):
            t = y / 9
            c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
            for x in range(136):
                im.putpixel((x, y), c)
        if edge:
            for x in range(136):
                im.putpixel((x, 0), edge)
                im.putpixel((x, 9), edge)
            for y in range(10):
                im.putpixel((0, y), edge)
                im.putpixel((135, y), edge)
        im.save(os.path.join(d, path))
    bar("obt_ind_fill.dds", (98, 160, 230), (34, 88, 160))
    bar("obt_ind_fill_neg.dds", (236, 170, 80), (170, 96, 30))
    bar("obt_ind_empty.dds", (40, 44, 52), (26, 28, 34), (70, 74, 84, 255))


def main():
    dashboard_loc()
    w("common/scripted_effects/99_OBT_defense_scripted_effects.txt", effects())
    w("common/scripted_triggers/99_OBT_defense_scripted_triggers.txt", triggers())
    w("common/decisions/OBT_defense_decisions.txt", decisions())
    w("common/decisions/categories/99_OBT_defense_categories.txt", categories())
    w("common/dynamic_modifiers/99_OBT_defense_dynamic_modifiers.txt", dynmod())
    w("common/on_actions/99_OBT_defense_on_actions.txt", on_actions())
    w("common/scripted_guis/99_OBT_defense_scripted_guis.txt", sgui())
    w("common/scripted_localisation/99_OBT_defense_scripted_localisation.txt", scripted_loc())
    w("interface/OBT_defense_dashboard.gui", gui())
    w("interface/OBT_defense_dashboard.gfx", gfx())
    w("events/OBT_procurement_events.txt", events())
    textures()
    w("localisation/english/MD_OBT_defense_l_english.yml",
      "l_english:\n # Operation Blue Tiger milestone 9: Defense and National Reform\n" + "\n".join(LOC) + "\n", bom=True)
    keys = [l.split(":")[0].strip() for l in LOC]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, dup
    print(len(DEC), "decisions,", len(EV), "events,", len(LOC), "loc keys")


main()
