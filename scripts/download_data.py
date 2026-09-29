"""Download the pinned runtime data; the original backend consumes its caches."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tarfile

import gdown


def checksum(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    work = Path(sys.argv[1]).resolve()
    release = json.loads(Path(__file__).with_name('data-release.json').read_text())
    destination = work / 'data'
    marker = destination / '.release-sha256'
    if marker.exists() and marker.read_text().strip() == release['sha256']:
        verify(destination)
        return
    downloads = work / 'downloads'
    downloads.mkdir(parents=True, exist_ok=True)
    archive = Path(os.environ.get('ELEDETECTIVE_DATA_ARCHIVE', downloads / release['filename']))
    if not archive.exists() or checksum(archive) != release['sha256']:
        if 'ELEDETECTIVE_DATA_ARCHIVE' in os.environ:
            raise RuntimeError('The supplied data archive does not match the release.')
        pieces = []
        for record in release['parts']:
            piece = downloads / record['filename']
            if not piece.exists() or checksum(piece) != record['sha256']:
                partial = piece.with_suffix(piece.suffix + '.partial')
                gdown.download(id=record['google_drive_file_id'], output=str(partial),
                               resume=True, use_cookies=False)
                if partial.stat().st_size != record['bytes'] or checksum(partial) != record['sha256']:
                    partial.unlink(missing_ok=True)
                    raise RuntimeError(f'Checksum mismatch: {record["filename"]}')
                partial.replace(piece)
            pieces.append(piece)
        with archive.with_suffix('.partial').open('wb') as output:
            for piece in pieces:
                with piece.open('rb') as stream:
                    shutil.copyfileobj(stream, output, 8 * 1024 * 1024)
        archive.with_suffix('.partial').replace(archive)
        if checksum(archive) != release['sha256']:
            raise RuntimeError('Archive checksum mismatch.')
        for piece in pieces:
            piece.unlink()
    staging = work / 'extracting'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    with tarfile.open(archive) as source:
        for member in source:
            name = PurePosixPath(member.name)
            if name.is_absolute() or '..' in name.parts or not name.parts or name.parts[0] != 'data' or not (member.isfile() or member.isdir()):
                raise RuntimeError('Invalid archive member.')
            source.extract(member, staging, filter='data')
    verify(staging / 'data')
    if destination.exists():
        raise RuntimeError('A different dataset already exists; use an empty ELEDETECTIVE_WORK_DIR.')
    (staging / 'data').replace(destination)
    marker.write_text(release['sha256'] + '\n')
    staging.rmdir()


def verify(root):
    count = 0
    for line in (root / 'MANIFEST.sha256').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or not path.is_file() or checksum(path) != expected:
            raise RuntimeError(f'Data verification failed: {name}')
        count += 1
    print(f'Verified {count:,} files.', flush=True)


if __name__ == '__main__':
    main()
