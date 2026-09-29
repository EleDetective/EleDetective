import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import random
import time
import math
import shapely
from scipy.optimize import linear_sum_assignment
from collections import Counter

from .eval2 import getFullScore, Group, if_cover, getShape, adjust_hierarchy, getSubType, getInnerShape, getBasicObj
from .SAM.sam import draw_polygon, getMaskFromBox, Mask
from .grouping_cpp import hierarchy_merge_with_cpp

def get_dist(obj1, obj2):
    box1 = obj1.box
    box2 = obj2.box

    [x1_A, y1_A, x2_A, y2_A] = box1
    [x1_B, y1_B, x2_B, y2_B] = box2
    # horizontal_distance = 0
    # if x1_A < x1_B and x2_A > x2_B:
    #     horizontal_distance = 0
    # elif x1_A > x1_B and x2_A < x2_B:
    #     horizontal_distance = 0
    # elif x1_A > x1_B and x2_A > x2_B:
    #     if x1_A < x2_B:
    #         horizontal_distance = 0
    #     else:
    #         horizontal_distance = min(abs(x2_A - x1_B), abs(x2_B - x1_A), abs(x1_A - x1_B), abs(x2_A - x2_B))
    # elif x1_A < x1_B and x2_A < x2_B:
    #     if x1_B < x2_A:
    #         horizontal_distance = 0
    #     else:
    #         horizontal_distance = min(abs(x2_A - x1_B), abs(x2_B - x1_A), abs(x1_A - x1_B), abs(x2_A - x2_B))
    # vertical_distance = 0
    # if y1_A < y1_B and y2_A > y2_B:
    #     vertical_distance = 0
    # elif y1_A > y1_B and y2_A < y2_B:
    #     vertical_distance = 0
    # elif y1_A > y1_B and y2_A > y2_B:
    #     if y1_A < y2_B:
    #         vertical_distance = 0
    #     else:
    #         vertical_distance = min(abs(y2_A - y1_B), abs(y2_B - y1_A), abs(y1_A - y1_B), abs(y2_A - y2_B))
    # elif y1_A < y1_B and y2_A < y2_B:
    #     if y1_B < y2_A:
    #         vertical_distance = 0
    #     else:
    #         vertical_distance = min(abs(y2_A - y1_B), abs(y2_B - y1_A), abs(y1_A - y1_B), abs(y2_A - y2_B))

    horizontal_distance = max(0, x1_A - x2_B, x1_B - x2_A)
    vertical_distance = max(0, y1_A - y2_B, y1_B - y2_A)

    dist = max(horizontal_distance, vertical_distance)

    horizontal_align = abs(x1_A - x1_B) + abs(x2_A - x2_B) + abs((x1_A + x2_A) / 2 - (x1_B + x2_B) / 2)
    vertical_align = abs(y1_A - y1_B) + abs(y2_A - y2_B) + abs((y1_A + y2_A) / 2 - (y1_B + y2_B) / 2)
    align = 0.9 * min(horizontal_align, vertical_align) + 0.1 * max(horizontal_align, vertical_align)

    horizontal_similar = abs((x2_A - x1_A) - (x2_B - x1_B))
    vertical_similar = abs((y2_A - y1_A) - (y2_B - y1_B))
    similar = 0.9 * min(horizontal_similar, vertical_similar) + 0.1 * max(horizontal_similar, vertical_similar)

    tot_dist = dist + 0.3 * align + 0.2 * similar

    # if obj1.type != obj2.type and obj1.type not in ['group'] and obj2.type not in ['group']:
    #     tot_dist *= 0.75
    # elif obj1.type == obj2.type == 'group':
    #     tot_dist *= 0.9
    
    if obj1.type != obj2.type and obj1.type not in ['group', "non-data", "data"] and obj2.type not in ['group', "non-data", "data"]:
        tot_dist *= 0.75
    elif (obj1.type == 'data' or (obj1.type == 'group' and obj1.sub_type == 'data')) and (obj2.type == 'data' or (obj2.type == 'group' and obj2.sub_type == 'data')):
        tot_dist *= 0.75
    elif (obj1.type == 'non-data' or (obj1.type == 'group' and obj1.sub_type == 'non-data')) and (obj2.type == 'non-data' or (obj2.type == 'group' and obj2.sub_type == 'non-data')):
        tot_dist *= 0.75
    elif obj1.type == obj2.type == 'group':
        tot_dist *= 0.9
    elif (obj1.type in ['data', 'non-data'] or (obj1.type == 'group' and obj1.sub_type in ['data', 'non-data'])) and obj2.type in ['text', 'image']:
        tot_dist *= 1.2
    elif (obj2.type in ['data', 'non-data'] or (obj2.type == 'group' and obj2.sub_type in ['data', 'non-data'])) and obj1.type in ['text', 'image']:
        tot_dist *= 1.2
    return tot_dist


def get_adjust_dist(dist_m, can_merge_lm=None, cover_m=None, can_merge_m=None):
    # start = time.time()

    dist_m = dist_m.copy()
    # print("thres", 0, time.time() - start)

    if cover_m is not None:
        tmp_arr = np.sum(cover_m, axis=1) > 1
        tmp_m = cover_m.astype('bool') & tmp_arr[:, np.newaxis]
        dist_m[tmp_m | tmp_m.T] *= 20

    # if cover_m is not None and can_merge_m is not None:
    #     tmp_m1 = cover_m.astype('bool')
    #     tmp_m2 = can_merge_m.astype('bool')
    #     dist_m[~tmp_m1 & ~tmp_m1.T & (tmp_m2 | tmp_m2.T)] /= 5
    if cover_m is not None and can_merge_m is not None:
        tmp_m1 = cover_m.astype('bool')
        tmp_m2 = can_merge_m.astype('bool')

        tmp_m3 = np.maximum(np.sum(cover_m, axis=0), 1)[:, np.newaxis]
        # dist_m[tmp_m2 & tmp_m2.T] /= 20*np.minimum(tmp_m3, tmp_m3.T)[tmp_m2 & tmp_m2.T]
        # dist_m[tmp_m2 & tmp_m2.T] /= 2*np.power(10, np.minimum(tmp_m3, tmp_m3.T)[tmp_m2 & tmp_m2.T])
        dist_m[tmp_m2 & tmp_m2.T] /= np.power(30, np.minimum(tmp_m3, tmp_m3.T)[tmp_m2 & tmp_m2.T])

    # print("thres", 1, time.time() - start)

    if can_merge_lm is not None:
        dist_m[can_merge_lm != True] = 100000000
    # print("thres", 2, time.time() - start)

    for i in range(dist_m.shape[0]):
        dist_m[i][i] = 100000000

    # print('dist_m.shape', dist_m.shape)
    return dist_m


def get_thres(dist_m, type='soft'):
    # start = time.time()

    tmp_arr = dist_m.flatten()
    tmp_sort = np.sort(tmp_arr)
    # print("thres", 3, time.time() - start)

    # thres = ori_thres = tmp_sort[int(1.5 * len(obj_list)) - 1]
    ori_thres = 0
    thres = 0
    for i in range(len(tmp_sort)):
        if tmp_sort[i] == 0:
            continue
        if ori_thres == 0:
            ori_thres = thres = tmp_sort[i]
        else:
            if type == 'soft':
                if (tmp_sort[i] < 2 * ori_thres) and (tmp_sort[i] < 1.1 * thres or tmp_sort[i] < 1.5 * ori_thres):
                    thres = tmp_sort[i]
                else:
                    break
            else:
                if tmp_sort[i] < 1.05 * ori_thres:
                    thres = tmp_sort[i]
                else:
                    break
    # print("thres", 4, time.time() - start)

    return thres


