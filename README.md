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

Local preview and Dokku both serve `build/` through Gunicorn and WhiteNoise
(`site_server.py`). This supports HTTP byte ranges, so videos can seek to an
unbuffered position without first downloading the entire file. `make serve`
enables development file refresh; production indexes the built files on startup.
After dependency changes, update an existing environment with
`.venv/bin/python -m pip install -r requirements.txt`. `make test` builds the
site and checks real HTTP range responses, media bytes, and existing routes.

The projects preview is at http://localhost:8000/ and the résumé is at
http://localhost:8000/resume/. Project descriptions live in `projects/solsolver.md`, `projects/zac.md`,
`projects/codemaestro.md`, `projects/rejectsynth.md`, and `projects/golden.md`. `project_catalog.py` supplies their titles,
dates, technologies, links, and demo assets to the reusable `render_project()` function. New projects
need a Markdown description and a catalog entry, without copied layout HTML.
Projects are sorted newest first, using the latest year in each displayed date range.
Project-specific layout is in `projects.css`. After editing, run `make html`
and refresh.
Project headers use the old Reading page's compact Graublau titles, linked to
their repositories, followed by a smaller "from <date> using <technologies>" line.
The projects page sets a default new-tab target for all links, including its
navigation and Markdown links; the résumé page keeps its existing behavior.
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

solsolver uses the same click-to-play component for `projects/solsolver-full.mp4`.
Only `projects/solsolver-poster.webp` downloads before Play. The 2560×1440,
60 FPS video includes recognition, solving, all 113 moves, the victory, and
original game music/effects, with timestamped terminal output. The opening
retains about seven seconds of computation; only output-free startup gaps
are shortened. Gameplay runs at its recorded speed. Its 2022 date comes from
the solver's September–November commit history.
The terminal clears after the last move so the victory fortune is readable.
The full video is about 30 MB and 2:47 long; its initial poster is about 87 KB.

The lossless master, complete logs, board snapshots and export script are in
`~/solsolver-portfolio-2026-11-21/1440p-tuned/`. Regenerate the full overlay
export there with `python3 terminal.py --full`; `full-edit.json` records every
kept interval. Copy `solsolver-1440p-full.mp4` to `projects/solsolver-full.mp4`
and run `make html`. The web export uses H.264 CRF 20 and AAC audio with MP4
faststart; the large lossless master is kept outside the site repository.

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

## Portfolio backlog

Working shortlist retained from `~/Downloads/portfolio_master_inventory.md`
(11 November 2026) and the portfolio discussion. Pick one project at a time;
Sumeet writes the public description. Prioritize a clear demo for the effort.

**solsolver**, selected 20 November 2026. The local checkout is
`~/solsolver`; The Zachtronics Solitaire Collection is installed in Steam.
Start by recovering the existing solver and screen automation, then capture
the game being solved. The Rust solver, Python card recognition, and actual
mouse playback should each be verified before recording.

