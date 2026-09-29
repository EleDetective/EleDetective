"""Offline preparation through the original SAM, selection and propagation code.

Run in a CUDA environment with the runtime dependencies, CUDA-enabled PyTorch
and SAM ViT-H weights. --help lists the source inputs. This is not run at startup.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import pickle
import random
import shutil
import subprocess
import sys
import tarfile

REPO = Path(__file__).resolve().parents[1]


def initialize(options, gpu_queue=None):
    global opts, root, metadata, du, control_module
    opts = options
    root = Path(opts['output'])
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_queue.get()) if gpu_queue is not None else ''
    os.environ['ELEDETECTIVE_IMAGE_DIR'] = str(root / 'images')
    os.environ['ELEDETECTIVE_IMAGE_URL'] = '/images/'
    os.environ['ELEDETECTIVE_SAM_CHECKPOINT'] = opts['sam_checkpoint']
    os.environ['ELEDETECTIVE_DREAMSIM_CACHE'] = opts['dreamsim_cache']
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MPLBACKEND'] = 'Agg'
    sys.path.insert(0, str(REPO / 'Visualization System/backend/data'))
    import torch
    torch.set_num_threads(1)
    import data_utils
    import dataControl_new2
    du, control_module = data_utils, dataControl_new2
    metadata = json.loads((root / 'backend/annotations.json').read_text())['images']


def prepare_inputs(args):
    import ijson
    from PIL import Image
    root = Path(args.output)
    parts = root / 'backend/parts'
    if (root / 'backend/annotations.json').exists():
        raise RuntimeError('Input preparation already exists; use --stage to resume later steps.')
    parts.mkdir(parents=True)
    (root / 'images').mkdir()
    shutil.copytree(args.grid_data, root / 'grid/infographic')
    meta = json.loads(Path(args.annotations).read_text())
    mapping, scales, images = {}, {}, []
    for i, record in enumerate(meta['images']):
        assert record['id'] not in mapping
        mapping[record['id']] = i
        with Image.open(Path(args.images) / record['file_name']) as image:
            assert image.size == (record['width'], record['height'])
            image = image.convert('RGB')
            image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            name = f'{i:04d}.jpg'
            image.save(root / 'images' / name, quality=92)
            scales[record['id']] = (image.width / record['width'], image.height / record['height'])
            images.append(dict(record, id=i, source_image_id=record['id'],
                               source_file_name=record['file_name'], file_name=name,
                               width=image.width, height=image.height))
    current, batch, completed = None, [], set()

    def save():
        if current is not None:
            assert current not in completed, 'Predictions must be grouped by image_id.'
            (parts / f'{mapping[current]:04d}.predictions.json').write_text(json.dumps(batch))
            completed.add(current)

    with Path(args.predictions).open('rb') as stream:
        for item in ijson.items(stream, 'item', use_float=True):
            source = item['image_id']
            if source != current:
                save()
                current, batch = source, []
            sx, sy = scales[source]
            x, y, w, h = item['bbox']
            batch.append(dict(item, image_id=mapping[source], bbox=[x*sx, y*sy, w*sx, h*sy]))
    save()
    assert completed == set(mapping)
    (root / 'backend/annotations.json').write_text(json.dumps(dict(meta, images=images, annotations=[])))


def sam_batch(ids):
    parts = root / 'backend/parts'
    ids = [i for i in ids if not (parts / f'{i:04d}.candidate.pkl').exists()]
    if not ids:
        return
    predictions = []
    for i in ids:
        predictions.extend(json.loads((parts / f'{i:04d}.predictions.json').read_text()))
    temp = parts / f'batch-{ids[0]}.tmp'
    candidates = du.getCandidate(predictions, [metadata[i] for i in ids], str(temp), use_mask=True, with_text=True)
    for i, candidate in zip(ids, candidates):
        write_pickle(parts / f'{i:04d}.candidate.pkl', candidate)
    temp.unlink()


def write_pickle(path, value):
    temporary = path.with_suffix('.tmp')
    with temporary.open('wb') as stream:
        pickle.dump(value, stream)
    temporary.replace(path)


def tree_one(i):
    import numpy as np
    parts = root / 'backend/parts'
    path = parts / f'{i:04d}.hierarchy.json'
    selected = parts / f'{i:04d}.selected.pkl'
    if path.exists() and selected.exists():
        return
    random.seed(42 + i)
    np.random.seed(42 + i)
    candidate = pickle.load((parts / f'{i:04d}.candidate.pkl').open('rb'))
    hierarchy = du.getHierarchy(candidate['annotations'], candidate['shape_dict'], candidate['subset'], metadata[i])
    write_pickle(selected, candidate)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(hierarchy))
    temporary.replace(path)


def controller():
    data = control_module.DataControl(with_text=True)
    data.load_data(str(root / 'backend'), model='dreamsim')
    return data


def compute_part(task):
    stage, part, count = task
    random.seed(42 + part)
    control_module.part_cnt = count  # Partitioning only; original methods do the calculations.
    data = controller()
    path = str(root / 'backend')
    if stage == 'features':
        data.get_dreamsim_feature(path, part, convert='L', no_dreamsim=['text', 'gridline'])
    elif stage == 'content':
        data.get_cross_influence(path, part)
    else:
        data.get_cross_hierarchy_influence(path, part)


def pooled(function, tasks, args, gpu=False):
    context = mp.get_context('spawn')
    queue = None
    workers = args.workers
    if gpu:
        devices = args.gpus.split(',')
        workers = len(devices)
        queue = context.Queue()
        for device in devices:
            queue.put(device)
    with ProcessPoolExecutor(max_workers=workers, mp_context=context,
                             initializer=initialize, initargs=(vars(args), queue)) as pool:
        for i, _ in enumerate(pool.map(function, tasks), 1):
            print(f'{function.__name__}: {i} tasks completed', flush=True)


class PackedSimilarity:
    """Unpickle as a normal dense array, using only the installed SciPy library."""
    def __init__(self, matrix):
        self.matrix = matrix

    def __reduce__(self):
        return self.matrix.toarray, ()


def compact_content(task):
    import numpy as np
    from scipy.sparse import csr_matrix
    source, target, threshold = task
    original = pickle.load(source.open('rb'))
    matrices = {}
    for key, matrix in original.items():
        # Original cache readers index only matches retained by this threshold.
        # Online matching still uses the complete, unchanged DreamSim features.
        rows, columns = np.nonzero(matrix > threshold)
        matrices[key] = PackedSimilarity(csr_matrix(
            (matrix[rows, columns], (rows, columns)), shape=matrix.shape))
    write_pickle(target, matrices)
    restored = pickle.load(target.open('rb'))
    for key, matrix in original.items():
        assert restored[key].dtype == matrix.dtype and np.array_equal(
            restored[key], np.where(matrix > threshold, matrix, 0)), source


def package(args):
    root = Path(args.output)
    initialize(vars(args))
    compact = root / 'runtime-content'
    compact.mkdir(exist_ok=True)
    influence = root / 'backend/content/dreamsim_influence'
    tasks = [(p, compact / p.name, control_module.content_sim_thres)
             for p in sorted(influence.glob('*.pkl'))]
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context('spawn')) as pool:
        for _ in pool.map(compact_content, tasks):
            pass
    print('Packed content scores; retained matches are unchanged.', flush=True)
    files = []
    for name in ['images', 'grid', 'backend/content', 'backend/hierarchy']:
        files.extend(p for p in (root / name).rglob('*') if p.is_file())
    files.extend(root / 'backend' / name for name in ['annotations.json', 'candidate_ori.pkl', 'candidate.pkl', 'hierarchy.json'])
    if (root / 'PROVENANCE.json').exists():
        files.append(root / 'PROVENANCE.json')
    def stored(path):
        return compact / path.name if path.parent == influence else path
    lines = []
    for path in sorted(files):
        with stored(path).open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        lines.append(f'{digest}  {path.relative_to(root).as_posix()}')
    (root / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
    files.append(root / 'MANIFEST.sha256')
    archive = root.parent / 'infographic_4class-interactive.tar.gz'
    if shutil.which('pigz'):
        with archive.open('wb') as output:
            compressor = subprocess.Popen(['pigz', '-3', '-p', str(args.workers)],
                                          stdin=subprocess.PIPE, stdout=output)
            with tarfile.open(fileobj=compressor.stdin, mode='w|') as target:
                for path in sorted(files):
                    target.add(stored(path), arcname='data/' + path.relative_to(root).as_posix(), recursive=False)
            compressor.stdin.close()
            if compressor.wait():
                raise RuntimeError('Archive compression failed.')
    else:
        with tarfile.open(archive, 'w:gz', compresslevel=3) as target:
            for path in sorted(files):
                target.add(stored(path), arcname='data/' + path.relative_to(root).as_posix(), recursive=False)
    print(archive, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='Prepared dataset directory')
    parser.add_argument('--stage', choices=['all', 'inputs', 'sam', 'trees', 'features', 'content', 'hierarchy', 'package'], default='all')
    parser.add_argument('--annotations', help='Original COCO image/category JSON')
    parser.add_argument('--predictions', help='Original 20-category detector predictions')
    parser.add_argument('--images', help='Original image directory')
    parser.add_argument('--grid-data', help='Aligned infographic grid dataset, including its existing features and thumbnails')
    parser.add_argument('--sam-checkpoint', default='', help='SAM ViT-H checkpoint for the sam stage')
    parser.add_argument('--dreamsim-cache', default='./dreamsim-weights')
    parser.add_argument('--gpus', default='0', help='Comma-separated GPU indices for offline preparation')
    parser.add_argument('--workers', type=int, default=8, help='CPU preparation processes')
    args = parser.parse_args()
    args.output = str(Path(args.output).resolve())
    args.dreamsim_cache = str(Path(args.dreamsim_cache).resolve())
    Path(args.dreamsim_cache).mkdir(parents=True, exist_ok=True)
    if args.stage in {'all', 'sam'} and not Path(args.sam_checkpoint).is_file():
        parser.error('SAM preparation needs --sam-checkpoint pointing to the ViT-H weights.')
    stages = ['inputs', 'sam', 'trees', 'features', 'content', 'hierarchy', 'package'] if args.stage == 'all' else [args.stage]
    for stage in stages:
        if stage == 'inputs':
            if not all([args.annotations, args.predictions, args.images, args.grid_data]):
                parser.error('Input preparation needs --annotations, --predictions, --images and --grid-data.')
            prepare_inputs(args)
            continue
        if stage == 'package':
            package(args)
            continue
        initialize(vars(args))
        count = len(metadata)
        if stage == 'sam':
            pooled(sam_batch, [list(range(i, min(i+25, count))) for i in range(0, count, 25)], args, gpu=True)
        elif stage == 'trees':
            pooled(tree_one, range(count), args)
            for name, suffix in [('candidate_ori.pkl', 'candidate.pkl'), ('candidate.pkl', 'selected.pkl')]:
                write_pickle(root / 'backend' / name, [pickle.load((root / 'backend/parts' / f'{i:04d}.{suffix}').open('rb')) for i in range(count)])
            (root / 'backend/hierarchy.json').write_text(json.dumps([json.loads((root / 'backend/parts' / f'{i:04d}.hierarchy.json').read_text()) for i in range(count)]))
        else:
            folders = {'features': ['content/dreamsim_features'],
                       'content': ['content/dreamsim_influence'],
                       'hierarchy': ['hierarchy/dreamsim_influence']}[stage]
            for folder in folders:
                (root / 'backend' / folder).mkdir(parents=True, exist_ok=True)
            partitions = len(args.gpus.split(',')) if stage == 'features' else 100
            pooled(compute_part, [(stage, i, partitions) for i in range(partitions)], args, gpu=stage == 'features')
            # Merge global ranking once after all partitions finish.
            if stage == 'content':
                controller().get_influence_info(str(root / 'backend'))
            elif stage == 'hierarchy':
                controller().get_hierarchy_influence_info(str(root / 'backend'))


if __name__ == '__main__':
    main()