def hierarchy_merge(obj_list):

    return hierarchy_merge_with_cpp(obj_list)

    if len(obj_list) <= 1:
        return obj_list

    full_flag = 1
    cnt = 100000
    cnt2 = 0

    import time
    time_cover = 0
    time_can_merge = 0
    time_dist = 0
    time_thres = 0
    time_merge = 0

    cnt_cover = 0
    cnt_dist = 0

    one_list = np.array([], dtype='int')
    ll = len(obj_list)
    cover_m = np.zeros((ll, ll))
    can_merge_l = np.ones(ll)
    can_merge_m = np.zeros((ll, ll))
    can_merge_m2 = np.zeros((ll, ll))
    can_merge_lm = np.zeros((ll, ll))
    dist_m = np.zeros((ll, ll))
    a_dist_m = np.zeros((ll, ll))

    while len(obj_list) > 1 and cnt > 0:
        # print(cnt, full_flag)
        cnt -= 1
        cnt2 += 1
        if cnt == 0:
            cnt = 0
        ll = len(obj_list)

        if full_flag > 0:
            start = time.time()

            old_ll = len(one_list)

            old_cover_m = cover_m
            cover_m = np.zeros((ll, ll))
            cover_m[:old_ll, :old_ll] = old_cover_m[np.ix_(one_list, one_list)]
            for i in range(old_ll):
                for j in range(old_ll, ll):
                    cover_m[i][j] = if_cover(obj_list[i], obj_list[j])
                    cover_m[j][i] = if_cover(obj_list[j], obj_list[i])
                    # if cnt==0 and i == 0 and j == 4:
                    #     print(obj_list[i].box, obj_list[j].box)
            for i in range(old_ll, ll - 1):
                for j in range(i + 1, ll):
                    cover_m[i][j] = if_cover(obj_list[i], obj_list[j])
                    cover_m[j][i] = if_cover(obj_list[j], obj_list[i])
            time_cover += time.time() - start
            cnt_cover += 2*old_ll*(ll-old_ll) + (ll-old_ll)*(ll-old_ll-1) 

            start = time.time()
            can_merge_l = np.ones(ll, dtype='bool')
            can_merge_m = np.zeros((ll, ll), dtype='bool')
            can_merge_m2 = np.zeros((ll, ll), dtype='bool')
            for i in range(ll):
                father = -1
                father_area = -1
                for j in np.where(cover_m[:, i])[0]:
                    box = obj_list[j].box
                    new_area = (box[2] - box[0]) * (box[3] - box[1])
                    if father == -1 or new_area < father_area:
                        father = j
                        father_area = new_area
                if father != -1:
                    can_merge_l[i] = 0
                    can_merge_l[father] = 0
                    can_merge_m[i][father] = can_merge_m2[father][i] = 1
                    # tmp = np.where(cover_m[father])
                    # can_merge_m[i, tmp] = 1
                    # can_merge_m2[father, tmp] = 1
                    for j in np.where(cover_m[father])[0]:
                        can_merge_m[i][j] = can_merge_m2[father][j] = 1

            # time_can_merge += time.time() - start

            for i in range(ll):
                if can_merge_m2[i].sum() > 0:
                    can_merge_m[i] = can_merge_m2[i].copy()
            # time_can_merge += time.time() - start

            # can_merge_lm = np.zeros((ll, ll))
            # for i in range(ll - 1):
            #     for j in range(i + 1, ll):
            #         can_merge_lm[i][j] = can_merge_lm[j][i] = (can_merge_l[i] > 0 or can_merge_m[i][j] > 0) and (
            #                     can_merge_l[j] > 0 or can_merge_m[j][i] > 0)
            tmp_m = can_merge_m.astype('bool') | can_merge_l[:, np.newaxis].astype('bool')
            can_merge_lm = tmp_m & tmp_m.T
            time_can_merge += time.time() - start

            start = time.time()

            tmp_time = 0
            tmp_start = time.time()

            old_dist_m = dist_m
            dist_m = np.zeros((ll, ll))
            dist_m[:old_ll, :old_ll] = old_dist_m[np.ix_(one_list, one_list)]

            # tmp_time += time.time() - tmp_start

            # time_dist += time.time() - start
            # start = time.time()
            for i in range(old_ll):
                for j in range(old_ll, ll):
                    # tmp_start = time.time()
                    dist_m[i][j] = dist_m[j][i] = get_dist(obj_list[i], obj_list[j])
                    # tmp_time += time.time() - tmp_start
            for i in range(old_ll, ll - 1):
                for j in range(i + 1, ll):
                    # tmp_start = time.time()
                    dist_m[i][j] = dist_m[j][i] = get_dist(obj_list[i], obj_list[j])
                    # tmp_time += time.time() - tmp_start
            time_dist += time.time() - start - tmp_time
            cnt_dist += 2*old_ll*(ll-old_ll) + (ll-old_ll)*(ll-old_ll-1) 

            start = time.time()
            a_dist_m = get_adjust_dist(dist_m, can_merge_lm=can_merge_lm, cover_m=cover_m, can_merge_m=can_merge_m)
            ori_thres = thres = get_thres(a_dist_m, type='hard')
            time_thres += time.time() - start
        
        # if cnt == 0:
        #     print('dist')
        #     print(dist_m)
        #     print(a_dist_m)
        #     print(cover_m)

        def merge(i, j, dist=0):
            cluster1 = merge_cluster[i]
            cluster2 = merge_cluster[j]
            if cluster1 == cluster2:
                return
            for k in merge_list[cluster2]:
                merge_cluster[k] = cluster1
                merge_list[cluster1].append(k)
            merge_list[cluster2] = []
            max_thres[cluster1] = max(max_thres[cluster1], max_thres[cluster2], dist)

        start = time.time()
        merge_list = []
        for i in range(ll):
            merge_list.append([i])
        merge_cluster = np.arange(ll, dtype='int')
        max_thres = np.zeros(ll)

        merge_scale1 = 2
        merge_scale2 = 1.5
        full_flag = 0
        flag = True
        rows, cols = np.where(a_dist_m <= thres * merge_scale1)
        true_coords = list(zip(rows, cols))
        while flag:
            flag = False
            for (i, j) in true_coords:
                # start = time.time()
                if i < j:
                    # for i in range(ll - 1):
                    #     for j in range(i + 1, len(obj_list)):
                    if merge_cluster[i] == merge_cluster[j]:
                        # time_merge += time.time() - start
                        continue

                    if not can_merge_lm[i][j]:
                        # time_merge += time.time() - start
                        continue

                    # tmp_thres = thres
                    # if len(merge_list[merge_cluster[i]]) > 1:
                    #     tmp_thres = min(thres * merge_scale1,
                    #                     max(max_thres[merge_cluster[i]] * merge_scale2, tmp_thres))
                    # if len(merge_list[merge_cluster[j]]) > 1:
                    #     tmp_thres = min(thres * merge_scale1,
                    #                     max(max_thres[merge_cluster[j]] * merge_scale2, tmp_thres))
                    tmp_thres = thres*merge_scale2

                    # time_merge += time.time() - start

                    if a_dist_m[i][j] > tmp_thres+0.000001:
                        # time_merge += time.time() - start
                        continue

                    full_flag += 1
                    flag = True
                    merge(i, j, a_dist_m[i][j])
                    # time_merge += time.time() - start

                    if cover_m[i][j]:
                        for k in np.where((cover_m[i] > 0) & (merge_cluster != merge_cluster[i]))[0]:
                            merge(i, k)
                    if cover_m[j][i]:
                        for k in np.where((cover_m[j] > 0) & (merge_cluster != merge_cluster[j]))[0]:
                            merge(j, k)
                # time_merge += time.time() - start

        # time_merge += time.time() - start

        new_obj_list = []
        one_list = []
        for i, cluster in enumerate(merge_list):
            if len(cluster) == 1:
                new_obj_list.append(obj_list[cluster[0]])
                one_list.append(i)
        one_list = np.array(one_list, dtype='int')

        for cluster in merge_list:
            if len(cluster) == 0:
                continue
            if len(cluster) == 1:
                continue
            new_obj = Group()
            min_x = 10000000
            min_y = 10000000
            max_x = -10000000
            max_y = -10000000
            for i in cluster:
                obj = obj_list[i]
                new_obj.children.append(obj)
                min_x = min(min_x, obj.box[0])
                min_y = min(min_y, obj.box[1])
                max_x = max(max_x, obj.box[2])
                max_y = max(max_y, obj.box[3])
            new_obj.box = [min_x, min_y, max_x, max_y]
            new_obj.type = 'group'
            getSubType(new_obj)

            new_obj_list.append(new_obj)

        if full_flag == 0:
            thres += min(0.5 * thres, max(0.2 * thres, ori_thres))

        time_merge += time.time() - start

        obj_list = new_obj_list

    print("time", time_cover, time_can_merge, time_dist, time_thres, time_merge)
    print("cnt", cnt_cover, cnt_dist)

    return obj_list


