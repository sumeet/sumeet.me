PYTHON_VERSION := $(shell cat .python-version)
PYTHON ?= $(if $(wildcard .venv/bin/python),$(CURDIR)/.venv/bin/python,python$(PYTHON_VERSION))

default: html pdf

setup:
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

html:
	mkdir -p build
	$(PYTHON) build_html.py
	cp style.css build/
	cp projects.css projects.js build/
	mkdir -p build/fonts
	cp fonts/* build/fonts/
	mkdir -p build/projects
	cp projects/*.gif build/projects/
	cp projects/*.mp4 build/projects/
	cp *.otf build/
	cp darkreader.js build/
	cp favicon.ico build/
	cp resume.md build/sumeet.txt

serve: html pdf
	cd build && $(PYTHON) -m http.server 8000 --bind 127.0.0.1

open_html:
	open build/index.html

test_html: html open_html

pdf:
	mkdir -p build
	./install_fonts.sh
	$(PYTHON) build_pdf.py build/sumeet.pdf

open_pdf:
	open build/sumeet.pdf

test_pdf: pdf open_pdf

clean:
	rm -rf build
	rm -rf __pycache__

.PHONY: default setup html serve open_html test_html pdf open_pdf test_pdf clean
