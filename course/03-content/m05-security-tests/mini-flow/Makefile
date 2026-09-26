# mini-flow - the Module 5 lab. The lab tests are the spec; `make lab-m5 STEPS=1,2,3,4` is the pass gate.
PYTHON ?= python3
# Comma-separated lab steps to un-skip, e.g. `make lab-m5 STEPS=1,3`. Empty = baseline only.
STEPS ?=

.PHONY: help setup lab-m5 step1 step2 step3 step4 pass-gate demo test

help:
	@echo "mini-flow lab targets:"
	@echo "  make setup       - install fastapi, sqlalchemy, pydantic, PyJWT, httpx, pytest, pytest-cov"
	@echo "  make lab-m5      - baseline suite + coverage floor >= 90; lab steps skipped unless STEPS=1,2,3,4"
	@echo "  make step1..4    - run one graded step's tests un-skipped (red on the shipped starter)"
	@echo "  make pass-gate   - every step un-skipped + coverage floor (the Lab M5 pass gate)"
	@echo "  make demo        - two tenants, one leaky endpoint: watch the status contract live"
	@echo "  make test        - the whole suite, no coverage floor"

setup:
	$(PYTHON) -m pip install "fastapi>=0.141" "sqlalchemy>=2.0" "pydantic>=2.0" "PyJWT>=2.7" "httpx>=0.27" "pytest>=8.0" "pytest-cov>=5.0"

lab-m5:
	MINIFLOW_LAB_STEPS=$(STEPS) $(PYTHON) -m pytest tests --cov=src/miniflow --cov-fail-under=90 -q

step1:
	MINIFLOW_LAB_STEPS=1 $(PYTHON) -m pytest tests/test_lab1_isolation.py -q

step2:
	MINIFLOW_LAB_STEPS=2 $(PYTHON) -m pytest tests/test_lab2_qualifications.py -q

step3:
	MINIFLOW_LAB_STEPS=3 $(PYTHON) -m pytest tests/test_lab3_route_policy.py -q

step4:
	MINIFLOW_LAB_STEPS=4 $(PYTHON) -m pytest tests/test_lab4_manifest.py -q

pass-gate:
	$(MAKE) lab-m5 STEPS=1,2,3,4

demo:
	PYTHONPATH=src:. $(PYTHON) demo.py

test:
	MINIFLOW_LAB_STEPS=$(STEPS) $(PYTHON) -m pytest tests -q