def getFullOverlapScore(obj_list, overlap_store=None, cover_type="soft", allow_same_cover=False):
    full_area = 0
    # full_area_s = 0
    min_x, min_y, max_x, max_y = 10000000, 10000000, -10000000, -10000000

    for i in range(len(obj_list)):
        obj1 = obj_list[i]
        # shape1 = shapely.geometry.box(obj1.box[0], obj1.box[1], obj1.box[2], obj1.box[3])
        # shape1 = obj1.mask_shape
        shape1 = obj1.mask_obj
        min_x = min(min_x, obj1.box[0])
        min_y = min(min_y, obj1.box[1])
        max_x = max(max_x, obj1.box[2])
        max_y = max(max_y, obj1.box[3])
        for j in range(i + 1, len(obj_list)):
            obj2 = obj_list[j]

            id1 = obj1.id
            id2 = obj2.id
            if (id1, id2) in overlap_store:
                full_area += overlap_store[(id1, id2)]
                continue

            # shape2 = shapely.geometry.box(obj2.box[0], obj2.box[1], obj2.box[2], obj2.box[3])
            # shape2 = obj2.mask_shape
            shape2 = obj2.mask_obj
            tmp_cover1 = if_cover(obj1, obj2, type=cover_type)
            tmp_cover2 = if_cover(obj2, obj1, type=cover_type)
            if allow_same_cover:
                true_cover1, true_cover2 = tmp_cover1, tmp_cover2
            else:
                true_cover1 = (tmp_cover1 == 1 and obj1.type != "text" and obj1.type != obj2.type)
                true_cover2 = (tmp_cover2 == 1 and obj2.type != "text" and obj1.type != obj2.type)

            if not isinstance(shape1, Mask):
                tmp_shape = shape1.intersection(shape2)
                mask_intersect = tmp_shape.area / (shape1.union(shape2).area+0.00001)
            else:
                tmp_shape = shape1.intersection(shape2, need_bounds=False)
                mask_intersect = tmp_shape.area / (shape1.union(shape2, need_bounds=False).area+0.00001)

            if mask_intersect > 0:
                mask_intersect = 1 / (1 + np.exp(-20 * (mask_intersect - 0.5)))
            if (obj1.type == 'chart' and obj2.type in ['sub-element']) or \
               (obj2.type == 'chart' and obj1.type in ['sub-element']):
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            if ('mark' in obj1.type and obj2.type in ['sub-element']) or \
               ('mark' in obj2.type and obj1.type in ['sub-element']):
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            # if true_cover1 or true_cover2:
            if (true_cover1 and (obj1.type!="HRO" or obj2.type!="mark")) or (true_cover2 and (obj1.type!="mark" or obj2.type!="HRO")):
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            # if (tmp_cover1 and obj2.type in ['HRO']) or \
            #    (tmp_cover2 and obj1.type in ['HRO']):
            #     overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
            #     continue
            # if (tmp_cover1 and 'mark' in obj2.type) or \
            #    (tmp_cover2 and 'mark' in obj1.type):
            #     overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
            #     continue
            if ('gridline' in obj1.type) or ('gridline' in obj2.type):
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = mask_intersect
            full_area += mask_intersect

    width = max(0, max_x - min_x)
    height = max(0, max_y - min_y)
    box_area = width * height

    # if full_area_s>0:
    #     print("overlap_area", full_area, full_area_s)
    #     exit(0)
    return full_area, 1


def getFullOverlapScoreBase(obj_list, overlap_store=None, cover_type="soft", allow_same_cover=False):
    full_area = 0
    # full_area_s = 0
    min_x, min_y, max_x, max_y = 10000000, 10000000, -10000000, -10000000

    for i in range(len(obj_list)):
        obj1 = obj_list[i]
        # shape1 = shapely.geometry.box(obj1.box[0], obj1.box[1], obj1.box[2], obj1.box[3])
        # shape1 = obj1.mask_shape
        shape1 = obj1.mask_obj
        min_x = min(min_x, obj1.box[0])
        min_y = min(min_y, obj1.box[1])
        max_x = max(max_x, obj1.box[2])
        max_y = max(max_y, obj1.box[3])
        for j in range(i + 1, len(obj_list)):
            obj2 = obj_list[j]

            id1 = obj1.id
            id2 = obj2.id
            if (id1, id2) in overlap_store:
                full_area += overlap_store[(id1, id2)]
                continue

            # shape2 = shapely.geometry.box(obj2.box[0], obj2.box[1], obj2.box[2], obj2.box[3])
            # shape2 = obj2.mask_shape
            shape2 = obj2.mask_obj
            tmp_cover1 = if_cover(obj1, obj2, type=cover_type)
            tmp_cover2 = if_cover(obj2, obj1, type=cover_type)
            if allow_same_cover:
                true_cover1, true_cover2 = tmp_cover1, tmp_cover2
            else:
                true_cover1 = (tmp_cover1 == 1 and obj1.type != obj2.type)
                true_cover2 = (tmp_cover2 == 1 and obj1.type != obj2.type)

            if not isinstance(shape1, Mask):
                tmp_shape = shape1.intersection(shape2)
                mask_intersect = tmp_shape.area / (shape1.union(shape2).area+0.00001)
            else:
                tmp_shape = shape1.intersection(shape2, need_bounds=False)
                mask_intersect = tmp_shape.area / (shape1.union(shape2, need_bounds=False).area+0.00001)

            if mask_intersect > 0:
                mask_intersect = 1 / (1 + np.exp(-20 * (mask_intersect - 0.5)))
            # if not tmp_shape.area<min(shape1.area, shape2.area):
            #     overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
            #     continue
            if true_cover1 or true_cover2:
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = mask_intersect
            full_area += mask_intersect

    width = max(0, max_x - min_x)
    height = max(0, max_y - min_y)
    box_area = width * height

    # if full_area_s>0:
    #     print("overlap_area", full_area, full_area_s)
    #     exit(0)
    return full_area, 1