Local demo work is saved in `~/solsolver-portfolio-2026-11-20/`, with raw
recordings and board snapshots under `~/.cache/solsolver-portfolio/`.
Use the private Xvfb display `:181` for the game and mouse automation, never
the physical desktop. `runtime.json` in the demo folder records the launch
setup and original save backup. The installed game needs the system SDL
library preloaded; no game files or solver source were changed. The demo
wrapper adds input pacing and stops if a move leaves its source unchanged.
`solsolver-log-preview.mp4` is a 25-second overlay layout preview from a
working portion of the first take; that full take later missed a drag.
The third take completed the remaining moves 16–85 without interruption
and reached the victory screen (win count 653 → 654). Its raw recording,
timestamped move log, and checkpoints are in the cache's `third-take/` folder;
`solsolver-ending-preview.mp4` shows the last three moves and the win.
Those 20 November previews are silent. A fresh offscreen recording with the
game's own music and effects is in `~/solsolver-portfolio-2026-11-21/`:
`solsolver-full-with-overlay-and-audio.mp4` contains all 66 moves and the win
(654 → 655), with the actual move log overlaid throughout.
`solsolver-full-with-audio.mp4` is the original capture without the overlay;
`solsolver-with-audio.mp4` shows the ending with the actual move log overlaid.
The audio take's starting board, save snapshot, solution, timestamped log,
and checkpoints are under the cache's `audio-take-2026-11-21/` folder.
Audio was captured through a private sink with no speaker loopback, leaving
the physical speakers muted. The private services and sink were stopped
after capture. These clips have not been added to the site or deployed.
The `smooth-test/` subfolder in the 21 November demo directory contains a
36-second, 12-move trial (`solsolver-smoother-terminal.mp4`) with game audio,
a larger terminal-style log panel, 60 FPS capture, and finer mouse movement.
Its wrapper reduces ordinary move intervals from about 3.9 to 2.1 seconds;
all 12 source checks passed, but game rendering still repeats some frames.
This is a pacing/style sample, not another complete winning run. Its board,
logs, and raw footage are in the cache's `smooth-take-2026-11-21/` folder.
The subsequent `gpu-test/solsolver-gpu-terminal.mp4` is a 35-second offscreen
trial using Intel Iris Xe acceleration through headless Weston + rootful
Xwayland. It retains the same movement timings, terminal panel, and game audio.
Sampled drag updates improved from roughly 30–33 to 51–60 distinct frames/s;
all 12 source checks passed. The private compositor also needs native pointer
events instead of XTEST, implemented in the isolated demo's `private-input.c`.
`gpu-test/runtime.json` records the setup and comparison limits. This compares
capture pipelines, not a GPU-only benchmark; no better computer was needed.
The `1440p-test/` subfolder contains two subsequent 2560×1440 trials with
timestamped console output captured from before recognition through solving
and the first 12 moves. `solsolver-1440p-terminal.mp4` uses software encoding;
`solsolver-1440p-hardware-terminal.mp4` tests Intel VAAPI encoding. Both retain
real game audio and the full console stream, including the debug board dump
and sleep messages, in a scrolling terminal panel. Neither is a complete win.
Both passed all 12 source checks, but sampled drag updates were less consistent
than the earlier 900p GPU trial (roughly 40–58 distinct FPS for software and
30–38 for hardware encoding). `1440p-test/runtime.json` records the measurements
and limits. The original solver is unchanged;
all private capture services and the recording-only audio sink were stopped.
Review of that opening found the full debug dump too dense for the five-line
overlay. The short portfolio preview now starts around the real
`solved in … moves` output, with the complete run/log kept separately.
The wrapper now invokes ImageMagick 7's `magick`
entry point instead of deprecated `convert`, tested without a warning.
An offline recognition benchmark is saved as `1440p-test/recognition-benchmark.json`.
Limiting OpenCV's per-worker thread count did not show a consistent improvement;
the precise capture/rendering bottleneck remains unisolated.

The subsequent `1080p/` folder contains a complete 1920×1080 winning run:
183 moves, 183 passed source checks, win count 655 → 656. The 39.6-second
`solsolver-1080p-preview.mp4` starts at the real `solved in 183 moves` line,
with a wider terminal panel, smaller DejaVu Sans Mono text, original music
and effects, and no speed changes. Recognition and computation are trimmed
from this preview. The entire 7:28 capture remains as
`solsolver-1080p-complete-raw.mp4`, without an overlay, alongside the complete
`console.log` and timestamped `console.jsonl`. The larger raw recording is a
review/master artifact, not a proposed website download.
Sampled drag updates have a median of 60 distinct FPS; three late samples
fell to 30–48, so this is not a claim of perfect 60 FPS throughout. The capture
reported 279 dropped frames across 7:28. `measurement.json` documents the
method and limits; `runtime.json` records the isolated setup. The new run has
no ImageMagick warning. Private services and the audio sink were stopped,
without changing the physical speaker mute setting. Nothing was deployed.

