#!/usr/bin/env python3
"""Apply the Silicon Island text edits (spirit modifiers and names) to existing files.

Exact, idempotent replacements: each edit is skipped if its new text is already present and the
script stops with an error if the old text is missing.

Usage: python3 -B apply_silicon_text.py <millennium_dawn_root> [<tools_dir>]
"""
import os
import sys

T = "\t"


def spirit(n, eff, res, extra):
    lines = [f"{T*2}TAI_ss_program_{n} = {{", f"{T*3}picture = {{PIC}}", f"{T*3}allowed_civil_war = {{ always = yes }}",
             f"{T*3}modifier = {{", f"{T*4}production_factory_efficiency_gain_factor = {eff}", f"{T*4}research_speed_factor = {res}"]
    lines += [f"{T*4}{k} = {v}" for k, v in extra]
    lines += [f"{T*3}}}", f"{T*2}}}"]
    return "\n".join(lines)


OLD_SPIRITS = "\n".join(spirit(n, e, r, []) for n, e, r in ((1, "0.03", "0.02"), (2, "0.05", "0.03"), (3, "0.08", "0.05"))).replace("{PIC}", "research_bonus")
NEW_SPIRITS = "\n".join(spirit(n, e, r, x) for n, e, r, x in (
    (1, "0.03", "0.02", [("production_speed_microchip_plant_factor", "0.10"), ("local_resources_microchips_factor", "0.05")]),
    (2, "0.05", "0.03", [("production_speed_microchip_plant_factor", "0.15"), ("local_resources_microchips_factor", "0.08"),
                         ("microchip_plant_productivity_modifier", "0.05"), ("microchip_export_multiplier_modifier", "0.05")]),
    (3, "0.08", "0.05", [("production_speed_microchip_plant_factor", "0.20"), ("local_resources_microchips_factor", "0.12"),
                         ("microchip_plant_productivity_modifier", "0.10"), ("microchip_export_multiplier_modifier", "0.08")]),
)).replace("{PIC}", "microchip_spirit")

OLD_SHIELD = """\t\tTAI_silicon_shield = {
\t\t\tpicture = digitalize_idea
\t\t\tallowed_civil_war = { always = yes }
\t\t\tmodifier = {
\t\t\t\tlocal_resources_microchips_factor = 0.05
\t\t\t\ttrade_opinion_factor = 0.10
\t\t\t\tforeign_influence_defense_modifier = 0.10
\t\t\t}
\t\t}"""
NEW_SHIELD = OLD_SHIELD.replace(
    "\t\t\t\tforeign_influence_defense_modifier = 0.10\n",
    "\t\t\t\tforeign_influence_defense_modifier = 0.10\n"
    "\t\t\t\tmicrochip_export_multiplier_modifier = 0.07\n"
    "\t\t\t\tmicrochip_plant_productivity_modifier = 0.05\n")

DESC_OLD = "Fabs, science parks and research institutes are the engine of the island's prosperity."
LOC = [
    (' TAI_ss_program_1: "The Silicon Island"', ' TAI_ss_program_1: "Silicon Island I"'),
    (f' TAI_ss_program_1_desc: "{DESC_OLD}"', ' TAI_ss_program_1_desc: "Hsinchu\'s fabs, science parks and research institutes are the engine of the island\'s prosperity, and the industry is only beginning to grow."'),
    (' TAI_ss_program_2: "The 12-Inch Economy"', ' TAI_ss_program_2: "Silicon Island II"'),
    (f' TAI_ss_program_2_desc: "{DESC_OLD}"', ' TAI_ss_program_2_desc: "The move to 12-inch wafers makes our foundries among the most productive in the world, and their exports a pillar of the economy."'),
    (' TAI_ss_program_3: "The Silicon Shield Economy"', ' TAI_ss_program_3: "Silicon Island III"'),
    (f' TAI_ss_program_3_desc: "{DESC_OLD}"', ' TAI_ss_program_3_desc: "Our leading-edge foundries make chips no one else can, and the world\'s technology industry depends on them."'),
]

EDITS = {
    "common/ideas/05_taiwan.txt": [(OLD_SPIRITS, NEW_SPIRITS), (OLD_SHIELD, NEW_SHIELD)],
    "localisation/english/MD_focus_TAI_l_english.yml": LOC,
}
SPEC_EDITS = [
    (OLD_SPIRITS, NEW_SPIRITS),
    ('("TAI_ss_program_1", "The Silicon Island")', '("TAI_ss_program_1", "Silicon Island I")'),
    ('("TAI_ss_program_2", "The 12-Inch Economy")', '("TAI_ss_program_2", "Silicon Island II")'),
    ('("TAI_ss_program_3", "The Silicon Shield Economy")', '("TAI_ss_program_3", "Silicon Island III")'),
]


def apply(path, edits):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    n = 0
    for old, new in edits:
        if new in s:
            continue
        if s.count(old) != 1:
            sys.exit(f"ERROR {path}: expected text found {s.count(old)} times: {old[:60]!r}")
        s = s.replace(old, new)
        n += 1
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)
    print(f"{path}: {n} edit(s)")


if __name__ == "__main__":
    root = sys.argv[1]
    for rel, edits in EDITS.items():
        apply(os.path.join(root, rel), edits)
    if len(sys.argv) > 2:
        apply(os.path.join(sys.argv[2], "events_spec.py"), SPEC_EDITS)
