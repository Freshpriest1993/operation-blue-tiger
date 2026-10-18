# Taiwan 2000 Order of Battle Audit

As of 18 October 2026. Historical cutoff: 1 January 2000.

## Summary

Taiwan's navy and fighter fleet in Millennium Dawn were close to history; the army was the outlier. MD started Taiwan with a pre-1997 division army that Project Jingshi had largely replaced with brigades by January 2000. It also shipped with several fake or renumbered formations and some equipment delivered after 2000.

**Implemented in Milestone 10 (18 October 2026).** The starting OOB and reserve mobilization below are now in the mod:

- **Army:** 40 starting land units: 34 named brigades, 4 unnumbered garrison brigades (2 in the 6th Corps, 1 in the 8th Corps, 1 in Hua-Tung) and the 2 Marine divisions. All brigades use the naming pools, so new brigades never repeat a starting number.
- **Stockpile fixes:** CH-47SD, T86 and the duplicate Bell 206 removed. AH-1W set to 42, M60A3 to 169, M48A5 to 100, CM-21 to 225 and Avenger to 74.
- **Air:** F-5s cut to about 160. Squadrons renamed with their wing and base, and the 8th and 14th Squadrons added.
- **Navy:** destroyer names corrected and the main fleet moved to Tsoying. 12 Jin Chiang and 49 Hai Ou boats added as Hsiung Feng I missile craft.
- **Reserve mobilization:** built as designed (see below).

The 373rd and 395th are in the OOB on the 351st template, with their conversion dates and 2000 equipment still open.

Findings before the rebuild:

- **Army: needed a rebuild.** MD had 7 infantry and 2 mechanized divisions plus 4 armored brigades with pre-1998 numbers (2nd, 4th, 5th, 6th). Three divisions were marked as fake names in the file and sat on Kinmen, Matsu and Tainan. Historically the army was converting to about 39 combined-arms brigades: 14 strike and 25 garrison, under 3 corps and 4 defense commands.
- **Marines: correct for the date.** Two divisions (66th and 99th) existed on 1 January 2000. Brigades came with the August 2000 reorganization.
- **Aviation and special forces: one fake unit.** The 601st Air Cavalry Brigade and the 862nd Special Warfare Brigade existed; the 603rd did not exist in 2000. The 602nd, which did exist, was missing.
- **Navy: counts right, names partly wrong.** 7 destroyers, 21 frigates and 4 submarines. Three destroyer names (Lo Yang, Nan Yang, Lai Yang) belonged to ships retired before 2000. About 60 missile boats and the main base at Tsoying were missing.
- **Air force: fighters right, F-5s doubled.** F-16, Mirage 2000-5 and IDF totals matched history. MD fielded about 300 F-5s against 144-200 historically, and labeled squadrons as groups.
- **Equipment: a handful of anachronisms and duplicates.** CH-47SD (delivered 2001-02), T86 rifles (2002) and a duplicated Bell 206 entry among them.

## Sources and confidence

The strongest sources for January 2000 are the FAS Taiwan pages updated in April 2000, which draw largely on IISS data, and Armor Quarterly unit histories published by Taiwan's Ministry of National Defense. The 2000 National Defense Report and the IISS *Military Balance 2000-2001* were not accessible online.

Every figure carries one of three labels:

- **Confirmed:** stated directly by a source for 1999-2000, or by a unit history with an exact date.
- **Approximate:** derived from a nearby year, a sale record or a target, not a dated count.
- **Conflicting:** sources disagree, and the range is given.

MD's setup was read from `TAI - Taiwan.txt`, `TAI_2000_nsb.txt`, `TAI_2000_nonnsb.txt`, `TAI_2000_bba.txt`, `TAI_2000_nonbba.txt` and `TAI_2000_naval_mtg.txt`. `TAI_names_divisions.txt` was used only to identify formations, not as proof that they were on the map.

## Army

In January 2000 the army was mid-way from divisions to brigades. Personnel figures conflict: FAS gives about 220,000 army and 270,000 ground forces including Military Police (April 2000). The Jingshi target was about 200,000 army inside a 385,000-400,000 total force.

