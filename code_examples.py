"""Render source examples and their recorded compiler output."""
from html import escape
from pathlib import Path
import re

from project_catalog import CodeComparison, CodeTaste, Project


TOKENS = re.compile(
    r'//[^\n]*|"[^"\n]*"|\b(?:spawn|link|kill|HALT|while|loop|if|else|continue|break|wait)\b'
    r'|%repeat\b|#[A-Za-z_]\w*|\$[A-Za-z_]\w*|\b\d+\b'
)

GOYLANG_TOKENS = re.compile(
    r'//[^\n]*|"(?:\\.|[^"\\])*"|\b(?:func|enum|struct|match|return|if|else|'
    r'while|break|continue|type|interface|var|for|range|import|package)\b|\b\d+\b'
)

def highlight_source(source, tokens=TOKENS):
    result = []
    position = 0
    for match in tokens.finditer(source):
        result.append(escape(source[position:match.start()]))
        token = match.group()
        kind = ('comment' if token.startswith('//') else
                'string' if token.startswith(('"', "'")) else
                'number' if token.isnumeric() else
                'hardware' if token.startswith('#') else
                'channel' if token.startswith('$') else 'keyword')
        result.append(f'<span class="syntax-{kind}">{escape(token)}</span>')
        position = match.end()
    result.append(escape(source[position:]))
    return ''.join(result)


def example_tab(tab_id, panel_id, title, selected):
    label = escape(title)
    return f'''<button type="button" role="tab" id="{tab_id}" aria-controls="{panel_id}"
        aria-selected="{str(selected).lower()}" tabindex="{0 if selected else -1}" data-label="{label}">{label}</button>'''


def render_code_taste(example: CodeTaste):
    source = Path(example.source).read_text().removesuffix('\n')
    output = Path(example.output).read_text().removesuffix('\n')
    code = re.sub(r'^(//[ \t]+)(https?://\S+)$',
                  r'\1<a href="\2" target="_blank" rel="noopener">\2</a>',
                  escape(source), flags=re.MULTILINE)
    return f'''<figure class="project-pad taste-example" aria-label="{escape(example.title, quote=True)}">
        <div class="taste-source"><pre><code>{code}</code></pre></div>
        <pre class="taste-value pad-output" aria-label="Output" aria-live="polite" aria-atomic="true"><samp>{escape(output)}</samp></pre>
    </figure>'''


def render_code_comparison(example: CodeComparison):
    panes = []
    for label, path, pane_class in [
        ('goylang', example.source, 'project-example-source'),
        ('Generated Go', example.generated, 'pad-output'),
    ]:
        source = Path(path).read_text()
        panes.append(f'''<figure class="{pane_class}">
            <figcaption class="comparison-label quiet">{label}</figcaption>
            <div class="example-code-scroll" tabindex="0" aria-label="{label} compiler excerpt">
                <pre><code data-code-source="/{escape(path, quote=True)}">{highlight_source(source, GOYLANG_TOKENS)}</code></pre>
            </div>
        </figure>''')
    return f'''<div class="project-pad pad-columns project-code-comparison">{''.join(panes)}</div>'''


def render_code_examples(project: Project):
    tabs, panels = [], []
    default = project.default_example or project.examples[0].slug
    for example in project.examples:
        selected = example.slug == default
        name = f'{project.slug}-{example.slug}'
        tab_id, panel_id = f'{name}-tab', f'{name}-panel'
        tabs.append(example_tab(tab_id, panel_id, example.title, selected))
        assembly = ''.join(
            f'<div class="example-assembly-file"><span class="example-exa-name">{Path(path).stem.upper()}</span>'
            f'<pre><code data-code-source="/{escape(path, quote=True)}">'
            f'{escape(Path(path).read_text())}</code></pre></div>'
            for path in example.assembly
        )
        panels.append(f'''<div class="project-example-panel" id="{panel_id}" role="tabpanel"
            aria-labelledby="{tab_id}"{'' if selected else ' hidden'}>
            <div class="project-example-content">
                <div class="project-pad pad-columns">
                    <figure class="project-example-source">
                        <div class="example-code-scroll" tabindex="0" aria-label="{escape(example.title)} EXAc source">
                            <pre><code data-code-source="/{escape(example.source, quote=True)}">{highlight_source(Path(example.source).read_text())}</code></pre>
                        </div>
                    </figure>
                    <figure class="project-example-assembly pad-output">
                        <div class="example-code-scroll" tabindex="0" aria-label="{escape(example.title)} EXAPUNKS assembly">{assembly}</div>
                    </figure>
                </div>
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
