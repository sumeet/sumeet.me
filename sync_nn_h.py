"""Import the built Rust/egui demo; editable source stays in the nn-h checkout."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def sync(source: Path):
    source = source.resolve()
    built = source / 'web/dist'
    if not (built / 'index.html').is_file():
        raise SystemExit('Build nn-h first: bash web/build.sh')
    destination = Path(__file__).resolve().parent / 'projects/nn-h'
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(built, destination)
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = bool(subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True))
    digest = hashlib.sha256()
    for path in sorted(built.rglob('*')):
        if path.is_file():
            digest.update(path.relative_to(built).as_posix().encode())
            digest.update(path.read_bytes())
    (destination / 'SOURCE.json').write_text(json.dumps({
        'repository': 'https://github.com/sumeet/nn-h',
        'revision': revision, 'uncommitted_changes': dirty,
        'build_sha256': digest.hexdigest(),
        'rebuild': 'make nn-h NN_H_DIR=../nn-h',
    }, indent=2) + '\n')
    print(f'Exported nn.h.rs to {destination}')


if __name__ == '__main__':
    sync(Path(sys.argv[1]) if len(sys.argv) > 1 else Path('../nn-h'))
