# Defense and National Reform: in-game test checklist

Milestone 9 adds the **Defense and National Reform** tab, real effects for Taiwan's national indicators, a U.S. arms procurement tracker and the deliveries themselves. Start a 2000 game as Taiwan unless a step says otherwise. Console commands are in `code`.

## Stage 1: dashboard, indicators and tracking

- [ ] The **Defense and National Reform** tab is visible from 1 January 2000, separate from Cross-Strait Relations.
- [ ] Nine bars show values in three rows: Military Reform, Washington and the Strait, Home Front. Pressure and Mainland Dependence use orange bars, the rest blue.
- [ ] At game start, every indicator effect in the tooltips reads **+0.0%** (effects are measured from the 2000 starting values).
- [ ] The **National Indicators** modifier appears on Taiwan (hover over the national spirits area) after the first month.
- [ ] `set_variable TAI_military_confidence 75` in Taiwan's scope, then wait a month: the Mil. Confidence bar grows, the tooltip shows +2.0% organization and +4.0% planning speed, and the modifier matches.
- [ ] The U.S. Confidence and U.S. Support tooltips each explain the difference between the two.
- [ ] The procurement lines read "Not offered" at start, then "Approved by Washington" after the April 2001 arms package (`event obt_crisis.20 USA`, then pick the first option).
- [ ] Postponing the package (third option) leaves all lines at "Not offered" until Taiwan completes *The 2001 Arms Package* in 2002.

## Funding (Special Defense Budget event, blue_tiger.23)

- [ ] "Pass the budget in full": Kidd line moves to *Funded, awaiting the transfer agreement*, P-3C to *Funded, awaiting procurement*, submarines to *Funded for design work*.
- [ ] "Accept a trimmed budget": only the Kidd line advances. **Pass the Remaining Special Budget** appears in the tab.
- [ ] "Let the budget stall": nothing advances. **Fund the Kidd Transfer** and **Pass the Remaining Special Budget** appear. Both need a Legislative Yuan that can pass legislation and enough treasury.

## Stage 2: deliveries

- [ ] **Kidd:** after *Accept the Kidd-Class Destroyers*, the line shows the refit countdown (about 31 months). At zero, ROCS Keelung and ROCS Su Ao appear in port with event obt_proc.1; about 11 months later ROCS Tso Ying and ROCS Ma Kong with obt_proc.2; 6 months later the line reads *In service* and Military Confidence rises by 5.
- [ ] **Expedite the Kidd Refit** cuts the remaining months by about 40% and can only be taken once.
- [ ] **P-3C:** after *Maritime Patrol Aircraft*, contract talks (about 20 months, event obt_proc.10), refurbishment (about 50 months), then 4 aircraft every 18 months until 12, then 6 months of training. The aircraft appear in the stockpile: P-3 Orion maritime patrol planes with By Blood Alone, naval_plane2 without it.
- [ ] **Negotiate Priority Delivery** halves the current stage; **Fund a Second Refurbishment Line** cuts it by 25% and halves the gap between batches.
- [ ] No ship or aircraft is ever delivered twice; reload a save and wait a few months after *In service* to confirm.

## Submarines

- [ ] After *The Submarine Question* with a full budget, event obt_proc.20 fires and the line reads *seeking a construction partner*.
- [ ] The three partner decisions show readable requirements (no blank lines). With the conditions unmet they cannot be taken.
- [ ] Raise the conditions (for the U.S. option: `set_variable TAI_us_confidence 80`, `set_variable TAI_military_confidence 60`, `set_variable TAI_reform_capacity 60`, and China's `CHI_taiwan_us_support` to 70), take the decision, wait 180 days: obt_proc.22, the line shows the builder, and **Appropriate the Submarine Construction Funds** appears.
- [ ] Drop a condition during the 180 days instead: obt_proc.23 fires, and that partner is locked for a year.
- [ ] With no partner by 1 January 2009: obt_proc.21 fires, the line reads *Failed*, and a submarine research bonus is granted.
- [ ] After the appropriation: first pair after about 6 years, then a pair each year (every 6 months with a second slip), 8 in total, then working up.

## Aegis (alternate history)

- [ ] Only if the U.S. chose "Approve everything, including Aegis": the Aegis line reads *awaiting funding* and **Fund the Aegis Destroyers** appears. Two pairs arrive about 7 and 8 years later; each delivery raises Cross-Strait Tension by 5.

## Suspension and safeguards

- [ ] Declare war on the United States, or set the flag `USA_withdrew_support_TAI` on the USA: the procurement header shows a red *Suspended* note and countdowns stop.
- [ ] At war with China while the United States is not: deliveries are suspended (the Strait is closed).
- [ ] Ships do not arrive while Taiwan controls no naval base; the delivery happens in the first month after a port is controlled again.
- [ ] Each **Cancel** decision stops its program, costs 5 U.S. Confidence, and keeps anything already delivered.

## AI

- [ ] Observe an AI Taiwan to 2010 (`observe`): the budget, refit and Han Kuang decisions are used, and the treasury is not drained into acceleration when money is short.
- [ ] With historical focus on, the AI does not pursue the submarine partner talks or Aegis funding, so the historical outcome (no foreign submarines) holds.
