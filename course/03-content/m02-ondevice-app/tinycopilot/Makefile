# TinyCopilot - the Module 2/3 lab. The tests are the spec; lab-m2 is the pass gate.
PYTHON ?= python3

# The coverage floor lab-m2 enforces. Lab M3 step 3 is "wire the floor in yourself":
# `make m3-start` rewrites this line to 0 and you set it back to 90; `make m3-restore` also resets it.
COV_FLOOR ?= 90

# What Lab M3 builds. `make m3-start` parks these in .m3-solution/ (git-ignored) so the lab starts
# from a tree that does not already contain its own answer; `make m3-restore` brings them back.
M3_FILES = src/tinycopilot/privacy.py tests/test_privacy.py tests/test_contract_real_llm.py
M3_PARK = .m3-solution

.PHONY: help lab-m2 lab-m3 e2e demo test m3-start m3-restore

help:
	@echo "TinyCopilot lab targets:"
	@echo "  make lab-m2     - unit suite + coverage floor >= $(COV_FLOOR) (Module 2 pass gate)"
	@echo "  make lab-m3     - privacy + streaming hardening suite (Module 3 pass gate)"
	@echo "  make e2e        - real-LLM contract test against the local Ollama daemon"
	@echo "  make demo       - scripted meeting through all three roles"
	@echo "  make test       - the full suite, e2e auto-skipped"
	@echo "  make m3-start   - Lab M3 step 0: park the shipped privacy module, its tests, the contract test; floor -> 0"
	@echo "  make m3-restore - put the reference Lab M3 solution back; floor -> 90"

lab-m2:
	$(PYTHON) -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=$(COV_FLOOR) -q

lab-m3:
	$(PYTHON) -m pytest tests/test_privacy.py tests/test_ollama_provider.py -q

e2e:
	LAB_E2E=1 $(PYTHON) -m pytest tests/test_contract_real_llm.py -q

demo:
	$(PYTHON) demo.py

test:
	$(PYTHON) -m pytest tests -q

m3-start:
	@test ! -e $(M3_PARK) || { echo "$(M3_PARK)/ already exists: Lab M3 is already started (make m3-restore undoes it)"; exit 1; }
	@for f in $(M3_FILES); do mkdir -p $(M3_PARK)/$$(dirname $$f) && mv $$f $(M3_PARK)/$$f; done
	@$(PYTHON) -c "import pathlib, re; p = pathlib.Path('Makefile'); p.write_text(re.sub(r'(?m)^COV_FLOOR \?= \d+', 'COV_FLOOR ?= 0', p.read_text()))"
	@echo "Lab M3 starting state: parked $(M3_FILES) in $(M3_PARK)/; COV_FLOOR is now 0."
	@echo "Run 'make lab-m3' and record the red output. 'make m3-restore' brings the reference back."

m3-restore:
	@test -d $(M3_PARK) || { echo "nothing parked in $(M3_PARK)/: this tree is already the reference"; exit 1; }
	@for f in $(M3_FILES); do test ! -e $$f || { echo "$$f exists - move your version aside before restoring"; exit 1; }; done
	@for f in $(M3_FILES); do mv $(M3_PARK)/$$f $$f; done
	@rm -rf $(M3_PARK)
	@$(PYTHON) -c "import pathlib, re; p = pathlib.Path('Makefile'); p.write_text(re.sub(r'(?m)^COV_FLOOR \?= \d+', 'COV_FLOOR ?= 90', p.read_text()))"
	@echo "Reference Lab M3 solution restored; COV_FLOOR back to 90."
