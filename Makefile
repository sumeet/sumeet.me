PYTHON ?= $(if $(wildcard .venv/bin/python),$(CURDIR)/.venv/bin/python,python)

default: html pdf

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements-local.txt

html:
	mkdir -p build
	$(PYTHON) build_html.py > build/index.html
	cp style.css build/
	cp *.otf build/
	cp darkreader.js build/
	cp favicon.ico build/
	cp resume.md build/sumeet.txt
	# /resume was the URL for my old resume, which is now the whole site. make
	# it work so old links to it don't 404
	ln -sfn . build/resume

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
