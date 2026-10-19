# Design note: the Failed Crusade and the ROCAF junta

Status: proposal for review (AUG, FoggyBottom). No code has been written.
Revised: the way out now uses decisions, in line with the extend-first rule in `PASS_VII_MATRIX.md`.
Author: Freshpriest1993

## Summary

When Taiwan's war to reclaim the mainland ends without victory, the outcome should depend on who was winning the argument at home. The Postwar Vision balance of power already tracks this. A defeat with the hardliners ascendant opens a military crisis that can end in an ROCAF junta. A defeat with the island already turning toward self-determination ends much as it does today. The junta is a playable failed state with a way back to democracy, which gives the ROCAF party slot a purpose.

## Where things stand today

| Piece | Current behaviour |
| --- | --- |
| `TAI_update_reclamation` (`99_TAI_scripted_effects.txt`) | When the reclamation war ends without Beijing capitulating, clears `TAI_reclamation_war` and fires `reclamation.18` |
| `reclamation.18` "The Crusade Falters" | One option: -5% stability, -50 political power, Postwar Vision +20% toward Self-Determination, Taiwanese identity +10 |
| `reclamation.5.b` (armistice) | Clears the war flag itself, so it does not fire `reclamation.18`. Unchanged by this proposal |
| `TAI_reclamation_bop` (`common/bop/TAI.txt`) | Restoration -100% to -20%, Contested -20% to +20%, Self-Determination +20% to +100% |
| `TAI_follow_chiang_teach` (National Glory) | Puts the government on the `Nat_Fascism` slot with John Chiang as leader |
| Party names | `Nat_Fascism` is named "(CDSP) China Democratic Socialist Party"; `Nat_Autocracy` is "(ROCAF) Republic of China Armed Forces" and is never used |

The event text already says "The generals blame the politicians", but nothing in the game follows from it.

**Existing issue:** unless the National Glory path renames its party (still to confirm), the National Glory dictatorship rules under the CDSP's name.

## Proposal

### 1. `reclamation.18` branches on the Postwar Vision

At the moment of defeat:

| Balance of power | Outcome |
| --- | --- |
| Restoration side (below -20%) | **Military crisis**: `reclamation.18` leads to the new event "The Generals' Ultimatum" |
| Contested (-20% to +20%) | **Political crisis**: the government falls and early elections are called |
| Self-Determination side (above +20%) | Current behaviour, unchanged |

The coup is never automatic. It follows from how the player ran the war and what the island believed while it was fought.

### 2. "The Generals' Ultimatum" (new event)

The General Staff demands the government hand over power to "restore order".

| Option | Effect (values are placeholders for balance) |
| --- | --- |
| **Accept military rule** | Government moves to the `Nat_Autocracy` (ROCAF) slot, elections suspended, a fictional senior officer becomes leader, the Failed Crusade spirit is added |
| **Resign and call elections** | Government stays democratic; -10% stability; a 180-day "Caretaker Government" spirit; Postwar Vision moves 10% toward Self-Determination |
| **Refuse the generals** | Government stays; a "Divided Army" spirit (division attack and defence penalty, organisation penalty) for 365 days; a follow-up event a few months later that can soften or worsen it. No civil war |

AI weights: accept only when `TAI_ai_behavior` is the National Glory or reclamation path; otherwise strongly prefer resigning.

### 3. The junta as a failed state

The **"A Failed Crusade"** national spirit (placeholder values):
- stability -15%
- political power -20%
- war support +10%
- consumer goods +5%
- monthly population or economic strain, to be tuned against existing MD failed-state spirits

**Abroad:**
- US confidence falls (`TAI_us_confidence`).
- If the United States guarantees Taiwan, the guarantee is withdrawn, as the National Glory path already does.
- Opinion penalty with democratic Western countries.

**Over time:** a hidden yearly check makes the spirit worse while the junta remains in power without reform.

### 4. A way out (decisions, no new focuses)

The way out uses decisions in the existing reclamation category, so the tree stays at its current size.

- **"Lift Martial Law"** is available only once the Postwar Vision is back above 0%. It leads to a referendum event and a return to the democratic government, echoing the end of martial law in 1987.
- **"Garrison State"** stays authoritarian. It removes the worsening timer, keeps a permanent stability penalty, and has stronger defensive bonuses.

The Postwar Vision bar becomes the junta's main mechanic. Junta decisions such as press controls or loyalty purges move it toward Restoration; reform decisions move it toward Self-Determination.

### 5. Party slots

| Slot | Role after this change |
| --- | --- |
| `Nat_Fascism` | National Glory regime, renamed with `set_party_name` when that path is taken, so it no longer appears as the CDSP |
| `Nat_Autocracy` (ROCAF) | The junta |
| CDSP | Name kept on `Nat_Fascism` outside the National Glory path, or moved to an unused slot (to discuss) |

## Rules this design keeps

- No automatic war, annexation or capitulation. The coup is conditional and the player chooses.
- No real, named Taiwanese officers are portrayed leading a coup; the junta leader is fictional or a role.
- AUG's National Glory path keeps its own victory outcome. Only the slot naming and the shared failure event change.
- Any change to shared files is recorded in `docs/CHINA_FILE_CHANGES.md`.

## Estimated scope

| Item | Files |
| --- | --- |
| 2 to 3 new events, `reclamation.18` reworked | `events/Taiwan_Reclamation.txt` |
| 3 to 4 spirits | Taiwan ideas file |
| Exit decisions | `TAI_reclamation_category` decisions |
| Party slot naming | `TAI_follow_chiang_teach`, party localisation |
| Localisation | `MD_TAI_reclamation_l_english.yml` |
| AI weights | Events and `TAI_ai_behavior` checks |

## To check by hand before building

- The party-array index for each slot. National Glory uses index 21 for `Nat_Fascism`; `Nat_Autocracy` is assumed to be 22.
- Whether the National Glory path already renames the nationalist party anywhere outside `TAI_follow_chiang_teach`.
- Whether any other content reads `reclamation.18` or expects its current single option.
- Balance values: every number above is a placeholder.

## Questions for review

1. AUG: are you happy for the National Glory government to be renamed off the CDSP slot, and for a failed National Glory war to lead into this crisis?
2. Both: keep the CDSP on `Nat_Fascism` outside National Glory, or move it to an unused slot?
