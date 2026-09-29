import json
import os
import pickle
from data_utils import getCandidate, getHierarchy, updateSubset, mergeCandidateText
from tqdm import tqdm
from scene_tree.grouping import test, getObjDict, getObjContext, getObjHierarchy, getBestSimilarity, getSimilarity
from feature.clip import clip_load_model, clip_model_get_feature
from feature.dreamsim import dreamsim_load_model, dreamsim_model_get_similarity, dreamsim_model_get_feature
import numpy as np
from scipy.stats import percentileofscore
import time
import random
from collections import Counter

content_sim_thres = 0.45
context_sim_thres = 0.33

part_cnt = 10

conf_thres = [0.3]*20  # TO FILL
category_dict_super = {1: "text", 2: "text", 3: "text", 4: "HRO", 5: "HRO", 6: "sub-element", 7: "sub-element", 8: "sub-element", 9: "sub-element",
    10: "chart", 11: "chart", 12: "chart", 13: "chart", 14: "chart", 15: "chart", 16: "chart", 17: "chart", 18: "chart", 19: "chart", 20: "chart"}  # TO FILL upper level class
category_dict = {1: "Annotation", 2: "Title", 3: "Source", 4: "Label-Icon", 5: "Embellishment", 6: "legend", 7: "axis", 8: "gridline", 9: "mark", 
    10: "Bar Chart", 11: "Line Chart", 12: "Radar Chart", 13: "Area Chart", 14: "Pie Chart", 15: "Proportional Chart", 16: "Treemap", 17: "ScatterPlot", 18: "Pyramid & Funnel Chart", 19: "Sankey Diagram", 20: "Heatmap"}  # TO FILL lower level class
image_pre = os.environ.get("ELEDETECTIVE_IMAGE_DIR", "/YOUR/IMAGE/FOLDER/PATH/").rstrip("/") + "/"
similarity_scale_dict = {i: 0.7 for i in range(1, len(category_dict)+1)}

