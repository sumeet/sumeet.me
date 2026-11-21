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
http://localhost:8000/resume/. Project descriptions live in `projects/zac.md`,
`projects/codemaestro.md`, `projects/rejectsynth.md`, and `projects/golden.md`. `project_catalog.py` supplies their titles,
dates, technologies, links, and demo assets to the reusable `render_project()` function. New projects
need a Markdown description and a catalog entry, without copied layout HTML.
Projects are sorted newest first, using the latest year in each displayed date range.
Project-specific layout is in `projects.css`. After editing, run `make html`
and refresh.
Project headers use the old Reading page's compact Graublau titles, linked to
their repositories, followed by a smaller "from <date> using <technologies>" line.
CodeMaestro uses the original WebP assets: the stack interpreter and completed
file-tree stills above the particle rename loop. The build copies them unchanged.

rejectsynth is embedded as a lazy-loaded, same-origin iframe. Its source remains
in `../rejectsynth/browser` and shares the desktop extension's editor behavior.
`projects/rejectsynth/` contains the static export, its source revision/build
fingerprint, and dependency notices. Do not edit those generated files. After
changing the editor in the rejectsynth repository, refresh the export with:

```sh
make rejectsynth
make html
```

Set `REJECTSYNTH_DIR=/path/to/rejectsynth` if the checkout is elsewhere. This
explicit export step needs Node, Rust and wasm-bindgen; ordinary site builds and
Dokku deployment still only need the existing Python/Make setup. The editor has
an inline Play/Stop link, fixed 50% gain, and optional Vim bindings behind its
top-right icon. It resizes to its content and stops playback when scrolled out
of view. The 2023 date comes from the original September–November commit history.

Zac's Game of Life, help, and Fibonacci demos are visible together and loop
independently, without visible controls or a selector.
The MP4s are converted from the GIFs in the Zac repository's `.README_assets/`
directory; hello-world is deliberately omitted. To regenerate an MP4 with ffmpeg:

```sh
ffmpeg -i input.gif -an -vf fps=30 -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart output.mp4
```

The three loops total about 2.18 MB. These encodes keep the original dimensions
and 30 fps; regenerate from the source GIFs rather than recompressing the MP4s.

golden also uses a muted, looping MP4. Its original GIF is retained for regeneration:

```sh
ffmpeg -i projects/golden-demo.gif -an -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart projects/golden-demo.mp4
```

The golden MP4 is about 1.14 MB, versus 12.81 MB for the GIF. The page references
only the MP4. These are lossy encodes, checked against the originals for text
readability; no resizing, denoising filters, or playback-speed changes are applied.
The converted files are included in the repository, so normal builds do not need ffmpeg.

Zac's presentation video sits below the help and Fibonacci demos in the right
column, with 8px gaps. Both columns align at the top; on narrow screens they
become a single column. Only the poster loads initially. Pressing Play assigns
the video's source and enables sound and native playback controls.
`projects/zac-presentation.mp4` is the 08:30.000–09:41.700 excerpt from
the supplied `~/Downloads/videoplayback.mp4`, ending before the next project.
The original file is unchanged. To recreate the clip and its title-card poster:

```sh
ffmpeg -ss 510 -i ~/Downloads/videoplayback.mp4 -t 71.7 -map 0:v:0 -map 0:a:0 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart projects/zac-presentation.mp4
ffmpeg -ss 511.5 -i ~/Downloads/videoplayback.mp4 -frames:v 1 projects/zac-presentation-poster.png
```

The site name and navigation use the bundled Liberation Sans Bold webfont in `fonts/`, matching
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
