# Learner site

The learner-facing build of the course: nine decks, one slide at a time, with narration, synchronized
captions, a transcript, and navigation that works with a keyboard.

```bash
cd course
make narration-preview   # free local preview voice (or `make narration` with ELEVENLABS_API_KEY)
make site                # generate index.html and mNN.html
make serve               # http://localhost:8043
```

`make site` is enough to read the decks; narration is layered on when recordings exist. A deck with no
recordings is still fully readable, and the player says so instead of failing.

## What is generated

| Path | Source | Committed? |
|---|---|---|
| `mNN.html`, `index.html` | `03-content/mNN-*/slides.md` + `06-production/narration/manifest.json` | No — generated |
| `narration.json` | `06-production/narration/manifest.json` | No — copied at build time |
| `assets/audio/…` | `generate_narration.py` | No — generated (see the narration README) |
| `assets/player.js`, `narration-media.js`, `player.css` | hand-written | **Yes** |
| `assets/fonts/source-sans-3.woff2` | Source Sans 3, SIL OFL 1.1 (licence travels with it) | **Yes** |
| `build_site.py`, `check_player.py` | hand-written | **Yes** |

## Design system

The presentation layer is ported from **ai_qe**, the third case study, because that site is the one
this course holds up as its own standard for publishing claims a skeptic can audit. What was borrowed,
and what was deliberately changed, is written down rather than implied:

| Borrowed | Detail |
|---|---|
| Typeface | Source Sans 3, self-hosted `woff2`, `font-display: swap`, preloaded |
| Palette | navy `#152e40` · teal `#096d69` · mint `#85d5c4` · ink `#405563` · paper `#fcfcfa` on `#eaf0ec` |
| The 16:9 master | `--frame-width: min(100vw - 32px, (100dvh - chrome - narration) * 16/9)`, `.slide { aspect-ratio: 16/9 }` |
| Container-query type | slide type is sized in `cqw`, so it scales with the frame instead of the viewport |
| Kicker + title | `M0.1 — Three archetypes` renders as kicker `M0.1` and title `Three archetypes`, exactly ai_qe's `02 / Strategic target state` |
| Source footer | every slide carries a footer with the deck tag, a transcript link and `NN / NN` |
| Modes | presentation (full screen), reading view, notes drawer, one 16:9 slide per printed page |
| Chapter grouping | `data-chapter` per slide; the picker is grouped with `<optgroup>` |

Changed for this course: proof slides (`<!-- _class: proof -->`) get a dark, accented treatment so the
evidence slides change the deck's rhythm; the vocabulary is limited to what these decks contain
(bullets, tables, code, takeaways, pillars, metrics); and the honesty badge for the preview voice keeps
its own light-theme styling because it must be legible wherever it appears.

## Transcripts

Every deck has a transcript, committed as Markdown rather than generated HTML:

```
learner-site/transcripts/m00.md … m08.md   one deck each
learner-site/transcripts/ALL.md            all nine modules in one file, with a table of contents
```

Each file carries the slide number, title, per-slide duration and caption method, then the spoken
words. **Speaker notes are excluded** — they are the presenter's version, not the narration. The words
are the approved narration scripts, so the transcript is a true text alternative to the audio and does
not change when the release voice is recorded. Each deck page has a **Transcript** link in its toolbar.

The convention that makes it checkable: **a line starting with `> ` is spoken narration and nothing
else.** Headings, timing and the voice note are ordinary lines, so `words()` over the blockquotes must
equal `words()` over the approved script. `build_site.py` asserts that at generation time,
`validate_narration.py` asserts it on the committed files, and `build_site.py --check` fails if they
are stale. Do not put metadata in a blockquote.

```
$ python3 06-production/narration/validate_narration.py --no-media
Transcripts verified: 10 documents match the approved scripts (22,239 words)
```

## Page structure

Each deck page is a 48px header, the 16:9 frame, a fixed navigation strip, and a notes dialog.

