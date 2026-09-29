"""Regenerate the small shipped cache with the original native KNN sampler.

After run_demo.sh has prepared the data and dependencies, run:
    .eledetective/venv/bin/python scripts/precompute_top_sampling.py
This is release preparation; reviewers do not need to run it.
"""
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / 'Treemap-Based Gridlayout'
os.chdir(GRID)
sys.path[:0] = [str(GRID), str(GRID / 'application/data/linear_assignment')]

import numpy as np
from joblib import hash as hash_inputs
from application.data.dataCtrler import DataCtrler
from application.data.label import mergeSmallLabels
from application.utils.sampling.SamplingMethods import OutlierBiasedDensityBasedSampling


def main():
    controller = DataCtrler()
    controller.preprocess('infographic')
    total = len(controller.labels)
    populations = Counter()
    for label, count in Counter(controller.labels).items():
        node = controller.hierarchy['id2label'][label]
        while node is not None:
            populations[node] += count
            node = controller.hierarchy['hierarchy'][node]['parent']
    counts = np.array(list(populations.values()))
    cuts, groups = set(), {}
    # Grid size changes the cut only when a population crosses these thresholds.
    for cells in range(1, 2 * total + 1):
        ratio = controller.getSpilitRatio(cells)
        split = ratio * total
        cutoff = max(1, min(0.1 * split, np.ceil(0.01 * total)))
        signature = ((counts > split).tobytes(), (counts > cutoff).tobytes())
        if signature in cuts:
            continue
        cuts.add(signature)
        controller.clean_stacks()
        top, labels, filtered = controller.reduce_labels(controller.labels, controller.hierarchy, spilit_ratio=ratio)
        merged = mergeSmallLabels(labels, top, filtered)
        for label in np.unique(merged):
            ids = np.flatnonzero(merged == label)
            features, categories = controller.features[ids], labels[ids]
            groups[hash_inputs((features, categories))] = (features, categories)

    probabilities = {}
    for index, (key, (features, labels)) in enumerate(sorted(groups.items()), 1):
        if len(labels) < 5:
            continue
        sampler = OutlierBiasedDensityBasedSampling(sampling_rate=0.1)
        np.random.seed(40)
        original = sampler.sample(features, labels)
        cached = OutlierBiasedDensityBasedSampling(0.1, probabilities=sampler.last_probabilities)
        np.random.seed(40)
        assert np.array_equal(original, cached.sample(features, labels))
        probabilities[key] = sampler.last_probabilities.tolist()
        print(f'{index}/{len(groups)} groups cached', flush=True)

    source = GRID / 'datasets/infographic'
    payload = {
        'algorithm': 'OutlierBiasedDensityBasedSampling, alpha=1, beta=1, original native KNN',
        'source_sha256': {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                          for name in ('infographic.json', 'infographic_features.npy', 'infographic_labels.npy')},
        'covered_grid_cells': [1, 2 * total],
        'probabilities': probabilities,
    }
    target = ROOT / 'assets/infographic-top-sampling.json.gz'
    target.write_bytes(gzip.compress(json.dumps(payload, separators=(',', ':')).encode(), mtime=0))
    print(f'Wrote {len(probabilities)} groups, {target.stat().st_size:,} bytes: {target}', flush=True)


if __name__ == '__main__':
    main()