| Element | Historical, 1 Jan 2000 | MD before Milestone 10 | Verdict |
| --- | --- | --- | --- |
| Higher command | 3 army corps (6th north, 8th south, 10th central); Kinmen, Matsu, Penghu and Hua-Tung defense commands (confirmed) | Corps only as comments; offshore islands held 8th Corps divisions | Restructured |
| Combat units | Converting to 39 combined-arms brigades: 14 strike, 25 garrison (end state 2001, confirmed). 8 division HQs kept as command posts: 16, 19, 26, 33, 34, 46, 49, 51 | 7 infantry divisions, 2 mechanized divisions | Wrong unit level for the date |
| Armor | Armored (5xx) and armored infantry (3xx) brigades, formed 1998-1999 (confirmed) | 2nd, 4th, 5th and 6th Armor Brigades | Pre-1998 numbering |
| Fake formations | None | 5th, 6th and 18th Infantry Divisions, marked `#fake name`, on Kinmen, Matsu and Tainan | Removed |
| Aviation and Special Warfare Command | 601st and 602nd Air Cavalry Brigades, 862nd Special Warfare Brigade (confirmed). The 603rd is judged probably nonexistent even in 2004 | 601st, 603rd, 862nd | 603rd replaced with 602nd |
| Marines | 66th and 99th Marine Divisions plus support regiments; brigades came with the August 2000 plan (confirmed) | 66th and 99th Marine Divisions | Correct; template slimmed |
| Reserves | 7 reserve divisions on paper; 1.5 to 3.87 million registered reservists (conflicting) | None on the map | Kept off the map; mobilization decisions added |
| Missile units | Missile Command with the 606th and 608th groups (post-reform, approximate for 2000) | SAMs only as stockpile | Not modeled |

## The Jingshi reorganization

By 1 January 2000 the armor had already become brigades; for most infantry the exact conversion date is not published. Armor Quarterly dates Jingshi to January 1998 through November 2004, longer than the 1997-2001 usually cited.

| Date | Change | Confidence |
| --- | --- | --- |
| 2001 | End state: all divisions and independent brigades abolished, 39 combined-arms brigades (14 strike, 25 garrison) | Confirmed |
| Aug 2000 | MND announces the Marine reorganization: divisions phased out for the 66th, 77th and 99th Brigades | Confirmed |
| Apr 2000 | FAS still lists 10 infantry divisions, 2 mechanized divisions and 6 armored brigades, probably from IISS data that lagged the reform | Conflicting |
| 1 Oct 1999 | 64th Independent Brigade becomes the 564th Armored Brigade, Kaohsiung | Confirmed |
| 1 Apr 1999 | 584th (Kinmen), 586th (Houli) Armored and 351st Armored Infantry Brigades formed | Confirmed |
| 1998 | 42nd Armored Brigade becomes the 542nd under 6th Army Corps | Confirmed |
| Aug 1998 | General Staff orders a stand-down in operating tempo for units being reorganized | Confirmed |
| 1 Jul 1997 | Jingshi starts: cut senior staff, fill the units, reduce the force toward 400,000 | Confirmed |

Garrison brigades at the end state: 6th Corps 7, 8th Corps 4, 10th Corps 5, Hua-Tung 2, Penghu 1, Kinmen 3, Matsu 3.

## Roster check, 1 January 2000 cutoff

| Brigade | Established | Organization, 1999-2000 | Equipment, 1999-2000 | Status for 1 Jan 2000 |
| --- | --- | --- | --- | --- |
| 351st Armored Infantry 'Leiting', 6th Corps, Guishan | 1 Apr 1999 (Armor Quarterly; its 2nd Tank Battalion also dated 1 Apr 1999) | 3 armored infantry, 2 tank, 1 artillery battalion | M60A3, CM21, M113, M109A2 | Included |
| 373rd Armored Infantry 'Tianshan', 10th Corps, Dali | Ex-Independent 73rd Brigade; conversion date not found | Not published for 2000; tank companies all CM11 in 2006 | CM11 (2006 evidence only) | Included on the 351st template; equipment approximate |
| 395th Armored Infantry, 8th Corps | Conversion date not found | Not published | Not found | Included on the 351st template; equipment approximate |
| 542nd Armored 'Xunlei', 6th Corps, Hukou | 1998 | 3 tank, 2 armored infantry battalions | CM11, M109 | Included |
| 584th Armored 'Dengbu', Kinmen Defense Command | 1 Apr 1999 | 2 tank, 1 armored infantry, 1 artillery battalion | M60A3; M41A3 replaced by 44 M41D in Sep 1999; CM21; 105 mm towed howitzers | Included (island template) |
| 586th Armored 'Zhongshan', 10th Corps, Houli | 1 Apr 1999 | 3 tank, 2 armored infantry, 1 artillery, 1 support battalion | 112 M60A3; 24 M109A2 | Included |
| 564th Armored 'Shaokang', 8th Corps, Alian | 1 Oct 1999 | 3 tank, 2 armored infantry, 1 artillery battalion | About 120 CM11, 6 M41A3, about 100 M113/CM21, 24 M109A2 | Included |
| 195th Infantry, Dongyin (Matsu) | Unit history begins July 1999 | Not published | Not found | Included |
| 269th Mechanized Infantry, 6th Corps, Yangmei | From the 269th Division; date not found | Not found | Not found | Excluded until dated |
| 200th Motorized Infantry 'Gubei', 10th Corps | Date not found; merged with the 373rd on 1 Jul 2006 | Not found | Not found | Included from the names file; verify |

