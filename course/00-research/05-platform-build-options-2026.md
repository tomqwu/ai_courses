# Research: Owning the Platform — Build-vs-Buy for Selling This Course (September 2026)

> Compiled 2026-09-17 by web research for the platform review (`04-platform-review-2026.md`). Every price
> carries a source and a tag: **[vendor]** (the vendor's own page or blog), **[3rd-party]** (a review or
> comparison site — approximately right, verify before committing money), **[independent]** (peer-reviewed
> or first-hand). Prices that could not be confirmed are marked *unverified*. Several vendor pricing pages
> were unreachable from the research environment, so third-party roundups stand in; re-check before any
> purchase decision.

The question this answers: the course already generates a static narrated site from Markdown
(`learner-site/build_site.py`), verifies itself (`06-production/verify.py`) and publishes to GitHub Pages
(`publish_site.py`). What is the cheapest credible way for one engineer to *own* the paid platform rather
than rent Teachable or Maven — and in what order?

## 1. Build-vs-buy matrix

| Option | Cost (2026) | Platform cut | Merchant of record / tax | You own emails and data? | Lock-in | Dev effort |
|---|---|---|---|---|---|---|
| **Teachable** | Starter $39/mo ($29 annual), Builder $89, Growth $189 [3rd-party](https://www.ruzuku.com/compare/teachable-pricing) | 7.5% on Starter, 0% above, plus processing [3rd-party](https://www.ruzuku.com/learn/articles/teachable-pricing-transaction-fees) | Teachable is MoR on its own gateway (verify per country) | CSV export of users [vendor](https://support.teachable.com/en/articles/12053250-how-to-export-school-content-and-data); progress data is harder [3rd-party](https://www.learniverse.app/blog/teachable-vs-thinkific-portability) | Medium | None |
| **Thinkific** | Basic $54/mo ($40 annual), Start $109/$82, Grow $219/$164 after an Aug 2026 rise [vendor](https://support.thinkific.com/hc/en-us/articles/41582716364567-Thinkific-s-2026-Plan-Pricing-Update-What-It-Means-for-You); no free plan since Mar 2026 [3rd-party](https://www.ruzuku.com/compare/thinkific-pricing) | 5%/2%/1% penalty for using your own Stripe; quizzes and certificates start at the Start tier | Thinkific Payments handles tax | Full student export [vendor](https://support.thinkific.com/hc/en-us/articles/360030354314-Migration-Support-Bulk-Student-Import-and-Course-Enrollment-Instructions) | Medium | None |
| **Podia** | Mover $42/mo annual (5% fee), Shaker $99/$84 (0%), Earthquaker $179/$150 [vendor](https://help.podia.com/en/articles/11371138-understanding-podia-transaction-fees) | 5% on Mover only, plus processing | Your own Stripe/PayPal — tax is on you | Yes | Low–medium | None |
| **Kajabi** | Basic $179/mo ($143 annual), Growth $249/$199, Pro $499/$399 after a Jan 2026 restructure [3rd-party](https://www.ruzuku.com/compare/kajabi-pricing) | Kajabi Payments adds 0.7% on subscriptions, 1.5% international [3rd-party](https://kourses.com/kajabi-pricing/) | Kajabi Payments | Yes (contacts capped) | High | None |
| **LearnWorlds** | Starter $29/mo (+$5 per enrollment), Pro Trainer $99/$79, Learning Center $299/$249 [3rd-party](https://www.ruzuku.com/compare/learnworlds-pricing) | $5/enrollment on Starter | Your gateway | Yes | Medium | None |
| **Maven** (cohort) | No monthly fee; 10% of revenue; extra 30% on Maven-attributed promo sales and up to 40% on B2B referrals [vendor](https://help.maven.com/en/articles/11888621-expert-guide-to-the-student-growth-program) | 10%+ | Maven is the seller | CSV export exists, but the instructor policy forbids importing students into external newsletters without opt-in [vendor](https://help.maven.com/en/articles/6069488-student-management-in-the-maven-admin-dashboard), [vendor](https://help.maven.com/en/articles/12240853-maven-instructor-policy-guidebook) | High for the audience relationship | None |
| **Skool** | Hobby $9/mo (10% + 30¢ per charge), Pro $99/mo (2.9% + 30¢; 3.9% above $900) [3rd-party](https://www.ruzuku.com/compare/skool-pricing) | see left | Skool processes payments | Member list yes; email tooling limited | Medium | None |
| **Circle** | Professional $89/mo, Business $199/mo (annual); 2%/1%/0.5% transaction fee on top of Stripe; Email Hub +$99/mo [3rd-party](https://www.ruzuku.com/compare/circle-pricing) | 0.5–2% | Your Stripe | Yes | Medium | None |
| **Mighty Networks** | Launch $95/mo ($79 annual), Scale ~$179–215, Growth $354/$295; fee 2% → 0.5%, never 0% [3rd-party](https://kourses.com/mighty-networks-pricing-2/), [vendor](https://www.mightynetworks.com/pricing) | 0.5–2% | Your Stripe | Yes | Medium | None |
| **Moodle / Canvas / Open edX** (self-host) | Software free; Open edX needs 8+ GB RAM and seven services [3rd-party](https://raccoongang.com/blog/open-source-lms-everything-you-need-know/), [3rd-party](https://cubite.io/blogs/open-edx-hosting) | 0% | You + Stripe Tax or an MoR | Everything | Low lock-in, high ops burden | High, and the UX is institutional |
| **Frappe LMS** | Open source, AGPL [vendor](https://github.com/frappe/lms); hosting quoted at $5–50/mo — *unverified* [3rd-party](https://softwarefinder.com/lms/frappe) | 0% | You | Yes | Low | Medium |
| **Tutor LMS** (WordPress) | Free core; Pro $199/yr, $499 lifetime [vendor](https://tutorlms.com/pricing/) | 0% via WooCommerce | You | Yes | Low | Medium (WordPress ops) |
| **Docs-site + paywall** (Astro/Next.js + Stripe + Clerk/Supabase) | Hosting ~$0–20/mo; Clerk free to 50k monthly active users then $25/mo [vendor](https://clerk.com/articles/clerk-pricing-explained); Supabase free to 50k MAU, Pro $25/mo [3rd-party](https://www.buildmvpfast.com/api-costs/authentication) | 0% + Stripe 2.9% + 30¢, or an MoR's 5% + 50¢ | Your choice (§2) | 100% | Lowest | Medium: 2–6 weeks for auth, entitlements, progress, checkout webhooks |
| **Gumroad / Lemon Squeezy / Polar** selling repo or site access | Gumroad 10% + 50¢ + processing (30% via Discover) [3rd-party](https://checkoutpage.com/blog/gumroad-fees); Lemon Squeezy 5% + 50¢; Polar 5% + 50¢ free tier or $20/mo at 3.8% + 40¢ [3rd-party](https://dodopayments.com/blogs/polar-sh-review) | see left | All three are MoR (Gumroad since Jan 2025 [3rd-party](https://roo.beehiiv.com/p/gumroad-fees-2026)) | Buyer emails yes; Polar auto-invites buyers to private GitHub repos [vendor](https://polar.sh/docs/features/benefits/github-access) | Low | Days |
| **GitHub Sponsors** / sponsors-only repos | 0% for personal sponsors, up to 6% for org sponsors; sponsors-only private repos attach to tiers [vendor](https://github.blog/open-source/maintainers/new-sponsors-only-repositories-custom-amounts-and-more/) | 0–6% | GitHub is not your MoR | Sponsor handles, not a mailing list | Low | Very low |
| **GitHub Classroom** | **Shut down**: new classrooms blocked 22 May 2026, site decommissioned 28 Aug 2026, data deleted 4 Sep 2026 [vendor](https://github.com/orgs/community/discussions/196615) | — | — | — | — | Replace with Classroom 50 (§4) |

**Reading the table.** Hosted LMSes cost $40–200/mo before the first student and keep the learner
relationship inside their product; Maven and Skool take a percentage forever. For a solo engineer who
already generates a static site from Markdown, the two cheap-and-owned paths are the docs-site + paywall
and an MoR selling repo/site access — and they compose: use the MoR on day one and grow into the site.

## 2. Merchant of record and tax

- **Lemon Squeezy** — acquired by Stripe in July 2024; still operating; 5% + 50¢ plus 1.5% international, 0.5% subscriptions, charged on the tax-inclusive total [3rd-party](https://getstacksmart.com/blog/lemon-squeezy-merchant-of-record-fees-2026), [vendor](https://www.lemonsqueezy.com/blog/2026-update). Migration paths to Stripe Managed Payments are being built [3rd-party](https://fungies.io/lemon-squeezy-stripe-acquisition-saas-founders-2026/). Treat as sunsetting.
- **Stripe Managed Payments** (Stripe's own MoR) — public preview Feb 2026; +3.5% on top of standard Stripe fees, so roughly 6.4% + 30¢ US domestic [3rd-party](https://dodopayments.com/blogs/stripe-managed-payments-fees-explained). Simplest if already on Stripe.
- **Paddle** — 5% + 50¢ all-in, no monthly fee; competitor-reported caveats: ~1% FX spread, fees not returned on refunds [3rd-party, competitor](https://dodopayments.com/blogs/paddle-fees-explained). Native per-country price overrides [vendor](https://developer.paddle.com/build/products/offer-localized-pricing/). Stricter onboarding.
- **Polar** — open-source engine; new orgs after 27 May 2026 pay 5% + 50¢ on the free plan or $20/mo at 3.8% + 40¢ [3rd-party](https://dodopayments.com/blogs/polar-sh-review), [vendor](https://polar.sh/blog/introducing-polar-plans). Unique: GitHub-repo-access and license-key benefits out of the box [vendor](https://polar.sh/features/benefits).
- **Gumroad** — 10% + 50¢ plus processing, 30% on Discover; MoR since Jan 2025; source MIT-licensed since April 2025 [3rd-party](https://checkoutpage.com/blog/gumroad-fees), [vendor](https://github.com/antiwork/gumroad). Highest cut; zero-effort only.
- **Stripe Tax** (DIY, not MoR) — 0.5% of volume where registered, or $0.50/transaction via API; filing is separate [vendor](https://stripe.com/tax/pricing). Cheapest, but you carry registration liability in the EU/UK once over thresholds.

**Net:** Paddle and Polar lead at 5% + 50¢ with full tax-liability transfer; Polar is the most
developer-native. Stripe Managed Payments is ~1.4 points dearer but keeps you on Stripe primitives.

## 3. Reference architectures from developer-educators

- **Josh Comeau** (CSS for JS Devs, Joy of React) — custom Next.js app with MDX, auth, roles, transactional email [vendor](https://www.joshwcomeau.com/blog/how-i-built-my-blog-v2/); PPP "regional licence" region-locked from day one; team licences 10–20% off with a seat-assignment UI [vendor](https://www.joshwcomeau.com/email/jor-launch-004-faq-primary/), [vendor](https://www.joyofreact.com/checkout/teams).
- **Kent C. Dodds / Epic Web** — sales site on **course-builder** (open source): Next.js, Drizzle, NextAuth, tRPC, Inngest, Mux video, Deepgram transcripts, Stripe [vendor](https://github.com/badass-courses/course-builder/blob/main/CLAUDE.md), [vendor](https://badass.dev/course-builder). Exercises run locally in the open-source **epicshop** workshop app (diffs, videos, progress) [vendor](https://github.com/epicweb-dev/epicshop).
- **Total TypeScript** (Matt Pocock) — same stack; pre-release launch did $415k [vendor](https://badass.dev/launch-of-a-developer-education-product); complete package cut to $500; PPP region-locks the purchase [vendor](https://www.totaltypescript.com/faq).
- **Wes Bos** — own store; pioneered opt-in PPP, kept even during sales; reports it cuts piracy and card fraud [vendor](https://wesbos.com/parity-purchasing-power).
- **ui.dev** — ~$149 per course or $495/yr all-access; merged with Fireship Jan 2026 [vendor](https://benadam.me/work/uidotdev/), [vendor](https://fireship.dev/uidotdev-and-fireship-join-forces).
- **Adam Wathan** — Refactoring UI > $2.5M, Tailwind UI > $2M, all sold from own sites after years of audience building [vendor](https://adamwathan.me/tailwindcss-from-side-project-byproduct-to-multi-mullion-dollar-business/).
- **boot.dev** — in-browser execution, gamified progress; $59/mo or $399/yr [3rd-party](https://www.coursefacts.com/guides/boot-dev-review-2026).
- **Emil Kowalski** (animations.dev) — custom platform explicitly modelled on Comeau and buildui [vendor](https://emilkowal.ski/ui/how-i-built-my-course-platform).

Common denominator: **own site, Stripe (sometimes via an MoR), Mux-class video with transcripts,
per-lesson progress, exercises that run on the learner's machine, region-locked PPP, and team
licensing.** None of them use a hosted LMS.

## 4. Delivering and verifying labs

- **GitHub Codespaces** — every GitHub user gets 120 core-hours/month + 15 GB; overage $0.18/core-hour [3rd-party](https://agentdeals.dev/vendor/github-codespaces). A `.devcontainer/devcontainer.json` in the course repo gives one-click labs; GPU types are not on the free tier [3rd-party](https://infragap.com/devcontainers/).
- **GitHub Classroom is gone** (dates in §1). Replacement: **Classroom 50** (Fifty Foundation, GitHub's official OSS education partner) — static web app + CLI, autograding via GitHub Actions, state in your GitHub org, announced 1 July 2026 [vendor](https://github.com/foundation50/classroom50/), [vendor](https://github.com/orgs/community/discussions/200700). Codio is the commercial partner [vendor](https://www.prnewswire.com/news-releases/github-selects-codio-as-exclusive-commercial-partner-to-extend-use-of-github-classroom-benefits-to-codios-advanced-cs-learning-platform-302696425.html).
- **Exercism-style CLI** — Exercism's CLI and test runners are open source [vendor](https://github.com/exercism/cli), but self-hosting the platform is undocumented. The practical pattern is a tiny `course check <lab>` command that runs the lab's tests and posts a signed result — which is what `verify.py` and TinyCopilot's `make lab-m2` already do locally.
- **Local-first with Ollama** — no usage fees; 7B Q4 models need ~8–16 GB RAM [3rd-party](https://www.sitepoint.com/run-local-llms-2026-complete-developer-guide/). Right fit for AI labs: zero API cost for learners; lab checks assert on deterministic structure, not model output.
- **Certificates** — Open Badges 3.0 = W3C Verifiable Credentials signed with the issuer's key [vendor](https://www.imsglobal.org/spec/ob/v3p0). Self-issue with **openbadgeslib** (Python; JWT-VC proofs, bakes into SVG/PNG, revocation via status lists) [vendor](https://pypi.org/project/openbadgeslib/4.5.0/) or the **Certo** OSS platform [vendor](https://github.com/schroedinger-Hat/certo). Hosted: Certifier free to 250 credentials/yr, then ~$45–76/mo [3rd-party](https://www.g2.com/products/certifier/pricing); Accredible ~$996/yr for 250 recipients plus setup [3rd-party, competitor](https://collegian.com/sponsored/2026/04/3-best-accredible-alternatives-in-2026/). The course's existing SHA-bounded certificate (`06-production/certificate.md`) is fine for v1 but carries no interoperable proof; OB3 is the credible version and is cheap to self-issue.

## 5. Video and narration

- **Mux** — free baseline encoding; storage and delivery per minute; exact 2026 rates *unverified* [vendor](https://www.mux.com/blog/our-next-pricing-lever-baseline-on-demand-assets-with-free-video-encoding). Best developer experience (player, signed URLs, transcripts).
- **Cloudflare Stream** — $5 per 1,000 minutes stored/month, $1 per 1,000 minutes delivered, no egress fees [3rd-party](https://flarecalc.com/calculators/stream/).
- **Bunny Stream** — $1/mo minimum; storage ~$0.01/GB, delivery from ~$0.005/GB, AI transcription $0.10/min [vendor](https://docs.bunny.net/stream/pricing). Cheapest for a ~25-hour course (~$15–25/mo) [3rd-party](https://swarmify.com/blog/bunny-stream-review/).
- **YouTube unlisted** — free, but no domain lock and the raw URL leaks from page source [3rd-party](https://www.ruzuku.com/learn/tools/video-privacy/paid-courses). Previews only.
- **AI narration** — ElevenLabs Free 10k characters, Starter $6, Creator $22 (121k credits), Pro $99 (600k) [3rd-party](https://www.happyrobot.ai/hub/elevenlabs-pricing). HeyGen Creator $29/mo but Avatar IV burns ~20 credits/min [3rd-party](https://www.arcade.software/post/heygen-pricing); Synthesia Creator $67/mo for 30 min [3rd-party](https://www.colossyan.com/posts/heygen-vs-synthesia/).
- **Do learners accept AI voices?** A 2025 *British Journal of Educational Technology* study found no significant exam-performance difference between AI-generated and recorded instructional videos, though students rated human videos slightly higher on experience [independent](https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.13530); a 2026 *Education and Information Technologies* paper compared real vs AI instructors on human-likeness, motivation and retention [independent](https://link.springer.com/article/10.1007/s10639-026-14085-y); an audiobook study found AI voices comparable in task-focused contexts but not for long-form emotional content [independent](https://www.sciencedirect.com/science/article/pii/S2451958826001429). The widely quoted "78% say quality matters more than human-vs-AI" figure comes from vendor blogs with no primary survey found **[vendor]**. Takeaway: a good TTS voice is defensible for technical narration if labelled — which the course already does — and human intros/outros are the cheap upgrade.

## 6. Purchasing-power-parity and regional pricing

- **ParityDeals** — geo-detects, issues coupons, blocks VPN/Tor; integrates Stripe, Paddle, Lemon Squeezy, Polar; free for one product, then ~$49–99/mo — *unverified* [vendor](https://www.paritydeals.com/integrations/paddle/), [3rd-party](https://www.evendeals.com/paritydeals-alternative).
- **Paddle** has native per-country overrides [vendor](https://developer.paddle.com/build/products/offer-localized-pricing/).
- **Custom** — Comeau and Pocock region-lock PPP purchases; Wes Bos makes it opt-in. `CF-IPCountry` or Vercel geo headers + a country→discount table + coupons is about a day of work [3rd-party](https://scastiel.dev/implement-ppp-fair-pricing-for-your-product/); the `purchasing-power-parity` npm package carries the index [3rd-party](https://www.npmjs.com/package/purchasing-power-parity).

## 7. Recommended path for this repository

**Stage 0 — launch now (1–2 weeks, ~$0–30/mo fixed).** Keep `build_site.py` and GitHub Pages for the
free preview. Put the paid site (and the private lab starters) in a private GitHub repo and sell access
through **Polar** (5% + 50¢, MoR, auto-invites buyers to the repo, license keys for later). Add a
`.devcontainer/devcontainer.json` so the labs open in Codespaces on the learner's free hours, with Ollama
for model calls. Turn `verify.py` into a `course check` command that emits a signed JSON result; issue the
SHA-bounded certificate page for now. Video: unlisted YouTube for previews only, Bunny Stream for paid
lessons. Risk: repo-access delivery feels developer-grade to this audience but caps you at technical
buyers and gives no in-browser progress tracking.

**Stage 1 — three months (4–6 weeks of evenings, ~$25–75/mo).** Build the docs-site + paywall: Astro or
Next.js rendering the existing Markdown; Supabase (auth + Postgres + row-level security for entitlements)
or Clerk; Polar/Paddle webhooks writing purchases; per-lesson progress and quiz results in Postgres; Mux
or Bunny signed playback; transcripts from the narration text you already have. Fork *ideas* from
course-builder and epicshop. Add Classroom 50 for autograded lab repos if you run cohorts, PPP via a
country table plus coupons, and Open Badges 3.0 on lab-gate pass. Fallback if the build slips: Podia
Shaker at $84/mo with 0% fees.

**Stage 2 — twelve months (~$100–250/mo at a few hundred sales).** Team licences with seat assignment
(Comeau model), a "playbooks" line sold as an all-access annual subscription (ui.dev model), cohorts on
your own site with Discord/Zoom rather than Maven's 10–40%, and Stripe Managed Payments once it is
generally available if you want to consolidate on Stripe. ElevenLabs Pro only if you regenerate narration
at volume; otherwise the labelled preview voice plus human intros is what the evidence supports.

**Not verified in this pass:** exact 2026 Mux per-minute rates, ParityDeals plan prices, Epic Web and
Total TypeScript current list prices, Frappe Cloud hosting, Mighty Networks' Business-tier fee.