```
deck page
├── header        brand · module · slide meta · Play narration · Present ↗ · Read all
│                 Sources & notes · Transcript · voice chip
├── main.slides   one <section class="slide"> per slide
│                 ├── .kicker      M0.1, Type 1, Lab M0 (falls back to "M0 · Orientation")
│                 ├── h2#slide-N-title
│                 ├── .slide-content
│                 └── footer        deck tag / slide transcript / 01 / 19
├── nav           ← → · live status · chapter-grouped slide picker
└── dialog        speaker notes for the current slide
```

Slide variants: `slide-cover` (slide 1, always), `slide-proof` (from `_class: proof`).

### Modes

| Mode | Control | Behaviour |
|---|---|---|
| One slide at a time | default | `goTo()` hides every other slide; the narration panel sits below the frame |
| Presentation | **Present ↗** or <kbd>P</kbd> | full screen, dark chrome, trimmed header; <kbd>Esc</kbd> leaves it |
| Reading | **Read all** | every slide as one scrolling document, 1200px measure |
| Notes | **Sources & notes** or <kbd>N</kbd> | dialog with the current slide's presenter notes |
| Print | <kbd>⌘P</kbd> | one 16:9 slide per page (`@page 13.333in 7.5in`) |

A deck without JavaScript still shows every slide in order, and the reading view has a CSS fallback so
it works even if the script never runs.

### Other pages

Every generated deck page is:

```
body[data-narration-manifest][data-narration-deck][data-site-base][data-voice]
  header.deck-header          title, slide/narration counts, Play narration, Captions download
  p.voice-badge               only when the recordings are a preview voice
  main#slides
    section.slide#slide-N     aria-roledescription="slide", aria-labelledby="slide-N-title"
                                data-audio / data-captions / data-duration from the manifest
      .slide-content          the rendered slide
      details.slide-notes     the presenter notes (not read aloud)
  nav.deck-navigation         prev · slide picker · next · status · message
  section.narration-panel     injected by player.js before .deck-navigation
    .narration-caption        the current cue
    .narration-controls       play · replay · seek · time · speed · CC · auto-next
    .narration-meta           status · Retry captions · Transcript
  audio[data-narration-audio]
```

Slides after the first are `hidden` so the page does not flash 233 slides before the script runs. A
`<noscript>` block reverses that for no-JS readers, and `@media print` reveals every slide.

## Player behaviour

* **No autoplay, ever.** Play starts the current slide; auto-next (on by default, opt-out) continues.
* **One clock.** Captions, the seek bar and the time readout all derive from `audio.currentTime`.
* **One audio owner per frame tree.** `narration-media.js` claims focus synchronously before buffering,
  coordinates across tabs via `BroadcastChannel` (with a `localStorage` fallback), and a cancelled play
  request cannot steal focus back.
* **A beat between slides.** Auto-next waits 2000 ms, or 700 ms under `prefers-reduced-motion`, and is
  cancelled by any navigation, seek, dialog or hidden tab.
* **Resume.** The last slide is remembered per deck in `localStorage` and offered back on return.
* **Captions on by default.** CC toggles them; every slide also has the full transcript in a dialog,
  labelled with the voice and the caption method.
* **A slide without a recording still navigates**, with an explanation rather than a dead player.
* **Keyboard:** `→`/`Space`/`PageDown` next, `←`/`PageUp` previous, `Home`/`End` first/last. Shortcuts
  are ignored while typing in a control or while a dialog is open.

## Accessibility

* One `h1` per page; slides are `<section>` landmarks labelled by their own heading.
* A polite status region announces `Slide N of M — title` on every move, and a separate live region
  announces playback and failure states.
* A skip link jumps to the slides. Focus follows the slide heading, not the window.
* Visible focus rings on every control; `aria-pressed` on Play and CC; `aria-valuetext` on the seek bar.
* Caption text is rendered as text, never as markup, and the cue element is `aria-live="off"` so a
  screen reader is not flooded during playback.