**Reserves:** the Reserve Command began building reserve brigades only in September 2000, with a goal of 21. Nine reserve brigades are reported activated in April 2004. None of them belong in the starting OOB.

## Starting OOB as implemented

| Formation | Type | Parent | MD state | Confidence |
| --- | --- | --- | --- | --- |
| 542nd Armored Brigade 'Xunlei' | Armored | 6th Corps | Hsinchu | Confirmed (1998) |
| 351st Armored Infantry Brigade 'Leiting' | Armored infantry | 6th Corps | Taipei (Guishan, Taoyuan) | Confirmed (1 Apr 1999) |
| 452nd, 453rd (151st Div), 102nd, 103rd, 108th Infantry Brigades + 2 unnumbered | Infantry | 6th Corps | Taipei, Hsinchu | Names file; unnumbered from the end-state count |
| 586th Armored Brigade 'Zhongshan' | Armored | 10th Corps | Taichung | Confirmed (1 Apr 1999) |
| 373rd Armored Infantry Brigade 'Tianshan' | Armored infantry | 10th Corps | Taichung | Documented; conversion date unverified |
| 200th Motorized Infantry Brigade | Motorized | 10th Corps | Taichung | Names file; date unverified |
| 104th, 157th, 169th, 616th, 617th (206th Div) Infantry Brigades | Infantry | 10th Corps | Taichung | Names file |
| 564th Armored Brigade 'Shaokang' | Armored | 8th Corps | Kaohsiung | Confirmed (1 Oct 1999) |
| 395th Armored Infantry Brigade | Armored infantry | 8th Corps | Kaohsiung | Documented; conversion date unverified |
| 298th Motorized Infantry Brigade 'Puchuan' | Motorized | 8th Corps | Tainan | Names file |
| 129th (210th Div), 178th (26th Div Cmd), 618th (206th Div) Infantry Brigades + 1 unnumbered | Infantry | 8th Corps | Tainan, Kaohsiung | Names file |
| 584th Armored Brigade 'Dengbu'; 119th, 127th, 158th Infantry Brigades | Armored, infantry | Kinmen Defense Command | Kinmen | Confirmed / names file |
| 193rd, 194th, 195th Infantry Brigades | Infantry | Matsu Defense Command | Lienchiang | Names file; 195th confirmed |
| 503rd Armored Brigade; 168th Infantry Brigade | Armored, infantry | Penghu Defense Command | Penghu | Names file |
| 128th Infantry Brigade + 1 unnumbered | Infantry | Hua-Tung Defense Command | Hualien | Names file |
| 601st, 602nd Air Cavalry Brigades; 862nd Special Warfare Brigade | Air cavalry, special forces | Aviation and Special Warfare Command | Hsinchu, Taichung, Taipei | Confirmed |
| 66th, 99th Marine Divisions | Marine | Marine Corps | Taipei (Linkou), Kaohsiung (Tsoying) | Confirmed |

Templates: Infantry Brigade (3 infantry + 1 artillery battalion), Motorized Infantry Brigade (3 + 1), Armored Infantry Brigade (3 armored infantry, 2 tank, 1 SP artillery), Armored Brigade (3 tank, 2 armored infantry, 1 SP artillery), Island Armored Brigade (2 tank, 1 armored infantry, 1 artillery; the 584th and 503rd), Air Cavalry Brigade (attack helicopters + 2 air assault), Special Warfare Brigade, Marine Division (6 marine + 2 artillery). The 206th and 210th Division brigades may have been training rather than garrison brigades in 2000; this is still open.

