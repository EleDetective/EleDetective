<template>
    <!-- <p class="title">Detection VA</p> -->
    <div class="container">
        <GridPanel
            ref="child2"
            :item="selectedItem"
            :selectedItemIndex="selectedItemIndex"
            @item-selected="selectItem"
            @categroy-selected="updateCategory"
            @click-node="clickNode"
            class="panel"
        />
        <ImageEdit
            ref="child1"
            :imageSrc="selectedImage"
            :inputBoxes="selectedBoxes"
            :inputHierarchy="selectedHierarchy"
            :selectedItemIndex="selectedItemIndex"
            :item="selectedItem"
            @hover-box="hoverBox"
            @show-hierarchy-change="showHierarchyChange"
            @categroy-selected="updateCategory"
            @score-edit="scoreEdit"
            @score-edit2="scoreEdit2"
            @class-edit="classEdit"
            @class-edit2="classEdit2"
            class="panel"
        />
    </div>
</template>

<script>

import GridPanel from './components/GridPanel.vue';
import ImageEdit from './components/ImageEdit.vue';

import { ref, watch } from 'vue';
import { mapState, mapActions } from 'vuex';
import axios from 'axios';

export default {
    name: 'App',
    components: {
        GridPanel,
        ImageEdit,
    },
    data: function() {
        return {
            backend_url: "http://YOUR_BACKEND_ADDR:5102",  // TO FILL
            // backend_url: "http://localhost:5000",
            items: null,
            items_len: 0,
            selectedItemIndex: null,
            selectedImage: "",
            selectedBoxes: [],
            selectedItem: {},
            selectedHierarchy: null,
            selectedInfluence: {},
            selectedWithinInfluence: {},
            quantiles: {},
            timer: null,
            tmp_edit_record: {},
            new_boxes_record: {},
            wait_cnt: 0,
            can_undo: false,
            can_redo: false,
            can_apply: false,
            categories_super: [  // TO FILL
                { text: "Text", color: "rgb(169, 129, 188)", show: false},
                { text: "HRO", color: "rgb(134, 204, 70)", show: true},
                { text: "Mark & Ref", color: "rgb(224, 102, 20)", show: true},
                { text: "Chart", color: "rgb(40, 176, 231)", show: true},
            ],
            categories_super2: [  // TO FILL
                { text: "Text", color: "rgb(199, 133, 252)"},
                { text: "HRO", color: "rgb(175, 237, 12)"},
                { text: "Mark & Ref", color: "rgb(237, 129, 56)"},
                { text: "Chart", color: "rgb(100, 220, 255)"},
            ],
            categories: [  // TO FILL
                { super: "Text", text: "Annotation", name: "Annotation", color: "rgb(169, 129, 188)", thres: 0.3 },
                { super: "Text", text: "Title", name: "Title", color: "rgb(169, 129, 188)", thres: 0.3 },
                { super: "Text", text: "Source", name: "Source", color: "rgb(169, 129, 188)", thres: 0.3 },
                { super: "HRO", text: "Data-relevant HRO", name: "Label-Icon", color: "rgb(134, 204, 70)", thres: 0.3 },
                { super: "HRO", text: "Data-irrelevant HRO", name: "Embellishment", color: "rgb(134, 204, 70)", thres: 0.3 },
                { super: "Mark & Ref", text: "Legend", name: "legend", color: "rgb(224, 102, 20)", thres: 0.3 },
                { super: "Mark & Ref", text: "Axis", name: "axis", color: "rgb(224, 102, 20)", thres: 0.3 },
                { super: "Mark & Ref", text: "Gridline", name: "gridline", color: "rgb(224, 102, 20)", thres: 0.3 },
                { super: "Mark & Ref", text: "Mark", name: "mark", color: "rgb(224, 102, 20)", thres: 0.3 },
                { super: "Chart", text: "Bar Chart", name: "Bar Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Line Chart", name: "Line Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Radar Chart", name: "Radar Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Area Chart", name: "Area Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Pie Chart", name: "Pie Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Proportional Chart", name: "Proportional Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Treemap", name: "Treemap", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "ScatterPlot", name: "ScatterPlot", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Pyramid & Funnel Chart", name: "Pyramid & Funnel Chart", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Sankey Diagram", name: "Sankey Diagram", color: "rgb(40, 176, 231)", thres: 0.3 },
                { super: "Chart", text: "Heatmap", name: "Heatmap", color: "rgb(40, 176, 231)", thres: 0.3 },
            ],
            categories2: [  // TO FILL
                { super: "Text", text: "Annotation", name: "Annotation", color: "rgb(199, 133, 252)", thres: 0.3 },
                { super: "Text", text: "Title", name: "Title", color: "rgb(199, 133, 252)", thres: 0.3 },
                { super: "Text", text: "Source", name: "Source", color: "rgb(199, 133, 252)", thres: 0.3 },
                { super: "HRO", text: "Data-relevant HRO", name: "Label-Icon", color: "rgb(175, 237, 12)", thres: 0.3 },
                { super: "HRO", text: "Data-irrelevant HRO", name: "Embellishment", color: "rgb(175, 237, 12)", thres: 0.3 },
                { super: "Mark & Ref", text: "Legend", name: "legend", color: "rgb(237, 129, 56)", thres: 0.3 },
                { super: "Mark & Ref", text: "Axis", name: "axis", color: "rgb(237, 129, 56)", thres: 0.3 },
                { super: "Mark & Ref", text: "Gridline", name: "gridline", color: "rgb(237, 129, 56)", thres: 0.3 },
                { super: "Mark & Ref", text: "Mark", name: "mark", color: "rgb(237, 129, 56)", thres: 0.3 },
                { super: "Chart", text: "Bar Chart", name: "Bar Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Line Chart", name: "Line Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Radar Chart", name: "Radar Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Area Chart", name: "Area Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Pie Chart", name: "Pie Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Proportional Chart", name: "Proportional Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Treemap", name: "Treemap", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "ScatterPlot", name: "ScatterPlot", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Pyramid & Funnel Chart", name: "Pyramid & Funnel Chart", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Sankey Diagram", name: "Sankey Diagram", color: "rgb(100, 220, 255)", thres: 0.3 },
                { super: "Chart", text: "Heatmap", name: "Heatmap", color: "rgb(100, 220, 255)", thres: 0.3 },
            ],
        };
    },
    mounted() {
        // 从 Flask 后端获取数据
        console.log("APP mounted");
        // if(this.items == null) {
        //     console.log("APP fetch");
        //     this.fetchData();
        // }

        // axios.get(this.backend_url+'/api/data')
        //     .then(response => {
        //         this.message = response.data.message;
        //         this.items = response.data.data;
        //         console.log(this.message, this.items);
        //         this.selectItem(4);
        //     })
        //     .catch(error => {
        //         console.error("Error fetching data:", error);
        //     });

        // this.$refs.child1.test();
        // this.$refs.child2.child_test();
    },
    watch: {
        wait_cnt: function(wait_cnt) {
            if(wait_cnt == 2) {
                console.log("tmp_edit_record", this.tmp_edit_record);
                if(this.selectedItemIndex in this.tmp_edit_record) {
                    let update_dict = this.$refs.child1.$refs.child_tree.restoreEdit(this.tmp_edit_record[this.selectedItemIndex]);
                    this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
                }
                this.update_button_able();
            }
        }
    },
    methods: {
        ...mapActions(['addOnLoadingFlag', 'decOnLoadingFlag']),
        checkCrossInfluencePre: function(bid) {
            let that = this;
            that.prop_bid = bid;
            that.$refs.child2.$refs.child_grid.can_prop = false;
            if(bid>=0)that.$refs.child2.$refs.child_grid.can_prop = true;
        },
        checkCrossInfluenceExcute: function(hide=false) {
            // this.checkCrossInfluenceExcute2(hide);

            this.$refs.child2.$refs.child_grid.addGridLoadingFlag();
            if((!hide)&&(!this.selectedInfluence[this.prop_bid]["checked"])) {
                axios.post(this.backend_url+'/api/get_sample_influence_bids', {
                    id: this.selectedItemIndex,
                    target_ids: this.$refs.child2.$refs.child_grid.gridlayout.sample_ids,
                    bids: [this.prop_bid],
                })
                .then(response => {
                    console.log("Sample Influence Bids Back:", response.data);
                    for(let bid of [this.prop_bid]) {
                        this.selectedInfluence[bid] = response.data["sample_influence"][bid];
                    }
                    this.checkCrossInfluenceExcute2(hide);
                    this.$refs.child2.$refs.child_grid.decGridLoadingFlag();
                })
                .catch(error => {
                    console.error("Error sending data:", error);
                });
            } else {
                this.checkCrossInfluenceExcute2(hide);
                this.$refs.child2.$refs.child_grid.decGridLoadingFlag();
            }
        },
        checkCrossInfluenceExcute2: function(hide=false) {
            let that = this;
            let influenceDict = {};
            let representDict = {};
            if(!hide) {
                if(that.prop_bid in that.selectedInfluence) {
                    influenceDict = that.selectedInfluence[that.prop_bid];
                    representDict = that.selectedInfluence[that.prop_bid]['represent'];
                }
            }
            // console.log("?", influenceDict, representDict);
            that.$refs.child2.$refs.child_grid.checkCrossInfluence(influenceDict, representDict);
        },
        checkCrossInfluence: function(id) {
            let that = this;
            if(that.timer != null) {
                clearTimeout(that.timer);
                that.timer = null;
            }
            that.timer = setTimeout(() => {
                let influenceDict = {};
                let representDict = {};
                if(id in that.selectedInfluence) {
                    influenceDict = that.selectedInfluence[id];
                    representDict = that.selectedInfluence[id]['represent'];
                    // console.log("?", that.selectedInfluence[id], that.selectedInfluence[id]['represent']);
                    // console.log("?", influenceDict, representDict);
                }
                // console.log("?", influenceDict, representDict);
                that.$refs.child2.$refs.child_grid.checkCrossInfluence(influenceDict, representDict);
            }, 2*600);
        },
        newEdit: function(update_dict, operate) {
            if(!(this.selectedItemIndex in this.tmp_edit_record)) {
                this.tmp_edit_record[this.selectedItemIndex] = {"now": 0, "len": 0, "update": []}
            }
            let record = this.tmp_edit_record[this.selectedItemIndex];
            record["len"] = record["now"]
            record["update"] = record["update"].slice(0, record["len"]);
            record["len"] += 1;
            record["update"].push({"update_dict": update_dict, "operate": operate})
            record["now"] = record["len"];
        },
        undoEdit: function() {
            if(!(this.selectedItemIndex in this.tmp_edit_record)) {
                this.tmp_edit_record[this.selectedItemIndex] = {"now": 0, "len": 0, "update": []}
            }
            let record = this.tmp_edit_record[this.selectedItemIndex];
            if(record["now"] <= 0) return null;
            record["now"] = Math.max(0, record["now"]-1);
            return record["update"][record["now"]];
        },
        redoEdit: function() {
            if(!(this.selectedItemIndex in this.tmp_edit_record)) {
                this.tmp_edit_record[this.selectedItemIndex] = {"now": 0, "len": 0, "update": []}
            }
            let record = this.tmp_edit_record[this.selectedItemIndex];
            if(record["now"] >= record["len"]) return null;
            record["now"] = Math.min(record["len"], record["now"]+1);
            return record["update"][record["now"]-1];
        },
        cancelEdit: function() {
            if(!(this.selectedItemIndex in this.tmp_edit_record)) {
                this.tmp_edit_record[this.selectedItemIndex] = {"now": 0, "len": 0, "update": []}
            }
            let record = this.tmp_edit_record[this.selectedItemIndex];
            if(record["now"] <= 0) return null;
            record["now"] = 0;
            return record["update"][record["now"]];
        },
        selectItem: function(index) {
            // console.log(index, items.value);

            console.log("get sample influence");
            
            axios.post(this.backend_url+'/api/get_sample_influence', {
                id: index,
                target_ids: this.$refs.child2.$refs.child_grid.gridlayout.sample_ids
            })
            .then(response => {
                console.log("Sample Influence Back:", response.data);
                this.checkCrossInfluencePre(-1);
                this.$refs.child2.$refs.child_grid.prop_showed = false;

                this.selectedInfluence = response.data["sample_influence"];
                this.selectedWithinInfluence = response.data["within_influence"];

                this.wait_cnt = 0;
                this.can_undo = false;
                this.can_redo = false;
                this.can_apply = false;

                this.selectedItemIndex = index;
                this.selectedImage = this.items[index].image;
                this.selectedBoxes = this.items[index].boxes;
                this.selectedHierarchy = this.items[index].hierarchy;
                this.selectedItem = this.items[index];
                // console.log(this.selectedItem, this.selectedItemIndex);


                // this.items[index].boxes = [
                //     {"x": 0, "y": 0, "width": 100, "height": 40, "score": 0.6, "class": "data_element", "unselected": false}, 
                //     {"x": 0, "y": 0, "width": 10, "height": 10, "score": 0.28, "class": "visual_element", "unselected": true}, 
                //     {"x": 0, "y": 0, "width": 10, "height": 32, "score": 0.47, "class": "visual_element", "unselected": false}, 
                //     {"x": 100, "y": 0, "width": 100, "height": 40, "score": 0.62, "class": "data_element", "unselected": false}, 
                //     {"x": 100, "y": 0, "width": 10, "height": 10, "score": 0.35, "class": "visual_element", "unselected": false}, 
                //     {"x": 100, "y": 0, "width": 10, "height": 10, "score": 0.2999, "class": "visual_element", "unselected": true}, 
                //     {"x": 100, "y": 0, "width": 10, "height": 32, "score": 0.48, "class": "visual_element", "unselected": false}
                // ];
                // this.items[index].hierarchy = {
                //     "deep": 2, "max_deep": 2, "x": 0, "y": 0, "width": 200, "height": 40, "box2": {"x": 0, "y": 0, "width": 200, "height": 40}, "children": [
                //         { "deep": 1, "max_deep": 1, "x": 0, "y": 0, "width": 100, "height": 40, "box2": {"x": 0, "y": 0, "width": 100, "height": 40}, "children": [0, 1, 2] }, 
                //         { "deep": 1, "max_deep": 1, "x": 100, "y": 0, "width": 100, "height": 40, "box2": {"x": 100, "y": 0, "width": 100, "height": 40}, "children": [3, 4, 5, 6] }
                //     ]
                // }
                // this.selectedBoxes = this.items[index].boxes;
                // this.selectedHierarchy = this.items[index].hierarchy;

            })
            .catch(error => {
                console.error("Error sending data:", error);
            });
        },
        update_button_able: function() {
            if(this.selectedItemIndex in this.tmp_edit_record) {
                this.can_undo = (this.tmp_edit_record[this.selectedItemIndex]["now"] > 0);
                this.can_redo = (this.tmp_edit_record[this.selectedItemIndex]["now"] < this.tmp_edit_record[this.selectedItemIndex]["len"]);
            }
            this.can_apply = false;
            for(let key in this.tmp_edit_record) {
                if(this.tmp_edit_record[key]["now"] > 0) {
                    this.can_apply = true;
                    break;
                }
            }
        },
        scoreTmpEdit: function(id, scale) {
            let update_dict = this.$refs.child1.$refs.child_tree.scoreTmpEdit(id, scale);
            this.newEdit(update_dict, {"type": "single-score", "id": id, "scale": scale});
            this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
            this.update_button_able();
        },
        scoreTmpEdit2: function(ids, scale) {
            let update_dict = this.$refs.child1.$refs.child_tree.scoreTmpEdit2(ids, scale);
            this.newEdit(update_dict, {"type": "group-score", "ids": ids, "scale": scale});
            this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
            this.update_button_able();
        },
        classTmpEdit: function(id, cls) {
            let update_dict = this.$refs.child1.$refs.child_tree.classTmpEdit(id, cls);
            this.newEdit(update_dict, {"type": "single-class", "id": id, "class": cls});
            this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
            this.update_button_able();
        },
        classTmpEdit2: function(ids, cls) {
            if(cls == "group") return;
            let update_dict = this.$refs.child1.$refs.child_tree.classTmpEdit2(ids, cls);
            this.newEdit(update_dict, {"type": "group-class", "ids": ids, "class": cls});
            this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
            this.update_button_able();
        },
        buttonApply: function() {
            this.applyEdit(this.tmp_edit_record, this.$refs.child2.$refs.child_grid.gridlayout.sample_ids);
            // this.applyEdit(this.tmp_edit_record, [this.selectedItemIndex]);
        },
        buttonUndo: function() {
            let tmp_result = this.undoEdit();
            if(tmp_result == null) return;
            let update_dict = tmp_result["update_dict"];
            // console.log("undo", update_dict);
            this.$refs.child1.$refs.child_tree.stepEdit(update_dict, "old_score", "old_class");
            this.$refs.child1.tmpEdit(update_dict, "old_score", "old_class");
            this.update_button_able();
        },
        buttonRedo: function() {
            let tmp_result = this.redoEdit();
            if(tmp_result == null) return;
            let update_dict = tmp_result["update_dict"];
            // console.log("redo", update_dict);
            this.$refs.child1.$refs.child_tree.stepEdit(update_dict, "new_score", "new_class");
            this.$refs.child1.tmpEdit(update_dict, "new_score", "new_class");
            this.update_button_able();
        },
        buttonCancel: function() {
            let tmp_result = this.cancelEdit();
            if(tmp_result == null) return;
            let update_dict = tmp_result["update_dict"];
            // console.log("cancel", update_dict);
            this.$refs.child1.$refs.child_tree.stepEdit(update_dict, "old_score", "old_class");
            this.$refs.child1.tmpEdit(update_dict, "old_score", "old_class");
            this.update_button_able();
        },
        scoreEdit: function(id, scale) {
            console.log("Score Edit:", id, scale, this.selectedItemIndex);

            this.scoreTmpEdit(id, scale);
        },
        scoreEdit2: function(ids, scale) {
            console.log("Score Edit2:", ids, scale, this.selectedItemIndex);

            this.scoreTmpEdit2(ids, scale);
        },
        classEdit: function(id, cls) {
            console.log("Class Edit:", id, cls, this.selectedItemIndex);

            this.classTmpEdit(id, cls);
        },
        classEdit2: function(ids, cls) {
            console.log("Class Edit2:", ids, cls, this.selectedItemIndex);

            this.classTmpEdit2(ids, cls);
        },
        applyEdit: function(edit_record, ids) {
            let that = this;

            console.log("Apply Edit:", edit_record, ids);

            axios.post(that.backend_url+'/api/apply_edit', {
                userMessage: "Hello from Vue!",
                edit_record,
                ids,
            })
            .then(response => {
                console.log("Edit Back:", response.data);
                for(let id in response.data["updated"]) {
                    if(id in that.tmp_edit_record)
                        that.tmp_edit_record[id] = {"now": 0, "len": 0, "update": []};
                    that.items[id] = response.data["updated"][id];
                }
                that.selectItem(that.selectedItemIndex);
                that.$refs.child2.update_detections(null);
            })
            .catch(error => {
                console.error("Error sending data:", error);
            });
        },
        getQuantiles: function() {
            function getAvgConfidence(boxes, without_text=false) {
                if(boxes.length==0)return 0;
                let a = 0;
                let a2 = 0;
                for(let box of boxes){
                    if((without_text)&&(box.class == "text")) continue;
                    a += box.score;
                    a2 += 1;
                }
                if(a2==0)return 0;
                return a/a2;
            }
            function getClassAvgConfidence(boxes) {
                if(boxes.length==0)return 0;
                let a = {};
                for(let box of boxes){
                    if(!(box.class in a))a[box.class] = [0, 0];
                    a[box.class][0] += box.score;
                    a[box.class][1] += 1;
                }
                let b = 0;
                let c = 0;
                for(let key in a) {
                    b += a[key][0]/a[key][1];
                    c += 1;
                }
                return b/c;
            }

            function calculatePercentile(sortedData, percentile) {
                const length = sortedData.length;
                const index = percentile * (length - 1);
                const lowerIndex = Math.floor(index);
                const upperIndex = Math.ceil(index);
            
                // console.log("percentile", lowerIndex, upperIndex, percentile);
                if (lowerIndex === upperIndex) {
                    return sortedData[lowerIndex];
                }
            
                const lowerValue = sortedData[lowerIndex];
                const upperValue = sortedData[upperIndex];
                const weight = index - lowerIndex;
                return lowerValue + (upperValue - lowerValue) * weight;
            }
            this.quantiles = [];
            let tmp_data = [];

            for(let key in this.items) {
                let item = this.items[key];
                // tmp_data.push(item.boxes.length);
                // tmp_data.push(getAvgConfidence(item.boxes));
                tmp_data.push(getAvgConfidence(item.boxes, true));
                // tmp_data.push(getClassAvgConfidence(item.boxes));
            }

            tmp_data = tmp_data.slice().sort((a, b) => a - b);
            // console.log("tmp_data", tmp_data);

            // for(let key of [0.225, 0.45, 0.675, 0.9]) {
            //     this.quantiles[key] = Math.round(calculatePercentile(tmp_data, key));
            // }
            for(let key of [0.1, 0.325, 0.55, 0.875]) {
                this.quantiles.push({"key": key, "value": calculatePercentile(tmp_data, key)});
            }
            console.log("tmp_data", tmp_data);
            console.log("quantiles", this.quantiles);
        },
        fetchData: function() {
            let that = this;
            that.addOnLoadingFlag();
            console.log("fetch data");
            return axios.get(`${this.backend_url}/api/data`)
                .then(response => {
                    that.decOnLoadingFlag();
                    this.message = response.data.message;
                    this.items = response.data.data;
                    this.items_len = this.items.length;
                    this.getQuantiles();
                    // console.log(this.message, this.items);
                    // this.selectItem(4);
                    return response;
                })
                .catch(error => {
                    that.decOnLoadingFlag();
                    console.error("Error fetching data:", error);
                    throw error;
                });
        },
        fetchDataIds: function(ids) {
            let that = this;
            that.addOnLoadingFlag();
            console.log("fetch data");
            if(that.selectedInfluence != null) {
                for(let key in that.selectedInfluence) {
                    that.selectedInfluence[key]["checked"] = false;
                }
            }
            return axios.post(`${this.backend_url}/api/data_ids`, {ids})
                .then(response => {
                    that.decOnLoadingFlag();
                    this.message = response.data.message;
                    if(this.items == null)this.items = {};
                    for(let key in response.data.data) {
                        this.items[key] = response.data.data[key];
                    }
                    this.items_len = response.data.tot;
                    this.getQuantiles();
                    // console.log(this.message, this.items);
                    // this.selectItem(4);
                    return response;
                })
                .catch(error => {
                    that.decOnLoadingFlag();
                    console.error("Error fetching data:", error);
                    throw error;
                });
        },
        updateCategory: function() {
            console.log('updated', this.selectedItemIndex, this.items[this.selectedItemIndex]);
            // console.log('grid_child', this.$refs.child2, this.selectedItemIndex);
            this.$refs.child2.update_detections(this.selectedItemIndex, this.items[this.selectedItemIndex]);
            axios.post(this.backend_url+'/api/send', {
                userMessage: "Hello from Vue!",
                data: this.items,
            })
            .then(response => {
                console.log("Data sent to backend:", response.data);
            })
            .catch(error => {
                console.error("Error sending data:", error);
            });
        },
        clickNode: function(id) {
            this.$refs.child1.setHover(id);
        },
        hoverBox: function(id) {
            this.$refs.child2.setClick(id);
        },
        showHierarchyChange: function(show) {
            this.$refs.child2.setShowHierarchy(show);
        }
    }
}
</script>

