"""Render the stdless source listing with in-page definition controls."""
from html import escape
from pathlib import Path
import re

from pygments.lexers import RustLexer
from pygments.token import Comment, Keyword, Name, Number, String

from project_catalog import Project


ITEM = re.compile(r'^(?:pub )?(?:fn|struct|type|const) (\w+)', re.MULTILINE)
IMPORT = re.compile(r'^use (\w+)::(\w+);', re.MULTILINE)
ENTRY = re.compile(r'^#\[no_mangle\](?=\s+fn _start\b)', re.MULTILINE)
COLORS = ((Comment, 'comment'), (Keyword, 'keyword'), (Name.Function, 'function'),
          (String, 'string'), (Number, 'number'))


def render_source(prefix, module, source, definitions):
    imports = {name: origin for origin, name in IMPORT.findall(source)}
    entry = ENTRY.search(source)
    tokens = list(RustLexer().get_tokens_unprocessed(source))
    parts = []
    i = 0
    while i < len(tokens):
        pos, token, value = tokens[i]
        i += 1
        html = escape(value, quote=False)
        color = next((color for group, color in COLORS if token in group), None)
        if color:
            html = f'<span class="syntax-{color}">{html}</span>'
        if entry and pos == entry.start():
            html = f'<span data-source-entry>{html}</span>'
        elif definitions[module].get(value) == pos:
            html = f'<span id="{prefix}-{module}-{value}" tabindex="-1">{html}</span>'
        elif token in Name:
            origin = imports.get(value, module)
            name = value
            if i + 1 < len(tokens) and tokens[i][2] == '::':
                qualifier = 'main' if value == 'crate' else value
                member = tokens[i + 1][2]
                if member in definitions.get(qualifier, {}):
                    origin, name = qualifier, member
                    html += '::' + escape(member)
                    i += 2
            # Method calls and macros can share names with module items.
            if (name in definitions.get(origin, {}) and source[pos-1:pos] != '.'
                    and not source.startswith('!', pos + len(value))):
                html = f'<button type="button" aria-controls="{prefix}-{origin}-{name}">{html}</button>'
        parts.append(html)
    label = f'{prefix}-{module}-file'
    return (f'<figure><figcaption class="example-exa-name" id="{label}">{module}.rs</figcaption>'
            f'<pre class="project-pad" tabindex="0" aria-labelledby="{label}">'
            f'<code>{"".join(parts)}</code></pre></figure>')


def render_rust_sources(project: Project):
    paths = [Path(name) for name in project.rust_sources]
    sources = {p.stem: p.read_text(encoding='utf-8') for p in paths}
    definitions = {module: {m[1]: m.start(1) for m in ITEM.finditer(source)}
                   for module, source in sources.items()}
    pads = [render_source(project.slug, module, source, definitions)
            for module, source in sources.items()]
    return '<div class="source-files">' + '\n'.join(pads) + '</div>'
