from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Demo:
    source: str
    description: str


@dataclass(frozen=True)
class Presentation:
    source: str
    poster: str
    description: str


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    dates: str
    technologies: tuple[str, ...]
    url: str
    description_file: str
    demos: tuple[Demo, ...]
    presentation: Presentation | None = None
    playground: str | None = None

    @property
    def latest_year(self):
        return max(int(year) for year in re.findall(r'\d{4}', self.dates))


# Rendered newest first by latest_year; descriptions are handwritten Markdown files.
PROJECTS = (
    Project(
        slug='solsolver',
        title='solsolver',
        dates='2022',
        technologies=('Rust', 'Python', 'OpenCV'),
        url='https://github.com/sumeet/solsolver',
        description_file='projects/solsolver.md',
        demos=(),
        presentation=Presentation(
            source='projects/solsolver-full.mp4',
            poster='projects/solsolver-poster.webp',
            description="solsolver recognizing, solving, and playing a complete game of Fortune's Foundation, with terminal output and game audio",
        ),
    ),
    Project(
        slug='zac',
        title='Zac',
        dates='2021',
        technologies=('Rust',),
        url='https://github.com/sumeet/Zac',
        description_file='projects/zac.md',
        demos=(
            Demo('projects/zac-gol.mp4', 'Zac: Game of Life running in source code comments'),
            Demo('projects/zac-help.mp4', 'Zac: built-in help written into source code comments'),
            Demo('projects/zac-fib.mp4', 'Zac: a Fibonacci sequence written into source code comments'),
        ),
        presentation=Presentation(
            source='projects/zac-presentation.mp4',
            poster='projects/zac-presentation-poster.png',
            description='Presentation of Zac with spoken commentary',
        ),
    ),
    Project(
        slug='codemaestro',
        title='CodeMaestro',
        dates='2018–2020',
        technologies=('Rust',),
        url='https://github.com/sumeet/CodeMaestro',
        description_file='projects/codemaestro.md',
        demos=(
            Demo('projects/codemaestro-stack-interpreter.webp', 'CodeMaestro stack interpreter showing instruction choices and the result'),
            Demo('projects/codemaestro-file-tree-completed.webp', 'Completed recursive file paths function in CodeMaestro'),
            Demo('projects/codemaestro-particle-rename.webp', 'Renaming a Particle field in CodeMaestro alongside the code that uses it'),
        ),
    ),
    Project(
        slug='rejectsynth',
        title='rejectsynth',
        dates='2023',
        technologies=('Rust', 'VSCode'),
        url='https://github.com/sumeet/rejectsynth',
        description_file='projects/rejectsynth.md',
        demos=(),
        playground='projects/rejectsynth/index.html',
    ),
    Project(
        slug='golden',
        title='golden',
        dates='2018',
        technologies=('Python',),
        url='https://github.com/sumeet/golden',
        description_file='projects/golden.md',
        demos=(
            Demo('projects/golden-demo.mp4', 'Windows resizing as focus moves around a tiled desktop'),
        ),
    ),
)