def getFullOverlapScoreNew(obj_list, overlap_store=None):
    full_area = 0
    # full_area_s = 0
    min_x, min_y, max_x, max_y = 10000000, 10000000, -10000000, -10000000

    for i in range(len(obj_list)):
        obj1 = obj_list[i]
        # shape1 = shapely.geometry.box(obj1.box[0], obj1.box[1], obj1.box[2], obj1.box[3])
        # shape1 = obj1.mask_shape
        shape1 = obj1.mask_obj
        min_x = min(min_x, obj1.box[0])
        min_y = min(min_y, obj1.box[1])
        max_x = max(max_x, obj1.box[2])
        max_y = max(max_y, obj1.box[3])
        for j in range(i + 1, len(obj_list)):
            obj2 = obj_list[j]

            id1 = obj1.id
            id2 = obj2.id
            if (id1, id2) in overlap_store:
                full_area += overlap_store[(id1, id2)]
                continue

            # shape2 = shapely.geometry.box(obj2.box[0], obj2.box[1], obj2.box[2], obj2.box[3])
            # shape2 = obj2.mask_shape
            shape2 = obj2.mask_obj
            hard_cover1, soft_cover1 = if_cover(obj1, obj2, type='both')
            hard_cover2, soft_cover2 = if_cover(obj2, obj1, type='both')
            true_cover1 = (hard_cover1 == 1 and obj1.type != obj2.type)
            true_cover2 = (hard_cover2 == 1 and obj1.type != obj2.type)

            if not isinstance(shape1, Mask):
                tmp_shape = shape1.intersection(shape2)
                mask_intersect = tmp_shape.area / (shape1.union(shape2).area+0.00001)
            else:
                tmp_shape = shape1.intersection(shape2, need_bounds=False)
                mask_intersect = tmp_shape.area / (shape1.union(shape2, need_bounds=False).area+0.00001)

            if mask_intersect > 0:
                mask_intersect = 1 / (1 + np.exp(-20 * (mask_intersect - 0.5)))
            # if mask_intersect > 0:
            #     if mask_intersect > 0.5:
            #         mask_intersect = 100
            #     else:
            #         mask_intersect = 0

            if true_cover1 or true_cover2:
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue
            if (hard_cover1 and obj2.type in ['visual_element']) or \
               (hard_cover2 and obj1.type in ['visual_element']):
                overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
                continue


            # if (true_cover1 and obj2.type in ['visual_element']) or \
            #    (true_cover2 and obj1.type in ['visual_element']):
            #     overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
            #     continue


            # if hard_cover1 or hard_cover2:
            #     overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = 0
            #     continue

            overlap_store[(id1, id2)] = overlap_store[(id2, id1)] = mask_intersect
            full_area += mask_intersect

    width = max(0, max_x - min_x)
    height = max(0, max_y - min_y)
    box_area = width * height

    # if full_area_s>0:
    #     print("overlap_area", full_area, full_area_s)
    #     exit(0)
    return full_area, 1


def getFullScore2(hierarchy, obj_list, weight_store=None, match_store=None, shape_store=None, overlap_store=None, adjust=True, img_shape=None):

    if hierarchy is not None:
        # print('start get score')

        # start = time.time()
        getShape(hierarchy, shape_store=shape_store)
        # print("shape time", time.time()-start)

        # full_score = getFullScore(hierarchy)
        # start = time.time()
        full_score = getFullScore(hierarchy, weight_store=weight_store, match_store=match_store, shape_store=shape_store, img_shape=img_shape)
        # print("cover time", time.time()-start)

        # print(time.time()-start)

        # if adjust:
        #     # print('start adjust')

        #     hierarchy = adjust_hierarchy(hierarchy, full_score, None, weight_store=weight_store, match_store=match_store, shape_store=shape_store)
        #     # full_score = getFullScore(hierarchy, weight_store=weight_store, match_store=match_store, shape_store=shape_store) 

        #     # print('end adjust')
    else:
        full_score = np.array([0, 1, 0, 0, 0, 1])
    
    # start = time.time()
    full_score[2], full_score[3] = getFullOverlapScore(obj_list, overlap_store=overlap_store, cover_type="hard")
    # full_score[2], full_score[3] = getFullOverlapScoreBase(obj_list, overlap_store=overlap_store, cover_type="hard")
    # full_score[2], full_score[3] = getFullOverlapScoreNew(obj_list, overlap_store=overlap_store)
    # print("overlap time", time.time()-start)

    return full_score
    

