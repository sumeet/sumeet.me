#!/usr/bin/env python
import os.path
import sys

from weasyprint import CSS
from weasyprint import HTML

import resume


def cwd():
    return os.path.dirname(os.path.realpath(__file__))


css = """
body {
    font-size: 75%;
    font-family: "Lucida Grande";
    color: #333333;
    line-height: 1.5em;
}

blockquote {
    margin-left: 0px;
    font-style: italic;
    color: #666;
    font-size: 90%;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Graublau Web";
}

ul { list-style-type: none; margin-left: 0px; padding: 0px; }
li ul { margin: 0px 1.5em; }
li { margin-left: 0px; }

h1 {
    font-weight: normal;
    color: #222222;
    font-size: 3em;
    line-height: 1;
    margin-bottom: 0.5em;
}

h2 { font-weight: normal; color: #222222; font-size: 2em; margin-top: 1em; margin-bottom: 0.75em; }

h3 { font-weight: normal; color: #222222; font-size: 1.5em; line-height: 1; margin-bottom: 1em; }

h4 { font-weight: normal; color: #222222; font-size: 1.2em; line-height: 1.25; margin-bottom: 1.25em; }

h5 { font-weight: normal; color: #222222; font-size: 1em; font-weight: bold; margin-bottom: 1.5em; }

h6 { font-weight: normal; color: #222222; font-size: 1em; font-weight: bold; }
"""

if __name__ == '__main__':
    try:
        output_filename = sys.argv[1]
    except IndexError:
        raise "First arg must be a file to write to (e.g. build/sumeet.pdf)"

    test_mode = True
    try:
        sys.argv[2]
    except IndexError:
        test_mode = False

    if test_mode:
        print(resume.html())
    else:
        html = HTML(string=resume.html(), base_url=f'file://{cwd()}/')
        html.write_pdf(output_filename, stylesheets=[CSS(string=css)])
