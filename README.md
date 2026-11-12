This is what powers www.sumeetagarwal.com.

This is a custom Python static-site generator. `resume.py` converts `resume.md`
from Markdown to HTML, and `build_html.py` wraps it in the page template.
`make html` writes `build/index.html` and copies the CSS, fonts, and other assets.
The generated `build/` directory is ignored by Git.

For a local preview, use Python 3.11+ and install the dependencies once:

```sh
make setup
```

This creates `.venv/` with the local Markdown and WeasyPrint dependencies.
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
