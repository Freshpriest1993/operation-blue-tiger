# Choice groups 2 and 3: dependency review

Status: design proposal. Nothing has been changed; hiding for both groups stays switched off.
Author: Freshpriest1993
Diagrams: `deps_nuclear_policy.png`, `deps_national_identity.png`.

## Group 2: Nuclear Policy (Maanshan Expansion or Nuclear-Free Homeland)

### Exact prerequisite chains today

| Focus | ID | Prerequisites | Why it is lost after Maanshan |
| --- | --- | --- | --- |
| A Nuclear-Free Homeland | `TAI_su_gpt_nuclear_free` | Partners with the Greens | Mutually exclusive with Maanshan |
| Wind and Sun | `TAI_su_gpt_wind_and_sun` | A Nuclear-Free Homeland | Only parent excluded |
| Let the People Decide on Nuclear Power | `TAI_su_gpt_nuclear_referendum` | A Nuclear-Free Homeland | Only parent excluded |
| Seats on the City Councils | `TAI_su_gpt_council_seats` | Let the People Decide on Nuclear Power (and from December 2002) | Parent lost |
| A Green Minister | `TAI_su_gpt_green_minister` | Wind and Sun **and** Seats on the City Councils | Both parents lost |
| The Green Conscience (capstone) | `TAI_su_gpt_conscience` | A Green Minister **and** The Civil Society Alliance **and** Ecological Tax Reform | A Green Minister lost |

**The five affected focuses** are Wind and Sun, Let the People Decide on Nuclear Power, Seats on the City Councils, A Green Minister and The Green Conscience. A Nuclear-Free Homeland itself is the excluded choice.

**Who controls the exclusion:** it is defined on AUG's Maanshan focus (Silicon Island energy chain, available to any government). A Pan-Blue government can take Maanshan early, which permanently removes the Green Party's capstone even if the Greens later join a Pan-Green government.

### Possible alternative routes

| Option | Change | Effect | Touches AUG's content? |
| --- | --- | --- | --- |
| **N1 (recommended)** | Wind and Sun and Let the People Decide on Nuclear Power each accept **either** A Nuclear-Free Homeland **or** Environmental Impact Assessment | The Greens can still reach their capstone after Maanshan, through renewables and a nuclear referendum instead of a phase-out. The exclusive pair is unchanged. Hiding Nuclear-Free Homeland then hides only that one focus | No: two prerequisite lines in the Green branch only |
| N2 | Maanshan excludes Nuclear-Free Homeland only while a Pan-Green government is in office | Closer to history (the fight was between governments), but mutual exclusion cannot depend on conditions, so it would become availability checks on both focuses | Yes: changes Maanshan |
| N3 | Remove the exclusion; Nuclear-Free Homeland after Maanshan triggers a decommissioning event instead | Most historical (Taiwan expanded nuclear power and later phased it out), but a gameplay change on both sides | Yes |

**Historical note for N1:** referendums on nuclear power were held in Taiwan in 2018, 2021 and 2025 regardless of which nuclear policy was in force, and renewable expansion went ahead alongside nuclear plants. So a Green route through renewables and a referendum fits even after Maanshan.

**Gameplay implications of N1:** Greens who skip Nuclear-Free Homeland also skip its spirit upgrade (Green programme I to II); the capstone replaces both anyway. No focus becomes reachable that conflicts with the exclusive choice.

## Group 3: National Identity (Status Quo or Name Rectification)

### Today

Taiwan's Own Path (DPP capstone) requires **all three**: Join the UN as Taiwan, A New Generation and The Economic Advisory Conference. Join the UN as Taiwan is reachable only through Name Rectification → The Council Ceases to Function. Reaffirm the Status Quo leads nowhere, so choosing it makes the capstone impossible.

### Proposed design (D2): a status-quo route to the capstone

| Change | Detail |
| --- | --- |
| **One new focus** after Reaffirm the Status Quo: **"The Republic of China (Taiwan)"** | From 2006. The DPP's status-quo framing of sovereignty: Taiwan is already a sovereign state under its current name, so no formal change is needed. Rewards to be set with Foggy (placeholder direction: Taiwanese identity and US confidence up, Cross-Strait tension down) |
| **Taiwan's Own Path** | Requires (Join the UN as Taiwan **or** The Republic of China (Taiwan)) **and** A New Generation **and** The Economic Advisory Conference |
| **Mutual exclusion unchanged** | A player still cannot complete both Reaffirm the Status Quo and Name Rectification |

**Why this route:** it gives the status-quo choice its own 2006–2007 step, so both routes take a similar time to reach the capstone. The name-rectification route keeps its higher identity gains and higher tension and US costs.

**Gameplay implications:**
1. **Tree size:** 368 → 369 focuses.
2. **Republic of Taiwan (AUG's focus).** It currently requires Taiwan's Own Path or the TSU capstone. With D2, a status-quo DPP could reach the capstone and then declare a Republic of Taiwan, which contradicts the choice. **Proposed guard** for AUG to approve: Republic of Taiwan is not available after Reaffirm the Status Quo, unless reached through the TSU capstone. Without that guard, D2 would open a contradictory route.
3. **Hiding afterwards:**
   - choosing Status Quo hides Name Rectification, The Council Ceases to Function and Join the UN as Taiwan, and the capstone stays visible;
   - choosing Name Rectification hides Reaffirm the Status Quo and the new focus.
4. **AI:** the Historical behaviour follows the name-rectification route as history did. Accommodation-type behaviours would prefer the status-quo route.

**Alternative (D1, no new focus):** Taiwan's Own Path accepts (Join the UN as Taiwan **or** Reaffirm the Status Quo). It is simpler, but the status-quo route becomes two focuses shorter and could reach the capstone years earlier, before 2007.

## Decisions needed

1. **Nuclear Policy:** take N1 to AUG for approval (no change to his focus), or discuss N2 or N3 with him?
2. **National Identity:** approve D2 (one new focus and an "either" prerequisite on Taiwan's Own Path)?
3. **Republic of Taiwan:** approve the proposed guard on AUG's focus, to be confirmed with AUG?

Once decided, each change will be its own commit, followed by the hiding for that group in a separate commit.
