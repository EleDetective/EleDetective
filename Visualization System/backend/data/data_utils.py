import sys
import numpy as np
import json
import os
import random
import shutil
import copy
from scene_tree.grouping import eval_hierarchy, mergeOtherCandidate
from scene_tree.opti import hill_climbing
from scene_tree.eval2 import getShape
from tqdm import tqdm
import pickle
from scene_tree.SAM.sam import get_mask_predictor, sam_get_mask_shape, sam_pred_image
import time

max_quata = 120  # TO FILL
conf_thres = [0.3]*20  # TO FILL
min_thres_ratio = 1/3  # TO FILL
category_dict_scenetree = {1: "text", 2: "text", 3: "text", 4: "HRO", 5: "HRO", 6: "sub-element", 7: "sub-element", 8: "gridline", 9: "mark",
    10: "chart", 11: "chart", 12: "chart", 13: "chart", 14: "chart", 15: "chart", 16: "chart", 17: "chart", 18: "chart", 19: "chart", 20: "chart"}    # TO FILL used in scene tree
category_dict_super = {1: "text", 2: "text", 3: "text", 4: "HRO", 5: "HRO", 6: "sub-element", 7: "sub-element", 8: "sub-element", 9: "sub-element",
    10: "chart", 11: "chart", 12: "chart", 13: "chart", 14: "chart", 15: "chart", 16: "chart", 17: "chart", 18: "chart", 19: "chart", 20: "chart"}    # TO FILL upper level class
category_dict = {1: "Annotation", 2: "Title", 3: "Source", 4: "Label-Icon", 5: "Embellishment", 6: "legend", 7: "axis", 8: "gridline", 9: "mark", 
    10: "Bar Chart", 11: "Line Chart", 12: "Radar Chart", 13: "Area Chart", 14: "Pie Chart", 15: "Proportional Chart", 16: "Treemap", 17: "ScatterPlot", 18: "Pyramid & Funnel Chart", 19: "Sankey Diagram", 20: "Heatmap"}  # TO FILL lower level class
image_pre = os.environ.get("ELEDETECTIVE_IMAGE_DIR", "/YOUR/IMAGE/FOLDER/PATH/").rstrip("/") + "/"
image_pre2 = os.environ.get("ELEDETECTIVE_IMAGE_URL", "YOUR/PUBLIC/IMAGE/FOLDER/PATH/").rstrip("/") + "/"

def mergeCandidateText(candidate_without_text, text, image_list, path, use_mask=False):

    if use_mask:
        mask_predictor = get_mask_predictor()

    full_candidate = []

    for i in tqdm(range(len(image_list))):
        item = image_list[i]
        image_id = item["id"]
        old_candidate_item = candidate_without_text[i]
        new_candidate_item = old_candidate_item.copy()
        new_candidate_item["annotations"] = new_candidate_item["annotations"][:]
        new_candidate_item["shape_dict"] = new_candidate_item["shape_dict"].copy()
        new_candidate_item["subset"] = new_candidate_item["subset"][:]

        if use_mask:
            sam_pred_image(mask_predictor, image_pre+item["file_name"])

        cnt2 = len(new_candidate_item["annotations"])
        for item2 in text:
            if item2["image_id"] != image_id:
                continue

            new_item = {"score": 1, "bbox": item2["bbox"], "category_id": 4, "image_id": image_id, "score_scale": 1}
            new_candidate_item["annotations"].append(new_item)
            new_candidate_item["subset"].append(cnt2)
            if use_mask:
                tmp_shape = sam_get_mask_shape(mask_predictor, np.array(new_item["bbox"]).astype('int'))
                if tmp_shape is not None:
                    new_candidate_item["shape_dict"][cnt2] = tmp_shape
            cnt2 += 1

        full_candidate.append(new_candidate_item)

    with open(path, 'wb') as file:
        pickle.dump(full_candidate, file)
    
    return full_candidate