def eval_hierarchy(dict_list, input_image=None, scale=1, line=1, padding=10, show=False, adjust=True, show_text=False, store=None, shape_dict=None, img_shape=None, tot_time=None):
    if store is not None:
        weight_store = store["weight"]
        match_store = store["match"]
        shape_store = store["shape"]
        overlap_store = store["overlap"]
    else:
        weight_store = {}
        match_store = {}
        shape_store = {}
        overlap_store = {}

    if tot_time is None:
        tot_time = {}

    obj_list = []

    if input_image is not None and show:
        if isinstance(input_image, tuple):
            width, height = input_image[0] * scale, input_image[1] * scale
            old_image = Image.new("RGB", (width, height), "white")
        else:
            old_image = Image.open(input_image).convert('RGB')

        new_width = old_image.width + 2 * padding * scale
        new_height = old_image.height + 2 * padding * scale
        image = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))
        image.paste(old_image, (padding, padding))

        draw = ImageDraw.Draw(image)
        for k, dc in enumerate(dict_list):
            color = "blue"
            if dc['type'] == 'image':
                color = 'yellow'
            if dc['type'] == 'non-data':
                color = 'red'
            if dc['type'] == 'data':
                color = 'green'
            
            adjust_box = ((np.array(dc['box']) + padding) * scale).tolist()

            if shape_dict is not None and dc['id'] in shape_dict and shape_dict[dc["id"]][0] is not None:
            # if False:
                tmp_shape = shapely.affinity.translate(shape_dict[dc["id"]][0], xoff=padding, yoff=padding)
                tmp_shape = shapely.affinity.scale(tmp_shape, xfact=scale, yfact=scale, origin=(0, 0))
                draw_polygon(draw, tmp_shape, outline_color=color, line=1 * line)
            else:
                draw.rectangle(adjust_box, outline=color, width=1 * line)
            # draw.rectangle(adjust_box, outline=color, width=1 * line)

            if show_text:
            # if True:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                draw.text(((adjust_box[0]+adjust_box[2])/2, (adjust_box[1]+adjust_box[3])/2), str(dc['id']), color, font=font)

        if isinstance(show, str):
            image.save(show + "_1.png")
        else:
            image.save("output_1.png")

    start = time.time()

    use_bits = False
    for dc in dict_list:
        if shape_dict is not None and dc['id'] in shape_dict and shape_dict[dc['id']][1] is not None:
            use_bits = True
            break

    for dc in dict_list:
        obj = Group()
        obj.box = dc['box']
        obj.type = dc['type']
        obj.id = dc['id']
        obj_list.append(obj)

        if shape_dict is None or len(shape_dict) == 0:
            obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            obj.mask_obj = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
        elif shape_dict is not None and dc['id'] in shape_dict and shape_dict[dc['id']][0] is not None:
            obj.mask_shape = shape_dict[dc['id']][0]
            if obj.mask_shape is None:
                obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            obj.mask_obj = shape_dict[dc['id']][1]
            if obj.mask_obj is None:
                if use_bits:
                    obj.mask_obj = getMaskFromBox(img_shape[0], img_shape[1], obj.box[0], obj.box[1], obj.box[2], obj.box[3])
                else:
                    obj.mask_obj = obj.mask_shape
        else:
            obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            if use_bits:
                obj.mask_obj = getMaskFromBox(img_shape[0], img_shape[1], obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            else:
                obj.mask_obj = obj.mask_shape

        # if img_shape is not None:
        if False:
            if dc['box'][2]-dc['box'][0]+dc['box'][3]-dc['box'][1]<min(img_shape[0]*8, img_shape[1]*8, img_shape[0]+img_shape[1])/10:
                obj.small = True
            else:
                obj.small = False

            if dc['box'][2]-dc['box'][0]+dc['box'][3]-dc['box'][1]<min(img_shape[0]*8, img_shape[1]*8, img_shape[0]+img_shape[1])/20:
            # if dc['box'][2]-dc['box'][0]+dc['box'][3]-dc['box'][1]<min(img_shape[0]*15, img_shape[1]*15, img_shape[0]+img_shape[1])/20:
                obj.tiny = True
            else:
                obj.tiny = False
        else:
            obj.small = False
            obj.tiny = False

    for i in range(len(obj_list)-1):
        obj1 = obj_list[i]
        for j in range(i+1, len(obj_list)):
            obj2 = obj_list[j]
            # if obj1.type == 'text' and obj2.type == 'text':
            #     cover1 = if_cover(obj1, obj2, type='very_hard')
            #     cover2 = if_cover(obj2, obj1, type='very_hard')
            #     if cover1:
            #         obj2.hide = True
            #     if cover2:
            #         obj1.hide = True

    # print('start merge')
    hierarchy_list = hierarchy_merge(obj_list)

    # obj_list2 = [obj for obj in obj_list if "mark" in obj.type.lower() and "gridline" not in obj.type.lower()]  # 去除掉本质上没有面积的元素、难以处理的元素
    # obj_list2 = [obj for obj in obj_list if obj.type.lower() not in ["text"] and "gridline" not in obj.type.lower()]  # 去除掉本质上没有面积的元素、难以处理的元素
    obj_list2 = [obj for obj in obj_list if "gridline" not in obj.type.lower()]  # 去除掉本质上没有面积的元素、难以处理的元素
    # obj_list2 = [obj for obj in obj_list if obj.type.lower() not in ["mark", "line_mark", "radar_mark", "bump_mark", "sankey_mark", "text"] and "gridline" not in obj.type.lower()]  # 去除掉本质上没有面积的元素、难以处理的元素

    if len(obj_list) != len(obj_list2):
        hierarchy_list2 = hierarchy_merge(obj_list2)
        if len(hierarchy_list2) == 0:
            hierarchy_list2 = [None]*len(hierarchy_list)
    else:
        hierarchy_list2 = hierarchy_list

    # print('end merge')

    # print("hierarchy time", len(obj_list), time.time()-start)
    if "hierarchy_time" not in tot_time:
        tot_time["hierarchy_time"] = 0
    tot_time["hierarchy_time"] += time.time()-start

    def get_deep_up(obj):
        if len(obj.children) == 0:
            obj.deep = 1
            obj.max_deep = 1
        else:
            obj.deep = 1
            obj.max_deep = 1
            for c_obj in obj.children:
                obj.deep = max(get_deep_up(c_obj) + 1, obj.deep)
                if abs(obj.box[0]-c_obj.box[0])<0.00001 or abs(obj.box[1]-c_obj.box[1])<0.00001 or abs(obj.box[2]-c_obj.box[2])<0.00001 or abs(obj.box[3]-c_obj.box[3])<0.00001:
                    obj.max_deep = max(c_obj.max_deep + 1, obj.max_deep)
        return obj.deep

    def get_deep_down(obj, deep, deep2):
        obj.deep = deep
        obj.deep2 = deep2
        for c_obj in obj.children:
            get_deep_down(c_obj, deep - 1, deep2 + 1)

    if input_image is not None and show:
        if isinstance(input_image, tuple):
            width, height = input_image[0] * scale, input_image[1] * scale
            old_image = Image.new("RGB", (width, height), "white")
        else:
            old_image = Image.open(input_image).convert('RGB')

        new_width = old_image.width + 2 * padding * scale
        new_height = old_image.height + 2 * padding * scale
        image = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))
        image.paste(old_image, (padding, padding))

        draw = ImageDraw.Draw(image)

    full_score = np.zeros(6)
    for i in range(len(hierarchy_list)):
        start = time.time()

        hierarchy = hierarchy_list[i]
        hierarchy2 = hierarchy_list2[i]

        full_score = getFullScore2(hierarchy2, obj_list, weight_store=weight_store, match_store=match_store, shape_store=shape_store, overlap_store=overlap_store, adjust=adjust, img_shape=img_shape)

        # print("score time", time.time()-start)
        if "score_time" not in tot_time:
            tot_time["score_time"] = 0
        tot_time["score_time"] += time.time()-start

        get_deep_up(hierarchy)
        get_deep_down(hierarchy, hierarchy.deep, 1)
        
        # if show:
        #     print(full_score)
        #     print(full_score[0] / full_score[1], full_score[2] / full_score[3], full_score[4] / full_score[5])

        if input_image is not None and show:

            color_list = ['blue', 'green', 'orange', 'red', 'purple', 'black']
            color_list2 = ['black', 'purple', 'red', 'orange', 'green', 'blue', 'grey']

            def draw_hierarchy(obj, draw):
                width = obj.deep
                adjust_box = ((np.array(obj.box) + padding) * scale).tolist()
                adjust_box[0] -= (width - 1) * line
                adjust_box[1] -= (width - 1) * line
                adjust_box[2] += (width - 1) * line
                adjust_box[3] += (width - 1) * line
                # draw.rectangle(adjust_box, outline=color_list[(obj.deep-1) % 6], width=width)
                draw.rectangle(adjust_box, outline=color_list2[(obj.deep2 - 1) % 7], width=width * line)
                for c_obj in obj.children:
                    draw_hierarchy(c_obj, draw)

            draw_hierarchy(hierarchy, draw)

        # print('end get score')

    if input_image is not None and show:
        if isinstance(show, str):
            image.save(show + "_2.png")
        else:
            image.save("output_2.png")
    
    output_hierarchy = None
    if len(hierarchy_list)>0:
        output_hierarchy = hierarchy_list[0]
    return full_score[0] / full_score[1], full_score[2] / full_score[3], full_score[4] / full_score[5], output_hierarchy


def if_overlap(obj1, obj2):
    box1 = obj1.box
    box2 = obj2.box

    [x1_A, y1_A, x2_A, y2_A] = box1
    [x1_B, y1_B, x2_B, y2_B] = box2

    x_left = max(x1_A, x1_B)
    y_top = max(y1_A, y1_B)
    x_right = min(x2_A, x2_B)
    y_bottom = min(y2_A, y2_B)

    if x_right < x_left or y_bottom < y_top:
        intersection_area = 0
    else:
        intersection_width = x_right - x_left
        intersection_height = y_bottom - y_top
        intersection_area = intersection_width * intersection_height

    A_area = (x2_A - x1_A) * (y2_A - y1_A)
    B_area = (x2_B - x1_B) * (y2_B - y1_B)

    if intersection_area > 0.2 * min(A_area, B_area):
        return 1

    return 0


