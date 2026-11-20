"""Import a built rejectsynth playground without duplicating its editable source."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def sync(source: Path):
    source = source.resolve()
    built = source / 'browser/dist'
    if not (built / 'index.html').is_file():
        raise SystemExit('Build rejectsynth/browser first: npm run wasm && npm run build')
    destination = Path(__file__).resolve().parent / 'projects/rejectsynth'
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
        'repository': 'https://github.com/sumeet/rejectsynth',
        'revision': revision, 'uncommitted_changes': dirty,
        'build_sha256': digest.hexdigest(),
        'rebuild': 'make rejectsynth REJECTSYNTH_DIR=../rejectsynth',
    }, indent=2) + '\n')

    # Carry dependency notices with the exported application.
    notices = ['Built from rejectsynth/browser. Edit that source, then run make rejectsynth.\n']
    lock = json.loads((source / 'browser/package-lock.json').read_text())
    for package in sorted(lock['packages']):
        if not package:
            continue
        root = source / 'browser' / package
        for path in sorted(root.glob('*')):
            if path.is_file() and path.name.lower().startswith(('license', 'notice', 'copyright')):
                notices.append(f'\n--- {package}/{path.name} ---\n{path.read_text(errors="replace")}')
    notices.append('\nVim logo: https://github.com/vim/vim/blob/master/runtime/vimlogo.svg\n')
    vim_license = source / 'browser/VIM-LICENSE.txt'
    if vim_license.exists():
        notices.append(vim_license.read_text())
    (destination / 'THIRD_PARTY_NOTICES.txt').write_text('\n'.join(notices))
    print(f'Exported rejectsynth to {destination}')


if __name__ == '__main__':
    sync(Path(sys.argv[1]) if len(sys.argv) > 1 else Path('../rejectsynth'))