def getCandidate(annotations_pred, image_list, path, use_mask=True, with_text=True):

    if use_mask:
        mask_predictor = get_mask_predictor()

    full_candidate = []

    pred_dict = {}
    for item in tqdm(image_list):
        image_id = item["id"]
        pred_dict[image_id] = []
    for item2 in annotations_pred:
        if item2["image_id"] not in pred_dict:
            pred_dict[item2["image_id"]] = []
        pred_dict[item2["image_id"]].append(item2)

    for item in tqdm(image_list):
        time_mask = 0

        image_id = item["id"]
        
        if use_mask:
            start = time.time()
            sam_pred_image(mask_predictor, image_pre+item["file_name"])
            time_mask += time.time() - start

        ori_select = []
        full_item_list = []
        shape_dict = {}

        cnt = 0
        cnt2 = 0
        sort_list = []
        candidate_list = []
        # for item2 in annotations_pred:
        for item2 in pred_dict[image_id]:
            if item2["image_id"] != image_id:
                continue
            candidate_list.append(item2)

            item2['score_scale'] = 1
            # if item2["category_id"] == 3 or ("1026" in mode and item2["category_id"] == 4):
            #     if item2["bbox"][2]+item2["bbox"][3] < min(item['width']*8, item['height']*8, item['width']+item['height'])/20:
            #         item2['score_scale'] = 2

            sort_list.append((cnt, item2['score_scale']*item2['score']/conf_thres[item2['category_id']-1]))
            cnt += 1
        for i in range(len(sort_list)-1):
            for j in range(i+1, len(sort_list)):
                if sort_list[i][1] < sort_list[j][1]:
                    sort_list[i], sort_list[j] = sort_list[j], sort_list[i]
        
        tmp_cnt = 0
        for i, (id, conf) in enumerate(sort_list):
            if tmp_cnt >= max_quata:
                break
            if with_text or category_dict_super[candidate_list[id]["category_id"]] != "text":
                tmp_cnt += 1
            thres = conf-0.000001

        thres = max(min_thres_ratio, thres)
        thres = min(thres, 1)
        print(thres)

        category_cnt_dict = {}

        for item2 in candidate_list:
            
            bbox = (round(item2["bbox"][0]), round(item2["bbox"][1]), round(item2["bbox"][0])+round(item2["bbox"][2]), round(item2["bbox"][1])+round(item2["bbox"][3]))

            category_id = item2["category_id"]

            if category_id in category_dict_scenetree:
                tp = category_dict_scenetree[category_id]
            else:
                tp = "other_" + str(category_id)
            
            if category_id in category_dict_super:
                tp2 = category_dict_super[category_id]
            else:
                tp2 = "other_" + str(category_id)

            if item2['score_scale']*item2['score'] > conf_thres[item2['category_id']-1]*max(1, thres):
                ori_select.append(cnt2)

            if item2['score_scale']*item2['score'] > conf_thres[item2['category_id']-1]*thres:
                full_item_list.append(item2)
                if use_mask:
                    # if with_text or tp2 != "text":
                    if tp in ["HRO", "mark"]:
                        start = time.time()
                        tmp_shape = sam_get_mask_shape(mask_predictor, np.array(bbox).astype('int'))
                        if tmp_shape is not None:
                            shape_dict[cnt2] = tmp_shape
                        time_mask += time.time() - start
                cnt2 += 1

                if tp not in category_cnt_dict:
                    category_cnt_dict[tp] = 0
                category_cnt_dict[tp] += 1

        print("category_cnt", category_cnt_dict)

        candidate_item = {"annotations": full_item_list, "shape_dict": shape_dict, "subset": ori_select}
        full_candidate.append(candidate_item)

        
        print(cnt, cnt2)
        print(candidate_item)
        print("time mask:", len(full_item_list), time_mask)

    with open(path, 'wb') as file:
        pickle.dump(full_candidate, file)
    
    return full_candidate

def updateSubset(candidate):
    ori_select = []
    for i in range(len(candidate["annotations"])):
        item2 = candidate["annotations"][i]
        if item2['score_scale']*item2['score'] > conf_thres[item2['category_id']-1]:
            ori_select.append(i)

    candidate["subset"] = ori_select

