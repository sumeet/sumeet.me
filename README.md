This is what powers www.sumeetagarwal.com.

This is a custom Python static-site generator. `build_html.py` builds the
projects homepage at `/` and the résumé at `/resume/`. `build_projects.py` and
`build_resume.py` supply their content to `page_template.py`, which owns the
shared header, navigation, active-page state, and optional sidebar. Both pages
use the same responsive 960px layout and typography from `style.css`.
`resume.py` converts `resume.md` to HTML; the same Markdown still powers the PDF.
`make html` writes `build/index.html` and `build/resume/index.html`, and copies
the CSS, fonts, and other assets. The old `/projects.html` preview redirects to `/`.
The generated `build/` directory is ignored by Git.

For a local preview, install Python 3.13 (the version specified in
`.python-version`), then install the dependencies once:

```sh
make setup
```

This creates `.venv/` using the same `requirements.txt` as the Python buildpack.
The Makefile automatically uses this environment when present. WeasyPrint
also needs system Pango libraries; see its [installation instructions](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

Build both HTML and PDF and start the preview:

```sh
make serve
```

Open http://localhost:8000. After editing the source, run `make` in another
terminal to rebuild both formats, then refresh the browser. The server does
not rebuild automatically.

Use `make html` or `make pdf` to rebuild only one format. PDF generation uses
WeasyPrint and the bundled fonts. `make clean` removes the generated output.
The PDF build derives italic faces from those fonts to preserve the original
renderer’s appearance; no separate font files or manual preparation are needed.

The projects preview is at http://localhost:8000/ and the résumé is at
http://localhost:8000/resume/. Project descriptions live in `projects/zac.md`
and `projects/golden.md`. `project_catalog.py` supplies their order, titles,
links, and demo assets to the reusable `render_project()` function. New projects
need a Markdown description and a catalog entry, without copied layout HTML.
Project-specific layout is in `projects.css`. After editing, run `make html`
and refresh.
Zac's Game of Life, help, and Fibonacci demos are visible together and loop
independently, without visible controls or a selector.
The MP4s are converted from the GIFs in the Zac repository's `.README_assets/`
directory; hello-world is deliberately omitted. To regenerate an MP4 with ffmpeg:

```sh
ffmpeg -i input.gif -an -vf fps=30 -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -movflags +faststart output.mp4
```

The converted files are included in the repository, so normal builds do not need ffmpeg.

Project titles use the bundled Liberation Sans Bold webfont in `fonts/`, matching
the old navigation's rendered appearance in Helium. Its SIL Open Font License
is included alongside it.

Deployment uses the Python and Make buildpacks listed in `.buildpacks`.
The Python buildpack reads `.python-version` and `requirements.txt`; the Make
buildpack runs `make`. The live Dokku app is `nice`, reached by the `dokku2`
Git remote. It uses the Heroku-24 build image, configured per app:

```sh
ssh root@sumeet.me dokku buildpacks:set-property nice stack gliderlabs/herokuish:latest-24
```

After committing changes, push the source to GitHub and deploy to Dokku:

```sh
git push origin master
git push dokku2 master
```
