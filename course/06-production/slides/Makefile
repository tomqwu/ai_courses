# Slide production. Decks are plain Markdown; this only renders them.
.PHONY: help check html pdf

help:
	@echo "make check  - validate every deck (front matter + speaker notes)"
	@echo "make html   - render decks to HTML in slides/out/"
	@echo "make pdf    - render decks to HTML + PDF"

check:
	./build.sh --check

html:
	./build.sh

pdf:
	./build.sh --pdf
