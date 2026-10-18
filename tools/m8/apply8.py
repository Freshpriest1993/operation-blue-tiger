#!/usr/bin/env python3
"""Apply OBT milestone 8 hooks to the MD repo (idempotent). Run from repo root."""
import re, io
def rd(p): return io.open(p, encoding="utf-8-sig").read()
def bom(p): return io.open(p,'rb').read(3)==b'\xef\xbb\xbf'
def wr(p, t, b): io.open(p, "w", encoding="utf-8-sig" if b else "utf-8", newline="\n").write(t)

# 1. Hainan hook in MD CHI_political_events.6
p = "events/05_china.txt"; b = bom(p); t = rd(p)
if "OBT_hainan_begin" not in t:
    for opt, flag in (("a", "CHI_hainan_honoured"), ("b", "CHI_hainan_settlement")):
        anchor = f'log = "[GetDateText]: [Root.GetName]: CHI_political_events.6.{opt}"\n'
        assert t.count(anchor) == 1, opt
        t = t.replace(anchor, anchor + f"\t\tset_country_flag = {flag} # OBT: Hainan chain\n\t\tOBT_hainan_begin = yes # OBT: Hainan chain\n")
    wr(p, t, b)

# 2. scripted effect in its own file, so the M5/M7 refresh scripts never touch it
p = "common/scripted_effects/99_OBT_crisis_scripted_effects.txt"
wr(p, """# Operation Blue Tiger milestone 8: starts the Hainan Island Incident chain (called from CHI_political_events.6)
OBT_hainan_begin = {
	if = {
		limit = {
			country_exists = USA
			NOT = { has_war_with = USA }
		}
		USA = { country_event = { id = obt_crisis.1 days = 1 } }
	}
}
""", False)

# 2b. focus links (mirrors the milestone 8 block in tools/spec.py)
p = "common/national_focus/05_taiwan.txt"; b = bom(p); t = rd(p).replace("\r\n", "\n")
if "OBT_2001_package_postponed" not in t:
    a = "\t\tavailable = {\n\t\t\tdate > 2001.4.1\n\t\t}\n\t\tcompletion_reward = {\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Focus TAI_na_2001_package\"\n"
    assert t.count(a) == 1
    t = t.replace(a, a.replace("date > 2001.4.1\n", "date > 2001.4.1\n\t\t\tOR = { NOT = { has_global_flag = OBT_2001_package_postponed } date > 2002.1.1 }\n"))
    k = "add_tech_bonus = { name = TAI_na_kidd_destroyers bonus = 0.5 uses = 2 category = CAT_destroyers }\n"
    assert t.count(k) == 1
    t = t.replace(k, k + "\t\t\tif = { limit = { has_global_flag = OBT_2001_aegis } add_tech_bonus = { name = TAI_na_kidd_destroyers_aegis bonus = 0.5 uses = 1 category = CAT_naval_electronics } }\n")
    wr(p, t, b)

# 3. yearly schedule
p = "common/scripted_effects/00_yearly_effects.txt"; b = bom(p); t = rd(p)
if "obt_crisis.20" not in t:
    t = t.replace("trigger_year_2001_events = {\n", "trigger_year_2001_events = {\n\tUSA = { country_event = { id = obt_crisis.20 days = 113 } } # OBT: 2001 arms package\n", 1)
    t = t.replace("trigger_year_2005_events = {\n", "trigger_year_2005_events = {\n\tJAP = { country_event = { id = obt_crisis.30 days = 49 } } # OBT: 2005 US-Japan 2+2 statement\n", 1)
    assert "obt_crisis.30" in t
    wr(p, t, b)
print("ok")
