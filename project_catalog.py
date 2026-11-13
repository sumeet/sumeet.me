from dataclasses import dataclass


@dataclass(frozen=True)
class Demo:
    source: str
    description: str


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    url: str
    description_file: str
    demos: tuple[Demo, ...]


# Display order is intentional; descriptions are handwritten Markdown files.
PROJECTS = (
    Project(
        slug='zac',
        title='Zac',
        url='https://github.com/sumeet/Zac',
        description_file='projects/zac.md',
        demos=(
            Demo('projects/zac-gol.mp4', 'Zac: Game of Life running in source code comments'),
            Demo('projects/zac-help.mp4', 'Zac: built-in help written into source code comments'),
            Demo('projects/zac-fib.mp4', 'Zac: a Fibonacci sequence written into source code comments'),
        ),
    ),
    Project(
        slug='golden',
        title='golden',
        url='https://github.com/sumeet/golden',
        description_file='projects/golden.md',
        demos=(
            Demo('projects/golden-demo.gif', 'Windows resizing as focus moves around a tiled desktop'),
        ),
    ),
)
