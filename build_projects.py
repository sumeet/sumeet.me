#!/usr/bin/env python

from pathlib import Path
from html import escape

from markdown import markdown

from page_template import asset_url, render_page
from project_catalog import PROJECTS, Demo, Project


def render_demo(demo: Demo):
    source = escape('/' + demo.source, quote=True)
    description = escape(demo.description, quote=True)
    if Path(demo.source).suffix == '.mp4':
        return f'<video src="{source}" autoplay loop muted playsinline aria-label="{description}"></video>'
    return f'<img src="{source}" alt="{description}">'


def render_project(project: Project):
    description = markdown(Path(project.description_file).read_text(encoding='utf-8'))
    demos = '\n'.join(render_demo(demo) for demo in project.demos)
    media_class = 'project-demos' if len(project.demos) > 1 else 'project-demo'
    return f"""<article class="project" id="{escape(project.slug, quote=True)}">
        <h2 class="box project-title"><a href="{escape(project.url, quote=True)}">{escape(project.title)}</a></h2>
        <div class="project-copy">{description}</div>
        <div class="{media_class}">{demos}</div>
    </article>"""


def render_html():
    projects = '\n'.join(render_project(project) for project in PROJECTS)
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
