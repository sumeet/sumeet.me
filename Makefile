default: clean html pdf

html:
	mkdir -p build
	./build_html.py > build/index.html
	cp style.css build/
	cp *.otf build/
	cp darkreader.js build/
	cp favicon.ico build/
	cp resume.md build/sumeet.txt
	# /resume was the URL for my old resume, which is now the whole site. make
	# it work so old links to it don't 404
	ln -s . build/resume

open_html:
	open build/index.html

test_html: html open_html

pdf:
	mkdir -p build
	./install_fonts.sh
	./build_pdf.py build/sumeet.pdf

open_pdf:
	open build/sumeet.pdf

test_pdf: pdf open_pdf

clean:
	rm -rf build
	rm -rf __pycache__
