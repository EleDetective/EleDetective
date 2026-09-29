import numpy as np
import random
import math
import time
import tempfile
import gzip
import json
from pathlib import Path
from joblib import hash as hash_inputs
from annoy import AnnoyIndex
from sklearn.neighbors import NearestNeighbors
from application.utils.sampling.Sampler import *
from application.utils.sampling.SamplingMethods import *
from application.utils.pickle import *

class DataSampler(object):

    def __init__(self, default_sample_num):
        super().__init__()
        self.default_sample_num = default_sample_num
        self.max_sample_num = 100000
        self.test_without_sample = False
        self.sampler = Sampler()
        self.sampling_method = OutlierBiasedDensityBasedSampling # MultiClassBlueNoiseSamplingFAISS
        self.precomputed_probabilities = {}
        precomputed = Path(__file__).resolve().parents[3] / 'assets/infographic-top-sampling.json.gz'
        if precomputed.exists():
            with gzip.open(precomputed, 'rt') as stream:
                self.precomputed_probabilities = json.load(stream)['probabilities']
        # self.sampling_method = RandomSampling # MultiClassBlueNoiseSamplingFAISS
        self.cache_root = './cache'
        if not os.path.exists(self.cache_root):
            os.makedirs(self.cache_root)
    
    def set_cache_path(self, dataset):
        self.cache_path = os.path.join(self.cache_root, dataset)
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def topSampling(self, X_feature: np.ndarray, labels: np.ndarray, cache=True):
        # 顶层采样, return sampled_id + sample_addition(额外信息，例如下挂关系)
        # 0. load cache
        if cache:
            cache_file = os.path.join(self.cache_path, 'topSampling.pkl')
            if os.path.exists(cache_file):
                cache_data = load_pickle(cache_file)
                return cache_data['sampled_ids'], cache_data['sample_addition']

        # 1. sample total samples
        start = time.time()
        self.sampler.set_data(X_feature, labels)
        rs_args = {'sampling_rate': min(self.max_sample_num / X_feature.shape[0], 1)}
        self.sampler.set_sampling_method(RandomSampling, **rs_args)
        all_sampled_ids = self.sampler.get_samples_idx()
        # print('all_sampled_ids', all_sampled_ids.shape, time.time() - start)

        # 2. sample top samples
        start = time.time()

    def sample(self, features, ids, num, labels=None):
        if labels is None:
            labels = np.zeros(len(ids), dtype='int')
        if len(ids) == 0:
            return np.array([]).astype('int')
        probabilities = None
        if self.sampling_method is OutlierBiasedDensityBasedSampling:
            # Original KNN-derived weights work at new viewport sizes, too.
            probabilities = self.precomputed_probabilities.get(hash_inputs((features, labels)))
        # Static features can reuse the original sampling result across page loads.
        cache_dir = os.path.join(getattr(self, 'cache_path', self.cache_root), 'sampling-v1')
        key = hash_inputs((self.sampling_method.__name__, features, ids, num, labels, probabilities))
        cache_file = os.path.join(cache_dir, key + '.npy')
        if os.path.exists(cache_file):
            return np.load(cache_file, allow_pickle=False)
        self.sampler.set_data(features, labels)
        rs_args = {'sampling_rate': min((num + 1) / len(ids), 1)}
        if self.sampling_method is OutlierBiasedDensityBasedSampling:
            rs_args['probabilities'] = probabilities
        self.sampler.set_sampling_method(self.sampling_method, **rs_args)
        sampled_ids = self.sampler.get_samples_idx()[:num]
        sampled_ids = ids[sampled_ids]
        os.makedirs(cache_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=cache_dir, delete=False) as stream:
            np.save(stream, sampled_ids, allow_pickle=False)
        os.replace(stream.name, cache_file)
        return sampled_ids

    def getNearestHangIndex(self, X, sampled_index, hang_index, selected=None, getNowlabels=None):

        if getNowlabels is not None:
            forest_full = AnnoyIndex(X.shape[1], 'euclidean')
            forest_dict = {}

            sampled_labels = getNowlabels(sampled_index)
            hang_labels = getNowlabels(hang_index)
            if selected is None:
                for i, index in enumerate(sampled_index):
                    if sampled_labels[i] not in forest_dict:
                        forest_dict[sampled_labels[i]] = AnnoyIndex(X.shape[1], 'euclidean')
                    forest_dict[sampled_labels[i]].add_item(i, X[index])
                    forest_full.add_item(i, X[index])
            else:
                for i in selected:
                    index = sampled_index[i]
                    if sampled_labels[i] not in forest_dict:
                        forest_dict[sampled_labels[i]] = AnnoyIndex(X.shape[1], 'euclidean')
                    forest_dict[sampled_labels[i]].add_item(i, X[index])
                    forest_full.add_item(i, X[index])

            for key in forest_dict:
                forest_dict[key].build(10)
            forest_full.build(10)
            sample_addition = [[] for _ in range(sampled_index.shape[0])]
            for i, index in enumerate(hang_index):
                if hang_labels[i] in forest_dict:
                    forest = forest_dict[hang_labels[i]]
                    ret = forest.get_nns_by_vector(X[index], 1, include_distances=False)
                    sample_addition[ret[0]].append(index)
                else:
                    ret = forest_full.get_nns_by_vector(X[index], 1, include_distances=False)
                    sample_addition[ret[0]].append(index)
            return sample_addition

        forest = AnnoyIndex(X.shape[1], 'euclidean')
        if selected is None:
            for i, index in enumerate(sampled_index):
                forest.add_item(i, X[index])
        else:
            for i in selected:
                index = sampled_index[i]
                forest.add_item(i, X[index])

        forest.build(10)
        sample_addition = [[] for _ in range(sampled_index.shape[0])]
        for index in hang_index:
            ret = forest.get_nns_by_vector(X[index], 1, include_distances = False)
            sample_addition[ret[0]].append(index)
        return sample_addition

    def normalizeLabels(self, labels):
        label_set = np.unique(labels)
        label_dict = {label: i for i, label in enumerate(label_set)}
        labels = np.array([label_dict[label] for label in labels])
        return labels