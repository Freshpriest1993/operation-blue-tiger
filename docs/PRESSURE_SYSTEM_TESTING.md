# Cross-Strait Tension meter: test plan

Static validation passes; these checks need the game.

## Setup and display
1. New game as Taiwan, 1 January 2000. Cross-Strait Relations shows **20/100 · FRICTION**, the bar filled green to the first marker, FRICTION highlighted under the bar, and the stage line "Rises to Coercion at 40 · falls to Calm below 20".
2. Hover the title or bar (stage list and modifiers in force), each stage name (range and effects), the stage line (effects, decisions, how to move the meter) and each indicator (what raises and lowers it).
3. `tag CHI`: One China Strategy shows the same meter. Hong Kong, Macau, Tibet, Xinjiang, Inner Mongolia and Taiwan decisions from Millennium Dawn stay hidden until the One China Framework focus.
4. Check the national spirits of both countries: a **Cross-Strait Tension** modifier is present. At Friction China has +1% political power and -2% trade opinion; Taiwan has +2% war support and -2% trade opinion.

## Stage transitions
5. As China, raise tension (console `set_var CHI_taiwan_strait_tension 45` if available, otherwise Issue a Stern Warning). The bar, number and highlighted stage change immediately. Within a month the modifiers change to Coercion and both countries get a stage event.
6. Within 180 days, push to 65: the stage and modifiers change, but no event fires (cooldown).
7. Use a crisis hotline: tension and the bar drop immediately; the falling-stage event fires once the cooldown has passed.
8. Repeat for Crisis (60) and Brink (80). At Crisis, Taiwan's Declare a Blue Tiger Emergency becomes available without a blockade. Trade talks close above Coercion.
9. At Brink, with the One China Framework focus, Prepare a Taiwan Contingency appears. Taking it gives a war goal only: no war starts, nothing is annexed, Taiwan does not capitulate.
10. Let tension decay back to Calm: both countries gain +2% stability, +5% political power, +5% trade opinion and +2% factory output.

## Indicators and decisions
11. After a month, the bracketed numbers next to each indicator show the monthly change, green when it helps the country viewing it.
12. Every decision's tooltip starts with a one-line summary (for example "Lowers Cross-Strait Tension by 10"), shows its cost, and shows the cooldown after use. Locked decisions name the stage they need.

## AI and performance
13. Observer mode for two to three years at Crisis: both AIs use hotlines and quiet channels when stability is low; a Hegemon-path China warns and surges patrols; only an aggressive, stable Chinese AI prepares a war goal.
14. No daily lag: the meter updates monthly, at start-up and after its own decisions.