<style>
html, body, #app {
    width: 100%;
    height: 100%;
    margin: 0 0 0 0;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    line-height: 1.42857143;
    color: #333333;
    background: linear-gradient(180deg, #D8E8F8 0%, #EBEFF8 100%);
    /*background-color: #fff;*/
}

.panel {
    display: inline-block;
    vertical-align: top;
    /* background-color: rgb(244, 244, 244); */
    /* background-color: rgb(237, 242, 254); */
    height: calc(100% - 20px);
    position: relative;
    /* border-left: 1px solid #ddd;
    border-right: 1px solid #ddd; */
    margin: 10px;
    /* border-radius: 20px; */
    /* box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.3);  */
    text-align: left;
}

.container {
    width: 100%;
    height: 100%;
}

.title {
    color: white;
    background-color: rgb(84, 84, 84);
    font-weight: bold;
    font-size: 36px;
    border-bottom: 1.5px solid #ddd;
    height: 5%;
    text-align: left;
    padding-left: 36px;
}

.sub-title {
    color: rgb(204, 204, 204);
    /*background-color: rgb(180, 206, 250);*/
    background-color: rgba(255, 255, 255, 0.5);
    /*background-color: rgba(157, 198, 238, 0.5);*/
    font-weight: bold;
    font-size: 28px;
    line-height: 28px;
    /* border-bottom: 1px solid #ddd; */
    text-align: left;
    padding-left: 10px;
    padding-right: 10px;
    /*padding-top: 25px;*/
    padding-top: 12.5px;
    padding-bottom: 12.5px;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    display: inline-block;
}

