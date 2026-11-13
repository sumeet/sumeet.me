from hashlib import sha256
from html import escape
from pathlib import Path


def asset_url(path):
    version = sha256(Path(path).read_bytes()).hexdigest()[:12]
    return f'/{path}?v={version}'


NAVIGATION = (
    ('projects', '/', 'projects'),
    ('resume', '/resume/', 'resume'),
)


def render_navigation(active_page):
    links = []
    for page, url, label in NAVIGATION:
        current = ' aria-current="page"' if page == active_page else ''
        links.append(f'<li><a href="{url}"{current}>{label}</a></li>')
    return f'<nav id="nav" aria-label="Main"><ul>{"".join(links)}</ul></nav>'


def render_page(content, *, title, active_page, sidebar=None, extra_head=''):
    if sidebar is not None:
        content = f"""<div class="page-with-sidebar">
                <div id="content">{content}</div>
                <aside id="sidebar">{sidebar}</aside>
            </div>"""
    return f"""<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(title)}</title>
        <link rel="stylesheet" href="{asset_url('style.css')}">
        {extra_head}
    </head>
    <body class="{escape(active_page, quote=True)}">
        <header id="header">
            <a class="site-name" href="/">sumeet.me</a>
            {render_navigation(active_page)}
        </header>
        <main id="container">
            {content}
        </main>
    </body>
</html>
"""
