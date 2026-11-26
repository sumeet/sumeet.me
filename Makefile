PYTHON_VERSION := $(shell cat .python-version)
PYTHON ?= $(if $(wildcard .venv/bin/python),$(CURDIR)/.venv/bin/python,python$(PYTHON_VERSION))
REJECTSYNTH_DIR ?= ../rejectsynth
NN_H_DIR ?= ../nn-h
MATCHARONI_DIR ?= ../matcharoni

default: html pdf

setup:
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

html:
	mkdir -p build
	cp style.css build/
	cp pads.css projects.css projects.js build/
	mkdir -p build/fonts
	cp fonts/* build/fonts/
	mkdir -p build/projects
	cp projects/*.gif build/projects/
	cp projects/*.mp4 build/projects/
	cp projects/*.png build/projects/
	cp projects/*.jpg build/projects/
	cp projects/*.webp build/projects/
	cp -R projects/rejectsynth build/projects/
	cp -R projects/nn-h build/projects/
	cp -R projects/exac build/projects/
	cp -R projects/goylang build/projects/
	cp -R projects/matcharoni build/projects/
	cp *.otf build/
	cp darkreader.js build/
	cp favicon.ico build/
	cp resume.md build/sumeet.txt
	$(PYTHON) build_html.py

serve: html pdf
	SITE_DEV=1 $(PYTHON) -m gunicorn site_server:application --bind 127.0.0.1:8000 --workers 1 --threads 4

# The synth source lives in its own repository; Dokku serves this static export.
rejectsynth:
	cd "$(REJECTSYNTH_DIR)/browser" && npm ci && npm run wasm && npm run build
	$(PYTHON) sync_rejectsynth.py "$(REJECTSYNTH_DIR)"

nn-h:
	cd "$(NN_H_DIR)" && bash web/build.sh
	$(PYTHON) sync_nn_h.py "$(NN_H_DIR)"

matcharoni:
	cargo rustc --manifest-path "$(MATCHARONI_DIR)/web/Cargo.toml" --locked --release --lib \
		--target wasm32-unknown-unknown --target-dir "$(MATCHARONI_DIR)/target" -- -C link-arg=--max-memory=67108864
	wasm-bindgen --target web --no-typescript --out-name matcharoni --out-dir projects/matcharoni/pkg \
		"$(MATCHARONI_DIR)/target/wasm32-unknown-unknown/release/matcharoni_web.wasm"
	cargo build --manifest-path "$(MATCHARONI_DIR)/Cargo.toml" --locked --target-dir "$(MATCHARONI_DIR)/target"
	$(PYTHON) record_matcharoni.py "$(MATCHARONI_DIR)/target/debug/matcharoni"

open_html:
	open build/index.html

test_html: html open_html

test: html pdf
	$(PYTHON) -m unittest discover -s tests -v

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

.PHONY: default setup html serve rejectsynth nn-h matcharoni open_html test_html test pdf open_pdf test_pdf clean