.sub-sub-title {
    display: none;
    color: rgb(204, 204, 204);
    background-color: rgb(210, 226, 252);
    font-weight: bold;
    font-size: 20px;
    border-bottom: 1px solid #ddd;
    text-align: left;
    padding-left: 20px;
    border-radius: 8px;
}

.buttons {
    position: absolute;
    right: 16px;
    top: 2px;
    transition: opacity 0.5s ease;
    opacity: 1;
    display: flex;
}

.buttons.hidden {
    opacity: 1;
}

.grid-top-legend {
    position: absolute;
    top: 2px;
    transition: opacity 0.5s ease;
    opacity: 1;
    display: flex;
}

.button {
    position: static;
    cursor: pointer;
    overflow: hidden;
    margin-bottom: 20px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    vertical-align: middle;
    color: #fff;
    z-index: 1;
    width: 30px;
    height: 30px;
    line-height: 30px;
    padding: 0;
    background-color: #9e9e9e;
    border-radius: 50%;
    box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),
        0 3px 1px -2px rgba(0, 0, 0, 0.12), 0 1px 5px 0 rgba(0, 0, 0, 0.2);
}

.small-button {
    position: static;
    cursor: pointer;
    overflow: hidden;
    /* margin-bottom: 20px; */
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    vertical-align: middle;
    color: #fff;
    z-index: 1;
    width: 24px;
    height: 24px;
    line-height: 24px;
    padding: 0;
    background-color: #9e9e9e;
    /*background-color: rgb(120, 159, 226);*/
    border-radius: 50%;
    /*box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),*/
    /*    0 3px 1px -2px rgba(0, 0, 0, 0.12), 0 1px 5px 0 rgba(0, 0, 0, 0.2);*/
}

.gap {
    width: 5px;
}

.left-panel {
    width: 70%;
}

.canvas-panel {
    width: 70%;
}

.ImageEdit {
    width: calc(64% - 15px);
    margin-left: 5px;
}

.grid-panel {
    width: calc(36% - 15px);
    margin-right: 5px;
}

.drag-cursor {
    cursor: grab;
}

.drag-cursor:active {
    cursor: grabbing;
}

.magnifier-cursor {
    cursor: zoom-in;
}

.shrink-cursor {
    cursor: zoom-out;
}

.my-loading {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: gray;
    opacity: 0.4;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 998;
}

.my-loading-svg {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 999;
}

.circle-path {
  transform: translate(15px,15px);
/*   transform-origin: center; */
  animation: rotate_arrow 2s infinite;
}

@keyframes rotate_arrow {
  from {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    99.999% {
        -webkit-transform: rotate(359deg);
        transform: rotate(359deg);
    }
    to {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
}
</style>