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
| `build_site.py`, `check_player.py` | hand-written | **Yes** |

## Page structure

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