**Removed:** the 5th, 6th and 18th Infantry Divisions (fake); the 16th, 26th, 49th and 51st Infantry Divisions; the 3rd and 8th Mechanized Divisions; the 2nd, 4th, 5th and 6th Armor Brigades (renumbered); the 603rd Air Cavalry Brigade.

## Air Force

| Type | Historical, early 2000 | Implemented |
| --- | --- | --- |
| F-16A/B Block 20 | 150 ordered 1992, deliveries from 1997; 4 lost by April 2000 (confirmed) | 146 in 7 squadrons (4th Wing Chiayi, 5th Wing Hualien) |
| Mirage 2000-5 | 60 delivered; 2 lost (confirmed) | 58 (2nd Wing, Hsinchu) |
| F-CK-1 IDF | 130 (confirmed) | 130 (1st Wing Tainan, 3rd Wing Ching Chuan Kang incl. the 8th Squadron) |
| F-5E/F and RF-5E | 144 (FAS, April 2000) to about 200 (IISS-era estimates) (conflicting) | About 160 (7th Wing Taitung, Taoyuan 15th and 16th, 12th TRS, reserve airframes) |
| AT-3, S-2T, E-2T, C-130H | About 58, 31, 4 and 20 | Unchanged |

Wings and bases follow FAS (April 2000). Squadron numbers were mislabeled as groups; a group is the three-squadron level.

## Navy

| Class | Historical, 1 Jan 2000 | Implemented |
| --- | --- | --- |
| Destroyers, Gearing Wu Chin III | 7: Chien Yang 912, Liao Yang 921, Shen Yang 923, Te Yang 925, Yun Yang 927, Chen Yang 928, Shao Yang 929 (confirmed count; status of remaining Sumner and FRAM ships conflicting for 2000) | All 7, at Tsoying |
| Frigates, Knox (Chi Yang) | 8, FFG-932 to 939; the last four commissioned 1998-99 (confirmed) | All 8, at Keelung |
| Frigates, Cheng Kung (Perry) | 7, PFG-1101 to 1109, commissioned 1993-98 (confirmed) | All 7, at Tsoying |
| Frigates, Kang Ding (La Fayette) | 6, commissioned 1996-98 (confirmed) | All 6, at Tsoying |
| Submarines | Hai Lung 793, Hai Hu 794; Hai Shih 791, Hai Pao 792 (confirmed) | All 4, 256th Submarine Group |
| Missile boats | 12 Jin Chiang (1994-2000), about 50 Hai Ou (approximate) | 12 Jin Chiang (Tsoying), 49 Hai Ou (Keelung) |
| Mine warfare, amphibious | About 12 and 22 | Not modeled |

## Equipment

| Item | Historical, 1999-2000 | Before | Implemented |
| --- | --- | --- | --- |
| CH-47SD Chinook | 9 sold 1998, delivered 2001-02 | 8 | Removed |
| T86 rifle | Adopted 2002 | 200 (non-NSB) | Removed |
| Bell 206 / TH-67 | 30 | 30 + 30 duplicate | 30 |
| AH-1W Cobra | 42 (FAS, April 2000); 21 more sold 1997 | 53 | 42 |
| M60A3 | 169 in the 1999 column (conflicting with later totals) | 189 / 0 | 169 in both setups |
| M48A5 | 100 (confirmed) | 189 (non-NSB) | 100 |
| CM-21 | 225 (confirmed) | 100 (NSB) | 225 |
| Avenger | 74 launchers sold 1996 | 100 | 74 |
| M24, TRF1, T69 (NSB), M42 Duster, Nike Hercules, Humvee | See notes | Unchanged | Open: verify |

## Reserve mobilization

Reserve formations appear only through mobilization decisions, never in the starting OOB.

| Stage | Available when | Costs | What it does |
| --- | --- | --- | --- |
| 1. Peacetime preparation | Always | Reserve Readiness Program: political power upkeep. Annual refresher recall: 25 political power, treasury and a little stability | Raises Reserve Readiness (starts at 15). Readiness sets the experience of mobilized brigades (0.10, 0.18 or 0.25). No units spawn |
| 2. Partial mobilization | Crisis-level tension, a Chinese blockade or war; readiness 20+; 12,000 manpower available | 100 political power, factory and dockyard output, stability | 4 reserve infantry brigades, 15 and 30 days after the decision |
| 3. General mobilization | Partial active; war with China or Brink-level tension; 24,000 manpower available | 150 political power, heavier economic penalty, stability | Up to 8 more brigades in pairs every 15 days (12 total) |
| Demobilization | No war with China; tension below Crisis | None | Disbands every mobilized reserve brigade, returning its manpower and equipment; one-year cooldown |

