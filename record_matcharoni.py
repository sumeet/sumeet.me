"""Record the example outputs with the same interpreter entry point as the browser pads."""
import argparse
from pathlib import Path
import subprocess

from project_catalog import PROJECTS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('interpreter', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    project = next(p for p in PROJECTS if p.slug == 'matcharoni')
    for example in project.tastes:
        result = subprocess.run(
            [args.interpreter.resolve(), '--pad', 'projects/matcharoni/prelude.roni', example.source],
            check=True, stdout=subprocess.PIPE, text=True,
        )
        output = Path(example.output)
        if args.check:
            if output.read_text() != result.stdout:
                raise SystemExit(f'{example.slug}: recorded value differs')
        else:
            output.write_text(result.stdout)
        print(f'{example.slug}: verified')


if __name__ == '__main__':
    main()
