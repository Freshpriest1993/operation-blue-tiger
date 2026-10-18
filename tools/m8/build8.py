#!/usr/bin/env python3
"""Generate Operation Blue Tiger milestone 8: Hainan Island Incident, 2001 arms package and 2005 US-Japan statement events.

Usage: python3 build8.py <out_dir>
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
NS = "obt_crisis"
EV, LOC = [], []


def w(name, text, bom=False):
    with open(os.path.join(OUT, name), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)


def tension(n):
    return ["if = {", "\tlimit = { country_exists = CHI }", "\tCHI = {",
            f"\t\tadd_to_variable = {{ CHI_taiwan_strait_tension = {n} tooltip = CHI_taiwan_strait_tension_tt }}",
            "\t\tclamp_variable = { var = CHI_taiwan_strait_tension min = 0 max = 100 }", "\t}", "}", "OBT_strait_update = yes"]


def var(owner, v, n):
    body = [f"add_to_variable = {{ {v} = {n} tooltip = {v}_tt }}", f"clamp_variable = {{ var = {v} min = 0 max = 100 }}"]
    return ["if = {", f"\tlimit = {{ country_exists = {owner} }}", f"\t{owner} = {{"] + ["\t\t" + l for l in body] + ["\t}", "}"]


def support(n):
    return var("CHI", "CHI_taiwan_us_support", n)


def opinion(a, b, mod):
    return ["if = {", f"\tlimit = {{ country_exists = {a} country_exists = {b} }}",
            f"\t{a} = {{ add_opinion_modifier = {{ target = {b} modifier = {mod} }} }}",
            f"\t{b} = {{ add_opinion_modifier = {{ target = {a} modifier = {mod} }} }}", "}"]


def fire(tag, n, days):
    return ["if = {", f"\tlimit = {{ country_exists = {tag} }}", f"\t{tag} = {{ country_event = {{ id = {NS}.{n} days = {days} }} }}", "}"]


def E(n, tag, title, desc, pic, options, extra_trigger=(), once=True):
    eid = f"{NS}.{n}"
    out = ["country_event = {", f"\tid = {eid}", f"\ttitle = {eid}.t"]
    LOC.append(f' {eid}.t: "{title}"')
    if isinstance(desc, str):
        out.append(f"\tdesc = {eid}.d")
        LOC.append(f' {eid}.d: "{desc}"')
    else:
        for suf, trig, text in desc:
            out.append(f"\tdesc = {{ text = {eid}.d_{suf} trigger = {{ {trig} }} }}")
            LOC.append(f' {eid}.d_{suf}: "{text}"')
    out += [f"\tpicture = {pic}", "\tis_triggered_only = yes"]
    if once:
        out.append("\tfire_only_once = yes")
    out += ["", "\ttrigger = {", f"\t\toriginal_tag = {tag}"] + ["\t\t" + t for t in extra_trigger] + ["\t}", ""]
    for i, o in enumerate(options):
        key = f"{eid}.{'abce'[i]}"
        out += ["\toption = {", f"\t\tname = {key}"]
        if o.get("trigger"):
            out += ["\t\ttrigger = {"] + ["\t\t\t" + t for t in o["trigger"]] + ["\t\t}"]
        out.append(f'\t\tlog = "[GetDateText]: [This.GetName]: {key} executed"')
        out += ["\t\t" + l for l in o["eff"]]
        out += ["\t\tai_chance = {"] + ["\t\t\t" + l for l in o["ai"]] + ["\t\t}", "\t}", ""]
        LOC.append(f' {key}: "{o["text"]}"')
    out[-1] = "}"
    EV.append("\n".join(out) + "\n")


def O(text, eff, ai, trigger=None):
    return {"text": text, "eff": eff, "ai": ai, "trigger": trigger}


def mod(f, t):
    return ["modifier = {", f"\tfactor = {f}", f"\t{t}", "}"]


AH = "(Alternate history) "
NOWITHDRAW = "NOT = { has_country_flag = USA_withdrew_support_TAI }"

# ------------------------------------------------------------------ Hainan
E(1, "USA", "Crew Down on Hainan",
  "One of our EP-3E reconnaissance aircraft and a Chinese J-8II fighter have collided over the South China Sea. Each government blames the other's pilot. The crippled EP-3E made an emergency landing at Lingshui on Hainan Island, and its 24 crew are now in Chinese custody. The Chinese pilot is missing.",
  "GFX_CHI_hainan_ep3",
  [O("Demand the crew's prompt return.", ["set_country_flag = USA_hainan_firm"] + support(2) + tension(3) + fire("TAI", 2, 1) + fire("CHI", 3, 3), ["base = 50"]),
   O("Express regret for the missing pilot.", ["set_country_flag = USA_hainan_regret"] + fire("TAI", 2, 1) + fire("CHI", 3, 3), ["base = 50"])],
  ["country_exists = CHI"])
E(2, "TAI", "Taipei Watches Hainan",
  "An American reconnaissance crew is being held on Hainan after a collision with a Chinese fighter. Washington and Beijing are trading accusations, and both are watching how Taipei responds.",
  "GFX_CHI_hainan_ep3",
  [O("Quietly support Washington.", var("TAI", "TAI_us_confidence", 2) + tension(1), ["base = 50"]),
   O("Stay out of it.", var("CHI", "CHI_TAI_trust", 2), ["base = 50"])])
E(3, "CHI", "The Crew Question",
  "Twenty-four American airmen are in our custody on Hainan, and the search for our pilot continues. Washington wants its crew back; our public wants an apology.",
  "GFX_CHI_hainan_ep3",
  [O("Hold the crew until Washington apologizes.", tension(2) + fire("USA", 4, 3), ["base = 70"]),
   O(AH + "Release them at once on humanitarian grounds.", ["set_country_flag = CHI_hainan_quick_release"] + var("CHI", "CHI_TAI_trust", 2) + opinion("CHI", "USA", "recent_actions_positive") + fire("CHI", 5, 1), ["base = 25"] + mod(2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH") + mod(1.5, "USA = { has_country_flag = USA_hainan_regret }")),
   O(AH + "Put the crew on trial.", ["set_country_flag = CHI_hainan_trial", "add_war_support = 0.03"] + support(10) + tension(10) + opinion("CHI", "USA", "large_decrease") + fire("USA", 7, 2),
     ["base = 2"] + mod(3, "has_global_flag = CHI_HEGEMON_FOCUS_PATH"), trigger=["has_country_flag = CHI_hainan_honoured"])],
  ["country_exists = USA"])
E(4, "USA", "The Letter",
  "Beijing will release the crew if we apologize. Our ambassador has drafted a letter saying we are very sorry for the loss of the Chinese pilot and that the aircraft landed without verbal clearance. It admits no fault for the collision.",
  "GFX_USA_event_congress",
  [O("Send the letter.", ["set_country_flag = USA_hainan_letter"] + fire("CHI", 5, 2), ["base = 80"]),
   O(AH + "Refuse any apology.", ["set_country_flag = USA_hainan_refused"] + support(3) + tension(2) + fire("USA", 6, 21), ["base = 20"])],
  ["country_exists = CHI"])
E(6, "USA", "The Standoff Drags On",
  AH + "Three weeks on, the crew is still held on Hainan. Families are on television every night, business groups warn about trade with China, and Congress is divided over what to do next.",
  "GFX_USA_event_congress",
  [O("Send the letter after all.", ["set_country_flag = USA_hainan_letter", "add_political_power = -50"] + fire("CHI", 5, 2), ["base = 70"]),
   O("Refuse again.", ["set_country_flag = USA_hainan_refused_twice"] + support(3) + opinion("CHI", "USA", "medium_decrease") + fire("CHI", 5, 3), ["base = 30"])],
  ["country_exists = CHI"])
E(7, "USA", "The Crew on Trial",
  AH + "Beijing has announced that our airmen will stand trial. The President faces demands for sanctions, for a carrier deployment and for restraint, often from the same senators.",
  "GFX_USA_event_congress",
  [O("Rally our allies and wait them out.", support(5) + fire("CHI", 5, 60), ["base = 60"]),
   O("Threaten sanctions.", support(5) + tension(5) + opinion("CHI", "USA", "medium_decrease") + fire("CHI", 5, 60), ["base = 40"])],
  ["country_exists = CHI"])
E(5, "CHI", "The Crew Goes Home",
  [("refused", "USA = { has_country_flag = USA_hainan_refused_twice } NOT = { has_country_flag = CHI_hainan_trial } NOT = { has_country_flag = CHI_hainan_quick_release }", "Washington still refuses to apologize, and the standoff is costing us abroad. Holding the crew longer gains nothing."),
   ("letter", "has_country_flag = CHI_hainan_honoured NOT = { USA = { has_country_flag = USA_hainan_refused_twice } } NOT = { has_country_flag = CHI_hainan_trial } NOT = { has_country_flag = CHI_hainan_quick_release }", "Washington's letter says it is very sorry for the loss of our pilot and for the landing without permission. Each side reads the words its own way, but the standoff can end."),
   ("settle", "has_country_flag = CHI_hainan_settlement NOT = { USA = { has_country_flag = USA_hainan_refused_twice } } NOT = { has_country_flag = CHI_hainan_quick_release }", "Washington's letter says it is very sorry for the loss of our pilot and for the landing without permission. Each side reads the words its own way, but the standoff can end."),
   ("quick", "has_country_flag = CHI_hainan_quick_release", "We have decided to send the American crew home without waiting for an apology."),
   ("trial", "has_country_flag = CHI_hainan_trial", "The trial has made its point and cost us abroad. It is time to send the airmen home.")],
  "GFX_CHI_hainan_ep3",
  [O("Release the crew and keep the aircraft for inspection.", ["set_country_flag = CHI_hainan_kept_aircraft"] + fire("USA", 9, 83), ["base = 70"]),
   O(AH + "Release the crew and return the aircraft intact.", var("CHI", "CHI_TAI_trust", 2) + opinion("CHI", "USA", "recent_actions_positive"), ["base = 30"] + mod(2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH") + mod(1.5, "USA = { has_country_flag = USA_hainan_letter }"))],
  ["country_exists = USA"])
E(9, "USA", "The Aircraft Comes Home",
  "The EP-3E has been taken apart on Hainan and flown home in pieces aboard a chartered Russian transport. Talks on reconnaissance flights and collision avoidance continue.",
  "GFX_CHI_hainan_ep3",
  [O("Close the chapter.", ["add_political_power = 10"], ["base = 100"])],
  ["country_exists = CHI", "CHI = { has_country_flag = CHI_hainan_kept_aircraft }"])

# ------------------------------------------------------------------ 2001 arms package
HAINAN_BAD = "OR = { has_country_flag = USA_hainan_refused has_country_flag = USA_hainan_firm CHI = { has_country_flag = CHI_hainan_trial } }"
E(20, "USA", "The Taiwan Arms Package",
  "The annual arms talks with Taipei have reached the President's desk. On the table are four Kidd-class destroyers, eight diesel submarines and twelve P-3C patrol aircraft. Taipei also wants Aegis-equipped destroyers, which Beijing has warned against above all.",
  "GFX_USA_event_congress",
  [O("Approve the package and defer Aegis.", ["set_global_flag = OBT_2001_package_approved"] + support(5) + tension(4) + fire("USA", 21, 1) + fire("TAI", 22, 2) + fire("CHI", 23, 3), ["base = 70"]),
   O(AH + "Approve everything, including Aegis destroyers.", ["set_global_flag = OBT_2001_package_approved", "set_global_flag = OBT_2001_aegis"] + support(8) + tension(8) + var("CHI", "CHI_TAI_trust", -5) + fire("USA", 21, 1) + fire("TAI", 22, 2) + fire("CHI", 23, 3),
     ["base = 15"] + mod(3, HAINAN_BAD)),
   O(AH + "Postpone the package.", ["set_global_flag = OBT_2001_package_postponed"] + support(-5) + tension(-3) + fire("TAI", 22, 2), ["base = 15"] + mod(0.3, HAINAN_BAD))],
  ["country_exists = TAI", "country_exists = CHI", NOWITHDRAW, "NOT = { has_war_with = TAI }"])
E(21, "USA", "Whatever It Takes?",
  "A television interviewer asks the President whether the United States has an obligation to defend Taiwan if it is attacked by China.",
  "GFX_USA_event_congress",
  [O("We will do whatever it takes to help Taiwan defend herself.", support(5) + tension(3) + var("CHI", "CHI_TAI_trust", -3), ["base = 70"]),
   O(AH + "Reaffirm strategic ambiguity.", var("TAI", "TAI_us_confidence", 2), ["base = 30"])],
  ["country_exists = TAI"])
E(22, "TAI", "Washington's Decision",
  [("approved", "has_global_flag = OBT_2001_package_approved NOT = { has_global_flag = OBT_2001_aegis }", "Washington has approved four Kidd-class destroyers, eight diesel submarines and twelve P-3C patrol aircraft. Aegis destroyers are deferred. The Legislative Yuan must now find the money, and the armed forces must learn to use what they buy."),
   ("aegis", "has_global_flag = OBT_2001_aegis", "Washington has approved everything we asked for, including Aegis destroyers. Beijing is furious. The Legislative Yuan must now find the money, and the armed forces must learn to use what they buy."),
   ("postponed", "has_global_flag = OBT_2001_package_postponed", "Washington has postponed this year's arms package. Officials say the door remains open, but the timing is wrong.")],
  "GFX_TAI_roc",
  [O("Welcome the package.", var("TAI", "TAI_us_confidence", 3) + var("TAI", "TAI_military_confidence", 5), ["base = 60"], trigger=["has_global_flag = OBT_2001_package_approved"]),
   O("Buy only what we can absorb.", var("TAI", "TAI_reform_capacity", 3), ["base = 40"], trigger=["has_global_flag = OBT_2001_package_approved"]),
   O("Lobby Congress and wait.", var("TAI", "TAI_us_confidence", -3) + ["add_political_power = -25"], ["base = 50"], trigger=["has_global_flag = OBT_2001_package_postponed"]),
   O("Invest in our own industry instead.", var("TAI", "TAI_reform_capacity", 2) + ["add_political_power = -25"], ["base = 50"], trigger=["has_global_flag = OBT_2001_package_postponed"])])
E(23, "CHI", "Washington Arms Taipei",
  [("approved", "NOT = { has_global_flag = OBT_2001_aegis }", "Washington has approved destroyers, submarines and patrol aircraft for Taiwan, though not the Aegis destroyers we warned against. The Foreign Ministry calls it blatant interference in China's internal affairs."),
   ("aegis", "has_global_flag = OBT_2001_aegis", "Washington has approved Aegis destroyers for Taiwan despite our warnings. The Foreign Ministry calls it blatant interference in China's internal affairs.")],
  "GFX_CHI_event_navy_ship",
  [O("Lodge a formal protest.", tension(2), ["base = 70"]),
   O("Answer with exercises in the Strait.", tension(5) + ["add_war_support = 0.02"] + support(2), ["base = 30"] + mod(3, "has_global_flag = CHI_HEGEMON_FOCUS_PATH"))],
  ["country_exists = TAI"])

# ------------------------------------------------------------------ 2005 US-Japan statement
E(30, "JAP", "The Security Consultative Committee",
  "Our foreign and defense ministers are meeting their American counterparts to agree on common strategic objectives for the alliance. The American side proposes listing the peaceful resolution of issues concerning the Taiwan Strait through dialogue.",
  "GFX_politics_negotiations",
  [O("Name the Taiwan Strait among our common objectives.", ["set_global_flag = OBT_2005_2plus2_taiwan"] + support(3) + tension(3) + var("CHI", "CHI_TAI_trust", -2) + opinion("JAP", "CHI", "small_decrease") + fire("TAI", 31, 1) + fire("CHI", 32, 2), ["base = 70"]),
   O(AH + "Leave Taiwan out of the statement.", opinion("JAP", "CHI", "recent_actions_positive"), ["base = 30"])],
  ["country_exists = USA", "country_exists = CHI", "country_exists = TAI", "NOT = { has_war_with = USA }", "NOT = { has_war_with = CHI }"])
E(31, "TAI", "Tokyo and Washington Speak",
  "For the first time, Japan and the United States have named the Taiwan Strait among their common strategic objectives, calling for the peaceful resolution of its issues through dialogue.",
  "GFX_politics_negotiations",
  [O("Welcome the statement.", var("TAI", "TAI_us_confidence", 2) + tension(2), ["base = 60"]),
   O("Respond with restraint.", var("CHI", "CHI_TAI_trust", 1), ["base = 40"])],
  ["has_global_flag = OBT_2005_2plus2_taiwan"])
E(32, "CHI", "The 2+2 Statement",
  "Tokyo and Washington have named the Taiwan Strait among their common strategic objectives. Our Foreign Ministry has expressed its resolute opposition to any interference in China's internal affairs.",
  "GFX_CHI_event_china_taiwan_flag",
  [O("Lodge a formal protest.", tension(2), ["base = 70"]),
   O("Play it down publicly.", ["add_stability = -0.01"], ["base = 30"] + mod(2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH"))],
  ["has_global_flag = OBT_2005_2plus2_taiwan"])

LOC.append(' OBT_2001_package_postponed: "Washington has postponed the 2001 arms package"')
LOC.append(' TAI_na_kidd_destroyers_aegis: "Aegis Combat System"')
for l in LOC:
    assert "—" not in l, l
w("OBT_crisis_events.txt", f"add_namespace = {NS}\n\n" + "\n".join(EV))
w("loc_crisis.yml", "l_english:\n # Operation Blue Tiger milestone 8: Hainan, arms package and US-Japan statement\n" + "\n".join(LOC) + "\n", bom=True)
print(len(EV), "events", len(LOC), "loc")
