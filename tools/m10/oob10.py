#!/usr/bin/env python3
"""OBT milestone 10: Taiwan 1 January 2000 starting order of battle (land, air, navy) from the OOB audit.

Usage: python3 oob10.py <millennium-dawn-root> <out_dir>
Reads the current MD Taiwan history files, keeps their equipment stockpile sections, applies the audit's fixes and
writes corrected copies to out_dir (same relative paths). Run apply10.py to copy them in.
"""
import os
import re
import sys

R, OUT = sys.argv[1:3]


def rd(rel):
    with open(os.path.join(R, rel), encoding="utf-8-sig") as fh:
        return fh.read()


def wr(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def sub1(text, old, new, label):
    assert text.count(old) == 1, (label, text.count(old))
    return text.replace(old, new)


# ------------------------------------------------------------------ land templates
def template(name, group, regs, regsup=(), sup=(), priority=None):
    out = ["division_template = {", f'\tname = "{name}"', f"\tdivision_names_group = {group}", "", "\tregiments = {"]
    for i, (t, x, y) in enumerate(regs):
        out.append(f"\t\t{t} = {{ x = {x} y = {y} }}")
    out.append("\t}")
    if regsup:
        out += ["", "\tregimental_support = {"] + [f"\t\t{t} = {{ x = {x} y = {y} }}" for t, x, y in regsup] + ["\t}"]
    if sup:
        out += ["", "\tsupport = {"] + [f"\t\t{t} = {{ x = {x} y = {y} }}" for t, x, y in sup] + ["\t}"]
    if priority is not None:
        out.append(f"\tpriority = {priority}")
    out.append("}")
    return "\n".join(out)


SUP = [("H_Engi_Comp", 0, 0), ("combat_service_support_company", 0, 1)]
TEMPLATES = [
    template("Infantry Brigade", "TAI_INF_BDE", [("L_Inf_Bat", 0, 0), ("L_Inf_Bat", 0, 1), ("L_Inf_Bat", 0, 2), ("Arty_Bat", 1, 0)],
             [("L_Recce_Comp", 0, 0)], SUP),
    template("Motorized Infantry Brigade", "TAI_INF_DIV", [("Mot_Inf_Bat", 0, 0), ("Mot_Inf_Bat", 0, 1), ("Mot_Inf_Bat", 0, 2), ("Arty_Bat", 1, 0)],
             [("Mot_Recce_Comp", 0, 0)], SUP),
    template("Armored Infantry Brigade", "TAI_MECH_BDE",
             [("Mech_Inf_Bat", 0, 0), ("Mech_Inf_Bat", 0, 1), ("Mech_Inf_Bat", 0, 2), ("armor_Bat", 1, 0), ("armor_Bat", 1, 1), ("SP_Arty_Bat", 2, 0)],
             [("armor_Recce_Comp", 0, 0)], SUP),
    template("Armored Brigade", "TAI_ARM_BDE",
             [("armor_Bat", 0, 0), ("armor_Bat", 0, 1), ("armor_Bat", 0, 2), ("Mech_Inf_Bat", 1, 0), ("Mech_Inf_Bat", 1, 1), ("SP_Arty_Bat", 2, 0)],
             [("armor_Recce_Comp", 0, 0)], SUP),
    template("Island Armored Brigade", "TAI_ARM_BDE",
             [("armor_Bat", 0, 0), ("armor_Bat", 0, 1), ("Mech_Inf_Bat", 1, 0), ("Arty_Bat", 2, 0)],
             [("armor_Recce_Comp", 0, 0)], SUP),
    template("Air Cavalry Brigade", "TAI_AIR_CAV_BRIGADES", [("attack_helo_bat", 0, 0), ("L_Air_assault_Bat", 0, 1), ("L_Air_assault_Bat", 0, 2)],
             [("air_assault_arty_battery", 0, 0)], SUP),
    template("Special Warfare Brigade", "TAI_SOF", [("Special_Forces", 0, 0), ("Special_Forces", 0, 1)], priority=2),
    template("Marine Division", "TAI_MAR",
             [("L_Marine_Bat", 0, 0), ("L_Marine_Bat", 0, 1), ("L_Marine_Bat", 0, 2), ("L_Marine_Bat", 1, 0), ("L_Marine_Bat", 1, 1), ("L_Marine_Bat", 1, 2),
              ("Arty_Bat", 2, 0), ("Arty_Bat", 2, 1)],
             [("L_Recce_Comp", 0, 0)], SUP),
]

# (name or None, name_order or None, template, province, experience, comment)
P = {"taipei": [7186, 14699, 14702], "hsinchu": [7214, 14412], "taichung": [11959, 14411], "tainan": [1091, 12027, 12068],
     "kaohsiung": [14410, 14700], "hualien": [4096, 9955], "penghu": [13274], "kinmen": [13275], "matsu": [14608]}
UNITS = [
    ("6th Army Corps (northern Taiwan)", [
        (542, "Armored Brigade", P["hsinchu"][1], 0.45, "542nd Armored 'Xunlei', Hukou; formed 1998"),
        (351, "Armored Infantry Brigade", P["taipei"][1], 0.45, "351st Armored Infantry 'Leiting', Guishan; formed 1 April 1999"),
        (452, "Infantry Brigade", P["taipei"][2], 0.4, "151st Division command"),
        (453, "Infantry Brigade", P["taipei"][2], 0.4, "151st Division command"),
        (102, "Infantry Brigade", P["taipei"][0], 0.4, ""),
        (103, "Infantry Brigade", P["taipei"][0], 0.4, ""),
        (108, "Infantry Brigade", P["hsinchu"][0], 0.4, ""),
        (None, "Infantry Brigade", P["hsinchu"][0], 0.4, "garrison brigade, number unverified (end-state count)"),
        (None, "Infantry Brigade", P["taipei"][1], 0.4, "garrison brigade, number unverified (end-state count)"),
    ]),
    ("10th Army Corps (central Taiwan)", [
        (586, "Armored Brigade", P["taichung"][0], 0.45, "586th Armored 'Zhongshan', Houli; formed 1 April 1999"),
        (373, "Armored Infantry Brigade", P["taichung"][0], 0.45, "373rd Armored Infantry 'Tianshan', Dali; conversion date unverified"),
        (200, "Motorized Infantry Brigade", P["taichung"][1], 0.4, "200th Motorized Infantry 'Gubei'"),
        (104, "Infantry Brigade", P["taichung"][1], 0.4, ""),
        (157, "Infantry Brigade", P["taichung"][0], 0.4, ""),
        (169, "Infantry Brigade", P["taichung"][1], 0.4, ""),
        (616, "Infantry Brigade", P["taichung"][0], 0.4, "206th Division command"),
        (617, "Infantry Brigade", P["taichung"][1], 0.4, "206th Division command"),
    ]),
    ("8th Army Corps (southern Taiwan)", [
        (564, "Armored Brigade", P["kaohsiung"][0], 0.45, "564th Armored 'Shaokang', Alian; formed 1 October 1999"),
        (395, "Armored Infantry Brigade", P["kaohsiung"][1], 0.45, "395th Armored Infantry; conversion date unverified"),
        (298, "Motorized Infantry Brigade", P["tainan"][1], 0.4, "298th Motorized Infantry 'Puchuan'"),
        (129, "Infantry Brigade", P["tainan"][2], 0.4, "210th Division"),
        (178, "Infantry Brigade", P["tainan"][0], 0.4, "26th Division command"),
        (618, "Infantry Brigade", P["tainan"][2], 0.4, "206th Division command"),
        (None, "Infantry Brigade", P["kaohsiung"][1], 0.4, "garrison brigade, number unverified (end-state count)"),
    ]),
    ("Kinmen Defense Command", [
        (584, "Island Armored Brigade", P["kinmen"][0], 0.45, "584th Armored 'Dengbu'; formed 1 April 1999"),
        (119, "Infantry Brigade", P["kinmen"][0], 0.4, ""),
        (127, "Infantry Brigade", P["kinmen"][0], 0.4, ""),
        (158, "Infantry Brigade", P["kinmen"][0], 0.4, ""),
    ]),
    ("Matsu Defense Command", [
        (193, "Infantry Brigade", P["matsu"][0], 0.4, ""),
        (194, "Infantry Brigade", P["matsu"][0], 0.4, ""),
        (195, "Infantry Brigade", P["matsu"][0], 0.4, "Dongyin; unit history from July 1999"),
    ]),
    ("Penghu Defense Command", [
        (503, "Island Armored Brigade", P["penghu"][0], 0.45, ""),
        (168, "Infantry Brigade", P["penghu"][0], 0.4, ""),
    ]),
    ("Hua-Tung Defense Command", [
        (128, "Infantry Brigade", P["hualien"][0], 0.4, ""),
        (None, "Infantry Brigade", P["hualien"][1], 0.4, "garrison brigade, number unverified (end-state count)"),
    ]),
    ("Aviation and Special Warfare Command", [
        (601, "Air Cavalry Brigade", P["hsinchu"][0], 0.4, ""),
        (602, "Air Cavalry Brigade", P["taichung"][0], 0.4, ""),
        (862, "Special Warfare Brigade", P["taipei"][0], 0.7, ""),
    ]),
    ("ROC Marine Corps (divisions until the August 2000 reorganization)", [
        ("66th Marine Division", "Marine Division", P["taipei"][0], 0.55, "Linkou"),
        ("99th Marine Division", "Marine Division", P["kaohsiung"][1], 0.55, "Tsoying"),
    ]),
]


def units_block():
    out = ["units = {"]
    for header, rows in UNITS:
        out += ["", f"\t### {header} ###"]
        for ident, tmpl, prov, xp, note in rows:
            out.append("\tdivision = {" + (f" # {note}" if note else ""))
            if isinstance(ident, int):
                out.append(f"\t\tdivision_name = {{ is_name_ordered = yes name_order = {ident} }}")
            elif isinstance(ident, str):
                out.append(f'\t\tname = "{ident}"')
            out += [f"\t\tlocation = {prov}", f'\t\tdivision_template = "{tmpl}"', f"\t\tstart_experience_factor = {xp}",
                    "\t\tstart_equipment_factor = 0.01", "\t}"]
    out.append("}")
    return "\n".join(out)


HEADER = ("# Taiwan, 1 January 2000. Operation Blue Tiger order of battle audit (docs/ORDER_OF_BATTLE_AUDIT.md):\n"
          "# Jingshi brigades under 3 army corps and 4 defense commands; Marine divisions until August 2000.\n"
          "# Reserve formations are not on the map; they appear only through the Reserve Mobilization decisions.\n\n")
LAND = HEADER + "\n\n".join(TEMPLATES) + "\n\n" + units_block() + "\n\n"
n_units = sum(len(r) for _h, r in UNITS)

for rel in ("history/units/TAI_2000_nsb.txt", "history/units/TAI_2000_nonnsb.txt"):
    t = rd(rel)
    i = t.index("instant_effect = {")
    stock = t[i:]
    nsb = rel.endswith("_nsb.txt")
    # duplicate Bell 206 entry
    dup = re.search(r"\tadd_equipment_to_stockpile = \{\n\t\ttype = transport_helicopter_1 #USA_transport_helicopter_1:0 \"Bell 206 aka TH-67\" 30\n\t\tamount = 30\n\t\tproducer = USA\n\t\}\n", stock)
    assert dup, rel
    stock = stock.replace(dup.group(0), "")
    # CH-47SD delivered 2001-2002
    ch = re.search(r"\tadd_equipment_to_stockpile = \{\n\t\ttype = transport_helicopter_1 #Boeing CH-47 Chinook\n\t\tamount = 8\n\t\tproducer = USA\n\t\}\n", stock)
    assert ch, rel
    stock = stock.replace(ch.group(0), "")
    if nsb:
        stock = sub1(stock, 'variant_name = "M60A3"\n\t\tamount = 189', 'variant_name = "M60A3"\n\t\tamount = 169 # FAS 1999', "m60")
        stock = sub1(stock, 'variant_name = "CM-21"\n\t\tamount = 100', 'variant_name = "CM-21"\n\t\tamount = 225 # FAS 1999', "cm21")
        stock = sub1(stock, "amount = 53\n\t\tproducer = USA\n\t\tvariant_name = \"AH-1 Cobra\"", "amount = 42 # AH-1W in service by April 2000\n\t\tproducer = USA\n\t\tvariant_name = \"AH-1 Cobra\"", "ah1")
        stock = sub1(stock, "amount = 100\n\t\tproducer = USA\n\t\tvariant_name = \"AN/TWQ-1 Avenger\"", "amount = 74 # 1996 sale\n\t\tproducer = USA\n\t\tvariant_name = \"AN/TWQ-1 Avenger\"", "avenger")
    else:
        t86 = re.search(r"\tadd_equipment_to_stockpile = \{\n\t\ttype = infantry_weapons_4 # \"T86\"\n\t\tamount = 200\n[^}]*\}\n", stock)
        assert t86, "t86"
        stock = stock.replace(t86.group(0), "")
        stock = re.sub(r"(type = MBT_1 #M48A5\n\t\tamount = )189", r"\g<1>100 # FAS 1999", stock)
        stock = re.sub(r"(type = attack_helicopter_1  #AH-1\n\t\tamount = )53", r"\g<1>42 # AH-1W in service by April 2000", stock)
        stock = re.sub(r"(type = SP_Anti_Air_1 #USA_SP_Anti_Air_1:0 \"AN/TWQ-1 Avenger\"\n\t\tamount = )100", r"\g<1>74 # 1996 sale", stock)
        if "#M60A3" not in stock:
            stock = stock.replace("\t####Vehicles##\n", "\t####Vehicles##\n\tadd_equipment_to_stockpile = {\n\t\ttype = MBT_1 #M60A3\n\t\tamount = 169 # FAS 1999\n\t\tproducer = USA\n\t}\n", 1)
        for k in ("100 # FAS", "42 # AH-1W", "74 # 1996"):
            assert k in stock, (rel, k)
    wr(rel, LAND + stock)

# ------------------------------------------------------------------ air (BBA)
rel = "history/units/TAI_2000_bba.txt"
t = rd(rel)
t = sub1(t, 'variant_name = "F-CK-1 Ching-kuo"\n\t\tamount = 8 #120 deployed', 'variant_name = "F-CK-1 Ching-kuo"\n\t\tamount = 0 # all 130 deployed', "idfstock")
t = sub1(t, "amount = 105 #168 deployed\n\t\tvariant_name = \"F-5E Chung Cheng\"", "amount = 24 # reserve airframes; about 160 F-5s in total (FAS 144, IISS-era estimates up to 200)\n\t\tvariant_name = \"F-5E Chung Cheng\"", "f5stock")
t = sub1(t, "amount = 6 #120 deployed\n\t\tvariant_name = \"F-16A Blk 20\"", "amount = 0 # 146 deployed (150 ordered, 4 lost by April 2000)\n\t\tvariant_name = \"F-16A Blk 20\"", "f16stock")
i = t.index("air_wings = {")
F16, F5, IDF, M2K = ("small_plane_strike_airframe_2", "F-16A Blk 20", "USA"), ("small_plane_airframe_1", "F-5E Chung Cheng", None), \
    ("small_plane_strike_airframe_2", "F-CK-1 Ching-kuo", None), ("small_plane_airframe_2", "Mirage 2000-5F", "FRA")


def wing(kind, n, name):
    typ, var, cr = kind
    c = f' creator = "{cr}"' if cr else ""
    return f'\t\t{typ} = {{ owner = "TAI"{c} amount = {n} version_name = "{var}" }}\n\t\tname = "{name}"\n\t\tstart_experience_factor = 0.5\n'


AIR = {
    598: [(F5, 24, "15th Tactical Fighter Squadron (Taoyuan)"), (F5, 24, "16th Tactical Fighter Squadron (Taoyuan)")],
    599: None,  # support wings kept from the original
    600: [(F16, 21, "17th Tactical Fighter Squadron (5th Wing, Hualien)"), (F16, 21, "26th Tactical Fighter Squadron (5th Wing, Hualien)"),
          (F16, 21, "27th Tactical Fighter Squadron (5th Wing, Hualien)"), (F5, 24, "44th Tactical Fighter Squadron (7th Wing, Taitung)"),
          (F5, 24, "45th Tactical Fighter Squadron (7th Wing, Taitung)"), (F5, 24, "46th Aggressor Squadron (7th Wing, Taitung)")],
    1155: [(M2K, 24, "41st Tactical Fighter Squadron (2nd Wing, Hsinchu)"), (M2K, 24, "42nd Tactical Fighter Squadron (2nd Wing, Hsinchu)"),
           (M2K, 10, "48th Training Squadron (2nd Wing, Hsinchu)")],
    1156: [(IDF, 22, "7th Tactical Fighter Squadron (3rd Wing, Ching Chuan Kang)"), (IDF, 22, "8th Tactical Fighter Squadron (3rd Wing, Ching Chuan Kang)"),
           (IDF, 21, "28th Tactical Fighter Squadron (3rd Wing, Ching Chuan Kang)")],
    1157: [(IDF, 22, "1st Tactical Fighter Squadron (1st Wing, Tainan)"), (IDF, 22, "3rd Tactical Fighter Squadron (1st Wing, Tainan)"),
           (IDF, 21, "9th Tactical Fighter Squadron (1st Wing, Tainan)"), (F16, 20, "14th Tactical Fighter Squadron (4th Wing, Chiayi)"),
           (F16, 21, "21st Tactical Fighter Squadron (4th Wing, Chiayi)"), (F16, 21, "22nd Tactical Fighter Squadron (4th Wing, Chiayi)"),
           (F16, 21, "23rd Tactical Fighter Squadron (4th Wing, Chiayi)"), (F5, 8, "12th Tactical Reconnaissance Squadron (Chiayi)")],
}
orig = t[i:]
m599 = re.search(r"\t599 = \{\n.*?\n\t\}\n", orig, re.S)
s599 = m599.group(0).replace('name = "Fighter Training Group"\n\t\tstart_experience_factor = 0.5\n\t\tsmall_plane_strike_airframe_1 = { owner = "TAI" amount = 24 version_name = "AT-3" }\n\t\tname = "Fighter Training Group"',
                             'name = "Fighter Training Group (AT-3)"\n\t\tstart_experience_factor = 0.5\n\t\tsmall_plane_strike_airframe_1 = { owner = "TAI" amount = 24 version_name = "AT-3" }\n\t\tname = "Advanced Training Group (AT-3)"')
blocks = ["air_wings = {"]
for st in (598, 599, 600, 1155, 1156, 1157):
    if st == 599:
        blocks.append(s599.rstrip("\n"))
        continue
    blocks.append(f"\t{st} = {{\n" + "".join(wing(*w) for w in AIR[st]) + "\t}")
blocks.append("}")
t = t[:i] + "\n".join(blocks) + "\n"
wr(rel, t)
tot = {}
for st, ws in AIR.items():
    for (typ, var, _c), n, _ in ws or []:
        tot[var] = tot.get(var, 0) + n

rel = "history/units/TAI_2000_nonbba.txt"
t = rd(rel)
t = sub1(t, 'type = MR_Fighter1 #"F-5E Tiger II & F5-F" 265\n\t\tamount = 265', 'type = MR_Fighter1 #"F-5E Tiger II & F5-F": FAS 144, IISS-era estimates up to 200\n\t\tamount = 160', "nonbba f5")
t = sub1(t, "type = MR_Fighter2 #F-CK-1 Ching-kuo\n\t\tamount = 128", "type = MR_Fighter2 #F-CK-1 Ching-kuo\n\t\tamount = 130", "nonbba idf")
t = sub1(t, "type = MR_Fighter2 #F-16A/B Fighting Falcon\n\t\tamount = 126", "type = MR_Fighter2 #F-16A/B Fighting Falcon: 150 ordered, 4 lost by April 2000\n\t\tamount = 146", "nonbba f16")
wr(rel, t)

# ------------------------------------------------------------------ navy
GEAR = 'destroyer_hull_1 = { amount = 1 owner = TAI creator = USA version_name = "Gearing Class (Taiwanese Modernization)" }'
KNOX = 'frigate_hull_1 = { amount = 1 owner = TAI creator = USA version_name = "Knox Class" }'


def ship(name, definition, equip, xp=0.40):
    return f'\t\t\tship = {{ name = "{name}" definition = {definition} start_experience_factor = {xp} equipment = {{ {equip} }} }}'


DD = ["ROCS Chien Yang (DDG-912)", "ROCS Liao Yang (DDG-921)", "ROCS Shen Yang (DDG-923)", "ROCS Te Yang (DDG-925)", "ROCS Yun Yang (DDG-927)",
      "ROCS Chen Yang (DDG-928)", "ROCS Shao Yang (DDG-929)"]
KN = ["ROCS Chi Yang (FFG-932)", "ROCS Fong Yang (FFG-933)", "ROCS Fen Yang (FFG-934)", "ROCS Lan Yang (FFG-935)", "ROCS Hae Yang (FFG-936)",
      "ROCS Hwai Yang (FFG-937)", "ROCS Ning Yang (FFG-938)", "ROCS Yi Yang (FFG-939)"]
CK = ["ROCS Cheng Kung (PFG-1101)", "ROCS Cheng Ho (PFG-1103)", "ROCS Chi Kuang (PFG-1105)", "ROCS Yueh Fei (PFG-1106)", "ROCS Tzu I (PFG-1107)",
      "ROCS Pan Chao (PFG-1108)", "ROCS Chang Chien (PFG-1109)"]
KD = ["ROCS Kang Ding (PFG-1202)", "ROCS Si Ning (PFG-1203)", "ROCS Kun Ming (PFG-1205)", "ROCS Di Hua (PFG-1206)", "ROCS Wu Chang (PFG-1207)",
      "ROCS Chen De (PFG-1208)"]
JC = [603, 605, 606, 607, 608, 609, 610, 611, 612, 613, 615, 616]
HAIOU = list(range(5, 13)) + list(range(14, 22)) + list(range(23, 31)) + list(range(32, 40)) + list(range(41, 58))
navy = ["# Taiwan navy, 1 January 2000 (OBT order of battle audit). Main base Tsoying (Kaohsiung); Keelung in the north.", "units = {",
        "\tfleet = {", '\t\tname = "ROCN Fleet Command"', "\t\tnaval_base = 11914",
        "\t\ttask_force = {", '\t\t\tname = "Tsoying Surface Group"', "\t\t\tlocation = 11914"]
navy += [ship(n, "destroyer", GEAR) for n in DD]
navy += [ship(n, "frigate", 'frigate_hull_2 = { amount = 1 owner = TAI version_name = "Cheng Kung Class" }') for n in CK]
navy += [ship(n, "frigate", 'frigate_hull_3 = { amount = 1 owner = TAI version_name = "Kang Ding Class" }') for n in KD]
navy += ["\t\t}", "\t\ttask_force = {", '\t\t\tname = "256th Submarine Group"', "\t\t\tlocation = 11914",
         ship("ROCS Hai Lung (SS-793)", "attack_submarine", 'attack_submarine_hull_2 = { amount = 1 owner = TAI version_name = "Hai Lung Class" }'),
         ship("ROCS Hai Hu (SS-794)", "attack_submarine", 'attack_submarine_hull_2 = { amount = 1 owner = TAI version_name = "Hai Lung Class" }'),
         ship("ROCS Hai Shih (SS-791)", "attack_submarine", 'attack_submarine_hull_1 = { amount = 1 owner = TAI creator = USA version_name = "Hai Shih Class" }'),
         ship("ROCS Hai Pao (SS-792)", "attack_submarine", 'attack_submarine_hull_1 = { amount = 1 owner = TAI creator = USA version_name = "Hai Shih Class" }'),
         "\t\t}", "\t\ttask_force = {", '\t\t\tname = "Jin Chiang Patrol Squadron"', "\t\t\tlocation = 11914"]
navy += [ship(f"ROCS Jin Chiang (PGG-603)" if h == 603 else f"PGG-{h}", "corvette", 'corvette_hull_1 = { amount = 1 owner = TAI version_name = "Jin Chiang Class" }', 0.35) for h in JC]
navy += ["\t\t}", "\t}", "\tfleet = {", '\t\tname = "Keelung Naval Group"', "\t\tnaval_base = 14701", "\t\ttask_force = {", '\t\t\tname = "Knox Frigate Squadron"', "\t\t\tlocation = 14701"]
navy += [ship(n, "frigate", KNOX) for n in KN]
navy += ["\t\t}", "\t\ttask_force = {", '\t\t\tname = "Hai Ou Missile Boat Squadrons"', "\t\t\tlocation = 14701"]
navy += [ship(f"FABG-{h}", "corvette", 'corvette_hull_1 = { amount = 1 owner = TAI version_name = "Hai Ou Class" }', 0.35) for h in HAIOU]
navy += ["\t\t}", "\t}", "}"]
wr("history/units/TAI_2000_naval_mtg.txt", "\n".join(navy) + "\n")

# missile boat variants in the Taiwan history file, beside the Hai Lung variant
rel = "history/countries/TAI - Taiwan.txt"
t = rd(rel)
VAR = '''
		#Jin Chiang Class patrol ship (OBT order of battle audit): 4 Hsiung Feng I, 40 mm gun
		create_equipment_variant = {
			name = "Jin Chiang Class"
			type = corvette_hull_1
			parent_version = 0
			modules = {
				fixed_ship_engine_slot = module_light_surface_diesel_power_1
				fixed_ship_fire_control_system_slot = module_analog_fire_control
				fixed_ship_radar_slot = module_radar_1
				fixed_ship_auxillary_slot = module_naval_missile_mount_quad
				fixed_ship_battery_slot = module_chain_gun
				front_1_custom_slot = empty
				rear_1_custom_slot = empty
				fixed_ship_missile_ammo_slot = module_naval_ammo_anti_ship_1
			}
		}

		#Hai Ou Class fast attack craft (OBT order of battle audit): 2 Hsiung Feng I
		create_equipment_variant = {
			name = "Hai Ou Class"
			type = corvette_hull_1
			parent_version = 0
			modules = {
				fixed_ship_engine_slot = module_light_surface_diesel_power_1
				fixed_ship_fire_control_system_slot = module_analog_fire_control
				fixed_ship_radar_slot = module_radar_1
				fixed_ship_auxillary_slot = module_naval_missile_mount_twin
				fixed_ship_battery_slot = module_chain_gun
				front_1_custom_slot = empty
				rear_1_custom_slot = empty
				fixed_ship_missile_ammo_slot = module_naval_ammo_anti_ship_1
			}
		}
'''
anchor = "\t\tcomplete_special_project = sp:sp_naval_vessel_project\n"
if "Jin Chiang Class" not in t:
    t = sub1(t, anchor, VAR.lstrip("\n") + "\n" + anchor, "variant anchor")
wr(rel, t)
print(f"land units {n_units}; air deployed {tot}; navy DD {len(DD)} FF {len(KN)+len(CK)+len(KD)} SS 4 PGG {len(JC)} FABG {len(HAIOU)}")
