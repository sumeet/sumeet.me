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
`projects/codemaestro.md`, `projects/rejectsynth.md`, `projects/nn-h.md`, `projects/exac.md`,
`projects/matcharoni.md`, `projects/stdless.md`, and `projects/golden.md`. `project_catalog.py` supplies their titles,
dates, technologies, links, and demo assets to the reusable `render_project()` function. New projects
need a Markdown description and a catalog entry, without copied layout HTML.
Projects are sorted newest first. An optional internal `sort_date` resolves
ties within a displayed year; otherwise the latest year in the date range is
used. These reflect original project work, not later portfolio maintenance:
nn.h.rs has commits from 15–20 May 2023, before rejectsynth's September–November
2023 history. Public dates remain years.
stdless is dated June 2022, before solsolver's November 2022 work.
Project-specific layout is in `projects.css`. Edit `pads.css` for the shared
code font, padding, frame, source and output surfaces, and syntax colors.
`make html` loads the same stylesheet in the projects page and in the local
copies of the embedded demos. Refresh the page to apply a theme change.
Project headers use the old Reading page's compact Graublau titles, linked to
their repositories, followed by a smaller "from <date> using <technologies>" line.
The projects page sets a default new-tab target for all links, including its
navigation and Markdown links; the résumé page keeps its existing behavior.
CodeMaestro shows the stack interpreter and completed file-tree stills above
the Particle field rename loop. The loop comes from
`~/codemaestro-portfolio-2026-11-23/assets/particle-rename.webp` and is served
as `projects/codemaestro-particle-conditional.webp`.

Matcharoni is dated December 2021, placing it after EXAc and Zac in that year.
On 24 November 2026, Sumeet supplied the expanded description now in
`projects/matcharoni.md`. Three editable pads and the video share a two-column
grid. Minutes parses durations, Binary converts a bit string to decimal, and
`mag` recursively computes the magnitude of a snailfish number. The page initially shows
recorded output. Editing a pad runs its source with the original Rust
interpreter in a WebAssembly worker and displays each top-level expression's
value. The examples share the `digit`, `num` and `sum` patterns in
`projects/matcharoni/prelude.roni`.

