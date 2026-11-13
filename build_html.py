#!/usr/bin/env python

from pathlib import Path

import build_projects
import build_resume


def build_site():
    output = Path('build')
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
    for destination, html in pages.items():
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
