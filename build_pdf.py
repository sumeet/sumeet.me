#!/usr/bin/env python
import os.path
import sys
from base64 import b64encode
from io import BytesIO
from math import atan, degrees

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from weasyprint import CSS
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

import resume


def cwd():
    return os.path.dirname(os.path.realpath(__file__))


def italic_font_face(family, filename):
    # The old Cairo renderer synthesized italics with a 0.2 shear. WeasyPrint
    # 53+ no longer does this (Kozea/WeasyPrint#1470), so supply that same face.
    # Derive it at build time: the bundled fonts remain the source of truth.
    font = TTFont(os.path.join(cwd(), filename), fontNumber=0)
    glyph_set = font.getGlyphSet()
    outlines = {}
    is_truetype = 'glyf' in font
    top_dict = None if is_truetype else font['CFF '].cff.topDictIndex[0]
    for name, glyph in glyph_set.items():
        recording = DecomposingRecordingPen(glyph_set)
        glyph.draw(recording)
        pen = TTGlyphPen(None) if is_truetype else T2CharStringPen(
            glyph.width - top_dict.Private.nominalWidthX, None)
        recording.replay(TransformPen(pen, (1, 0, 0.2, 1, 0, 0)))
        outlines[name] = pen.glyph() if is_truetype else pen.getCharString(
            private=top_dict.Private, globalSubrs=font['CFF '].cff.GlobalSubrs)
    if is_truetype:
        font['glyf'].glyphs = outlines
        # Keep each outline's left bearing in sync after shearing it. Otherwise
        # TrueType renderers shift letters to preserve the old upright bearing.
        for name, glyph in outlines.items():
            glyph.recalcBounds(font['glyf'])
            advance, _ = font['hmtx'][name]
            font['hmtx'][name] = (advance, getattr(glyph, 'xMin', 0))
    else:
        for name, outline in outlines.items():
            top_dict.CharStrings[name] = outline
        top_dict.ItalicAngle = -degrees(atan(0.2))
    font['post'].italicAngle = -degrees(atan(0.2))
    font['head'].macStyle |= 2
    font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~64) | 1
    output = BytesIO()
    font.save(output)
    source = b64encode(output.getvalue()).decode('ascii')
    font_type = 'ttf' if is_truetype else 'otf'
    return f'''@font-face {{
        font-family: "{family}";
        font-style: italic;
        font-weight: normal;
        src: url(data:font/{font_type};base64,{source});
    }}'''


css = """
@page {
    size: A4;
    margin: 18mm 20mm;
}

@page:first {
    margin-top: 22mm;
}

body {
    font-size: 75%;
    font-family: "Lucida Grande";
    color: #333333;
    line-height: 1.5em;
}

/* Preserve the original renderer's link blue and font-size / 18 underline. */
a[href] {
    color: #0000ee;
    text-decoration-thickness: 0.0555555556em;
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
p, ul { margin-top: 0.75em; margin-bottom: 0.75em; }

/* Preserve the original spacing around the stacked link lists. */
blockquote p, blockquote ul { margin-top: 1em; margin-bottom: 1em; }

h1 {
    font-weight: normal;
    color: #222222;
    font-size: 3em;
    line-height: 1;
    margin-top: 0;
    margin-bottom: 0.5em;
}

h2 { font-weight: normal; color: #222222; font-size: 2em; margin-top: 1em; margin-bottom: 0.75em; }

h3 { font-weight: normal; color: #222222; font-size: 1.5em; line-height: 1; margin-bottom: 1em; }

h4 { font-weight: normal; color: #222222; font-size: 1.2em; line-height: 1.25; margin-top: 1em; margin-bottom: 0.5em; }

h4 + h4 { margin-top: 0; }

h5 { font-weight: normal; color: #222222; font-size: 1em; font-weight: bold; margin-top: 1em; margin-bottom: 0.75em; }

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
        font_config = FontConfiguration()
        italic_faces = ''.join([
            italic_font_face('Lucida Grande', 'LucidaGrande.ttc'),
            italic_font_face('Graublau Web', 'GraublauWeb.otf'),
        ])
        html = HTML(string=resume.html(), base_url=f'file://{cwd()}/')
        html.write_pdf(output_filename, font_config=font_config, stylesheets=[
            CSS(string=italic_faces + css, font_config=font_config),
        ])
