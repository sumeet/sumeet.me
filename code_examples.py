"""Render recorded examples with the exact source and assembly used in-game."""
from html import escape
from pathlib import Path
import re

from project_catalog import Project


TOKENS = re.compile(
    r'//[^\n]*|"[^"\n]*"|\b(?:spawn|link|kill|HALT|while|loop|if|else|continue|break|wait)\b'
    r'|%repeat\b|#[A-Za-z_]\w*|\$[A-Za-z_]\w*|\b\d+\b'
)


def highlight_source(source):
    result = []
    position = 0
    for match in TOKENS.finditer(source):
        result.append(escape(source[position:match.start()]))
        token = match.group()
        kind = ('comment' if token.startswith('//') else
                'string' if token.startswith('"') else
                'number' if token.isnumeric() else
                'hardware' if token.startswith('#') else
                'channel' if token.startswith('$') else 'keyword')
        result.append(f'<span class="syntax-{kind}">{escape(token)}</span>')
        position = match.end()
    result.append(escape(source[position:]))
    return ''.join(result)


def render_code_examples(project: Project):
    tabs, panels = [], []
    default = project.default_example or project.examples[0].slug
    for example in project.examples:
        selected = example.slug == default
        name = f'{project.slug}-{example.slug}'
        tab_id, panel_id = f'{name}-tab', f'{name}-panel'
        tabs.append(f'''<button type="button" role="tab" id="{tab_id}"
            aria-controls="{panel_id}" aria-selected="{str(selected).lower()}"
            tabindex="{0 if selected else -1}">{escape(example.title)}</button>''')
        assembly = ''.join(
            f'<div class="example-assembly-file"><span class="example-exa-name">{Path(path).stem.upper()}</span>'
            f'<pre><code data-code-source="/{escape(path, quote=True)}">'
            f'{escape(Path(path).read_text())}</code></pre></div>'
            for path in example.assembly
        )
        panels.append(f'''<div class="project-example-panel" id="{panel_id}" role="tabpanel"
            aria-labelledby="{tab_id}"{'' if selected else ' hidden'}>
            <div class="project-example-content">
                <figure class="project-example-source">
                    <div class="example-code-scroll" tabindex="0" aria-label="{escape(example.title)} EXAc source">
                        <pre><code data-code-source="/{escape(example.source, quote=True)}">{highlight_source(Path(example.source).read_text())}</code></pre>
                    </div>
                </figure>
                <figure class="project-example-assembly">
                    <div class="example-code-scroll" tabindex="0" aria-label="{escape(example.title)} EXAPUNKS assembly">{assembly}</div>
                </figure>
                <figure class="project-example-replay">
                    <img class="example-replay" src="/{escape(example.poster, quote=True)}"
                        data-src="/{escape(example.replay, quote=True)}" data-poster="/{escape(example.poster, quote=True)}"
                        width="816" height="603" loading="lazy"
                        alt="EXAPUNKS replay of {escape(example.title, quote=True)}">
                    <noscript><img class="example-replay" src="/{escape(example.replay, quote=True)}"
                        width="816" height="603" loading="lazy"
                        alt="EXAPUNKS replay of {escape(example.title, quote=True)}"></noscript>
                </figure>
            </div>
        </div>''')
    return f'''<div class="project-examples">
        <div class="project-example-tabs site-choices" role="tablist" aria-label="{escape(project.title)} examples">{''.join(tabs)}</div>
        {''.join(panels)}
        <div class="example-legend" aria-label="EXAc notation">
            <span><code>spawn</code> create an EXA</span>
            <span><code>link</code> move between hosts</span>
            <span><code>name/x</code> a name for register X</span>
            <span><code>$ch</code> send or receive a message</span>
            <span><code>#ctrl</code> a host’s hardware register</span>
            <span><code>%repeat</code> repeat code at compile time</span>
        </div>
        <noscript><style>.projects .project-examples, .projects .project-example-panel[hidden] {{ display: block; }} .projects .project-example-tabs, .projects .example-replay[data-src] {{ display: none; }}</style></noscript>
    </div>'''