def mergeOtherCandidate(hierarchy, dict_list, shape_dict=None, img_shape=None, virtual_hang=True):

    obj_list = []

    use_bits = False
    for dc in dict_list:
        if shape_dict is not None and dc['id'] in shape_dict and shape_dict[dc['id']][1] is not None:
            use_bits = True
            break

    for dc in dict_list:
        obj = Group()
        obj.box = dc['box']
        obj.type = dc['type']
        obj.id = dc['id']
        obj_list.append(obj)

        if shape_dict is None or len(shape_dict) == 0:
            obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            obj.mask_obj = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
        elif shape_dict is not None and dc['id'] in shape_dict and shape_dict[dc['id']][0] is not None:
            obj.mask_shape = shape_dict[dc['id']][0]
            if obj.mask_shape is None:
                obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            obj.mask_obj = shape_dict[dc['id']][1]
            if obj.mask_obj is None:
                if use_bits:
                    obj.mask_obj = getMaskFromBox(img_shape[0], img_shape[1], obj.box[0], obj.box[1], obj.box[2], obj.box[3])
                else:
                    obj.mask_obj = obj.mask_shape
        else:
            obj.mask_shape = shapely.geometry.box(obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            if use_bits:
                obj.mask_obj = getMaskFromBox(img_shape[0], img_shape[1], obj.box[0], obj.box[1], obj.box[2], obj.box[3])
            else:
                obj.mask_obj = obj.mask_shape
                
        # if img_shape is not None:
        if False:
            if dc['box'][2]-dc['box'][0]+dc['box'][3]-dc['box'][1]<min(img_shape[0]*8, img_shape[1]*8, img_shape[0]+img_shape[1])/10:
                obj.small = True
            else:
                obj.small = False

            if dc['box'][2]-dc['box'][0]+dc['box'][3]-dc['box'][1]<min(img_shape[0]*8, img_shape[1]*8, img_shape[0]+img_shape[1])/20:
                obj.tiny = True
            else:
                obj.tiny = False
        else:
            obj.small = False
            obj.tiny = False

        obj.unselected = True

    outer_list = []
    def ClearDFS(obj):
        if obj is None:
            return
        obj.cover_list = []
        obj.hang_list = []
        for child in obj.children:
            ClearDFS(child)
    ClearDFS(hierarchy)

    def findBestNode(new_obj):
        best_obj = [None]
        best_area = [-1]

        def findBestNodeDFS(obj, new_obj):
            if obj is None:
                return

            if if_cover(obj, new_obj, 'soft'):
                flag = False
                area = (obj.box[2]-obj.box[0]) * (obj.box[3]-obj.box[1])
                if best_obj[0] == None:
                    flag = True
                elif obj.type == best_obj[0].type and area < best_area[0]:
                    flag = True
                elif obj.type == "group" and best_obj[0].type != "group":
                    flag = True
                if flag:
                    best_obj[0] = obj
                    best_area[0] = area
            
            for child_obj in obj.children:
                findBestNodeDFS(child_obj, new_obj)

        findBestNodeDFS(hierarchy, new_obj)

        def moveDown(target_obj, new_obj):
            overlap_list = []

            if not hasattr(target_obj, "outer_obj"):
                getShape(target_obj, recalc=False)
                getInnerShape(target_obj)
                
            for child in target_obj.children:
                if if_overlap(child, new_obj) and child not in target_obj.outer_obj:
                    overlap_list.append(child)

            if len(overlap_list) > 1:
                return target_obj
            if len(overlap_list) == 1:
                if if_cover(new_obj, overlap_list[0], 'soft'):
                    return moveDown(overlap_list[0], new_obj)
            tmp_best_obj = None
            tmp_best_dist = -1


            for child in target_obj.children:
                tmp_dist = get_dist(child, new_obj)
                if if_cover(child, new_obj, 'soft'):
                    if child in target_obj.outer_obj:
                        tmp_dist *= 20
                    else:
                        tmp_dist /= 20
                if (tmp_best_obj is None) or (tmp_dist < tmp_best_dist):
                    tmp_best_obj = child
                    tmp_best_dist = tmp_dist
            if tmp_best_obj is not None:
                return moveDown(tmp_best_obj, new_obj)
            return target_obj

        if best_obj[0] is not None:
            if len(best_obj[0].children)>0:
                best_obj[0] = moveDown(best_obj[0], new_obj)
            if not virtual_hang and if_cover(best_obj[0], new_obj, 'soft'):
                if not hasattr(best_obj[0], 'cover_list'):
                    best_obj[0].cover_list = []
                best_obj[0].cover_list.append(new_obj)
            else:
                if not hasattr(best_obj[0], 'hang_list'):
                    best_obj[0].hang_list = []
                best_obj[0].hang_list.append(new_obj)
        else:
            outer_list.append(new_obj)
    
    for new_obj in obj_list:
        findBestNode(new_obj)

    def updateHang(obj):
        if obj is None:
            return None
        
        for i in range(len(obj.children)):
            child_obj = obj.children[i]
            obj.children[i] = updateHang(child_obj)

        old_obj = obj

        cover_flag = False
        if hasattr(old_obj, 'cover_list') and len(old_obj.cover_list)>0:
            new_obj = hierarchy_merge(old_obj.cover_list)[0]
            
            if obj.type == 'group':
                obj.children.append(new_obj)
            else:
                merge_obj = Group()
                merge_obj.box = [obj.box[0], obj.box[1], obj.box[2], obj.box[3]]
                merge_obj.type = 'group'
                merge_obj.children.append(obj)
                merge_obj.children.append(new_obj)
                getSubType(merge_obj)
                obj = merge_obj
            
            cover_flag = True

        if hasattr(old_obj, 'hang_list') and len(old_obj.hang_list)>0:
            new_obj = hierarchy_merge(old_obj.hang_list)[0]
            
            if obj.type == 'group' and not cover_flag:
                obj.children.append(new_obj)
            else:
                merge_obj = Group()
                merge_obj.box = [obj.box[0], obj.box[1], obj.box[2], obj.box[3]]
                merge_obj.type = 'group'
                merge_obj.children.append(obj)
                merge_obj.children.append(new_obj)
                getSubType(merge_obj)
                obj = merge_obj


        return obj
    
    hierarchy = updateHang(hierarchy)

    if len(outer_list)>0:
        # if len(outer_list) == 1:
        #     new_obj = outer_list[0]
        # else:
        #     new_obj = Group()
        #     min_x = 10000000
        #     min_y = 10000000
        #     max_x = -10000000
        #     max_y = -10000000
        #     for hang_obj in outer_list:
        #         new_obj.children.append(hang_obj)
        #         min_x = min(min_x, hang_obj.box[0])
        #         min_y = min(min_y, hang_obj.box[1])
        #         max_x = max(max_x, hang_obj.box[2])
        #         max_y = max(max_y, hang_obj.box[3])
        #     new_obj.box = [min_x, min_y, max_x, max_y]
        #     new_obj.type = 'group'
        #     getSubType(new_obj)
        new_obj = hierarchy_merge(outer_list)[0]

        if hierarchy is None:
            hierarchy = new_obj
        else:
            merge_obj = Group()
            merge_obj.box = [hierarchy.box[0], hierarchy.box[1], hierarchy.box[2], hierarchy.box[3]]
            merge_obj.type = 'group'
            merge_obj.children.append(hierarchy)
            merge_obj.children.append(new_obj)
            getSubType(merge_obj)
            hierarchy = merge_obj

    def get_deep_up(obj):
        if len(obj.children) == 0:
            obj.deep = 1
            obj.max_deep = 1
        else:
            obj.deep = 1
            obj.max_deep = 1
            for c_obj in obj.children:
                obj.deep = max(get_deep_up(c_obj) + 1, obj.deep)
                if abs(obj.box[0]-c_obj.box[0])<0.00001 or abs(obj.box[1]-c_obj.box[1])<0.00001 or abs(obj.box[2]-c_obj.box[2])<0.00001 or abs(obj.box[3]-c_obj.box[3])<0.00001:
                    obj.max_deep = max(c_obj.max_deep + 1, obj.max_deep)
        return obj.deep

    def get_deep_down(obj, deep, deep2):
        obj.deep = deep
        obj.deep2 = deep2
        for c_obj in obj.children:
            get_deep_down(c_obj, deep - 1, deep2 + 1)
    
    if virtual_hang:
        updateBox2(hierarchy)
    else:
        updateBox(hierarchy)
    get_deep_up(hierarchy)
    get_deep_down(hierarchy, hierarchy.deep, 1)

    return hierarchy


def updateBox(obj):
    if len(obj.children) == 0:
        return
    min_x = 10000000
    min_y = 10000000
    max_x = -10000000
    max_y = -10000000
    for child in obj.children:
        updateBox(child)
        min_x = min(min_x, child.box[0])
        min_y = min(min_y, child.box[1])
        max_x = max(max_x, child.box[2])
        max_y = max(max_y, child.box[3])
    
    obj.box = [min_x, min_y, max_x, max_y]


# 考虑所有候选框来计算bounding box
def updateBox2(obj):
    if len(obj.children) == 0:
        obj.box2 = [obj.box[0], obj.box[1], obj.box[2], obj.box[3]]
        return
    min_x = 10000000
    min_y = 10000000
    max_x = -10000000
    max_y = -10000000
    for child in obj.children:
        updateBox2(child)
        min_x = min(min_x, child.box2[0])
        min_y = min(min_y, child.box2[1])
        max_x = max(max_x, child.box2[2])
        max_y = max(max_y, child.box2[3])
    
    obj.box2 = [min_x, min_y, max_x, max_y]


def getObjHierarchy(hierarchy_json, boxes_json, with_text=True, use_type="class"):
    def getGroupFrom(box_json, id):
        new_obj = Group()
        new_obj.box = [box_json["x"], box_json["y"], box_json["x"]+box_json["width"], box_json["y"]+box_json["height"]]
        new_obj.type = box_json[use_type]
        new_obj.base_type = box_json["class"]
        new_obj.id = id
        if "unselected" in box_json and box_json["unselected"]:
            new_obj.hide = True
        return new_obj

    if hierarchy_json is None:
        if len(boxes_json) == 0:
            return None
        return getGroupFrom(boxes_json[0], 0)
    if isinstance(hierarchy_json, int):
        if not with_text and boxes_json[hierarchy_json]["super_class"] == "text":
            return None
        return getGroupFrom(boxes_json[hierarchy_json], hierarchy_json)

    new_obj = Group()
    min_x = 10000000
    min_y = 10000000
    max_x = -10000000
    max_y = -10000000
    hide_flag = True
    for child in hierarchy_json["children"]:
        child_obj = getObjHierarchy(child, boxes_json, with_text=with_text, use_type=use_type)

        if child_obj is None:
            continue

        child_obj.parent = new_obj
        new_obj.children.append(child_obj)
        min_x = min(min_x, child_obj.box[0])
        min_y = min(min_y, child_obj.box[1])
        max_x = max(max_x, child_obj.box[2])
        max_y = max(max_y, child_obj.box[3])
        if not hasattr(child_obj, "hide") or not child_obj.hide:
            hide_flag = False
    
    if len(new_obj.children) == 0:
        return None
    # if len(new_obj.children) == 1:
    #     return new_obj.children[0]
    
    if hide_flag:
        new_obj.hide = True
    
    new_obj.box = [min_x, min_y, max_x, max_y]
    new_obj.type = 'group'
    new_obj.base_type = 'group'

    return new_obj


def getCrossObjSimilarity(obj1, obj2, full_obj1, full_obj2, type='soft'):
    if obj1 is None or obj2 is None:
        return 0

    if obj1.type != obj2.type:
        return 0

    width1 = (obj1.box[2] - obj1.box[0]) / (full_obj1.box[2] - full_obj1.box[0])
    height1 = (obj1.box[3] - obj1.box[1]) / (full_obj1.box[3] - full_obj1.box[1])
    width2 = (obj2.box[2] - obj2.box[0]) / (full_obj2.box[2] - full_obj2.box[0])
    height2 = (obj2.box[3] - obj2.box[1]) / (full_obj2.box[3] - full_obj2.box[1])

    similarity = 1 - max(abs(width1-width2), abs(height1-height2))

    if type == 'hard':
        if width2 > width1*4 or width1 > width2*4 or height2 > height1*4 or height1 > height2*4:
            return 0
        if width2*height1 > width1*height2*2 or width1*height2 > width2*height1*2:
            return 0

    if similarity > 0.8:
        return 1
    
    return 0


def if_Bigger(obj1, obj2, full_obj1, full_obj2):
    width1 = (obj1.box[2] - obj1.box[0]) / (full_obj1.box[2] - full_obj1.box[0])
    height1 = (obj1.box[3] - obj1.box[1]) / (full_obj1.box[3] - full_obj1.box[1])
    width2 = (obj2.box[2] - obj2.box[0]) / (full_obj2.box[2] - full_obj2.box[0])
    height2 = (obj2.box[3] - obj2.box[1]) / (full_obj2.box[3] - full_obj2.box[1])

    if height2-height1 > 0.2:
        return 1
    if width2-width1 > 0.2:
        return 1
    return 0


def getCrossGroupSimilarity(basic_obj1, basic_obj2, full_obj1, full_obj2):
    ll = max(len(basic_obj1), len(basic_obj2))
    mtx = np.zeros((ll, ll))
    for i in range(len(basic_obj1)):
        for j in range(len(basic_obj2)):
            mtx[i][j] = getCrossObjSimilarity(basic_obj1[i], basic_obj2[j], full_obj1, full_obj2)
    row_ind, col_ind = linear_sum_assignment(-mtx)
    match = mtx[row_ind, col_ind].sum()
    # print("match", match)
    ans = match / max(0.000001, len(basic_obj1) + len(basic_obj2) - match)
    return ans


def getAllBasicObj(obj):
    if obj.type != "group":
        return [obj]
    if hasattr(obj, 'all_basic_obj') and obj.all_basic_obj is not None:
        return obj.all_basic_obj[:]
    all_obj_list = []
    for sub_obj in obj.children:
        all_obj_list.extend(getAllBasicObj(sub_obj))
    obj.all_basic_obj = all_obj_list[:]
    return all_obj_list


def getBestSimilarity(now_obj, source_hierarchy, source_obj, store=None, cover_store_source=None, cover_store_now=None, show=False):
    if now_obj.type != source_obj.type:
        return 0 

    source_obj_list = getBasicObj(source_hierarchy)
    # if source_obj not in source_obj_list:
    #     source_obj_list.append(source_obj)
    source_all_obj_list = getAllBasicObj(source_hierarchy)

    if cover_store_source is not None and source_hierarchy in cover_store_source:
        one_cover_all, source_one = cover_store_source[source_hierarchy]
    else:
        one_cover_all, source_one = ifOneCoverAll(source_all_obj_list)
    if cover_store_source is not None:
        cover_store_source[source_hierarchy] = (one_cover_all, source_one)
    
    source_obj_list = [obj for obj in source_obj_list if obj.base_type not in ["Annotation", "Title", "Source", "gridline", "mark"]]   # text mark不计数

    if show:
        print("source one cover all", len(source_all_obj_list), one_cover_all)

    # print("source_obj_list len", len(source_obj_list))
    
    def getBestSimilarityUp(now_hierarchy, now_obj):
        now_obj_list = getBasicObj(now_hierarchy)
        now_all_obj_list = getAllBasicObj(now_hierarchy)
        # if now_obj not in now_obj_list:
        #     now_obj_list.append(now_obj)

        now_obj_list = [obj for obj in now_obj_list if obj.base_type not in ["Annotation", "Title", "Source", "gridline", "mark"]]   # text mark不计数

        if len(now_obj_list) >= 3*len(source_obj_list):
            return 0
        
        if show:
            print("compare", len(source_obj_list), len(now_obj_list))
            print("now hierarchy", now_hierarchy)

        if getCrossObjSimilarity(now_obj, source_obj, now_hierarchy, source_hierarchy, 'hard'):
            if (store is not None) and ((now_hierarchy, source_hierarchy) in store):
                score = store[(now_hierarchy, source_hierarchy)]
            else:
                score = getCrossGroupSimilarity(now_obj_list, source_obj_list, now_hierarchy, source_hierarchy)
                if one_cover_all:
                    if cover_store_now is not None and now_hierarchy in cover_store_now:
                        now_one_cover_all, now_one = cover_store_now[now_hierarchy]
                    else:
                        now_one_cover_all, now_one = ifOneCoverAll(now_all_obj_list)
                    if cover_store_now is not None:
                        cover_store_now[now_hierarchy] = (now_one_cover_all, now_one)
                    
                    if show:
                        print("target one cover all", len(now_all_obj_list), now_one_cover_all)
                    
                    score = score * getCrossObjSimilarity(now_one, source_one, now_hierarchy, source_hierarchy)
            if store is not None:
                store[(now_hierarchy, source_hierarchy)] = score
        else:
            if if_Bigger(now_obj, source_obj, now_hierarchy, source_hierarchy):
                return 0
            score = 0
        # print("score", score)
        if hasattr(now_hierarchy, "parent"):
            score = max(score, getBestSimilarityUp(now_hierarchy.parent, now_obj))
        return score

    return getBestSimilarityUp(now_obj, now_obj)


def getSimilarity(now_hierarchy, now_obj, source_hierarchy, source_obj, store=None):
    if now_obj.type != source_obj.type:
        return 0 

    if getCrossObjSimilarity(now_obj, source_obj, now_hierarchy, source_hierarchy):
        if store is not None:
            if (now_hierarchy, source_hierarchy) in store:
                return store[(now_hierarchy, source_hierarchy)]
        
        source_obj_list = getBasicObj(source_hierarchy)
        # if source_obj not in source_obj_list:
        #     source_obj_list.append(source_obj)

        now_obj_list = getBasicObj(now_hierarchy)
        # if now_obj not in now_obj_list:
        #     now_obj_list.append(now_obj)

        ans = getCrossGroupSimilarity(now_obj_list, source_obj_list, now_hierarchy, source_hierarchy)
        if store is not None:
            store[(now_hierarchy, source_hierarchy)] = ans
        return ans
    else:
        return 0


def getObjDict(now_hierarchy):
    result = {}
    def getObjDictDFS(now_hierarchy):
        if now_hierarchy.type != "group":
            result[now_hierarchy.id] = now_hierarchy
        for child in now_hierarchy.children:
            getObjDictDFS(child)
    if now_hierarchy is not None:
        getObjDictDFS(now_hierarchy)
    return result


def ifOneCoverAll(obj_list):
    min_x, min_y, max_x, max_y = 10000000, 10000000, -10000000, -10000000

    area_list = []
    for tmp_obj in obj_list:
        # area_list.append(tmp_obj.shape.area)
        area_list.append((tmp_obj.box[2]-tmp_obj.box[0])*(tmp_obj.box[3]-tmp_obj.box[1]))
        min_x = min(min_x, tmp_obj.box[0])
        min_y = min(min_y, tmp_obj.box[1])
        max_x = max(max_x, tmp_obj.box[2])
        max_y = max(max_y, tmp_obj.box[3])

    width = max(0, max_x - min_x)
    height = max(0, max_y - min_y)
    box_area = width * height

    ls = [i for i in range(len(obj_list))]
    for i in range(len(obj_list) - 1):
        for j in range(i + 1, len(obj_list)):
            if area_list[ls[i]] < area_list[ls[j]]:
                ls[i], ls[j] = ls[j], ls[i]

    flag = False
    result = None

    for i in range(len(ls)):
        tmp_obj = obj_list[ls[i]]
        if i < min(1, len(ls) - 1) and area_list[ls[i]] > 0.95 * box_area and tmp_obj.type != 'group':
            flag = True
            result = obj_list[ls[i]]
    
    return flag, result


def getObjContext(now_obj):
    result = [None]
    def getObjContextUp(now_hierarchy, now_obj):
        result[0] = now_hierarchy
        flag = False

        now_obj_list = getBasicObj(now_hierarchy)
        now_obj_list = [obj for obj in now_obj_list if obj.base_type not in ["Annotation", "Title", "Source", "gridline", "mark"]]   # text mark不计数
        if now_obj not in now_obj_list:
            now_obj_list.append(now_obj)
        if len(now_obj_list) >= 2:
            if_one_cover_all, cover_obj = ifOneCoverAll(now_obj_list)
            if if_one_cover_all and cover_obj != now_obj:
                flag = True
        if not flag and len(now_obj_list) >= 10:
            out_cnt = 0
            for obj in now_obj_list:
                if not if_cover(now_obj, obj, 'hard'):
                    out_cnt += 1
            if len(now_obj_list) >= 20 and out_cnt >= 10:
                flag = True
            else:
                type_list = []
                for obj in now_obj_list:
                    type_list.append(obj.type)
                if len(Counter(type_list)) > 1 and out_cnt >= 5:
                    flag = True

        if (not flag) and hasattr(now_hierarchy, "parent"):
            getObjContextUp(now_hierarchy.parent, now_obj)
    
    getObjContextUp(now_obj, now_obj)
    return result[0]
    

def test(hierarchy_json_list):
    id1 = 5370
    # id2 = 5370
    id2 = 5113
    hierarchy1 = getObjHierarchy(hierarchy_json_list[id1]["hierarchy"], hierarchy_json_list[id1]["boxes"])
    hierarchy2 = getObjHierarchy(hierarchy_json_list[id2]["hierarchy"], hierarchy_json_list[id2]["boxes"])

    # list1 = getBasicObj(hierarchy1)
    # list2 = getBasicObj(hierarchy2)
    # tmp = hierarchy2
    # while len(tmp.children)>0:
    #     tmp = tmp.children[-1]
    # # print(tmp.type)
    # print(getBestSimilarity(tmp, hierarchy1, list1[0]))

    list1 = getBasicObj(hierarchy1)
    list2 = getBasicObj(hierarchy2)
    print(len(list1), len(list2))
    obj_dict1 = getObjDict(hierarchy1)
    obj_dict2 = getObjDict(hierarchy2)
    print(len(obj_dict1), len(obj_dict2))
    print()
    for key in obj_dict1:
        context1 = getObjContext(obj_dict1[key])
        cnt = 0
        obj1 = obj_dict1[key]
        while obj1 != context1:
            obj1 = obj1.parent
            cnt += 1
        print(key, cnt, len(getBasicObj(context1)))


if __name__ == '__main__':
    scale = 3

    dict_list = [{'type': 'text', 'box': [0, 0, 100, 20]}, {'type': 'text', 'box': [0, 30, 10, 40]},
                 {'type': 'text', 'box': [0, 60, 10, 70]}, {'type': 'image', 'box': [15, 25, 40, 45]},
                 {'type': 'image', 'box': [15, 55, 40, 75]}]
    dict_list.extend([{'type': 'text', 'box': [50, 30, 60, 40]}, {'type': 'text', 'box': [50, 60, 60, 70]},
                      {'type': 'image', 'box': [65, 25, 90, 45]}, {'type': 'image', 'box': [65, 55, 90, 75]}])
    dict_list.extend([{'type': 'non-data', 'box': [0 - 1, 25 - 1, 40 + 1, 45 + 1]},
                      {'type': 'non-data', 'box': [0 - 1, 55 - 1, 40 + 1, 75 + 1]}])
    dict_list.extend([{'type': 'non-data', 'box': [50 - 1, 25 - 1, 90 + 1, 45 + 1]},
                      {'type': 'non-data', 'box': [50 - 1, 55 - 1, 90 + 1, 75 + 1]}])

    dict_list.extend([{'type': 'data', 'box': [0 - 2, 100 - 2, 100 + 2, 165 + 2]},
                      {'type': 'data', 'box': [0, 100, 30, 130]}, {'type': 'data', 'box': [0, 135, 30, 165]},
                      {'type': 'data', 'box': [35, 100, 65, 130]}, {'type': 'data', 'box': [35, 135, 65, 165]},
                      {'type': 'data', 'box': [70, 100, 100, 130]}, {'type': 'data', 'box': [70, 135, 100, 165]}])
    random.seed(70)
    np.random.seed(40)

    ori_dict_list = dict_list
    ori_select = [i for i in range(len(dict_list))]

    # num_to_remove = 5
    # elements_to_remove = random.sample(ori_select, num_to_remove)
    # for elem in elements_to_remove:
    #     ori_select.remove(elem)
    # dict_list = [ori_dict_list[i] for i in ori_select]
    #
    # for i in ori_select:
    #     dc = ori_dict_list[i]
    #     noise_std = 2
    #     noise = np.random.normal(0, noise_std, np.array(dc['box']).shape)
    #     dc['box'] = np.round(np.array(dc['box'])+noise).tolist()

    # dict_list = [{'type': 'text', 'box': [0, 0, 30, 30]}, {'type': 'text', 'box': [0, 30, 30, 60]},
    #              {'type': 'text', 'box': [30, 0, 60, 30]}, {'type': 'image', 'box': [0-1, 0-1, 30+1, 60+1]}]

    eval_hierarchy(dict_list, (100, 180), scale=3, show=True)
