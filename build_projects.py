#!/usr/bin/env python

from pathlib import Path
from html import escape

from markdown import markdown

from page_template import asset_url, render_page
from project_catalog import PROJECTS, Demo, Presentation, Project


def render_demo(demo: Demo):
    source = escape('/' + demo.source, quote=True)
    description = escape(demo.description, quote=True)
    if Path(demo.source).suffix == '.mp4':
        return f'<video src="{source}" autoplay loop muted playsinline aria-label="{description}"></video>'
    return f'<img src="{source}" alt="{description}">'


def render_presentation(presentation: Presentation | None):
    if presentation is None:
        return ''
    source = escape('/' + presentation.source, quote=True)
    poster = escape('/' + presentation.poster, quote=True)
    description = escape(presentation.description, quote=True)
    return f"""<div class="project-presentation">
        <video data-src="{source}" poster="{poster}" playsinline preload="none" aria-label="{description}">
            <a href="{source}">Watch presentation</a>
        </video>
        <button class="project-presentation-play" type="button" aria-label="Play video" title="Play video" hidden>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <noscript><a href="{source}">Watch presentation</a></noscript>
    </div>"""


def render_project(project: Project):
    description = markdown(Path(project.description_file).read_text(encoding='utf-8'))
    demo_items = [render_demo(demo) for demo in project.demos]
    presentation = render_presentation(project.presentation)
    if presentation and len(demo_items) > 1:
        secondary = '\n'.join([*demo_items[1:], presentation])
        demos = f'{demo_items[0]}<div class="project-demo-stack">{secondary}</div>'
        presentation = ''
    else:
        demos = '\n'.join(demo_items)
    media_class = 'project-demos' if len(project.demos) > 1 else 'project-demo'
    media = f'<div class="{media_class}">{demos}</div>' if demos else ''
    if project.playground:
        media = f'''<iframe class="project-playground" src="{asset_url(project.playground)}"
            title="{escape(project.title, quote=True)} interactive music editor"
            loading="lazy" allow="autoplay" height="490"></iframe>'''
    technology_names = [f'<span class="loud">{escape(technology)}</span>'
                        for technology in project.technologies]
    technologies = (', '.join(technology_names[:-1]) + ' and ' + technology_names[-1]
                    if len(technology_names) > 1 else ''.join(technology_names))
    return f"""<article class="project" id="{escape(project.slug, quote=True)}">
        <header class="box project-heading">
            <h2 class="project-title"><a href="{escape(project.url, quote=True)}">{escape(project.title)}</a></h2>
            <p class="project-meta quiet">from <span class="project-date loud">{escape(project.dates)}</span> using {technologies}</p>
        </header>
        <div class="project-copy">{description}</div>
        {media}
        {presentation}
    </article>"""


def render_html():
    projects = '\n'.join(render_project(project) for project in
                         sorted(PROJECTS, key=lambda project: project.latest_year, reverse=True))
    extra_head = f"""
        <link rel="stylesheet" href="{asset_url('projects.css')}">
        <script src="{asset_url('projects.js')}" defer></script>
"""
    return render_page(
        f'<h1>Projects</h1>\n{projects}',
        title='Projects — Sumeet Agarwal',
        active_page='projects',
        extra_head=extra_head,
    )


if __name__ == '__main__':
    print(render_html())