def getHierarchy(full_annots, shape_dict, subset, image_info, use_optimal=True, with_text=True):
    full_dict_list = []
    full_conf_list = []
    full_conf_list2 = []
    forbid_list = []

    cnt2 = 0
    for item2 in full_annots:
        category_id = item2["category_id"]

        if category_id in category_dict_scenetree:
            tp = category_dict_scenetree[category_id]
        else:
            tp = "other_" + str(category_id)
        
        if category_id in category_dict_super:
            tp2 = category_dict_super[category_id]
        else:
            tp2 = "other_" + str(category_id)

        bbox = (round(item2["bbox"][0]), round(item2["bbox"][1]), round(item2["bbox"][0])+round(item2["bbox"][2]), round(item2["bbox"][1])+round(item2["bbox"][3]))
        full_dict_list.append({"type": tp, "box": bbox, "id": cnt2})
        full_conf_list.append(item2['score_scale']*item2['score'])
        full_conf_list2.append(item2['score_scale']*item2['score']-conf_thres[item2['category_id']-1])
        if not with_text and tp2 == "text":
            forbid_list.append(cnt2)

        cnt2 += 1
        
    sub_dict_list = [full_dict_list[i] for i in subset]
    sub_annots = [full_annots[i] for i in subset]

    other_subset = [i for i in range(len(full_annots)) if i not in subset]
    other_dict_list = [full_dict_list[i] for i in other_subset]

    img_shape = (image_info['width'], image_info['height'])
    _, _, _, hierarchy = eval_hierarchy(sub_dict_list, shape_dict=shape_dict, img_shape=img_shape, show=True)

    # with_text = True
    if use_optimal:
        # _, _, _, hierarchy = eval_hierarchy(full_dict_list, shape_dict=shape_dict, img_shape=img_shape, show="result/images/"+image_info["file_name"]+"_full", show_text=True, input_image=image_pre+image_info["file_name"])
        # # tmp_subset = [0, 1, 2, 3, 4, 5, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 46, 44, 45, 48, 47, 6]
        # tmp_subset = [0, 1, 2, 3, 4, 5, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 46, 44, 45, 47, 48, 49, 50, 6, 7]
        # _, _, _, hierarchy = eval_hierarchy([full_dict_list[id] for id in tmp_subset], shape_dict=shape_dict, img_shape=img_shape, show="result/images/"+image_info["file_name"]+"_test", show_text=True, input_image=image_pre+image_info["file_name"])

        ori_subset = np.array(subset)
        ori_select = np.array(subset).tolist()
        if not with_text:
            ori_select = np.setdiff1d(subset, forbid_list).tolist()
            forbid_select = np.intersect1d(subset, forbid_list).tolist()
        subset, _, hierarchy = hill_climbing(ori_select=ori_select, full_dict_list=full_dict_list, full_conf_list=full_conf_list, full_conf_list2=full_conf_list2, shape_dict=shape_dict, img_shape=img_shape, forbid_list=forbid_list, only_nms=(len(full_dict_list)>max_quata))
        # print("subset", subset, forbid_select, ori_subset)
        if not with_text:
            for i in forbid_select:
                subset.append(i)
            text_dict_list = [full_dict_list[i] for i in forbid_select]
            # print("text subset", text_dict_list)
            hierarchy = mergeOtherCandidate(hierarchy, text_dict_list, shape_dict=shape_dict, img_shape=img_shape, virtual_hang=False)
            getShape(hierarchy)
        # print("subset", subset)

        sub_dict_list = [full_dict_list[i] for i in subset]
        sub_annots = [full_annots[i] for i in subset]
        other_subset = [i for i in range(len(full_annots)) if i not in subset]
        other_dict_list = [full_dict_list[i] for i in other_subset]
        for i in subset:
            item2 = full_annots[i]
            item2["score"] = max(item2["score"], (conf_thres[item2['category_id']-1])/item2['score_scale'])
        for i in other_subset:
            item2 = full_annots[i]
            item2["score"] = min(item2["score"], (conf_thres[item2['category_id']-1]-0.0001)/item2['score_scale'])
        
        # print("other subset", other_dict_list)

    hierarchy = mergeOtherCandidate(hierarchy, other_dict_list, shape_dict=shape_dict, img_shape=img_shape)
    
    tmp = {
        "image": image_pre2 + image_info["file_name"],
        # "image": image_info["file_name"],
        "name": "Item",
        "boxes": [],
        "hierarchy": None,
        "influence_within": None
    }
    for annot in full_annots:
        tmp2 = {"x": annot["bbox"][0], "y": annot["bbox"][1], "width": annot["bbox"][2], "height": annot["bbox"][3]}
        tmp2["score"] = annot['score_scale']*annot["score"]

        category_id = annot["category_id"]

        if category_id in category_dict_super:
            tp = category_dict_super[category_id]
        else:
            tp = "other_" + str(category_id)

        if category_id in category_dict:
            tp2 = category_dict[category_id]
        else:
            tp2 = "other_" + str(category_id)

        tmp2["super_class"] = tp
        tmp2["class"] = tp2

        if annot in sub_annots:
            tmp2["unselected"] = False
        else:
            tmp2["unselected"] = True

        tmp['boxes'].append(tmp2)
    
    def get_hierarchy(obj):
        if len(obj.children)==0:
            return obj.id
        hierarchy_json = {}
        hierarchy_json["deep"] = obj.deep-1
        hierarchy_json["max_deep"] = obj.max_deep-1
        hierarchy_json["x"] = obj.box[0]
        hierarchy_json["y"] = obj.box[1]
        hierarchy_json["width"] = obj.box[2]-obj.box[0]
        hierarchy_json["height"] = obj.box[3]-obj.box[1]
        if hasattr(obj, "box2"):
            hierarchy_json["box2"] = {"x": obj.box2[0], "y": obj.box2[1], "width": obj.box2[2]-obj.box2[0], "height": obj.box2[3]-obj.box2[1]}
        hierarchy_json["children"] = []
        for child in obj.children:
            hierarchy_json["children"].append(get_hierarchy(child))
        return hierarchy_json
    
    if hierarchy is not None and (len(hierarchy.children)>0):
        tmp["hierarchy"] = get_hierarchy(hierarchy)

    tmp["influence_within"] = getInfluenceNaive(tmp['boxes'], image_info)
    
    return tmp

def getInfluenceNaive(boxes, image_info):
    influence_within = []
    for i in range(len(boxes)):
        influence_within.append([])
        for j in range(len(boxes)):
            if i == j:
                continue
            if boxes[i]['class'] != boxes[j]['class']:
                continue
            if abs(boxes[i]['width']-boxes[j]['width']) > max(2, 0.01*boxes[i]['width']):
                continue
            if abs(boxes[i]['height']-boxes[j]['height']) > max(2, 0.01*boxes[i]['height']):
                continue
            influence_within[i].append(j)
    return influence_within


