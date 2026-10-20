#!/usr/bin/env python3
"""Write the Silicon Island support files: scripted effects, deferred-plant decisions, localisation.

Usage: python3 -B build_silicon.py <out_dir>
"""
import os
import sys

OUT = sys.argv[1]
SITES = [  # (suffix, state id, display name)
    ("hsinchu", 1155, "Hsinchu"),
    ("taichung", 1156, "Taichung"),
    ("tainan", 1157, "Tainan"),
]
PAY = "\t\tset_temp_variable = { treasury_change = -10.5 }\n\t\tmodify_treasury_effect = yes\n"
BUILD = "add_building_construction = { type = microchip_plant level = 1 instant_build = yes }"


def can_build(state=None):
    s = ["\t\t\tTAI_can_build_microchip_plant = yes"]
    if state:
        s.append(f"\t\t\t{state} = {{ is_controlled_by = ROOT }}")
    else:
        s.append("\t\t\tany_controlled_state = { free_shared_building_slots = yes }")
    return "\n".join(s)


effects = ["# Operation Blue Tiger: Silicon Island microchip plants",
           "# A plant is built at once if Taiwan can staff and power it and is not under a full blockade;",
           "# otherwise it is deferred and a decision in the Economic Policy category builds it later.", ""]
decisions = ["# Operation Blue Tiger: Silicon Island deferred microchip plants",
             "TAI_economy_decisions_category = {"]
loc = ["﻿l_english:"]

for suf, sid, name in SITES:
    flag = f"TAI_deferred_fab_{suf}"
    effects += [
        f"TAI_science_park_fab_{suf} = {{",
        "\tif = {",
        "\t\tlimit = {", can_build(sid), "\t\t}",
        f"\t\t{sid} = {{",
        "\t\t\tadd_extra_state_shared_building_slots = 1",
        f"\t\t\t{BUILD}",
        "\t\t}",
        PAY.rstrip("\n"),
        "\t}",
        "\telse = {",
        f"\t\tset_country_flag = {flag}",
        f"\t\tcustom_effect_tooltip = TAI_deferred_fab_{suf}_tt",
        "\t}",
        "}", ""]
    decisions += [
        f"\tTAI_build_deferred_fab_{suf} = {{",
        "\t\ticon = GFX_decision_microchips",
        f"\t\tvisible = {{ has_country_flag = {flag} }}", "",
        "\t\tavailable = {", can_build(sid), "\t\t}", "",
        "\t\tcost = 25", "",
        "\t\tcomplete_effect = {",
        f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision TAI_build_deferred_fab_{suf}"',
        f"\t\t\tclr_country_flag = {flag}",
        f"\t\t\tTAI_science_park_fab_{suf} = yes",
        "\t\t}", "",
        "\t\tai_will_do = {",
        "\t\t\tbase = 10",
        "\t\t\tmodifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }",
        "\t\t}",
        "\t}", ""]
    loc += [
        f' TAI_deferred_fab_{suf}_tt: "If we lack the workers or power for a new fab, or are under blockade, the §Y{name}§! plant is deferred: the decision §YBuild the {name} Fab§! becomes available."',
        f' TAI_build_deferred_fab_{suf}: "Build the {name} Fab"',
        f' TAI_build_deferred_fab_{suf}_desc: "The {name} microchip plant was postponed for lack of workers, power or supplies. With conditions improved, construction can begin."',
    ]

# any state with a free slot (Advanced Process R&D)
effects += [
    "TAI_science_park_fab_any = {",
    "\tif = {",
    "\t\tlimit = {", can_build(), "\t\t}",
    "\t\trandom_controlled_state = {",
    "\t\t\tlimit = { free_shared_building_slots = yes }",
    f"\t\t\t{BUILD}",
    "\t\t}",
    PAY.rstrip("\n"),
    "\t}",
    "\telse = {",
    "\t\tset_country_flag = TAI_deferred_fab_any",
    "\t\tcustom_effect_tooltip = TAI_deferred_fab_any_tt",
    "\t}",
    "}", ""]
decisions += [
    "\tTAI_build_deferred_fab_any = {",
    "\t\ticon = GFX_decision_microchips",
    "\t\tvisible = { has_country_flag = TAI_deferred_fab_any }", "",
    "\t\tavailable = {", can_build(), "\t\t}", "",
    "\t\tcost = 25", "",
    "\t\tcomplete_effect = {",
    '\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision TAI_build_deferred_fab_any"',
    "\t\t\tclr_country_flag = TAI_deferred_fab_any",
    "\t\t\tTAI_science_park_fab_any = yes",
    "\t\t}", "",
    "\t\tai_will_do = {",
    "\t\t\tbase = 10",
    "\t\t\tmodifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }",
    "\t\t}",
    "\t}",
    "}"]