The rejectsynth font/palette comparison is resolved: keep DejaVu Sans Mono
and the original colors, with gutters removed and inline error diagnostics.
Alternative font/theme specimens remain in `~/rejectsynth-comparison-2026-11-21/`.

Sumeet prefers 1440p and some visible startup over the immediate-play 1080p
cut. `~/solsolver-portfolio-2026-11-21/1440p-opening/solsolver-1440p-opening.mp4`
is the resulting 46-second review preview (6.2 MB): recognition, the original
board dump, solution output, then mouse playback beginning at about 8.4 seconds.
The terminal has ten rows during startup and five during play, using smaller
DejaVu Sans Mono text with the original dump indentation preserved. The edit
removes only an output-free recognition pause; game speed is unchanged and
the original music/effects remain. `edit.json` records the exact cut.
This is an opening sample, not a complete winning game. The uncut 86-second
take includes recognition, solving and 18 verified moves; its video and complete
console logs are in the same folder. The raw capture uses fragmented MP4 and
an independent systemd user service after an earlier take was interrupted.
1440p still has frame drops: sampled drag updates were about 46–57 distinct
FPS (median 47), below the 1080p take. All private services and the audio sink
were stopped. These files remain local and have not been added to the site.

The approved opening is preserved. The next iteration is
`~/solsolver-portfolio-2026-11-21/1440p-tuned/solsolver-1440p-tuned.mp4`:
1440p/60 FPS, the same terminal treatment, roughly seven seconds of visible
startup, and original music/effects. The full 113-move run won the game
(656 → 657), with all 113 source checks passing and no warnings.
The private input driver now uses 120 Hz monotonic deadlines and avoids
PyAutoGUI's repeated pointer queries and implicit per-action pauses.
Base settling is 0.3 seconds plus 0.4 per automatically collected card;
ordinary moves have a measured median of 1.04 seconds versus 2.69 in the
preceding 1440p take. This verifies one complete game, not every possible deal.
Recording uses lossless RGB to avoid realtime color conversion; final H.264
compression happens afterward. Recognition/solving concurrency is limited
to leave capacity for recording. Capture drops fell from 1,123 out of 5,167
frames (21.7%) to 77 out of 10,686 (0.72%). Ten of twelve sampled drags reached
60 distinct FPS; the others were about 53 and 57. Different boards and host
load mean this is a practical comparison, not an isolated hardware benchmark.
The folder includes the full 178-second lossless master, console/timing logs,
starting and completed boards, scripts, measurements, and `runtime.json`.
The master is a large local review artifact, not a website download. The
original solver repo is untouched, all private capture services/sink were
cleaned up, and nothing was deployed.

Included in the projects catalog: rejectsynth, solsolver, Zac, CodeMaestro, golden.

| Candidate | What it could show |
|---|---|
| Matcharoni | Pattern-matching language; existing introduction video |
| ClipShare | Copy text or images on one computer, paste on another |
| Goylang | Self-hosting compiler targeting Go |
| EXAc | Higher-level source compiled to EXAPUNKS assembly and run in the game |
| Linux desktop setup | Mouse-driven tiling workflow; recover the setup and media |
| Ceremoney | Haskell CHIP-8 emulator running a game |
| nn-h | Rust port of Tsoding's neural-network library with an egui interface |
| stdless | Rust HTTP server without the standard library |
| SecondDisplay | Linux-to-iPad second-monitor prototype; verify what runs |
| Advent of Code collection | Selected x86, LLVM IR, WebAssembly, and other experiments |
| Noulith LSP | Semantic highlighting for Noulith |
| Hotplug | bspwm workspace and monitor management |
| RejectDOS | Real-mode OS experiments |
| Twitchdrop | Tcl-scriptable Twitch IRC bot written in C |
| Sumcademy | Original software engineering exercises |

Still to locate: VGMix and the Morphy Chess Club bot. The full inventory in
Downloads includes additional small projects and unresolved historical leads.
