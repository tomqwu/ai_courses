# Figures library

What the ```` ```figure ```` blocks in the decks and lessons draw from (content standard §2.1a).

## `shots/` — real product screenshots

Byte-identical copies of images in the case-study repos, taken at the commit the course pins
(`.github/workflows/gate.yml`). Never edited, cropped or annotated: callouts are drawn over the image
by the page. `manifest.json` records each copy's repo, path, commit and sha256, and `verify.py`
(Figures) re-checks every entry against its origin.

```bash
python3 course/06-production/figures_shots.py copy SignUpFlow/docs/screenshots/current/basketball/1440/dashboard.png --as signupflow-dashboard.png
python3 course/06-production/figures_shots.py verify
```

| Copy | Shows | Frame |
|---|---|---|
| `signupflow-dashboard.png` | the admin dashboard: setup progress, four health tiles, the attention queues | `browser` |
| `signupflow-onboarding.png` | first-run onboarding | `browser` |
| `signupflow-schedule-change-admin.png` | a schedule change, as the admin sees it | `browser` |
| `signupflow-replacement-needed.png` | a replacement request after a volunteer drops out | `browser` |
| `listentome-app.png` | the macOS window: transcript, and the Listener / Quick / Deep panes | `none` (it carries its own window chrome) |
| `ai_qe-context-route.svg` | ai_qe's own context-routing diagram | `none` |
| `ai_qe-contract-chain.svg` | ai_qe's own contract-chain diagram | `none` |

## `scenes/` — illustrations

Hand-drawn SVGs, 640×360, for situations rather than systems. They are inlined into the page and
coloured only with the `sc-*` classes in `learner-site/assets/player.css` (Studio tokens), so they
carry no colour of their own; `test_figures.py` fails a scene with a hex colour or another class.
Every scene has a `<title>`, and the page captions it "Illustration" — a scene proves nothing.

| Scene | Shows | Fits |
|---|---|---|
| `meeting.svg` | a video call with a copilot pane offering a suggestion | M1–M3 (ListenToMe) |
| `stranger-clone.svg` | a stranger clones a repo and follows the README to a passing check | M0, M4, M9 |
| `buyer-checkout.svg` | a buyer reads a product page, presses Buy, gets a receipt | M6, M7 |
| `auditor.svg` | a reviewer checks claims against evidence; one is flagged | M5, M8 |
| `launch-arc.svg` | a sequence of emails leads to the course page | M7 |
| `cohort.svg` | a small cohort watches a member demo a build | M8 |
