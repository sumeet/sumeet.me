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
    embed_url: str | None = None


@dataclass(frozen=True)
class Playground:
    source: str
    description: str
    height: int = 490


@dataclass(frozen=True)
class CodeExample:
    slug: str
    title: str
    source: str
    assembly: tuple[str, ...]
    replay: str
    poster: str


@dataclass(frozen=True)
class CodeComparison:
    source: str
    generated: str


@dataclass(frozen=True)
class CodeTaste:
    slug: str
    title: str
    source: str
    output: str


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
    playground: Playground | None = None
    sort_date: str | None = None
    examples: tuple[CodeExample, ...] = ()
    default_example: str | None = None
    code_comparison: CodeComparison | None = None
    tastes: tuple[CodeTaste, ...] = ()
    rust_sources: tuple[str, ...] = ()
    listed: bool = True

    @property
    def latest_year(self):
        return max(int(year) for year in re.findall(r'\d{4}', self.dates))

    @property
    def sort_key(self):
        return self.sort_date or f'{self.latest_year:04d}-01-01'


# Historical work dates break year ties; present-day demo maintenance does not.
# Descriptions are handwritten Markdown files.
PROJECTS = (
    Project(
        slug='stdless',
        title='stdless',
        dates='2022',
        sort_date='2022-06-29',
        technologies=('Rust', 'Linux syscalls'),
        url='https://github.com/sumeet/stdless',
        description_file='projects/stdless.md',
        demos=(),
        rust_sources=('projects/stdless/main.rs', 'projects/stdless/linux.rs'),
    ),
    Project(
        slug='goylang',
        title='goylang',
        dates='2022',
        sort_date='2022-03-24',
        technologies=('Go',),
        url='https://github.com/sumeet/goylang',
        description_file='projects/goylang.md',
        demos=(),
        code_comparison=CodeComparison(
            source='projects/goylang/compiler.goy',
            generated='projects/goylang/compiler.go',
        ),
    ),
    Project(
        slug='matcharoni',
        title='matcharoni',
        dates='2021',
        sort_date='2021-12-10',
        technologies=('Rust',),
        url='https://github.com/sumeet/matcharoni',
        description_file='projects/matcharoni.md',
        demos=(),
        tastes=(
            CodeTaste(
                'duration', 'Minutes',
                'projects/matcharoni/duration.roni',
                'projects/matcharoni/duration.output.txt',
            ),
            CodeTaste(
                'binary', 'Binary',
                'projects/matcharoni/binary.roni',
                'projects/matcharoni/binary.output.txt',
            ),
            CodeTaste(
                'mag', 'Snailfish magnitude',
                'projects/matcharoni/mag.roni',
                'projects/matcharoni/mag.output.txt',
            ),
        ),
        presentation=Presentation(
            source='https://www.youtube.com/watch?v=2GnqHe2wx_M',
            poster='projects/matcharoni-poster.jpg',
            description="Matcharoni ('n cheese): introduction and demonstration by Sumeet",
            embed_url='https://www.youtube-nocookie.com/embed/2GnqHe2wx_M',
        ),
    ),
    Project(
        slug='exac',
        title='EXAc',
        dates='2021',
        sort_date='2021-10-19',
        technologies=('Rust',),
        url='https://github.com/sumeet/EXAc',
        description_file='projects/exac.md',
        demos=(),
        examples=tuple(
            CodeExample(
                slug=slug,
                title=title,
                source=f'projects/exac/{slug}/source.exc',
                assembly=tuple(f'projects/exac/{slug}/{name}.exa' for name in names),
                replay=f'projects/exac/{slug}/replay.gif',
                poster=f'projects/exac/{slug}/poster.webp',
            )
            for slug, title, names in (
                ('wormhole', 'The Wormhole', ('xa',)),
                ('valhalla', 'Valhalla', ('xa', 'xb')),
                ('unknown-network', 'Unknown Network 2', ('xa', 'xb')),
            )
        ),
        default_example='wormhole',
    ),
    Project(
        slug='nn-h',
        title='nn.h.rs',
        dates='2023',
        sort_date='2023-05-20',
        technologies=('Rust',),
        url='https://github.com/sumeet/nn-h',
        description_file='projects/nn-h.md',
        demos=(),
        listed=False,
        playground=Playground(
            source='projects/nn-h/index.html',
            description='nn.h.rs interactive handwriting recognition demo',
            height=302,
        ),
    ),
    Project(
        slug='solsolver',
        title='solsolver',
        dates='2022',
        sort_date='2022-11-05',
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
        technologies=('Rust', 'Dear ImGui'),
        url='https://github.com/sumeet/CodeMaestro',
        description_file='projects/codemaestro.md',
        demos=(
            Demo('projects/codemaestro-stack-interpreter.webp', 'CodeMaestro stack interpreter showing instruction choices and the result'),
            Demo('projects/codemaestro-file-tree-completed.webp', 'Completed recursive file paths function in CodeMaestro'),
            Demo('projects/codemaestro-particle-conditional.webp', 'Renaming a Particle field to height updates its uses in the step particle function'),
        ),
    ),
    Project(
        slug='rejectsynth',
        title='rejectsynth',
        dates='2023',
        sort_date='2023-11-26',
        technologies=('Rust', 'VSCode'),
        url='https://github.com/sumeet/rejectsynth',
        description_file='projects/rejectsynth.md',
        demos=(),
        playground=Playground(
            source='projects/rejectsynth/index.html',
            description='rejectsynth interactive music editor',
        ),
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