* Reduced-motion users get no smooth scrolling and a shorter auto-advance beat.
* Print output contains every slide, without the player chrome.

## Verifying the site

`check_player.py` does two things: it drives the player's behaviour, and it **measures the rendered
frame** rather than trusting the stylesheet. The second part exists because a design port can look
right in source and still render wrong — and it caught exactly that during this work (the `@font-face`
URL was copied from ai_qe's `/assets/css/` layout while our CSS sits in `/assets/`, so the font 404'd
and silently fell back).

The probe loads the deck in a same-origin iframe at a fixed 1600x1000 viewport, then asserts geometry
and interaction:

```
$ python3 learner-site/check_player.py --deck m06 --measure
{
  "slideWidth": 1228, "slideHeight": 691, "ratio": 1.778, "aspectRatio": "16 / 9",
  "overflowing": false,
  "fontLoaded": true, "fontsStatus": "loaded",
  "kicker": "AI Product Studio · Module 6 of 9",
  "title": "The Expertise Product: Evidence, Routing, Editions",
  "footer": "AI Product Studio / M6 · The Expertise Product / Slide transcript / 01 / 28",
  "panelHeight": "124px", "panelTop": 812, "panelBottom": 936, "navTop": 948, "viewportHeight": 1000,
  "coverSlide": true, "chapters": 4, "optgroups": 4, "titleIds": 28, "footerLinks": 28,
  "presentMode": true, "readingMode": true, "slidesVisibleWhileReading": 28,
  "backToOneSlide": 1, "drawerOpen": true, "drawerHasNotes": true, "drawerClosed": true
}
```

This is not ceremony. It has caught four bugs that all rendered wrong while looking right in source:

| Bug | What the measurement showed |
|---|---|
| `@font-face` URL | copied from ai_qe's `/assets/css/` layout while our CSS sits in `/assets/`, so the font 404'd and silently fell back to a system sans |
| **Read all** | switched the class but left every other slide `hidden` — 1 slide visible when 28 should be |
| Narration panel | pushed to 897..1021 in a 900px viewport: the controls were **off-screen**, because `--frame-width` is declared on `:root` and a `var()` inside a custom property is substituted where that property is declared, so setting `--narration-height` on `<body>` never reached the frame maths |
| Chrome budget | the honesty badge adds ~49px that a hardcoded `112px` constant did not know about, so the panel ran under the navigation strip |

The fourth is why `--chrome-height` is measured by the player rather than assumed.

So every deck is checked for: the frame really is 16:9 and does not overflow, the typeface actually
loaded, the kicker/title/footer exist on the current slide, **the narration panel is inside the
viewport and clear of the navigation strip**, every slide has an anchored title and a transcript link,
the picker is chapter-grouped, and Present / Read all / Sources & notes all change state correctly.


```bash
python3 course/learner-site/check_player.py        # headless Chrome, no npm install
python3 course/learner-site/build_site.py --check  # build into a temp dir
python3 course/06-production/verify.py             # the whole course gate, incl. narration
```

`check_player.py` drives a browser already on the machine (Chrome or Chromium) and asserts that the
panel was injected, exactly one slide is `aria-current`, the status region names the right slide, the
CC control became enabled (which can only happen after the `.vtt` fetched *and* parsed), a cue is
rendered, and a deep link (`#slide-5`) navigates correctly. It exits 2 with a clear message if no
browser is installed, so it can never become an unverifiable dependency.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Page is text-only, player says narration is unavailable | `narration.json` was not built or the manifest is empty — run `make site` after generating narration. |
| "Captions could not load" | The `.vtt` is missing or invalid. Run `python3 course/06-production/narration/validate_narration.py`. |
| A visible "preview narration" badge | The recordings are the free local voice. Record the release voice (`make narration`) to replace it. |
| Audio works from the server but not from `file://` | Browsers block `fetch` for local files. Use `make serve`. |
| Two tabs fight over playback | Should not happen — `narration-media.js` coordinates them. If it does, note the reproduction; that is a bug worth fixing. |