Safeguards: a locked reserve template (demobilization removes exactly those units), spawn caps per stage, units filling from the stockpile with 1% starting equipment, generic "Reserve Infantry Brigade" names from their own naming pool, and AI weights that mobilize only in a crisis or war.

## Open questions

- When were the 373rd and 395th converted, and what tanks did they field in 1999-2000?
- Were the 616th to 618th (206th Division) and the 129th (210th Division) garrison or training brigades in 2000?
- When were the 200th and 298th Motorized Infantry Brigades and the 269th Mechanized Infantry Brigade established?
- The 2000 National Defense Report and IISS 2000-01 would settle the personnel and F-5 figures.

## Sources

- [FAS: ROC Army (April 2000)](https://irp.fas.org/world/taiwan/army-intro.htm)
- [FAS: Army equipment inventory (April 2000)](https://irp.fas.org/world/taiwan/army-inventory.htm)
- [FAS: ROC Air Force table of organization (April 2000)](https://irp.fas.org/world/taiwan/taf-toe.htm)
- [GlobalSecurity: ROC Army](https://www.globalsecurity.org/military/world/taiwan/army-intro.htm)
- [GlobalSecurity: ROC Army brigade order of battle](https://www.globalsecurity.org/military/world/taiwan/army-orbat.htm)
- [GlobalSecurity: ROC Marine Corps](https://www.globalsecurity.org/military/world/taiwan/rocmc.htm)
- [GlobalSecurity: ROC Navy](https://www.globalsecurity.org/military/world/taiwan/navy.htm)
- [Hazegray World Navies Today: Taiwan (March 2002)](https://hazegray.org/worldnav/asiapac/taiwan.htm)
- [Wikipedia: List of Republic of China Navy ships](https://en.wikipedia.org/wiki/List_of_Republic_of_China_Navy_ships)
- [Seaforces: Republic of China Navy ships](https://www.seaforces.org/marint/Republic-China-Navy/ships.htm)
- [Wikipedia: List of U.S. arms sales to Taiwan](https://en.wikipedia.org/wiki/List_of_U.S._arms_sales_to_Taiwan)
- [Wikipedia: 542nd Armored Brigade](https://en.wikipedia.org/wiki/542nd_Armored_Brigade_(Taiwan))
- [Wikipedia (Chinese): ROC Army, Jingshi structure](https://zh.wikipedia.org/zh-tw/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E9%99%B8%E8%BB%8D)
- [Wikipedia (Chinese): Jingshi program](https://zh.wikipedia.org/wiki/%E7%B2%BE%E5%AF%A6%E6%A1%88)
- [Armor Quarterly 273: 564th Armored Brigade](https://www.mnd.gov.tw/File/49253)
- [Armor Quarterly 267: 586th Armored Brigade](https://www.mnd.gov.tw/NewUpload/202304/04%E4%B8%AD%E5%8F%B0%E7%81%A3%E5%8B%81%E6%97%85%E9%99%B8%E8%BB%8D%E8%A3%9D%E7%94%B2%E7%AC%AC%E4%BA%94%E5%85%AB%E5%85%AD%E6%97%85%20-%20%E9%8D%BE%E5%B1%B1%E9%83%A8%E9%9A%8A0407_232220.pdf)
- [Armor Quarterly 277: 584th Armored Brigade](https://www.mnd.gov.tw/File/53572)
- [National Cultural Memory Bank: 195th Infantry Brigade history, Jul 1999 to Dec 2000](https://tcmb.culture.tw/zh-tw/detail?indexCode=Culture_Object&id=291107)
- [Armed Forces Reserve Command history](https://afrc.mnd.gov.tw/AFRCWeb/Unit.aspx?ListID=15&MenuID=45)
- [RAND: Transformation of Taiwan's Reserve Force (2017)](https://www.rand.org/pubs/research_reports/RR1757.html)
- [Personal blog: ROC Army unit list](https://blog.udn.com/0936331038/8596075) (low confidence)
- [Forum thread on the 373rd Brigade, 2005](https://www.coolaler.com/forums/threads/373.75992/page-2) (low confidence)
