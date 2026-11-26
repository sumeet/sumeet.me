#!/usr/bin/env python

import os
from pathlib import Path
import shutil

import build_projects
import build_resume
from page_template import asset_url
from project_catalog import PROJECTS


def build_site():
    output = Path('build')
    local_preview = os.environ.get('SITE_DEV') == '1'
    output.mkdir(exist_ok=True)
    resume_directory = output / 'resume'
    # Older builds made /resume an alias for the homepage.
    if resume_directory.is_symlink():
        resume_directory.unlink()
    resume_directory.mkdir(exist_ok=True)

    pages = {
        output / 'index.html': build_projects.render_html(),
        resume_directory / 'index.html': build_resume.render_html(),
    }
    # Theme the embedded copies while keeping each project's export standalone.
    pad_link = f'<link rel="stylesheet" href="{asset_url("pads.css")}">'
    for project in PROJECTS:
        if not project.playground:
            continue
        entry = Path(project.playground.source)
        destination = output / entry.parent
        if not project.listed and not (local_preview and entry.is_file()):
            # An earlier preview build may have left the entire export here.
            if destination.exists():
                shutil.rmtree(destination)
            continue
        shutil.copytree(entry.parent, destination, dirs_exist_ok=True)
        pages[output / entry] = entry.read_text(encoding='utf-8').replace(
            '</head>', f'    {pad_link}\n</head>', 1)

    replay = Path('previews/nn-h-training')
    if local_preview and (output / 'projects/nn-h/index.html').is_file():
        shutil.copytree(replay, output / replay, dirs_exist_ok=True)
    elif (output / replay).exists():
        shutil.rmtree(output / replay)
    for destination, html in pages.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding='utf-8')

    # Keep existing local preview bookmarks pointing at the projects homepage.
    (output / 'projects.html').write_text('''<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="0; url=/">
        <link rel="canonical" href="/">
        <title>Projects — Sumeet Agarwal</title>
    </head>
    <body><a href="/">Projects</a></body>
</html>
''', encoding='utf-8')


if __name__ == '__main__':
    build_site()