loc += [
    ' TAI_deferred_fab_any_tt: "If we lack the workers, power or a free building slot for a new fab, or are under blockade, the plant is deferred: the decision §YBuild a New Fab§! becomes available."',
    ' TAI_build_deferred_fab_any: "Build a New Fab"',
    ' TAI_build_deferred_fab_any_desc: "A planned microchip plant was postponed. With workers, power and a site available, construction can begin."',
    ' TAI_can_build_microchip_plant_tt: "We can staff and power a new microchip plant and are not under a full blockade"',
]

triggers = """# Operation Blue Tiger: Silicon Island
# Workforce (Millennium Dawn's staffing check), energy and blockade conditions for a new microchip plant.
TAI_can_build_microchip_plant = {
\tcustom_trigger_tooltip = {
\t\ttooltip = TAI_can_build_microchip_plant_tt
\t\tcan_staff_an_microchip_plant = yes
\t\tNOT = { has_an_energy_deficit = yes }
\t\tNOT = {
\t\t\tany_country = {
\t\t\t\ttag = CHI
\t\t\t\thas_country_flag = CHI_TAI_full_blockade_active
\t\t\t}
\t\t}
\t}
}
"""


# Energy Security Review: two fossil-fuel power stations
POWER_SITES = [(1156, "Taichung"), (599, "Kaohsiung")]
power = ["", "# Energy Security Review: two fossil-fuel power stations, in Taichung and Kaohsiung where possible",
         "# (any state with room otherwise). Deferred to a decision if Taiwan lacks the workers.",
         "TAI_energy_review_power_stations = {", "\tif = {", "\t\tlimit = { TAI_can_staff_power_stations = yes }"]
for sid, _ in POWER_SITES:
    power += [
        "\t\tif = {",
        "\t\t\tlimit = {",
        f"\t\t\t\t{sid} = {{",
        "\t\t\t\t\tis_controlled_by = ROOT",
        "\t\t\t\t\tfree_building_slots = { building = fossil_powerplant size > 0 }",
        "\t\t\t\t}",
        "\t\t\t}",
        f"\t\t\t{sid} = {{ add_building_construction = {{ type = fossil_powerplant level = 1 instant_build = yes }} }}",
        "\t\t}",
        "\t\telse = {",
        "\t\t\trandom_controlled_state = {",
        "\t\t\t\tlimit = { fossil_powerplant_random_build_loc = yes }",
        "\t\t\t\tadd_building_construction = { type = fossil_powerplant level = 1 instant_build = yes }",
        "\t\t\t}",
        "\t\t}"]
power += [
    "\t\tset_temp_variable = { treasury_change = -6.5 }",
    "\t\tmodify_treasury_effect = yes",
    "\t}",
    "\telse = {",
    "\t\tset_country_flag = TAI_deferred_power_stations",
    "\t\tcustom_effect_tooltip = TAI_deferred_power_stations_tt",
    "\t}",
    "}", ""]
effects += power
decisions.insert(-1, "")
decisions[-1:-1] = [
    "\tTAI_build_deferred_power_stations = {",
    "\t\ticon = GFX_decision_generic_factory",
    "\t\tvisible = { has_country_flag = TAI_deferred_power_stations }",
    "\t\tavailable = { TAI_can_staff_power_stations = yes }",
    "\t\tcost = 25", "",
    "\t\tcomplete_effect = {",
    '\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision TAI_build_deferred_power_stations"',
    "\t\t\tclr_country_flag = TAI_deferred_power_stations",
    "\t\t\tTAI_energy_review_power_stations = yes",
    "\t\t}", "",
    "\t\tai_will_do = {",
    "\t\t\tbase = 10",
    "\t\t\tmodifier = { factor = 3 has_an_energy_deficit = yes }",
    "\t\t\tmodifier = { factor = 0 has_active_mission = bankruptcy_incoming_collapse }",
    "\t\t}",
    "\t}"]
loc += [
    ' TAI_deferred_power_stations_tt: "If we lack the workers to run them, the two power stations are deferred: the decision §YExpand the Power Stations§! becomes available."',
    ' TAI_build_deferred_power_stations: "Expand the Power Stations"',
    ' TAI_build_deferred_power_stations_desc: "New generating units at our coal- and gas-fired stations were postponed for lack of workers. With the labour available, construction can begin."',
    ' TAI_can_staff_power_stations_tt: "We have at least 15,000 unemployed workers to run two new power stations"',
]
triggers += """
# Two fossil-fuel power stations need about 15,000 workers (Millennium Dawn: 7,500 per plant).
TAI_can_staff_power_stations = {
\tcustom_trigger_tooltip = {
\t\ttooltip = TAI_can_staff_power_stations_tt
\t\tcheck_variable = { total_unemployed_k > 15 }
\t}
}
"""

FILES = {
    "common/scripted_effects/99_OBT_silicon_scripted_effects.txt": "\n".join(effects),
    "common/scripted_triggers/99_OBT_silicon_scripted_triggers.txt": triggers,
    "common/decisions/OBT_silicon_decisions.txt": "\n".join(decisions) + "\n",
    "localisation/english/MD_OBT_silicon_l_english.yml": "\n".join(loc) + "\n",
}
for rel, text in FILES.items():
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
print(f"silicon files: {len(FILES)}")