class DataControl:

    def __init__(self, with_text=True, use_prop=True):
        self.data = None
        self.annotations_pred = None
        self.sample_list = None
        self.candidate = None
        self.hierarchy = None
        self.with_text = with_text
        self.prop_text = False
        # self.clip_feature = {}
        self.image_pre = image_pre
        # self.image_pre = 
        self.path = None

        self.use_prop = use_prop

        self.use_hierarchy = True


    def get_hierarchy(self):
        return self.hierarchy


    def get_candidate(self):
        return self.candidate


    def load_data(self, path=None, need_feature=False, need_hierarchy_feature=False, part=-1, model="clip", before_part=False):
        if path is None:
            print("no path")
            return
        self.path = path
        self.model = model

        pred_path = os.path.join(path, "pred.bbox.json")
        info_path = os.path.join(path, "annotations.json")
        if part == -1 or not before_part:
            candidate_ori_path = os.path.join(path, "candidate_ori.pkl")
            candidate_path = os.path.join(path, "candidate.pkl")
            hierarchy_path = os.path.join(path, "hierarchy.json")
        else:
            candidate_ori_path = os.path.join(path, "candidate_ori_"+str(part)+".pkl")
            candidate_path = os.path.join(path, "candidate_"+str(part)+".pkl")
            hierarchy_path = os.path.join(path, "hierarchy_"+str(part)+".json")
        
        with open(info_path, 'r') as file:
            self.sample_list = json.load(file)["images"]
        
        use_mask = True
        print("candidate start")
        if not os.path.exists(candidate_ori_path):
            with open(pred_path, 'r') as file:
                self.annotations_pred = json.load(file)
            if part == -1 or not before_part:
                self.candidate = getCandidate(self.annotations_pred, self.sample_list, candidate_ori_path, use_mask, with_text=self.with_text)
            else:
                ln = len(self.sample_list)
                self.candidate = getCandidate(self.annotations_pred, self.sample_list[int(ln*part/part_cnt):int(ln*(part+1)/part_cnt)], candidate_ori_path, use_mask, with_text=self.with_text)
        else:
            with open(candidate_ori_path, 'rb') as file:
                self.candidate = pickle.load(file)
        print("candidate done")
        
        print("hierarchy start")
        if not os.path.exists(hierarchy_path) or not os.path.exists(candidate_path):
            self.hierarchy = []
            if part == -1 or not before_part:
                for i in tqdm(range(len(self.candidate))):
                    item = self.candidate[i]
                    self.hierarchy.append(getHierarchy(item["annotations"], item["shape_dict"], item["subset"], self.sample_list[i], with_text=self.with_text))
                with open(hierarchy_path, 'w') as file:
                    json.dump(self.hierarchy, file)
                with open(candidate_path, 'wb') as file:
                    pickle.dump(self.candidate, file)
            else:
                ln = len(self.sample_list)
                for i in tqdm(range(len(self.candidate))):
                    item = self.candidate[i]
                    self.hierarchy.append(getHierarchy(item["annotations"], item["shape_dict"], item["subset"], self.sample_list[int(ln*part/part_cnt)+i], with_text=self.with_text))
                with open(hierarchy_path, 'w') as file:
                    json.dump(self.hierarchy, file)
                with open(candidate_path, 'wb') as file:
                    pickle.dump(self.candidate, file)
                return
        else:
            with open(hierarchy_path, 'r') as file:
                self.hierarchy = json.load(file)
            with open(candidate_path, 'rb') as file:
                self.candidate = pickle.load(file)
            # for i in tqdm(range(len(self.candidate))):
            #     if len(self.hierarchy[i]["boxes"])==0:
            #         print(i, self.hierarchy[i])
        print("hierarchy done")


        if need_feature:
            if model == "clip":
                self.get_clip_feature(path, part)
                # ----------------------------------
                self.get_cross_influence(path, part)
                self.get_influence_info(path, part)
            elif model == "dreamsim":
                print("use dreamsim")
                self.get_dreamsim_feature(path, part, convert="L", no_dreamsim=["text", "gridline"])
                # ----------------------------------
                self.get_cross_influence(path, part)
                self.get_influence_info(path, part)

        if need_hierarchy_feature:
            self.get_cross_hierarchy_influence(path, part)
            self.get_hierarchy_influence_info(path, part)


    def get_clip_feature(self, path=None, part=-1):
        folder_path = os.path.join(path, "content")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        now_candidate = self.get_candidate()
        clip_model = clip_load_model()
        folder_path = os.path.join(path, "content/clip_features")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]

        for i in tqdm(rg):
            feature_path = os.path.join(folder_path, str(i)+".pkl")
            if os.path.exists(feature_path):
                continue
            item = now_candidate[i]
            image_info = self.sample_list[i]
            boxes = []
            for item2 in item["annotations"]:
                boxes.append((item2["bbox"][0], item2["bbox"][1], item2["bbox"][0]+item2["bbox"][2], item2["bbox"][1]+item2["bbox"][3]))
            features = clip_model_get_feature(clip_model, os.path.join(self.image_pre, image_info["file_name"]), boxes)
            with open(feature_path, 'wb') as file:
                pickle.dump(features, file)


    def get_dreamsim_feature(self, path=None, part=-1, convert="RGB", no_dreamsim=[]):
        folder_path = os.path.join(path, "content")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        now_candidate = self.get_candidate()
        dreamsim_model = dreamsim_load_model()
        folder_path = os.path.join(path, "content/dreamsim_features")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]

        for i in tqdm(rg):
            feature_path = os.path.join(folder_path, str(i)+".pkl")
            if os.path.exists(feature_path):
                continue
            item = now_candidate[i]
            image_info = self.sample_list[i]
            boxes = []
            for item2 in item["annotations"]:
                if no_dreamsim:
                    if category_dict_super[item2["category_id"]] in no_dreamsim or category_dict[item2["category_id"]] in no_dreamsim:
                        continue
                boxes.append((item2["bbox"][0], item2["bbox"][1], item2["bbox"][0]+item2["bbox"][2], item2["bbox"][1]+item2["bbox"][3]))
            
            if len(boxes) > 0:
                features = dreamsim_model_get_feature(dreamsim_model, os.path.join(self.image_pre, image_info["file_name"]), boxes, convert=convert)
            else:
                features = np.array([])
            
            if no_dreamsim:
                tmp_cnt = 0
                tmp_features = []
                for item2 in item["annotations"]:
                    if category_dict_super[item2["category_id"]] in no_dreamsim or category_dict[item2["category_id"]] in no_dreamsim:
                        tmp_features.append(np.zeros(1792))
                        continue
                    tmp_features.append(features[tmp_cnt])
                    tmp_cnt += 1
                features = np.array(tmp_features)
            
            features = features.reshape((-1, 1792))
            print(features.shape)
            
            with open(feature_path, 'wb') as file:
                pickle.dump(features, file)


    def score_edit(self, id, box, scale):
        pass
        # if self.with_text:
        #     tmp_hierarchy = self.hierarchy
        # else:
        #     tmp_hierarchy = self.hierarchy_without_text

        # if self.candidate is None or tmp_hierarchy is None:
        #     return {}
        # print(id, self.candidate[id])
        # for annot in self.candidate[id]["annotations"]:
        #     if annot["category_id"] == 1:
        #         tmp_class = 'data_element'
        #     elif annot["category_id"] == 2:
        #         tmp_class = 'non-data_element'
        #     elif annot["category_id"] == 3:
        #         tmp_class = 'visual_element'
        #     else:
        #         tmp_class = "text"
        #     if box["class"] != tmp_class:
        #         continue
        #     if((abs(box["width"]-annot["bbox"][2])<max(0.2*box["width"], 0.02*self.sample_list[id]["width"]))and(abs(box["height"]-annot["bbox"][3])<max(0.2*box["height"], 0.02*self.sample_list[id]["height"]))):
        #         annot["score"] *= scale
        
        # updateSubset(self.candidate[id])
        # tmp_hierarchy[id] = getHierarchy(self.candidate[id]["annotations"], self.candidate[id]["shape_dict"], self.candidate[id]["subset"], self.sample_list[id])
        # return {id: tmp_hierarchy[id]}

    
    def apply_edit(self, edit_record, ids):
        if os.path.exists("full_edit_record.json"):
            with open("full_edit_record.json", "r") as file:
                full_edit_record = json.load(file)
        else:
            full_edit_record = []
        
        tmp_record_dict = {}

        result = self.apply_edit_excute(edit_record, ids, save_record=tmp_record_dict)

        full_edit_record.append(tmp_record_dict)

        with open("full_edit_record.json", 'w') as file:
            json.dump(full_edit_record, file)
        with open("new_hierarchy.json", 'w') as file:
            json.dump(self.hierarchy, file)
        with open("new_candidate.pkl", 'wb') as file:
            pickle.dump(self.candidate, file)
        
        return result


    def apply_edit_excute(self, edit_record, ids, save_record=None):
        if not self.use_prop:
            ids = []

        tmp_hierarchy = self.hierarchy

        if self.candidate is None or tmp_hierarchy is None:
            return {}

        updated_sample_id_list = []

        def custom_deepcopy(obj):
            if isinstance(obj, list):
                return [custom_deepcopy(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: custom_deepcopy(value) for key, value in obj.items()}
            else:
                return obj

        new_candidate = {}
        for i in edit_record:
            source_sample_id = int(i)
            new_candidate[source_sample_id] = custom_deepcopy(self.candidate[source_sample_id])
        for target_sample_id in ids:
            new_candidate[target_sample_id] = custom_deepcopy(self.candidate[target_sample_id])

        tmp_cnt = 0
        for i in tqdm(edit_record):
            tmp_cnt += 1
            # if tmp_cnt <= 15:
            #     continue
            record = edit_record[i]
            source_sample_id = int(i)
            if record["now"]==0:
                continue
            
            # print("update: ", i)

            if save_record is not None:
                save_record[i] = record
            
            # _, within_influence = self.get_sample_influence(source_sample_id, ids, return_all=True)
            bids = []
            for update in record["update"][:record["now"]]:
                if "id" in update["operate"]:
                    if update["operate"]["id"] not in bids:
                        bids.append(update["operate"]["id"])
                if "ids" in update["operate"]:
                    for id in update["operate"]["ids"]:
                        if id not in bids:
                            bids.append(id)
            _, within_influence = self.get_sample_influence_bids(source_sample_id, bids, ids, return_all=True, must_hierarchy=True)

            for update in record["update"][:record["now"]]:
                operate = update["operate"]

                if operate["type"] == "single-score":
                    source_bid = operate["id"]

                    source_annot = new_candidate[source_sample_id]["annotations"][source_bid]
                    tmp_change = min(0.2, max(-0.2, source_annot["score"] * (operate["scale"]-1)))
                    old_score = source_annot["score"]
                    new_score = source_annot["score"] + tmp_change
                    source_annot["score"] = max(min(1, new_score), 0)
                    if source_sample_id not in updated_sample_id_list:
                        updated_sample_id_list.append(source_sample_id)
                    print("score change:", old_score, tmp_change)

                    thres = within_influence["thres"]

                    for target_sample_id in ids:
                        for target_bid in within_influence[str(source_bid)][target_sample_id]:
                            if (source_sample_id == target_sample_id) and (source_bid == target_bid):
                                continue

                            if within_influence[str(source_bid)][target_sample_id][target_bid] < thres:
                                continue

                            tmp_ratio = min(0.8, within_influence[str(source_bid)][target_sample_id][target_bid]/(thres*2))
                            target_annot = new_candidate[target_sample_id]["annotations"][target_bid]
                            tmp_change2 = (source_annot["score"] - target_annot["score"]) * tmp_ratio
                            tmp_change2 = max(-abs(tmp_ratio*tmp_change), min(abs(tmp_ratio*tmp_change), tmp_change2))

                            if tmp_change2*(operate["scale"]-1) < 0:
                                continue
                            old_score2 = target_annot["score"]
                            new_score2 = target_annot["score"] + tmp_change2
                            target_annot["score"] = max(min(1, new_score2), 0)

                            if target_sample_id not in updated_sample_id_list:
                                updated_sample_id_list.append(target_sample_id)
                
                elif operate["type"] == "group-score":
                    base_score_dict = {}
                    old_score_dict = {}

                    for source_bid in operate["ids"]:
                        source_annot = new_candidate[source_sample_id]["annotations"][source_bid]
                        tmp_change = min(0.2, max(-0.2, source_annot["score"] * (operate["scale"]-1)))
                        old_score = source_annot["score"]
                        new_score = source_annot["score"] + tmp_change
                        source_annot["score"] = max(min(1, new_score), 0)

                        base_score_dict[source_bid] = source_annot["score"]

                        if source_sample_id not in updated_sample_id_list:
                            updated_sample_id_list.append(source_sample_id)

                    thres = within_influence["thres"]

                    for source_bid in operate["ids"]:
                        for target_sample_id in ids:
                            for target_bid in within_influence[str(source_bid)][target_sample_id]:
                                if (source_sample_id == target_sample_id) and (source_bid == target_bid):
                                    continue
                                
                                if within_influence[str(source_bid)][target_sample_id][target_bid] < thres:
                                    continue

                                target_annot = new_candidate[target_sample_id]["annotations"][target_bid]

                                if (target_sample_id, target_bid) not in old_score_dict:
                                    old_score_dict[(target_sample_id, target_bid)] = target_annot["score"]

                                tmp_ratio = min(0.8, within_influence[str(source_bid)][target_sample_id][target_bid]/(thres*2))
                                tmp_change2 = (base_score_dict[source_bid] - old_score_dict[(target_sample_id, target_bid)]) * tmp_ratio
                                tmp_change2 = max(-abs(tmp_ratio*tmp_change), min(abs(tmp_ratio*tmp_change), tmp_change2))

                                if tmp_change2*(operate["scale"]-1) < 0:
                                    continue
                                old_score2 = old_score_dict[(target_sample_id, target_bid)]
                                new_score2 = old_score2 + tmp_change2
                                
                                if (operate["scale"]-1)>0:
                                    new_score2 = max(new_score2, target_annot["score"])
                                if (operate["scale"]-1)<0:
                                    new_score2 = min(new_score2, target_annot["score"])

                                target_annot["score"] = max(min(1, new_score2), 0)

                                if target_sample_id not in updated_sample_id_list:
                                    updated_sample_id_list.append(target_sample_id)
                                    
                elif operate["type"] == "single-class":
                    source_bid = operate["id"]

                    source_annot = new_candidate[source_sample_id]["annotations"][source_bid]
                    new_class = operate["class"]
                    for cid in category_dict:
                        if category_dict[cid] == new_class:
                            source_annot["category_id"] = cid
                    if source_sample_id not in updated_sample_id_list:
                        updated_sample_id_list.append(source_sample_id)

                    thres = within_influence["thres"]

                    for target_sample_id in ids:
                        for target_bid in within_influence[str(source_bid)][target_sample_id]:
                            if (source_sample_id == target_sample_id) and (source_bid == target_bid):
                                continue

                            target_annot = new_candidate[target_sample_id]["annotations"][target_bid]

                            for cid in category_dict:
                                if category_dict[cid] == new_class:
                                    target_annot["category_id"] = cid

                            if target_sample_id not in updated_sample_id_list:
                                updated_sample_id_list.append(target_sample_id)

                elif operate["type"] == "group-class":
                    for source_bid in operate["ids"]:
                        source_annot = new_candidate[source_sample_id]["annotations"][source_bid]
                        new_class = operate["class"]
                        old_cid = source_annot["category_id"]
                        for cid in category_dict:
                            if category_dict[cid] == new_class:
                                source_annot["category_id"] = cid
                        if source_sample_id not in updated_sample_id_list:
                            updated_sample_id_list.append(source_sample_id)
                        
                        if source_annot["score"] < conf_thres[old_cid-1]:    # 仅使confidence较高的元素修改进行传播
                            continue

                        thres = within_influence["thres"]

                        for target_sample_id in ids:
                            for target_bid in within_influence[str(source_bid)][target_sample_id]:
                                if (source_sample_id == target_sample_id) and (source_bid == target_bid):
                                    continue

                                target_annot = new_candidate[target_sample_id]["annotations"][target_bid]

                                for cid in category_dict:
                                    if category_dict[cid] == new_class:
                                        target_annot["category_id"] = cid

                                if target_sample_id not in updated_sample_id_list:
                                    updated_sample_id_list.append(target_sample_id)
                print("updated len:", len(updated_sample_id_list))

        for sample_id in new_candidate:
            self.candidate[sample_id] = new_candidate[sample_id]

        result = {}
        for sample_id in tqdm(updated_sample_id_list):
            updateSubset(self.candidate[sample_id])
            tmp_hierarchy[sample_id] = getHierarchy(self.candidate[sample_id]["annotations"], self.candidate[sample_id]["shape_dict"], self.candidate[sample_id]["subset"], self.sample_list[sample_id], with_text=self.with_text)
            result[sample_id] = tmp_hierarchy[sample_id]

        return result


    def apply_edit_to_dataset(self):
        if os.path.exists("full_edit_record.json"):
            with open("full_edit_record.json", "r") as file:
                full_edit_record = json.load(file)
        else:
            full_edit_record = []

        ids = np.arange(len(self.hierarchy), dtype='int')

        result = {}

        cnt = 0
        for tmp_record_dict in full_edit_record:
            cnt += len(tmp_record_dict)
        print("cnt", cnt)

        for tmp_record_dict in full_edit_record:
            tmp_result = self.apply_edit_excute(tmp_record_dict, ids)
            result.update(tmp_result)

        with open("full_new_hierarchy.json", 'w') as file:
            json.dump(self.hierarchy, file)
        with open("full_new_candidate.pkl", 'wb') as file:
            pickle.dump(self.candidate, file)
            
        with open("full_new_result.pkl", 'wb') as file:
            pickle.dump(result, file)

        return result


    def apply_edit_to_dataset2(self, save=True):
        if os.path.exists("full_edit_record.json"):
            with open("full_edit_record.json", "r") as file:
                full_edit_record = json.load(file)
        else:
            full_edit_record = []

        ids = np.arange(len(self.hierarchy), dtype='int')

        result = {}

        full_record_dict = {}
        cnt = 0
        for tmp_record_dict in full_edit_record:
            cnt += len(tmp_record_dict)
            for key in tmp_record_dict:
                if key not in full_record_dict:
                    full_record_dict[key] = {"now": 0, "len": 0, "update": []}
                print("cnt:", cnt, "key:", self.sample_list[int(key)]["file_name"])
                full_record_dict[key]["now"] += tmp_record_dict[key]["now"]
                full_record_dict[key]["len"] = full_record_dict[key]["now"]
                full_record_dict[key]["update"] += tmp_record_dict[key]["update"][:tmp_record_dict[key]["now"]]
        print("cnt", cnt)

        tmp_result = self.apply_edit_excute(full_record_dict, ids)
        result.update(tmp_result)

        if save:
            with open("full_new_hierarchy2.json", 'w') as file:
                json.dump(self.hierarchy, file)
            with open("full_new_candidate2.pkl", 'wb') as file:
                pickle.dump(self.candidate, file)
                
            with open("full_new_result2.pkl", 'wb') as file:
                pickle.dump(result, file)

        return result


    def apply_edit_check(self):
        if os.path.exists("full_edit_record.json"):
            with open("full_edit_record.json", "r") as file:
                full_edit_record = json.load(file)
        else:
            full_edit_record = []

        ids = np.arange(len(self.hierarchy), dtype='int')

        result = {}

        full_record_dict = {}
        cnt = 0
        for tmp_record_dict in full_edit_record:
            cnt += len(tmp_record_dict)
            for key in tmp_record_dict:
                if key not in full_record_dict:
                    full_record_dict[key] = {"now": 0, "len": 0, "update": []}
                print("cnt:", cnt, "key:", self.sample_list[int(key)]["file_name"])
                full_record_dict[key]["now"] += tmp_record_dict[key]["now"]
                full_record_dict[key]["len"] = full_record_dict[key]["now"]
                full_record_dict[key]["update"] += tmp_record_dict[key]["update"][:tmp_record_dict[key]["now"]]
        print("cnt", cnt)

        add_image_cnt = 0
        change_image_cnt = 0
        add_cnt = 0
        change_cnt = 0
        for key in full_record_dict:
            add_list = []
            change_list = []
            for i in range(full_record_dict[key]["now"]):
                operate = full_record_dict[key]["update"][i]["operate"]
                if operate["type"] == "single-score":
                    if operate["id"] not in add_list:
                        add_list.append(operate["id"])
                if operate["type"] == "group-score":
                    for id in operate["ids"]:
                        if id not in add_list:
                            add_list.append(id)
                if operate["type"] == "single-class":
                    if operate["id"] not in change_list:
                        change_list.append(operate["id"])
                if operate["type"] == "group-class":
                    for id in operate["ids"]:
                        if id not in change_list:
                            change_list.append(id)
            if len(add_list) > 0:
                add_cnt += len(add_list)
                add_image_cnt += 1
            if len(change_list) > 0:
                change_cnt += len(change_list)
                change_image_cnt += 1

        print("image_cnt", add_image_cnt, change_image_cnt)
        print("cnt", add_cnt, change_cnt)

        return


    def get_cross_influence(self, path=None, part=-1):
        feature_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"features")

        influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        if not os.path.exists(influence_folder_path):
            os.makedirs(influence_folder_path)

        feature_dict = {}
        for i in range(len(self.sample_list)):
            feature_path = os.path.join(feature_folder_path, str(i)+".pkl")
            with open(feature_path, 'rb') as file:
                feature_dict[i] = pickle.load(file)
        
        now_candidate = self.get_candidate()

        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]

        for i in tqdm(rg):
            similarity_scale = []
            for item in now_candidate[i]["annotations"]:
                if item["category_id"] in similarity_scale_dict:
                    similarity_scale.append(similarity_scale_dict[item["category_id"]])
                else:
                    similarity_scale.append(1.0)
            similarity_scale = np.array(similarity_scale)

            influence_path = os.path.join(influence_folder_path, str(i)+".pkl")
            if os.path.exists(influence_path):
                continue
            influence = {}
            feature1 = feature_dict[i]
            for j in random.sample(range(len(self.sample_list)), 100)+[i]:    # 仅取100个计算影响力
                feature2 = feature_dict[j]
                influence[j] = np.dot(feature1, feature2.T)
                influence[j] = influence[j] * similarity_scale[:, np.newaxis]
            
            with open(influence_path, 'wb') as file:
                pickle.dump(influence, file)


    def get_influence_info(self, path, part=-1):
        feature_folder_path = os.path.join(path, "content/"+str(self.model)+"_features")
        influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")

        influence_info_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence_info")
        if not os.path.exists(influence_info_folder_path):
            os.makedirs(influence_info_folder_path)

        ranking = []

        thres = content_sim_thres*1.6
        if self.model == "dreamsim":
            thres = content_sim_thres     
        
        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]
        
        for i in tqdm(rg):
            influence_info_path = os.path.join(influence_info_folder_path, str(i)+".pkl")
            if os.path.exists(influence_info_path):
                with open(influence_info_path, 'rb') as file:
                    influence_info = pickle.load(file)
                box_len = len(influence_info)
            else:
                feature_path = os.path.join(feature_folder_path, str(i)+".pkl")
                with open(feature_path, 'rb') as file:
                    feature = pickle.load(file)
                box_len = len(feature)

                influence_path = os.path.join(influence_folder_path, str(i)+".pkl")
                with open(influence_path, 'rb') as file:
                    influence = pickle.load(file)

                influence_info = []
                for bid in range(box_len):
                    influence_info.append({"full": []})

                for j in influence:
                    cross = influence[j]
                    for bid in range(cross.shape[0]):
                        tmp_ids = np.arange(cross.shape[1], dtype='int')[cross[bid]>thres].tolist()
                        influence_info[bid][j] = tmp_ids
                        influence_info[bid]["full"].extend(tmp_ids)

                with open(influence_info_path, 'wb') as file:
                    pickle.dump(influence_info, file)

            for bid in range(box_len):
                ranking.append(len(influence_info[bid]["full"]))

        ranking.sort()
        with open(os.path.join(influence_info_folder_path, "ranking.pkl"), 'wb') as file:
            pickle.dump(ranking, file)


    def get_sample_influence(self, id, target_ids, return_all=False):
        if not self.use_hierarchy:
            return self.get_sample_content_influence(id, target_ids, return_all)
        else:
            # return self.get_sample_hierarchy_influence(id, target_ids, return_all)
            return self.get_online_hierarchy_influence(id, [], target_ids, return_all)

    def get_sample_influence_bids(self, id, bids, target_ids, return_all=False, must_hierarchy=True):
        if not self.use_hierarchy:
            return None
        else:
            return self.get_online_hierarchy_influence(id, bids, target_ids, return_all, must_hierarchy=must_hierarchy)    

    def get_sample_content_influence(self, id, target_ids, return_all=False):
        start = time.time()

        path = self.path

        thres = content_sim_thres*1.6
        if self.model == "dreamsim":
            thres = content_sim_thres

        influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        influence_info_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence_info")

        with open(os.path.join(influence_info_folder_path, "ranking.pkl"), 'rb') as file:
            ranking = pickle.load(file)

        print("load 1", time.time()-start, len(ranking))

        influence_path = os.path.join(influence_folder_path, str(id)+".pkl")
        with open(influence_path, 'rb') as file:
            influence = pickle.load(file)

        influence_info_path = os.path.join(influence_info_folder_path, str(id)+".pkl")
        with open(influence_info_path, 'rb') as file:
            influence_info = pickle.load(file)

        print("load 2", time.time()-start)

        result_dict = {}
        for bid in range(len(influence_info)):
            result_dict[bid] = {}
            result_dict[bid]["represent"] = {}
            for target_id in target_ids:
                if len(influence_info[bid][target_id])>0:
                    result_dict[bid][str(target_id)] = len(influence_info[bid][target_id])
                    result_dict[bid]["represent"][str(target_id)] = influence_info[bid][target_id][0]
            result_dict[bid]["quantile"] = percentileofscore(ranking, len(influence_info[bid]['full']), kind='mean') / 100

        result_dict2 = {"thres":  thres}

        tmp_ids = target_ids
        if not return_all:
            tmp_ids = [id]

        for bid1 in range(len(influence_info)):
            result_dict2[str(bid1)] = {}
            for now_id in tmp_ids:
                result_dict2[str(bid1)][now_id] = {}
                for bid2 in influence_info[bid1][now_id]:
                    score = influence[now_id][bid1][bid2]
                    result_dict2[str(bid1)][now_id][bid2] = score

        print("finish", time.time()-start)
        
        return result_dict, result_dict2


    def get_cross_hierarchy_influence(self, path=None, part=-1):

        hierarchy_json_list = self.get_hierarchy()
        
        folder_path = os.path.join(path, "hierarchy")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        hierarchy_influence_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence")
        if not os.path.exists(hierarchy_influence_folder_path):
            os.makedirs(hierarchy_influence_folder_path)

        content_influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        content_influence_info_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence_info")

        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]

        for i in tqdm(rg):
            hierarchy_influence_path = os.path.join(hierarchy_influence_folder_path, str(i)+".pkl")
            if os.path.exists(hierarchy_influence_path):
                continue
            
            hierarchy1 = getObjHierarchy(hierarchy_json_list[i]['hierarchy'], hierarchy_json_list[i]['boxes'], with_text=self.prop_text, use_type="super_class")   # use type 使用super_class来判断结构相似性
            obj_dict1 = getObjDict(hierarchy1)
            context_dict1 = {}
            for bid in obj_dict1:
                context_dict1[bid] = getObjContext(obj_dict1[bid])

            content_influence_path = os.path.join(content_influence_folder_path, str(i)+".pkl")
            with open(content_influence_path, 'rb') as file:
                content_influence = pickle.load(file)
            content_influence_info_path = os.path.join(content_influence_info_folder_path, str(i)+".pkl")
            with open(content_influence_info_path, 'rb') as file:
                content_influence_info = pickle.load(file)

            hierarchy_influence = {}

            for bid in range(len(content_influence_info)):
                hierarchy_influence[bid] = {}
            
            print("need to calc:", Counter([hierarchy_json_list[i]['boxes'][bid1]["class"] for bid1 in range(len(content_influence_info))]))
            tmp_list = [context_dict1[bid1] for bid1 in range(len(content_influence_info)) if bid1 in context_dict1]
            print("need to calc:", len(tmp_list), len(Counter(tmp_list)))

            cover_store_source = {}

            for j in tqdm(content_influence):
                store = {}
                cover_store_now = {}

                hierarchy2 = getObjHierarchy(hierarchy_json_list[j]['hierarchy'], hierarchy_json_list[j]['boxes'], with_text=self.prop_text, use_type="super_class") # use type 使用super_class来判断结构相似性
                obj_dict2 = getObjDict(hierarchy2)
                context_dict2 = {}
                for bid2 in obj_dict2:
                    context_dict2[bid2] = getObjContext(obj_dict2[bid2])

                for bid1 in range(len(content_influence_info)):
                    hierarchy_influence[bid1][j] = {}
                    for bid2 in content_influence_info[bid1][j]:
                        if hierarchy_json_list[i]['boxes'][bid1]["class"] != hierarchy_json_list[j]['boxes'][bid2]["class"]:  # 传播的元素类别必须相同
                            continue

                        if bid1 not in obj_dict1:
                            continue
                        if bid2 not in obj_dict2:
                            continue
                        
                        hierarchy_influence[bid1][j][bid2] = getBestSimilarity(obj_dict2[bid2], context_dict1[bid1], obj_dict1[bid1], store=store, cover_store_source=cover_store_source, cover_store_now=cover_store_now)
                        # hierarchy_influence[bid1][j][bid2] = getSimilarity(context_dict2[bid2], obj_dict2[bid2], context_dict1[bid1], obj_dict1[bid1], store=store)
            
            with open(hierarchy_influence_path, 'wb') as file:
                pickle.dump(hierarchy_influence, file)


    def get_hierarchy_influence_info(self, path, part=-1):
        
        hierarchy_json_list = self.get_hierarchy()

        content_influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        hierarchy_influence_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence")

        hierarchy_influence_info_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence_info")
        if not os.path.exists(hierarchy_influence_info_folder_path):
            os.makedirs(hierarchy_influence_info_folder_path)

        ranking = []
        
        thres = content_sim_thres*1.6
        if self.model == "dreamsim":
            thres = content_sim_thres
        thres = thres * context_sim_thres

        rg = list(range(len(self.sample_list)))
        ln = len(self.sample_list)
        if part >= 0:
            rg = rg[int(part*ln/part_cnt):int((part+1)*ln/part_cnt)]

        for i in tqdm(rg):
            hierarchy_influence_info_path = os.path.join(hierarchy_influence_info_folder_path, str(i)+".pkl")
            if os.path.exists(hierarchy_influence_info_path):
                with open(hierarchy_influence_info_path, 'rb') as file:
                    hierarchy_influence_info = pickle.load(file)
            else:
                content_influence_path = os.path.join(content_influence_folder_path, str(i)+".pkl")
                with open(content_influence_path, 'rb') as file:
                    content_influence = pickle.load(file)

                hierarchy_influence_path = os.path.join(hierarchy_influence_folder_path, str(i)+".pkl")
                with open(hierarchy_influence_path, 'rb') as file:
                    hierarchy_influence = pickle.load(file)

                hierarchy_influence_info = {}
                for bid in hierarchy_influence:
                    hierarchy_influence_info[bid] = {"full": []}

                for j in content_influence:
                    for bid1 in hierarchy_influence_info:
                        hierarchy_influence_info[bid1][j] = []
                        for bid2 in hierarchy_influence[bid1][j]:
                            score = hierarchy_influence[bid1][j][bid2] * content_influence[j][bid1][bid2]
                            if score>thres:
                                hierarchy_influence_info[bid1][j].append(bid2)
                        hierarchy_influence_info[bid1]["full"].extend(hierarchy_influence_info[bid1][j])

                with open(hierarchy_influence_info_path, 'wb') as file:
                    pickle.dump(hierarchy_influence_info, file)

            for bid in hierarchy_influence_info:
                if not self.prop_text and hierarchy_json_list[i]['boxes'][bid]["super_class"] == "text":   # text不传播
                    # print("text")
                    continue
                ranking.append(len(hierarchy_influence_info[bid]["full"]))

        ranking.sort()
        with open(os.path.join(hierarchy_influence_info_folder_path, "ranking.pkl"), 'wb') as file:
            pickle.dump(ranking, file)


    def get_sample_hierarchy_influence(self, id, target_ids, return_all=False):
        start = time.time()

        path = self.path

        thres = content_sim_thres*1.6
        if self.model == "dreamsim":
            thres = content_sim_thres
        thres = thres * context_sim_thres

        content_influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        hierarchy_influence_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence")
        
        hierarchy_influence_info_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence_info")

        with open(os.path.join(hierarchy_influence_info_folder_path, "ranking.pkl"), 'rb') as file:
            ranking = pickle.load(file)

        print("load 1", time.time()-start, len(ranking))

        content_influence_path = os.path.join(content_influence_folder_path, str(id)+".pkl")
        with open(content_influence_path, 'rb') as file:
            content_influence = pickle.load(file)

        hierarchy_influence_path = os.path.join(hierarchy_influence_folder_path, str(id)+".pkl")
        with open(hierarchy_influence_path, 'rb') as file:
            hierarchy_influence = pickle.load(file)

        hierarchy_influence_info_path = os.path.join(hierarchy_influence_info_folder_path, str(id)+".pkl")
        with open(hierarchy_influence_info_path, 'rb') as file:
            hierarchy_influence_info = pickle.load(file)

        print("load 2", time.time()-start)

        result_dict = {}
        for bid in hierarchy_influence_info:
            result_dict[bid] = {}
            result_dict[bid]["represent"] = {}
            for target_id in target_ids:
                if len(hierarchy_influence_info[bid][target_id])>0:
                    result_dict[bid][str(target_id)] = len(hierarchy_influence_info[bid][target_id])
                    result_dict[bid]["represent"][str(target_id)] = hierarchy_influence_info[bid][target_id][0]
            result_dict[bid]["quantile"] = percentileofscore(ranking, len(hierarchy_influence_info[bid]['full']), kind='mean') / 100

        result_dict2 = {"thres":  thres}

        tmp_ids = target_ids
        if not return_all:
            tmp_ids = [id]

        for bid1 in hierarchy_influence_info:
            result_dict2[str(bid1)] = {}
            for now_id in tmp_ids:
                result_dict2[str(bid1)][now_id] = {}
                for bid2 in hierarchy_influence_info[bid1][now_id]:
                    score = hierarchy_influence[bid1][now_id][bid2] * content_influence[now_id][bid1][bid2]
                    result_dict2[str(bid1)][now_id][bid2] = score

        print("finish", time.time()-start)
        
        return result_dict, result_dict2


    def get_online_hierarchy_influence(self, id, bids, target_ids, return_all=False, must_hierarchy=True):
        start = time.time()

        path = self.path

        thres1 = content_sim_thres*1.6
        if self.model == "dreamsim":
            thres1 = content_sim_thres
        thres2 = thres1 * context_sim_thres
        
        hierarchy_json_list = self.get_hierarchy()

        if not os.path.exists(os.path.join(path, "online")):
            os.makedirs(os.path.join(path, "online"))
        online_influence_info_folder_path = os.path.join(path, "online/"+str(self.model)+"_"+"influence_info")

        if not os.path.exists(online_influence_info_folder_path):
            os.makedirs(online_influence_info_folder_path)

        online_influence_info_path = os.path.join(online_influence_info_folder_path, str(id)+".pkl")
        if os.path.exists(online_influence_info_path):
            with open(online_influence_info_path, 'rb') as file:
                online_influence_info = pickle.load(file)
        else:
            online_influence_info = {}
            
        # print("load 1", time.time()-start)

        feature_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"features")
        feature_source_path = os.path.join(feature_folder_path, str(id)+".pkl")
        with open(feature_source_path, 'rb') as file:
            feature_source = pickle.load(file)
        
        if bids is None:
            bids = list(range(len(feature_source)))
        
        feature_dict = {}
        content_influence_dict = {}
        if len(bids)>0:
            now_candidate = self.get_candidate()
            similarity_scale = []
            for item in now_candidate[id]["annotations"]:
                if item["category_id"] in similarity_scale_dict:
                    similarity_scale.append(similarity_scale_dict[item["category_id"]])
                else:
                    similarity_scale.append(1.0)
            similarity_scale = np.array(similarity_scale)

            for target_id in target_ids:
                feature_path = os.path.join(feature_folder_path, str(target_id)+".pkl")
                with open(feature_path, 'rb') as file:
                    feature_dict[target_id] = pickle.load(file)
                    content_influence_dict[target_id] = np.zeros((len(feature_source), len(feature_dict[target_id])))
                    tmp_bids = []
                    for bid1 in bids:
                        if bid1 not in online_influence_info or target_id not in online_influence_info[bid1]:
                            tmp_bids.append(bid1)
                    content_influence_dict[target_id][tmp_bids] = np.dot(feature_source[tmp_bids], feature_dict[target_id].T)
                    content_influence_dict[target_id][tmp_bids] = content_influence_dict[target_id][tmp_bids] * similarity_scale[tmp_bids, np.newaxis]
        
        # print("load 2", time.time()-start)
        
        content_influence_folder_path = os.path.join(path, "content/"+str(self.model)+"_"+"influence")
        hierarchy_influence_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence")
        content_influence_path = os.path.join(content_influence_folder_path, str(id)+".pkl")
        with open(content_influence_path, 'rb') as file:
            content_influence = pickle.load(file)
        hierarchy_influence_path = os.path.join(hierarchy_influence_folder_path, str(id)+".pkl")
        with open(hierarchy_influence_path, 'rb') as file:
            hierarchy_influence = pickle.load(file)

        hierarchy_source = getObjHierarchy(hierarchy_json_list[id]['hierarchy'], hierarchy_json_list[id]['boxes'], with_text=self.prop_text, use_type="super_class") # use type 使用super_class来判断结构相似性
        obj_dict_source = getObjDict(hierarchy_source)

        # print("load 3", time.time()-start)
        
        context_dict_source = {}
        for bid1 in bids:
            if bid1 not in obj_dict_source:
                continue
            context_dict_source[bid1] = getObjContext(obj_dict_source[bid1])
        hierarchy_dict = {}
        obj_dict_dict = {}
        context_dict_dict = {}
        
        if len(bids) > 0:
            for i in target_ids:
                hierarchy_dict[i] = getObjHierarchy(hierarchy_json_list[i]['hierarchy'], hierarchy_json_list[i]['boxes'], with_text=self.prop_text, use_type="super_class") # use type 使用super_class来判断结构相似性
                obj_dict_dict[i] = getObjDict(hierarchy_dict[i])
                context_dict_dict[i] = {}
                for bid1 in obj_dict_dict[i]:
                    context_dict_dict[i][bid1] = getObjContext(obj_dict_dict[i][bid1])
        
        # print("load 4", time.time()-start)

        hierarchy_influence_info_folder_path = os.path.join(path, "hierarchy/"+str(self.model)+"_"+"influence_info")
        with open(os.path.join(hierarchy_influence_info_folder_path, "ranking.pkl"), 'rb') as file:
            ranking = pickle.load(file)
        hierarchy_influence_info_path = os.path.join(hierarchy_influence_info_folder_path, str(id)+".pkl")
        with open(hierarchy_influence_info_path, 'rb') as file:
            hierarchy_influence_info = pickle.load(file)
        
        # print("load 5", time.time()-start)

        cover_store_source = {}
        store = {}
        cover_store_now = {}
        
        for bid1 in bids:
            if not bid1 in online_influence_info:
                online_influence_info[bid1] = {}
            
            for target_id in target_ids:
                if not target_id in online_influence_info[bid1]:
                    online_influence_info[bid1][target_id] = {}
                else:
                    continue

                content_influence_now = content_influence_dict[target_id]
                for bid2 in range(len(content_influence_now[bid1])):
                    content_score = content_influence_now[bid1][bid2]

                    show_flag = False
                    
                    # if (id == 9089) and (bid1 == 26) and (target_id in [9591, 2284]):
                    # if (id == 9089) and (bid1 == 26) and (target_id in [2933]):
                    if (id == 9089) and (bid1 == 26) and (target_id in [id]):
                        show_flag = True
                        print("bid2:", bid2, "content score:", content_score)

                    if hierarchy_json_list[id]['boxes'][bid1]["class"] != hierarchy_json_list[target_id]['boxes'][bid2]["class"]:  # 传播的元素类别必须相同
                        continue

                    if content_score < thres1:
                        continue

                    if bid1 not in obj_dict_source:
                        continue
                    if bid2 not in obj_dict_dict[target_id]:
                        continue

                    # if target_id in hierarchy_influence[bid1]:
                    if False:
                        hierarchy_score = hierarchy_influence[bid1][target_id][bid2]
                    else:
                        hierarchy_score = getBestSimilarity(obj_dict_dict[target_id][bid2], context_dict_source[bid1], obj_dict_source[bid1], store=store, cover_store_source=cover_store_source, cover_store_now=cover_store_now, show=show_flag)

                    if show_flag:
                        print("bid2:", bid2, "hierarchy score:", hierarchy_score)

                    hierarchy_flag = True
                    if content_score*hierarchy_score < thres2:
                        hierarchy_flag = False

                    online_influence_info[bid1][target_id][bid2] = {"content_score": content_score, "hierarchy_score": hierarchy_score, "hierarchy_flag": hierarchy_flag}
        
        with open(online_influence_info_path, 'wb') as file:
            pickle.dump(online_influence_info, file)

        # print("done 1", time.time()-start)

        result_dict = {}
        for bid1 in hierarchy_influence_info:
            result_dict[bid1] = {}
            result_dict[bid1]["represent"] = {}
            result_dict[bid1]["quantile"] = percentileofscore(ranking, len(hierarchy_influence_info[bid1]['full']), kind='mean') / 100
            result_dict[bid1]["checked"] = False
            flag = True
            for target_id in target_ids:
                if bid1 not in online_influence_info or target_id not in online_influence_info[bid1]:
                    flag = False
                    break
            if not flag:
                continue
            for target_id in target_ids:
                if not must_hierarchy:
                    tmp_dict = online_influence_info[bid1][target_id]
                else:
                    tmp_dict = {}
                    for bid2 in online_influence_info[bid1][target_id]:
                        item = online_influence_info[bid1][target_id][bid2]
                        if item["hierarchy_flag"]:
                            tmp_dict[bid2] = item
                if len(tmp_dict)>0:
                    result_dict[bid1][str(target_id)] = len(tmp_dict)
                    result_dict[bid1]["represent"][str(target_id)] = list(tmp_dict.keys())[0]
            result_dict[bid1]["checked"] = True

        # print("done 2", time.time()-start)

        result_dict2 = {"thres":  thres2}

        tmp_ids = target_ids
        if not return_all:
            tmp_ids = [id]

        for bid1 in hierarchy_influence_info:
            result_dict2[str(bid1)] = {}
            for now_id in tmp_ids:
                result_dict2[str(bid1)][now_id] = {}
                if bid1 in online_influence_info and now_id in online_influence_info[bid1]:
                    for bid2 in online_influence_info[bid1][now_id]:
                        if must_hierarchy and not online_influence_info[bid1][now_id][bid2]["hierarchy_flag"]:
                            continue
                        score = online_influence_info[bid1][now_id][bid2]["content_score"] * online_influence_info[bid1][now_id][bid2]["hierarchy_score"]
                        result_dict2[str(bid1)][now_id][bid2] = score
                else:
                    if not now_id in hierarchy_influence_info[bid1]:
                        continue
                    for bid2 in hierarchy_influence_info[bid1][now_id]:
                        score = hierarchy_influence[bid1][now_id][bid2] * content_influence[now_id][bid1][bid2]
                        result_dict2[str(bid1)][now_id][bid2] = score

        # print("finish", time.time()-start)
        
        return result_dict, result_dict2

    
    def preprocess_data(self):
        """
        数据处理: 可以根据需要添加处理步骤
        包括但不限于：缺失值填充、标准化等
        """
        if self.data is None:
            print("数据为空，请先加载数据！")
            return
        
        # 1. 缺失值处理：使用列的均值填充
        self.data.fillna(self.data.mean(), inplace=True)
        
        # 2. 数据标准化：对数值列进行标准化
        numeric_cols = self.data.select_dtypes(include=["float64", "int64"]).columns
        scaler = StandardScaler()
        self.data[numeric_cols] = scaler.fit_transform(self.data[numeric_cols])
        
        print("数据预处理完成！")


    def get_data(self):
        """
        返回处理后的数据
        :return: 处理后的数据
        """
        if self.data is None:
            print("数据为空！")
            return None
        return self.data

if __name__ == "__main__":
    import sys
    arg = -1
    args = sys.argv[1:]
    if len(args)>0:
        arg = int(args[0])

    data_control = DataControl(with_text=True)
    data_control.load_data("datasets/infographic", need_feature=True, model="dreamsim", need_hierarchy_feature=True, part=arg, before_part=False)  # TO FILL