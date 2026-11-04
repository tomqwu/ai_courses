# Design

## The Expedition

The learner site is a field guide for shipping AI products. It takes the **Quantic MBA** spine — a
programme with camps, progress and a serious editorial voice — and the **Duolingo** engine — short
legs, a visible route, immediate feedback and a reason to come back — without turning the course into
a game skin. The evidence system is the identity: the amber EVIDENCE chip, the file / lines / commit
header, the SOURCE footer and the pointer counts stay.

The world contributes **type, palette, density and one signature move**: a route map whose line is the
navigation and whose checkpoints stamp as the learner completes real work. Controls stay standard web
controls; a map node is a link, a pace is a select, a primary action is a button.

## Tokens

The existing Studio tokens are the palette; no new brand colours.

| Role | Token | Use |
|---|---|---|
| Ground | `--page` `#f6f4ef` | page, trailhead ground |
| Surface | `--surface` `#ffffff` | map panel, quiet panels |
| Ink | `--ink-strong`, `--ink`, `--ink-soft` | headings, body, secondary |
| Act | `--accent` `#2446c8` | current camp, route, primary panel |
| Evidence | `--proof-bg`, `--proof-line`, `--proof-ink` | field note, evidence labels |
| Done | `--done`, `--done-soft` | stamped camps, completed state |
| Line | `--line`, `--line-soft` | rules, borders, ahead route |
| Display | `--font-display` Bricolage Grotesque | camp titles, large numbers |
| Reading | `--font-body` IBM Plex Sans | prose, labels |
| Data | `--font-mono` JetBrains Mono | tags, source lines, counts |

The contour lines behind the home are a ground, not a texture: one SVG at low opacity, aligned to the
page, never behind body copy. Shadows are offset and soft; no hard offset shadow, no coloured
left-border cards.

## The signature move

The **route line** connects ten basecamps in a two-row snake. It is drawn in cobalt ahead, green once
travelled, and a marching cobalt dash on the leg from the current camp. A small arrow at each segment
midpoint shows the direction, including on the second row where the camps read right to left. A camp
is stamped with a check; a partly-read camp carries an amber ring and the words “in progress”. The
current camp has a halo and “you are here”. The line is not decoration: each camp is a link to its
module, and the map header states the camps and legs completed.

The **field note** is the second signature: a real exhibit from the current camp, with its source and
a link to the proof. It is the evidence system inside the learning loop.

## Home surface brief

The first viewport is the **trailhead**, not a sales page:

1. A breadcrumb (The full studio course / Camp N), an `h1` naming the current camp, and one sentence
   on the next leg. No eyebrow or kicker.
2. A stats strip: day trail, field notes, camps stamped, evidence log.
3. A route map on the left, the current camp marked; a rail on the right with the next action, today's
   pace and a field note.
4. A single primary action: **Start the first leg** for a first visit, **Continue** for a return.
   The first-visit variant also offers the 30-minute first win and the free beginner route as
   secondary links.
5. Below the fold, the learner can choose another route or open a camp in detail. The old sales
   sections still sit below the trailhead and are the next thing to redesign.

The first-visit and returning states are both built; `home.js` shows the one that fits the stored
progress. A first visit starts at Camp 0 with zero stamps and zero field notes; a return starts at the
camp of the last part opened, or the next unfinished camp after it. Nothing is ticked by hand.

The mobile composition puts the next action first, then the route as a vertical list of camps, then
today and the field note.

## The player and the check

The Learn page is a **recorder dock**, not a dark slab over the reading column. It is a paper surface
with the route rail on top, the play control in cobalt, the part and time in mono, and — once the
unit is recorded — a single **Next leg** link. The end of every teaching leg is a checkpoint card:
“Leg endpoint” before, “Leg stamped” after, with the next leg or next module. The stamp comes from a
recorded watch or read, never a hand tick. On a phone the dock sits above the four-mode tab bar, and
the content keeps enough bottom room that the last line is reachable.

The Check is a **one-question loop**: one card, a progress rail, the key and the learner's answer in
words, the rationale and its revisit link, then **Next question**. The last answer opens the result:
score, pass state, objectives to revisit, and **Next camp**. The result is the only celebratory
surface; it uses the green stamp, not confetti.

## Motion

- The route segment from the current camp marches; the current camp breathes; both stop under
  `prefers-reduced-motion`.
- The map is usable without motion. No section entrance animations.

## Rules

- No page kicker above a heading; the heading carries its own weight.
- No same-size icon + heading + text card grid as page structure; the map is the structure.
- No progress ring standing in for content; progress is the route and the stamp.
- No invented streak or XP: the day trail is consecutive local dates with a recorded study event;
  field notes are weights on those events.
- The evidence system and text-first transcripts survive every future surface.
