# TinyCopilot - the Module 2/3 lab. The tests are the spec; lab-m2 is the pass gate.
PYTHON ?= python3

.PHONY: help lab-m2 lab-m3 e2e demo test

help:
	@echo "TinyCopilot lab targets:"
	@echo "  make lab-m2  - unit suite + coverage floor >= 90 (Module 2 pass gate)"
	@echo "  make lab-m3  - privacy + streaming hardening suite (Module 3 pass gate)"
	@echo "  make e2e     - real-LLM contract test against the local Ollama daemon"
	@echo "  make demo    - scripted meeting through all three roles"
	@echo "  make test    - the full suite, e2e auto-skipped"

lab-m2:
	$(PYTHON) -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q

lab-m3:
	$(PYTHON) -m pytest tests/test_privacy.py tests/test_ollama_provider.py -q

e2e:
	LAB_E2E=1 $(PYTHON) -m pytest tests/test_contract_real_llm.py -q

demo:
	$(PYTHON) demo.py

test:
	$(PYTHON) -m pytest tests -q