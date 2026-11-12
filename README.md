This is what powers www.sumeetagarwal.com.

This is a custom Python static-site generator. `resume.py` converts `resume.md`
from Markdown to HTML, and `build_html.py` wraps it in the page template.
`make html` writes `build/index.html` and copies the CSS, fonts, and other assets.
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