The pad entry point lives in `../matcharoni`. After changing the interpreter or
examples, run `make matcharoni` with nightly Rust, the `wasm32-unknown-unknown`
target and wasm-bindgen CLI 0.2.100 installed, then `make html`. Regular HTML
builds use the exported runtime in `projects/matcharoni/pkg/`.
Its media is Sumeet's own [introduction video](https://www.youtube.com/watch?v=2GnqHe2wx_M),
titled "Matcharoni ('n cheese) - langjam 0002" on the `sumeeta` channel.
The local poster is the video's YouTube `hqdefault.jpg` thumbnail.
The shared presentation renderer supports an optional `embed_url`: it creates
the YouTube privacy-enhanced player only when the visitor presses play, so no
YouTube player is loaded with the page. Without JavaScript, the poster links
directly to YouTube. The following archive research is retained for future use.
JT's results video is [Langjam #0002 Winners!](https://www.youtube.com/watch?v=acZx0hDs_u4),
identified through [this Reddit announcement](https://www.reddit.com/r/ProgrammingLanguages/comments/rmuq92/langjam_0002_winners_systems_with_jt/).
The [December 23, 2021 Wayback page](https://web.archive.org/web/20211223232611/https://www.youtube.com/watch?v=acZx0hDs_u4)
confirms a 949-second video by Systems with JT and explicitly mentions Matcharoni.
As checked November 22, 2026, the archived page survives, but the playable media
has not been recovered: Wayback's YouTube media lookup returns 404, and neither
of the two progressive MP4 URLs in the archived player has a CDX capture.
The same media lookup still serves the Zac results recording successfully.
An [Archivarix exact-ID search](https://tube.archivarix.net/?q=acZx0hDs_u4)
also returned metadata without a playable file. Its completed reupload search
found no copy on Archive.org, Dailymotion, or RuTube. The archived player's
16 adaptive audio/video URLs and English caption URL also had no CDX captures.
After manual CAPTCHA verification, [Filmot](https://filmot.com/video/acZx0hDs_u4)
showed a partial metadata record and "Video was not found on archive.org";
no transcript was displayed. Ghostarchive's full-URL search returned no archives,
and [PreserveTube](https://preservetube.com/watch?v=acZx0hDs_u4) returned
"Archive not found". Context Free's current YouTube channel search for `langjam`
returned the first jam's livestream and retrospective, with no second-jam result.
Steve Klabnik's [current channel](https://www.youtube.com/@steveklabnik/streams)
lists one stream: [LangJam: Let's make a programming language! (Part 1)](https://www.youtube.com/watch?v=bze2FAUu32Q),
dated August 20, 2021. Its description explicitly identifies it as work on his
own first-jam entry. His Twitch video archive showed older gaming recordings;
no second-jam roundup was found there. Filmot title searches and channel-filtered
caption searches (including unavailable videos) also found no second-jam roundup
by Klabnik or Context Free. These indexes are incomplete, so this is not proof
that neither creator covered it.

One unresolved Context Free record is [`cGKFHofvzpo`](https://filmot.com/video/cGKFHofvzpo):
Filmot dates it December 5, 2021, but titles it "Trying out JT's langjam - Theme:
\"first-class comments\"" (the first jam's theme). It has only partial metadata,
zero recorded views and no transcript. YouTube reports it unavailable, and
Wayback CDX found neither a watch-page capture nor a YouTube media capture.
Do not treat this date/title mismatch as confirmed second-jam coverage.

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
an inline Play/Stop button, fixed 50% gain, and optional Vim bindings behind its
top-right icon. It resizes to its content and stops playback when scrolled out
of view. The editor grows without a height cap, including when lines wrap, and
wheel input scrolls the containing page rather than an inner editor region.
The 2023 date comes from the original September–November commit history.

nn.h.rs is a local preview. Its CPU neural network, training utility, saved
weights and browser UI live in `../nn-h`. To regenerate the local drawing pad
and open the training replay at `http://localhost:8000/previews/nn-h-training/`, run:

```sh
make nn-h
make serve
```

Set `NN_H_DIR=/path/to/nn-h` for another checkout. Training is a separate step
documented in that repository; visitors load saved weights and recognize digits
locally through WebAssembly. The previous export is also available in site commit
`486b107` under `projects/nn-h/`. Production builds omit the drawing pad and replay.
The egui interface uses WebGL. If that renderer cannot start, the loader uses a
Canvas2D/DOM view with the same controls. Both paths call the same Rust stroke
rasterization, MNIST centering, trained model, and CPU inference; the fallback
does not reimplement the neural network in JavaScript. Its view is maintained
in `../nn-h/web/canvas-pad.js`.

EXAc has three tabbed examples: The Wormhole (selected initially), Valhalla,
and Unknown Network 2. Each tab places its original source and compiled assembly
in a shared pad, with the native EXAPUNKS GIF beside it on desktop.
The replay moves below the pad on narrower screens, and the code panes stack on phones.
The columns have no headings; the example choices sit on one line above all three columns.
The notation legend follows the complete example.
`code_examples.py` renders the shared layout from the catalog; `projects.js`
loads only the selected GIF when the section comes into view, replacing it
with its still poster offscreen. Arrow keys switch examples. The selector uses
regular body type and grey choices; the selected example is bold with a pale
blue rounded background, borrowing the main navigation's colors. The code
panes show thin scrollbars only when their code overflows. Chromium/WebKit gets a minimal 3px thumb override to
keep the scrollbar visible when code overflows; other browsers use native
`scrollbar-width: thin`. These demo GIFs
loop whenever visible, including when the browser requests reduced motion.

`projects/exac/` contains matched source/assembly snapshots and web media.
`provenance.json` records their upstream revision, hashes, and observed game
results. These examples come from the October 2021 EXAc history, placing the
project after Zac chronologically. The source checkout is `../exapunks`.
To update an example, compile its `soln.exc` with `compiler01`, load that exact
assembly into a separate game save, and record the corresponding replay before
replacing the source, assembly, and media together. Compiler-generated labels
can change between invocations; retain the assembly actually used in-game.

The original native GIF exports, isolated saves, and capture evidence are in
`~/exac-portfolio-2026-11-22/`. The site uses byte-for-byte copies of those GIFs
at their native 816×603 resolution and timing, with infinite looping. They total
about 10.2 MB, with only the selected example's GIF requested. `export-tabs.py`
in the capture folder verifies source/save agreement, copies the GIFs, and
refreshes their provenance. Earlier MP4 conversions are archived outside the site.
Ordinary `make html` builds only copy these assets; they need neither the Rust
compiler nor the game. No game saves are shipped with the site.

Zac's Game of Life, help, and Fibonacci demos are visible together and loop
independently, without visible controls or a selector.
The muted H.264 loops are 2× restorations of the original `.README_assets/`
GIFs in Zac at `1515668`. The Langjam submission has identical source files.
The restoration reduces palette dithering, uses repeated letter shapes from the
recordings to recover text detail, and lifts the contrast of dim comments.
Each frame retains its original GIF delay. Game of Life is 748×1204 (495 frames,
16.51s), help is 1300×668 (335 frames, 11.16s), and Fibonacci is 1000×568
(287 frames, 9.56s). Together they are 1.04 MB. The rebuild scripts and timing
check are in `~/zac-portfolio-2026-11-25/recipe/`.

golden also uses a muted, looping MP4. Its original GIF is retained for regeneration:

```sh
ffmpeg -i projects/golden-demo.gif -an -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart projects/golden-demo.mp4
```

The golden MP4 is about 1.14 MB, versus 12.81 MB for the GIF. The page references
only the MP4. The golden encode retains its original dimensions and speed.
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

The navigation uses the bundled Liberation Sans Bold webfont in `fonts/`, matching
the old navigation's rendered appearance in Helium. The site name recreates the
old 167×24 PNG's bold black name and regular grey domain as 28px HTML text.
Liberation Sans is a close approximation; the exact font in that image is unknown,
and its letter shapes differ from the bundled Graublau headings. The regular
wordmark webfont contains only `.me` (about 3 KB); the bold face is shared with
navigation. The SIL Open Font License is included alongside the fonts.

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

Next projects, selected 22 November 2026: **goylang → stdless → Advent of Code**.
goylang is awaiting research; stdless has a local text entry, with Advent of Code next.

The rejected local goylang proposal uses `compileDeclaration` from `~/goylang` at
`fd68d83`, beside its actual generated Go, followed by a recorded
self-compilation transcript. Source provenance is in
`projects/goylang/SOURCE.json`. The transcript's second and third compiler
generations were compared after `gofmt` and are identical. Its description
is intentionally unwritten. Sumeet rejected this presentation on 22 November
2026; do not treat it as an approved demo for deployment. The research handoff
is in `~/Downloads/goylang-research-handoff-2026-11-22/`.

**stdless**, started 22 November 2026: cloned to `~/stdless` at `aaad143`
(original work 26–29 June 2022). The source runs unchanged with
`RUSTC_BOOTSTRAP=1 cargo +1.77.2 build --locked --offline`; the current nightly
rejects its obsolete `maybe_uninit_uninit_array` feature declaration.
An isolated network-namespace check verified the bundled index and page 2
responses byte-for-byte, plus the 404 response. Evidence and the check script
are in `~/stdless-portfolio-2026-11-22/`. `readelf` reports no `DT_NEEDED`
libraries, though the executable still has an ELF interpreter; do not call it
fully static. Sumeet chose a compact text entry with technologies Rust and
Linux syscalls, using his exact wording in `projects/stdless.md`. It is in the
local preview only. No recording or running demo is needed for this entry.

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

Included in the projects catalog: rejectsynth, nn.h.rs, solsolver, Matcharoni, EXAc, Zac, CodeMaestro, golden.

| Candidate | What it could show |
|---|---|
| ClipShare | Copy text or images on one computer, paste on another |
| goylang | Self-hosting compiler targeting Go |
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
