# AI Product Studio — course tasks.
#
#   make narration          release voice  (needs ELEVENLABS_API_KEY)
#   make narration-preview  free local preview voice, no key needed
#   make site               build the learner site from the decks + recordings
#   make serve              build, then serve on http://localhost:8043
#   make check              validate scripts, media, decks, the site build and the player
#
# The learner site is generated: the deck Markdown and narration/scripts/*.json are the source of
# truth, and nothing under learner-site/ except the player assets is committed.

PYTHON ?= python3
NARRATION := 06-production/narration
SITE := learner-site
PORT ?= 8043

.PHONY: narration narration-preview narration-plan site serve check test browser-check

narration-plan:
	$(PYTHON) $(NARRATION)/generate_narration.py plan

# The release voice. Fails loudly if ELEVENLABS_API_KEY is unset rather than degrading silently.
narration:
	$(PYTHON) $(NARRATION)/generate_narration.py generate --provider elevenlabs

# Free, offline, sentence-accurate preview. Clearly labelled as a preview in provenance and in the UI.
narration-preview:
	$(PYTHON) $(NARRATION)/generate_narration.py generate --provider say

site:
	$(PYTHON) $(SITE)/build_site.py

serve: site
	@echo "serving $(SITE) on http://localhost:$(PORT)/  (Ctrl-C to stop)"
	@cd $(SITE) && $(PYTHON) -m http.server $(PORT)

test:
	cd $(NARRATION) && $(PYTHON) test_captions.py

check: test
	$(PYTHON) $(NARRATION)/validate_narration.py --scripts-only
	$(PYTHON) $(NARRATION)/validate_narration.py
	$(PYTHON) $(SITE)/build_site.py --check
	$(PYTHON) $(SITE)/check_player.py --all --print-skip
	$(PYTHON) 06-production/verify.py

# The browser check needs a built site; it skips with a note if no browser is installed.
browser-check: site
	$(PYTHON) $(SITE)/check_player.py --all --print-skip
