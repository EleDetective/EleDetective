<template>
    <div class="TreeFlex" @mouseenter="showButton" @mouseleave="hideButton">
        <div style="position: relative;" >
            <p class="sub-sub-title" style="color: #4e4e4e;">Scene Tree</p>
            <div id='tree_buttons' class='buttons' style='top: 0px; right: 0px'>
                <!-- <div class="sector_switch">
                    <el-switch
                        v-model="isShowInfluence"
                        active-text="influence"
                        inactive-text="score"
                        @change="showSectorChange"
                        style="height: 20px;"
                        >
                    </el-switch>
                </div> -->

                <!-- <div id='tree_no_drag' title='No Drag' @click='buttonChangeDrag' v-ripple class='small-button' v-show="no_drag">
                    <svg class='icon' width='18px' height='18px' transform='translate(0, 3)' viewBox='0 0 1024 1024'>
                        <path d="M543.232 613.814857l-0.219429 121.124572h-0.073142l-0.512 169.472 110.006857-110.006858 44.617143 44.617143L512 1024l-185.051429-185.051429 44.909715-44.836571 107.373714 107.373714 0.585143-166.546285 0.073143-57.782858 63.341714-63.341714z m295.789714-286.793143L1024 512l-185.051429 185.051429-44.836571-44.909715 107.373714-107.373714-288.329143-0.877714 63.049143-63.049143 228.205715 0.731428-110.006858-110.006857 44.617143-44.617143z m-654.043428 0l44.909714 44.836572-107.373714 107.373714 166.546285 0.585143 98.377143 0.219428-63.049143 62.976h-35.328v-0.073142l-169.472-0.512L222.281143 645.12l-44.544 44.617143L0 512l185.051429-185.051429z m358.838857 79.36l-0.146286 74.093715 50.029714 0.146285-113.664 113.664 0.219429-50.761143-73.362286-0.219428 63.049143-63.049143h10.532572l-0.073143-10.459429 63.414857-63.414857zM512 0l177.737143 177.737143-44.909714 44.836571-100.059429-100.059428-0.658286 200.850285-63.414857 63.414858 0.877714-267.190858L371.565714 229.595429l-44.617143-44.617143L512 0z" fill="white"></path><path d="M877.120591 73.082483m31.031886 31.031886l0 0q31.031886 31.031886 0 62.063773l-765.453192 765.453192q-31.031886 31.031886-62.063773 0l0 0q-31.031886-31.031886 0-62.063772l765.453192-765.453193q31.031886-31.031886 62.063773 0Z" fill="white"></path>
                    </svg>
                </div>
                <div id='tree_drag' title='Drag' @click='buttonChangeDrag' v-ripple class='small-button' v-show="!no_drag">
                    <svg class='icon' width='18px' height='18px' transform='translate(0, 3)' viewBox='0 0 1024 1024'>
                        <path d="M236.8 620.8c12.8 12.8 12.8 25.6 0 38.4-6.4 6.4-25.6 12.8-32 0h-6.4l-128-128V512H64V492.8l128-128c12.8-12.8 25.6-12.8 38.4 0 6.4 6.4 12.8 25.6 0 32v6.4L153.6 486.4h332.8V153.6L403.2 236.8c-12.8 12.8-25.6 12.8-38.4 0-6.4-6.4-12.8-25.6 0-32v-6.4l128-128h12.8L512 64H531.2l128 128c12.8 12.8 12.8 25.6 0 38.4-6.4 6.4-25.6 12.8-32 0h-6.4L537.6 153.6v332.8h332.8l-83.2-83.2c-12.8-12.8-12.8-25.6 0-38.4 6.4-6.4 25.6-12.8 32 0h6.4l128 128V512h6.4V531.2l-128 128c-12.8 12.8-25.6 12.8-38.4 0-6.4-6.4-12.8-25.6 0-32v-6.4l83.2-83.2H537.6v332.8l83.2-83.2c12.8-12.8 25.6-12.8 38.4 0 6.4 6.4 12.8 25.6 0 32v6.4l-128 128H512v6.4H492.8l-128-128c-12.8-12.8-12.8-25.6 0-38.4 6.4-6.4 25.6-12.8 32 0h6.4l83.2 83.2V537.6H153.6l83.2 83.2z" fill="white" p-id="10244"></path>
                    </svg>
                </div>
                <div class='gap'></div>
                <div id='tree_zoom_in' title='Zoom in' @click='buttonZoomIn' v-ripple class='small-button'>
                    <svg class='icon' width='18px' height='18px' transform='translate(0, 3)' viewBox='0 0 1024 1024'>
                        <path d="M754.2 151.5h-89.5v42.7h89.5c59.5 0 108 48.4 108 108v67.6h42.7v-67.6c0-83.1-67.6-150.7-150.7-150.7zM862.2 737.3c0 59.5-48.4 108-108 108h-89.5V888h89.5c83.1 0 150.7-67.6 150.7-150.7v-67.6h-42.7v67.6zM166.3 737.8v-67.6h-42.7v67.6c0 83.1 67.6 150.7 150.7 150.7h89.5v-42.7h-89.5c-59.5 0-108-48.4-108-108zM416.3 261.8h-42.8v126H247.6v42.7h125.9V556h42.8V430.5h125.4v-42.7H416.3z" fill="white" p-id="1775"></path><path d="M773.6 789.4l30.2-30.2-190.1-190.6c32.7-44.8 52-99.9 52-159.5 0-149.7-121.6-271.3-271.3-271.3-149.3 0-271.3 121.6-271.3 271.3 0 149.3 121.5 271.3 271.3 271.3 74.5 0 142.3-30.3 191.4-79.3l187.8 188.3zM394.4 637.7c-126 0-228.6-102.5-228.6-228.6s102.5-228.6 228.6-228.6S623 283.1 623 409.2 520.5 637.7 394.4 637.7z" fill="white" p-id="1776"></path>
                    </svg>
                </div>
                <div class='gap'></div>
                <div id='tree_zoom_out' title='Zoom out' @click='buttonZoomOut' v-ripple class='small-button'>
                    <svg class='icon' width='18px' height='18px' transform='translate(0, 3)' viewBox='0 0 1024 1024'>
                        <path d="M754.2 151.5h-89.5v42.7h89.5c59.5 0 108 48.4 108 108v67.6h42.7v-67.6c0-83.1-67.6-150.7-150.7-150.7zM862.2 737.3c0 59.5-48.4 108-108 108h-89.5V888h89.5c83.1 0 150.7-67.6 150.7-150.7v-67.6h-42.7v67.6zM166.3 737.8v-67.6h-42.7v67.6c0 83.1 67.6 150.7 150.7 150.7h89.5v-42.7h-89.5c-59.5 0-108-48.4-108-108zM247.6 387.8h294.2v42.7H247.6z" p-id="1938" fill="white"></path><path d="M773.6 789.4l30.2-30.2-190.1-190.6c32.7-44.8 52-99.9 52-159.5 0-149.7-121.6-271.3-271.3-271.3-149.3 0-271.3 121.6-271.3 271.3 0 149.3 121.6 271.3 271.3 271.3 74.5 0 142.3-30.3 191.4-79.3l187.8 188.3zM394.4 637.7c-126 0-228.6-102.5-228.6-228.6s102.5-228.6 228.6-228.6S623 283.1 623 409.2 520.5 637.7 394.4 637.7z" p-id="1939" fill="white"></path>
                    </svg>
                </div> -->
            </div>
        </div>
        <div class="svg-info V-centered" id="meta-svg-container2">
            <div class="tree-box H-centered">
                <svg class="datainfo-svg" id="meta-svg2" @contextmenu="disableRightClick">
                    <defs>
                        <linearGradient id="myGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#FFF" />
                            <stop offset="100%" stop-color="rgba(255, 255, 255, 0.2)" />
                        </linearGradient>
                    </defs>
                    <g class="tree-g">
                        <g class="tree-back-g">
                        </g>
                    </g>
                </svg>
                <div id="control-tree">
                    <!-- <div class="control">
                        <button id='apply_bottom' title='Apply' :disabled="!$parent.$parent.can_apply" @click='buttonApply' v-ripple class='rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M1004.50304 266.82624l-587.072 594.16064-17.1904 16.19328-17.1904-16.19328L19.49696 493.03808l118.53696-119.9872 262.17856 265.37984 485.7536-491.6096L1004.50304 266.82624 1004.50304 266.82624zM1004.50304 266.82624" fill="white"></path>
                            </svg>
                            Apply
                        </button>
                        <button id='undo_bottom' title='Undo' :disabled="!$parent.$parent.can_undo" @click='buttonUndo' v-ripple class='rect-button icon-rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M223.300267 221.320533h410.555733c214.493867 0 388.437333 173.192533 388.437333 386.798934 0 213.674667-173.943467 386.8672-388.437333 386.8672H116.053333a64.580267 64.580267 0 0 1-64.7168-64.512c0-35.566933 29.013333-64.443733 64.7168-64.443734h517.802667a258.389333 258.389333 0 0 0 258.935467-257.911466 258.389333 258.389333 0 0 0-258.935467-257.8432h-415.061333L293.546667 424.823467a64.3072 64.3072 0 0 1-28.672 108.7488 64.853333 64.853333 0 0 1-62.941867-17.6128L19.114667 333.687467a64.375467 64.375467 0 0 1 0-91.204267L201.9328 60.074667a64.9216 64.9216 0 0 1 91.613867 0c25.258667 25.122133 25.258667 65.9456 0 91.136l-70.314667 70.0416z" fill="white"></path>
                            </svg>
                        </button>
                        <button id='redo_bottom' title='Redo' :disabled="!$parent.$parent.can_redo" @click='buttonRedo' v-ripple class='rect-button icon-rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M828.893867 220.091733H418.338133C203.844267 220.091733 29.969067 393.216 29.969067 606.890667c0 213.674667 173.8752 386.798933 388.369066 386.798933h517.802667a64.580267 64.580267 0 0 0 64.7168-64.443733 64.580267 64.580267 0 0 0-64.7168-64.443734H418.338133A258.389333 258.389333 0 0 1 159.402667 606.890667a258.389333 258.389333 0 0 1 258.935466-257.911467h415.1296l-74.888533 74.615467a64.3072 64.3072 0 0 0 28.672 108.7488 64.853333 64.853333 0 0 0 62.941867-17.6128l183.022933-182.272a64.375467 64.375467 0 0 0 0-91.272534L850.193067 58.914133a64.9216 64.9216 0 0 0-91.5456 0 64.3072 64.3072 0 0 0 0 91.136l70.314666 70.0416z" fill="white"></path>
                            </svg>
                        </button>
                        <button id='cancel_bottom' title='Cancel' :disabled="!$parent.$parent.can_undo" @click='buttonCancel' v-ripple class='rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M617.92 516.096l272 272-101.824 101.824-272-272-272 272-101.856-101.824 272-272-275.008-275.04L241.056 139.2l275.04 275.04 275.04-275.04 101.824 101.824-275.04 275.04z" fill="white"></path>
                            </svg>
                            Cancel
                        </button>
                    </div> -->
                    <div class="color-legend-div">
                        <svg class="color-legend"></svg>
                    </div>
                    <div class="tree-legend-div">
                        <svg class="tree-legend"></svg>
                    </div>
                </div>
            </div>
            <!-- <SankeyTree
                ref="sankey_tree"
                :item="h_data"
            /> -->
        </div>
    </div>
</template>

<script>
import { VContainer, VRow, VCol } from 'vuetify/components'; 
import * as d3 from 'd3';
import * as Global from '../plugins/global';
import { mapState, mapActions } from 'vuex';
// import SankeyTree from './sankey_tree.vue'
window.d3 = d3;

export default {
    name: 'TreeView',
    components: {
        VContainer,
        VRow,
        VCol,
        // SankeyTree,
    },
    props: ['item', "imageSrc"],
    emits: ['hover-node', 'click-node', 'score-edit', 'score-edit2'],
    data: function() {
        return {
            thres: 0.3,
            selectedCategory: '',
            svg: null,
            svg_g: null,
            svg_back_g: null,
            svgsize: null,
            svg_width: 100,
            svg_height: 100,
            color_list: ['rgb(255, 23, 23)', 'rgb(255, 139, 23)', 'rgb(255, 238, 23)', 'rgb(180, 255, 23)', 'rgb(23, 255, 35)', 'rgb(23, 255, 255)', 'rgb(23, 64, 255)', 'rgb(168, 23, 255)', 'rgb(255, 83, 247)'],
            max_deep: 0,
            root: null,
            click_id: -1,
            click_parent_id: -1,
            focus_id: -1,
            click_ids: [],
            scale: 1,
            xshift: 0,
            yshift: 0,
            isShowHierarchy: false,
            no_drag: true,
            is_zoom: 0,
            only_drag: false,
            remove_time: 100,
            update_time: 300,
            create_time: 200,
            image_timer: null,
            image_timer2: null,
            click_timer: null,
            range_timer: null,
            emit_timer: null,
            old_last_path: {},
            last_path: {},
            context_ratio: 0.4,
            now_context_ratio: 0.4,
            between_area_padding: 5,
            axis_top_padding: 5,
            area_padding: 5,
            focus_ratio: 4,
            class_order: {}, 
            confidence_range: [0, 1],
            hand_confidence_range: [0, 1],
            default_confidence_range: [0, 1],
            isShowInfluence: false,
            circle_ratio: 0.8,
        };
    },
    methods: {
        buttonApply: function() {
            this.$parent.$parent.buttonApply();
        },
        buttonUndo: function() {
            // console.log("buttonUndo", this.$parent.$parent.tmp_edit_record);
            this.$parent.$parent.buttonUndo();
        },
        buttonRedo: function() {
            this.$parent.$parent.buttonRedo();
        },
        buttonCancel: function() {
            // console.log("buttonCancel", this.$parent.$parent.tmp_edit_record);
            this.$parent.$parent.buttonCancel();
        },
        showSectorChange() {
            this.resetNode();
            this.updateTree();
        },
        getDFSList: function(data, child_key) {
            let that = this;
            let result = [data];
            if(data[child_key] != null) {
                for(let child of data[child_key])
                    result = result.concat(that.getDFSList(child, child_key));
            }
            return result;
        },
        updateAvgScoreAndClass: function(data, child_key) {
            let that = this;
            if(data[child_key] != null) {
                for(let child of data[child_key])
                    that.updateAvgScoreAndClass(child, child_key);
            }
            let score_avg = 0;
            for(let i=0;i<data.child_index.length;i++) {
                score_avg += that.boxes[data.child_index[i]].score;
            }
            data.score = score_avg / Math.max(1, data.child_index.length);
            if(data.class != "group") {
                data.class = that.boxes[data.child_index[0]].class;
            }
        },
        scoreTmpEdit: function(id, scale) {
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            let node_dict = {};
            for(let data of DFSlist) node_dict[data.name] = data;

            let update_dict = {};
            let data = node_dict[id];
            let tmp_change = Math.min(0.2, Math.max(-0.2, that.boxes[id].score * (scale-1)));
            let old_score = that.boxes[id].score;
            let new_score = that.boxes[id].score + tmp_change;
            that.boxes[id].score = Math.max(Math.min(1, new_score), 0);
            update_dict[id] = {"old_score": old_score, "new_score": that.boxes[id].score, "old_class": that.boxes[id].class, "new_class": that.boxes[id].class};

            let thres = that.$parent.$parent.selectedWithinInfluence["thres"];
            for(let id2 in that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex]) {
                if(id == id2) continue;
                let tmp_ratio = Math.min(0.8, that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex][id2]/(thres*2));
                let data2 = node_dict[id2];
                
                let tmp_change2 = (update_dict[id]["new_score"] - that.boxes[id2].score) * tmp_ratio;
                tmp_change2 = Math.max(-Math.abs(tmp_ratio*tmp_change2), Math.min(Math.abs(tmp_ratio*tmp_change2), tmp_change2));

                if(tmp_change2*(scale-1) < 0) continue;
                let old_score2 = that.boxes[id2].score;
                let new_score2 = old_score2 + tmp_change2;
                that.boxes[id2].score = Math.max(Math.min(1, new_score2), 0);
                update_dict[id2] = {"old_score": old_score2, "new_score": that.boxes[id2].score, "old_class": that.boxes[id2].class, "new_class": that.boxes[id2].class};
            }
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            // this.updateTree();
            this.updateTreeTwoStep();
            return update_dict;
        },
        scoreTmpEdit2: function(ids, scale) {
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            let node_dict = {};
            for(let data of DFSlist) node_dict[data.name] = data;

            let update_dict = {};
            for(let id of ids) {
                let data = node_dict[id];
                let tmp_change = Math.min(0.2, Math.max(-0.2, that.boxes[id].score * (scale-1)));
                let old_score = that.boxes[id].score;
                let new_score = that.boxes[id].score + tmp_change;
                that.boxes[id].score = Math.max(Math.min(1, new_score), 0);
                if(!(id in update_dict)) {
                    update_dict[id] = {"old_score": old_score, "old_class": that.boxes[id].class};
                }
                Object.assign(update_dict[id], {"new_score": that.boxes[id].score, "new_score_base": that.boxes[id].score, "new_class": that.boxes[id].class});
            }

            let thres = that.$parent.$parent.selectedWithinInfluence["thres"];

            for(let id of ids) {
                for(let id2 in that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex]) {
                    if(id == id2) continue;
                    let tmp_ratio = Math.min(0.8, that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex][id2]/(thres*2));
                    let data2 = node_dict[id2];

                    if(!(id2 in update_dict)) {
                        update_dict[id2] = {"old_score": that.boxes[id2].score, "new_score": that.boxes[id2].score, "old_class": that.boxes[id2].class, "new_class": that.boxes[id2].class};
                    }

                    let tmp_change2 = (update_dict[id]["new_score_base"] - update_dict[id2]["old_score"]) * tmp_ratio;
                    tmp_change2 = Math.max(-Math.abs(tmp_ratio*tmp_change2), Math.min(Math.abs(tmp_ratio*tmp_change2), tmp_change2));

                    if(tmp_change2*(scale-1) < 0) continue;

                    let old_score2 = update_dict[id2]["old_score"];
                    let new_score2 = old_score2 + tmp_change2;
                    if((scale-1)>0) new_score2 = Math.max(new_score2, update_dict[id2]["new_score"]);
                    if((scale-1)<0) new_score2 = Math.min(new_score2, update_dict[id2]["new_score"]);

                    that.boxes[id2].score = Math.max(Math.min(1, new_score2), 0);

                    Object.assign(update_dict[id2], {"new_score": that.boxes[id2].score, "new_class": that.boxes[id2].class});
                }
            }
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            // this.updateTree();
            this.updateTreeTwoStep();
            return update_dict;
        },
        classTmpEdit: function(id, cls) {
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            let node_dict = {};
            for(let data of DFSlist) node_dict[data.name] = data;

            let update_dict = {};
            let data = node_dict[id];
            let old_class = that.boxes[id].class;
            let new_class = cls;
            that.boxes[id].class = new_class;
            update_dict[id] = {"old_score": that.boxes[id].score, "new_score": that.boxes[id].score, "old_class": old_class, "new_class": that.boxes[id].class};

            let thres = that.$parent.$parent.selectedWithinInfluence["thres"];
            for(let id2 in that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex]) {
                if(id == id2) continue;
                let tmp_ratio = Math.min(0.8, that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex][id2]/(thres*2));
                let data2 = node_dict[id2];
                let old_class2 = that.boxes[id2].class;
                let new_class2 = cls;
                that.boxes[id2].class = new_class2;
                update_dict[id2] = {"old_score": that.boxes[id2].score, "new_score": that.boxes[id2].score, "old_class": old_class2, "new_class": that.boxes[id2].class};
            }
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            // this.updateTree();
            this.updateTreeTwoStep();
            return update_dict;
        },
        classTmpEdit2: function(ids, cls) {
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            let node_dict = {};
            for(let data of DFSlist) node_dict[data.name] = data;

            let update_dict = {};
            for(let id of ids) {
                let data = node_dict[id];
                let old_class = that.boxes[id].class;
                let new_class = cls;
                that.boxes[id].class = new_class;
                if(!(id in update_dict)) {
                    update_dict[id] = {"old_score": that.boxes[id].score, "old_class": old_class};
                }
                Object.assign(update_dict[id], {"new_score": that.boxes[id].score, "new_class": that.boxes[id].class});

                let thres = that.$parent.$parent.selectedWithinInfluence["thres"];
                for(let id2 in that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex]) {
                    if(id == id2) continue;
                    let tmp_ratio = Math.min(0.8, that.$parent.$parent.selectedWithinInfluence[id][that.$parent.$parent.selectedItemIndex][id2]/(thres*2));
                    let data2 = node_dict[id2];
                    let old_class2 = that.boxes[id2].class;
                    let new_class2 = cls;
                    that.boxes[id2].class = new_class2;
                    if(!(id2 in update_dict)) {
                        update_dict[id2] = {"old_score": that.boxes[id2].score, "old_class": old_class2};
                    }
                    Object.assign(update_dict[id2], {"new_score": that.boxes[id2].score, "new_class": that.boxes[id2].class});
                }
            }
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            // this.updateTree();
            this.updateTreeTwoStep();
            return update_dict;
        },
        stepEdit: function(update_dict, key, key2) {
            if (update_dict == null) return;
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            let node_dict = {};
            for(let data of DFSlist) node_dict[data.name] = data;

            for(let id2 in update_dict) {
                let data = node_dict[id2];
                that.boxes[data.child_index[0]].score = update_dict[id2][key];
                that.boxes[data.child_index[0]].class = update_dict[id2][key2];
            }
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            // this.updateTree();
            this.updateTreeTwoStep();
        },
        restoreEdit: function(record) {
            if (record == null) return null;
            let that = this;
            let DFSlist = that.getDFSList(that.h_data, "_children");
            // let node_dict = {};
            // for(let data of DFSlist) node_dict[data.name] = data;
            
            let update_dict = {};
            for(let i=0;i<record["now"];i++) {
                let tmp_update_dict = record["update"][i]["update_dict"];
                for(let id2 in tmp_update_dict) {
                    // let data = node_dict[id2];
                    that.boxes[id2].score = tmp_update_dict[id2]["new_score"];
                    that.boxes[id2].class = tmp_update_dict[id2]["new_class"];
                    update_dict[id2] = {"new_score": that.boxes[id2].score, "new_class": that.boxes[id2].class};
                }
            }
            console.log("restore update dict", update_dict);
            that.updateAvgScoreAndClass(that.h_data, "_children");
            that.resetNode();

            this.updateTreeTwoStep();
            return update_dict;
        },
        scoreEdit: function(e, d, scale) {
            let that = this;
            if(d.data.class == "group") {
                that.$parent.$emit('score-edit2', d.data.child_names2, scale);
                return;
            }
            // let tmp_box = {"class": d.data.class, "x": d.data.bbox[0], "y": d.data.bbox[1], "width": d.data.bbox[2], "height": d.data.bbox[3]}
            // that.$parent.$emit('score-edit', tmp_box, scale);
            that.$parent.$emit('score-edit', d.data.name, scale);
        },
        calculateBoxPlotProperties: function(data) {
            const sortedData = data.slice().sort((a, b) => a - b);
            const length = sortedData.length;
            const median = this.calculatePercentile(sortedData, 0.5);
            const q1 = this.calculatePercentile(sortedData, 0.25);
            const q3 = this.calculatePercentile(sortedData, 0.75);
            const min = sortedData[0];
            const max = sortedData[length - 1];
            return {
                "min": min,
                "q1": q1,
                "median": median,
                "q3": q3,
                "max": max,
                "outliers": []
            };
        },
        calculatePercentile: function(sortedData, percentile) {
            const length = sortedData.length;
            const index = percentile * (length - 1);
            const lowerIndex = Math.floor(index);
            const upperIndex = Math.ceil(index);
        
            if (lowerIndex === upperIndex) {
                return sortedData[lowerIndex];
            }
        
            const lowerValue = sortedData[lowerIndex];
            const upperValue = sortedData[upperIndex];
            const weight = index - lowerIndex;
            return lowerValue + (upperValue - lowerValue) * weight;
        },
        showButton: function() {
            let buttons = document.querySelector('#tree_buttons');
            buttons.classList.remove('hidden');
        },
        hideButton: function() {
            let buttons = document.querySelector('#tree_buttons');
            buttons.classList.add('hidden');
        },
        clickTitle: function() {
            let card = document.querySelector('.svg-info');
            card.classList.toggle('expanded');
            let arrow = document.querySelector('#sankey-arrow');
            arrow.classList.toggle('expanded');
        },
        disableRightClick(event) {
            event.preventDefault();
        },
        buttonChangeDrag: function() {
            this.no_drag = !this.no_drag;
        },
        buttonZoomIn: function() {
            let tmp = document.getElementById('meta-svg2');
            if(this.is_zoom == 1) {
                tmp.classList.remove('magnifier-cursor');
                if(this.only_drag)
                    tmp.classList.add('drag-cursor');
                this.is_zoom = 0;
            }else {
                if(this.is_zoom == -1) {
                    tmp.classList.remove('shrink-cursor');
                    if(this.only_drag)
                        tmp.classList.add('drag-cursor');
                    this.is_zoom = 0;
                }
                if(this.only_drag)
                    tmp.classList.remove('drag-cursor');
                tmp.classList.add('magnifier-cursor');
                this.is_zoom = 1;
            }
        },
        buttonZoomOut: function() {
            let tmp = document.getElementById('meta-svg2');
            if(this.is_zoom == -1) {
                tmp.classList.remove('shrink-cursor');
                if(this.only_drag)
                    tmp.classList.add('drag-cursor');
                this.is_zoom = 0;
            }else {
                if(this.is_zoom == 1) {
                    tmp.classList.remove('magnifier-cursor');
                    if(this.only_drag)
                        tmp.classList.add('drag-cursor');
                    this.is_zoom = 0;
                }
                if(this.only_drag)
                    tmp.classList.remove('drag-cursor');
                tmp.classList.add('shrink-cursor');
                this.is_zoom = -1;
            }
        },
        setClick: function(id) {
            // console.log("setClick", id);
            if(this.image_timer != null) {
                clearTimeout(this.image_timer);
                this.image_timer = null;
            }
            this.image_timer = setTimeout(() => {
                this.hover_id = id;
                // this.nodeFullTmpExpand(this.h_data, id);

                this.resetNode();
                // console.log("timer click");

                this.updateTree();
            }, 100);
        },
        setClick2: function(id) {
            // console.log("setClick2", id);
            if(this.image_timer2 != null) {
                clearTimeout(this.image_timer2);
                this.image_timer2 = null;
            }
            this.image_timer2 = setTimeout(() => {
                this.click_id = id;
                this.focus_id = id;

                this.nodeFullExpand(this.h_data, id);
                this.nodeTrim(this.h_data, id);
                this.resetNode();
                // console.log("timer click");
                
                this.updateTree();
                // this.updateTreeTwoStep();
            }, 100);
        },
        setShowHierarchy: function(show) {
            this.isShowHierarchy = show;
            this.updateTree();
        },
        getClickIds: function(id) {
            let that = this;
            function dfs_find_ids(node, id) {
                if(node.name == id) {
                    if(node.children == null || node.children.length==0)
                        that.click_score = node.score;
                    return node.child_names;
                }
                let result = [];
                for(let child of node._children) {
                    let ret = dfs_find_ids(child, id);
                    if(ret != null) result = result.concat(ret);
                }
                return result;
            }
            return dfs_find_ids(this.h_data, id);
        },
        getFocusIds: function(id) {
            function dfs_find_ids(node) {
                let result = [];
                for(let child of node._children) {
                    let ret = dfs_find_ids(child, id);
                    if(ret != null) result = result.concat(ret);
                }
                if(node.is_focus)result.push(node.name);
                return result;
            }
            return dfs_find_ids(this.h_data, id);
        },
        generatePathWithArcs: function(x1, y1, x2, y2, x3, y3, x4, y4, radius) {
            let d = 1;
            if(x4<x1) d = -1;
            let new_radius0 = Math.min(radius, Math.abs(y1-y2));
            let new_radius = Math.min(radius, Math.abs(x1-x4)/2);
            const line1 = `M ${x1} ${y1} L ${x2} ${y2-new_radius0}`;
            const arc1 = `A ${new_radius} ${new_radius0} 0 0 ${(1-d)/2} ${x2+d*new_radius} ${y2}`;
            const line2 = `L ${x3-d*new_radius} ${y3}`;
            const arc2 = `A ${new_radius} ${radius} 0 0 ${(1+d)/2} ${x3} ${y3+radius}`;
            const line3 = `L ${x4} ${y4}`;
            // 合并路径
            return `${line1} ${arc1} ${line2} ${arc2} ${line3}`;
        },
        updateClick: function(id, pid=-1) {
            // console.log("update click", id, pid);
            let that = this;

            if(that.click_timer != null) {
                clearTimeout(that.click_timer);
                that.click_timer = null;
            }
            that.click_timer = setTimeout(function() {
                // console.log("click");
                if((that.click_id != id) || (that.click_parent_id != pid)) {
                    // console.log(d);
                    that.click_id = id;
                    that.click_parent_id = pid;
                    that.focus_id = id;
                    if((that.focus_id == that.h_data.name)&&("_children" in that.h_data)&&(that.h_data._children.length>0)) that.focus_id = -1;
                    // that.$emit('click-node', id);
                    that.emitClick(id);

                    // that.nodeExpand(that.h_data, id);
                    that.nodeFullExpand(that.h_data, id);
                    that.nodeTrim(that.h_data, id);
                    
                    that.resetNode();

                    // that.updateTree();
                    that.updateTreeTwoStep();
                        
                }else {
                    that.click_id = -1;
                    that.focus_id = -1;
                    that.click_parent_id = -1;
                    // that.$emit('click-node', -1);
                    that.emitClick(-1);

                    that.nodeClose(that.h_data, id);

                    that.resetNode();

                    // that.updateTree();
                    that.updateTreeTwoStep();
                }
            }, 200);
        },
        updateDoubleClick: function(id) {
            let that = this;
            // console.log("dblclick");
            if(that.click_timer != null) {
                clearTimeout(that.click_timer);
                that.click_timer = null;
            }
            that.click_id = id;
            that.focus_id = id;
            if(that.focus_id == that.h_data.name) that.focus_id = -1;
            // that.$emit('click-node', id);
            that.emitClick(id);
            that.nodeFullExpand(that.h_data, id);

            that.resetNode();
            
            // this.updateTree();
            this.updateTreeTwoStep();
        },
        updateNode: function(node, is_zoom=false) {
            let that = this;

            // console.log("root", that.node_data);
            
            // node.each(function(d) {
            //     console.log(d.data.name, d);
            // });
            
            node.transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("transform", d => `translate(${d.x*that.scale},${d.y*that.scale})`)
                .attr('opacity', function(d) {
                    if(that.click_ids.length>0){
                        if(that.click_ids.includes(d.data.name))
                            return 1;
                        if((d.data.child_names2.includes(that.click_id))&&(!("children" in d)||d.children.length==0))
                            return 1;
                        return 0.33;
                    }
                    return 1;
                });

            // console.log(that.click_id, node.filter((d) => that.click_id == d.data.name));
            // node.filter((d) => that.click_id == d.data.name).raise();
            
            that.updateSector(node, is_zoom);
        },
        updateSector: function(node, is_zoom=false) {
            let that = this;

            node.select(".circle_g")
                .attr("visibility", function(d) {
                    if(d.data.class != "empty")return "visible";
                    return "hidden";
                })
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("opacity",  function(d) {
                    if(d.data.class != "empty")return 1;
                    return 0;
                });
            
            node.select(".circle_g").each(function(d) {

                let now_group = d3.select(this);

                let full_radius = that.width_ratio*d.data.width_weight_focus*Math.sqrt(that.scale)/2;
                let parent_radius = that.circle_ratio*full_radius;
                let middle_radius = Math.min(3, parent_radius/6)

                now_group.select(".circle-middle")
                    .raise()
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("fill", "gray")
                    .attr("stroke", function() {
                        if((that.click_id == d.data.name)||(that.hover_id == d.data.name))
                            return "black";
                        if(((d.data.child_names2.includes(that.click_id))||(d.data.child_names2.includes(that.hover_id)))&&(!("children" in d)||d.children.length==0))
                            return "black";
                        return "gray";
                    })
                    .attr("stroke-width", function() {
                        if((that.click_id == d.data.name)||(that.hover_id == d.data.name))
                            return 1;
                        if(((d.data.child_names2.includes(that.click_id))||(d.data.child_names2.includes(that.hover_id)))&&(!("children" in d)||d.children.length==0))
                            return 1;
                        return 1;
                    })
                    .attr("r", middle_radius)

                now_group.select(".circle-outer")
                    .attr("fill", "transparent")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("stroke", function() {
                        if((that.click_id == d.data.name)||(that.hover_id == d.data.name))
                            return "black";
                        if(((d.data.child_names2.includes(that.click_id))||(d.data.child_names2.includes(that.hover_id)))&&(!("children" in d)||d.children.length==0))
                            return "black";
                        return "gray";
                    })
                    .attr("stroke-width", function() {
                        if(d.data.is_focus)
                            return 4;
                        // if((that.click_id == d.data.name)||(that.hover_id == d.data.name))
                        //     return 1;
                        return 1;
                    })
                    .attr("r", parent_radius)
                    .attr("stroke-dasharray", function(d) {
                        let dash = 4;
                        dash = Math.max(1.5, Math.min(dash, parent_radius/10));
                        // TODO 修改判定规则
                        if(d.data.unselected)
                            return `${dash} ${dash}`
                        return "none";
                    })

                let r_bias = middle_radius + (parent_radius-middle_radius)*0.1;
                let a_bias = 0;
                if(d.parent) a_bias = 1/32;

                let axis_g = now_group.selectAll(".axis_g")
                    .attr("visibility", "visible");
                if(parent_radius-r_bias < 25) {
                    now_group.selectAll(".axis-1")
                        .attr("visibility", "hidden");
                    now_group.selectAll(".axis-3")
                        .attr("visibility", "hidden");
                }
                if(parent_radius-r_bias < 12.5) {
                    now_group.selectAll(".axis-2")
                        .attr("visibility", "hidden");
                }
                if(that.isShowInfluence) {
                    now_group.selectAll(".axis-4")
                        .attr("visibility", "hidden");
                }
                axis_g.select(".axis-circle")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("r", d2 => parent_radius*d2+r_bias*(1-d2));
                axis_g.select(".axis-text")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("y", d2 => -(parent_radius*d2+r_bias*(1-d2)));
                

                let sector_g = now_group.selectAll(".sector_g")
                    .data(d.data.all_children, d2 => d2.node.name);
                // console.log("select sector", now_group, sector_g);
                const arcGenerator = d3.arc()
                    .innerRadius(r_bias);

                sector_g.select(".sector")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("opacity", function(d2) {
                        return 1;
                    })
                    .attr("fill", function(d2) {
                        let color = d3.color(that.categories_dict[d2.node.class]["color"]);
                        color.opacity = 0.9;
                        // TODO 修改判定规则
                        let tmp_thres = that.thres;
                        if("thres" in that.categories_dict[d2.node.class]) tmp_thres = that.categories_dict[d2.node.class]["thres"];
                        if(d2.node.score<tmp_thres)
                            color.opacity = 0.5;
                        return color.toString();
                    })
                    .attr("stroke", function(d2) {
                        let color = d3.color("transparent");
                        
                        // // let color = d3.color("gray");
                        // let color = d3.color("rgb(128, 128, 128)");
                        // if((that.click_id == d.data.name)||(that.hover_id == d.data.name))
                        //     // color = d3.color("black");
                        //     color = d3.color("rgb(64, 64, 64)");

                        // if(((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))&&(!("children" in d)||d.children.length==0))
                        if((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))
                            color = d3.color("rgb(0, 0, 0)");
                        return color.toString();
                    })
                    .attr("stroke-dasharray", function(d2) {
                        // let dash = 4;
                        // dash = Math.max(0.5, Math.min(dash, parent_radius/20));
                        // // TODO 修改判定规则
                        // if(d2.node.score<that.thres)
                        //     return `${dash} ${dash}`
                        return "none";
                    })
                    .attr("stroke-width", function(d2) {
                        let stroke = Math.min(0.75, 15/d.data.all_children.length);
                        // // TODO 修改判定规则
                        // if(d2.node.score<that.thres)
                        //     return stroke*0.75;
                        // if(((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))&&(!("children" in d)||d.children.length==0)&&(that.click_id != d.data.name))
                        if((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))
                            return Math.max(1.5, stroke);
                        return stroke;
                    })
                    .attr("d", function(d2) {
                        let tmp_score = d2.node.score;
                        if(that.isShowInfluence) tmp_score = d2.node.influence;
                        return arcGenerator
                            .outerRadius(parent_radius*tmp_score+r_bias*(1-tmp_score))
                            // .startAngle(2*Math.PI*d2.bias)
                            // .endAngle(2*Math.PI*(d2.bias+d2.ratio))();
                            .startAngle(2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio)))
                            .endAngle(2*Math.PI*(1-a_bias-(1-2*a_bias)*d2.bias))();
                    });
                
                sector_g.select(".sector_circle")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("opacity", function(d2) {
                        return 1;
                    })
                    .attr("fill", function(d2) {
                        let color = d3.color(that.categories_dict[d2.node.class]["color"]);
                        color.opacity = 0.9;
                        // TODO 修改判定规则
                        let tmp_thres = that.thres;
                        if("thres" in that.categories_dict[d2.node.class]) tmp_thres = that.categories_dict[d2.node.class]["thres"];
                        if(d2.node.score<tmp_thres)
                            color.opacity = 0.4;
                        return color.toString();
                    })
                    .attr("stroke", function(d2) {
                        let color = d3.color("transparent");
                        
                        if((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))
                            color = d3.color("rgb(0, 0, 0)");
                        return color.toString();
                    })
                    .attr("stroke-dasharray", function(d2) {
                        return "none";
                    })
                    .attr("stroke-width", function(d2) {
                        let stroke = Math.min(0.75, 15/d.data.all_children.length);
                        if((that.click_id == d2.node.name)||(that.hover_id == d2.node.name))
                            return Math.max(1.5, stroke);
                        return stroke;
                    })
                    // .attr("x", function(d2) {
                    //     let angle = 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio/2));
                    //     return (full_radius+parent_radius)/2 * Math.cos(angle);
                    // })
                    // .attr("y", function(d2) {
                    //     let angle = 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio/2));
                    //     return -(full_radius+parent_radius)/2 * Math.sin(angle);
                    // })
                    .attr("transform", function(d2) {
                        let angle = 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio/2));
                        let tmp_score = d2.node.influence;
                        let r = full_radius - (full_radius-parent_radius)/2*tmp_score;
                        let x = r * Math.sin(angle);
                        let y = -r * Math.cos(angle);
                        return `translate(${x},${y})`
                    })
                    .attr("r", function(d2) {
                        let tmp_score = d2.node.influence;
                        return (full_radius-parent_radius)/2 * tmp_score;
                    });
            })
            node.select(".edit_g")
                .attr("visibility", function(d) {
                    if(d.data.class != "empty") {
                        // if((d.data.is_focus)&&(that.click_id == d.data.name)&&(!("children" in d)||d.children.length==0))
                        if((d.data.is_focus)&&(that.click_id == d.data.name))
                            return "visible";
                        return d3.select(this).attr("visibility");
                    }
                    return "hidden";
                })
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("opacity",  function(d) {
                    // if((d.data.is_focus)&&(that.click_id == d.data.name)&&(!("children" in d)||d.children.length==0))
                    if((d.data.is_focus)&&(that.click_id == d.data.name))
                        return 1;
                    return 0;
                })
                .attr("transform", function(d) {
                    let tmp = that.width_ratio*d.data.width_weight_focus*Math.sqrt(that.scale)/2;
                    return `translate(0, ${-tmp})`;
                })
                .on('end', function(d) {
                    // if((d.data.is_focus)&&(that.click_id == d.data.name)&&(!("children" in d)||d.children.length==0))
                    if((d.data.is_focus)&&(that.click_id == d.data.name))
                        return;
                    d3.select(this).attr("visibility", "hidden");
                });
        },
        updateTreeTwoStep: function(is_zoom=false) {
            let that = this;
            that.updateTree(is_zoom, true);

            if(that.range_timer != null) {
                clearTimeout(that.range_timer);
                that.range_timer = null;
            }
            that.range_timer = setTimeout(function() {
                that.resetNode();
                that.updateTree(is_zoom);
            }, that.remove_time+that.update_time+that.create_time);
        },
        emitClick: function(id, time=0) {
            let that = this;

            if(that.emit_timer != null) {
                clearTimeout(that.emit_timer);
                that.emit_timer = null;
            }
            that.emit_timer = setTimeout(function() {
                that.$emit('click-node', id);
            }, time);
        },
        emitHover: function(id, time=0) {
            let that = this;

            if(that.emit_timer != null) {
                clearTimeout(that.emit_timer);
                that.emit_timer = null;
            }
            that.emit_timer = setTimeout(function() {
                that.$emit('hover-node', id);
            }, time);
        },
        updateTree: function(is_zoom=false, fixed_range=false) {
            // console.log("update tree");
            let that = this;
            if(that.svg == null)return;

            that.old_last_path = that.last_path;
            that.last_path = {};

            // that.svg_g.selectAll(".link").remove();
            // that.svg_g.selectAll(".node").remove();

            that.updateTreeLayout(is_zoom, fixed_range);

            let node_basesize = this.node_basesize;

            this.svg_g.attr("transform", "translate("+this.xshift+","+this.yshift+")");

            let lineGenerator = d3.line().curve(d3.curveBasis);
            // let lineGenerator = d3.line().interpolate("basis");

            // let links = that.svg_g.selectAll(".link")
            //     .data(that.link_data, d => { return String(d.source.data.name)+"&"+String(d.target.data.name); });
            let links = that.old_links;
            // console.log("update links", links);
            links.attr("stroke", "#ccc")
                .attr("fill", "none")
                .attr("visibility", function(d) {
                    if(d.source.data.class == "empty")return "hidden";
                    if(d.target.data.class == "empty")return "hidden";
                    return null;
                })
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attrTween("d", d => {
                    let f_data = d.source, c_data = d.target;
                    if(f_data.y > c_data.y) { c_data = d.source; f_data = d.target; }
                    let f_bias = 0;
                    let c_bias = 0;
                    const source = [f_data.x*that.scale, f_data.y*that.scale+f_bias*Math.sqrt(that.scale)];
                    const target = [c_data.x*that.scale, c_data.y*that.scale-c_bias*Math.sqrt(that.scale)];
                    // return lineGenerator([source, [source[0], (source[1]*2+target[1])/3], [target[0], (source[1]+target[1]*2)/3], target]);
                    let corner = (that.level_dist-2*node_basesize)/2*Math.pow(0.9, d.target.order);
                    let old_path = that.old_last_path[d.target.data.name];
                    that.last_path[d.target.data.name] = [source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3];
                    // console.log("change", old_path, that.last_path[d.target.data.name]);
                    return function(t) {
                        if(old_path == null)
                            return that.generatePathWithArcs(source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3);
                        let new_path = [source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3];
                        // if((d.target.data._children.length == 2)&&(d.target.depth==1))
                        //     console.log("change", old_path, new_path);
                        for(let i=0;i<new_path.length;i++)
                            new_path[i] = new_path[i]*t + old_path[i]*(1-t);
                        return that.generatePathWithArcs(...new_path);
                    }
                })
                .attr("stroke-width", function(d) {
                    if(d.source.data.is_focus && d.target.data.is_focus) return 4;
                    return 1.5;
                })
                .attr("stroke-dasharray", function(d) {
                    let dash = 4;
                    // TODO 修改判定规则
                    if(d.target.data.unselected)
                        return `${dash} ${dash}`
                    return "none";
                })
                .attr('opacity', function(d) {
                    if(that.click_ids.length>0){
                        if((that.click_ids.includes(d.source.data.name))&&(that.click_ids.includes(d.target.data.name)))
                            return 1;
                        else return 0.33;
                    }
                    return 1;
                });
            // console.log("changed", that.node_data);

            const node = that.svg_g.selectAll(".node")
                .data(that.node_data, d=>d.data.name);

            that.updateNode(node, is_zoom);
            
        },
        cropImage(imageSrc, cropX, cropY, cropWidth, cropHeight) {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.crossOrigin = "anonymous"; // 处理跨域图片加载
                img.onload = () => {
                    // 创建 canvas 用于裁剪
                    const canvas = document.createElement("canvas");
                    const ctx = canvas.getContext("2d");

                    // 设置 canvas 的大小为裁剪区域的大小
                    canvas.width = cropWidth;
                    canvas.height = cropHeight;

                    // 绘制裁剪的部分
                    ctx.drawImage(
                        img,
                        cropX, // 裁剪起点 x
                        cropY, // 裁剪起点 y
                        cropWidth, // 裁剪宽度
                        cropHeight, // 裁剪高度
                        0, // 绘制起点 x
                        0, // 绘制起点 y
                        cropWidth, // 绘制宽度
                        cropHeight // 绘制高度
                    );

                    // 导出裁剪后的图片为 dataURL
                    const croppedImageUrl = canvas.toDataURL("image/png");
                    resolve(croppedImageUrl);
                };
                img.onerror = (err) => reject(err);
                img.src = imageSrc; // 加载图片
            });
        },
        preAdjustTree(node) {
            let that = this;
            if(node.children != null && node.children.length>0) {
                for(let child of node.children) {
                    that.preAdjustTree(child);
                }
            } else {
                that.leaf_list.push(node);
            }
        },
        initialAdjustTree(node, calc_size, top_weight=0) {
            let that = this;
            node.top_weight = top_weight+node.data.width_weight_focus/2;
            node.final_children = [];
            if(node.children != null && node.children.length>0) {
                let tmp_y = calc_size[1] * that.context_ratio - that.axis_top_padding - that.area_padding - that.between_area_padding
                let min_y = tmp_y * node.top_weight/Math.max(0.000001, top_weight+node.data.width_weight_focus);
                for(let child of node.children) {
                    that.initialAdjustTree(child, calc_size, top_weight+node.data.width_weight_focus);
                    node.width_ratio_y = Math.min(node.width_ratio_y, child.width_ratio_y);
                    node.final_children = node.final_children.concat(child.final_children);
                    node.final_children.push(child);
                }
                
                // for(let child of node.final_children) {
                //     min_y = Math.min(min_y, child.y*node.top_weight/Math.max(0.000001, child.top_weight));
                // }

                node.y = min_y;
            } else {
                let confidence_pos = that.confidence_range[1] - Math.max(Math.min(that.hard_confidence_range[1], node.data.score), that.hard_confidence_range[0])
                confidence_pos = confidence_pos / (that.confidence_range[1] - that.confidence_range[0]);
                node.y = calc_size[1]*(that.context_ratio + (1-that.context_ratio)*confidence_pos);
            }
        },
        secondAdjustTree(node) {
            let that = this;
            if(node.children != null && node.children.length>0) {
                let min_y = node.y;
                for(let child of node.children) {
                    that.secondAdjustTree(child);
                }
                // for(let child of that.leaf_list) {
                //     min_y = Math.min(min_y, (child.y-2*that.area_padding-that.between_area_padding)*node.top_weight/Math.max(0.000001, node.top_weight+node.data.width_weight_focus/2+child.data.width_weight_focus/2));
                // }
                for(let child of node.final_children) {
                    if(!(child.children != null && child.children.length>0)) continue;
                    min_y = Math.min(min_y, child.y*node.top_weight/Math.max(0.000001, child.top_weight));
                }
                node.y = min_y;
            }
        },
        checkChildOrder(node) {
            let that = this;
            if(node.children != null && node.children.length>0) {
                for(let child of node.children) {
                    that.checkChildOrder(child);
                    child.order = 0;
                }
                let right_cnt = 0;
                for(let child of node.children) {
                    if(child.x>node.x){
                        child.order = right_cnt;
                        right_cnt += 1;
                    }
                }
                let left_cnt = 0;
                for(let i=node.children.length-1;i>=0;i--) {
                    let child = node.children[i];
                    if(child.x<node.x){
                        child.order = left_cnt;
                        left_cnt += 1;
                    }
                }
            }
        },
        getTreelayout(node, min_weight, scale) {
            let that = this;
            if(node.children != null && node.children.length>0) {
                // console.log("get tree layout", node, min_weight, scale);
                let last = 0;
                let first_flag = true;
                for(let child of node.children) {
                    if(first_flag)
                        child.x = last + (child.data.separation_weight[0]+child.data.separation_weight[1]*min_weight)/2*scale;
                    else
                        child.x = last + (child.data.separation_weight[0]+child.data.separation_weight[1]*min_weight)/2*scale;
                        // child.x = last + (child.data.separation_weight[0]+child.data.separation_weight[1]*min_weight)/2*scale + min_weight*scale;
                    last = child.x + (child.data.separation_weight[0]+child.data.separation_weight[1]*min_weight)/2*scale;
                    first_flag = false;
                }
                for(let child of node.children) {
                    child.x += node.x-last/2;
                    that.getTreelayout(child, min_weight, scale);
                }
            }
        },
        getTreelayoutUp(node, min_weight) {
            let that = this;
            node.x = 0;
            node._x = 0;
            let tmp_width = node.data.separation_weight[0]+node.data.separation_weight[1]*min_weight;
            node.data.left_width = tmp_width/2;
            node.data.right_width = tmp_width/2;
            if(node.children != null && node.children.length>0) {
                for(let child of node.children) {
                    that.getTreelayoutUp(child, min_weight);
                }
                let last = 0;
                let first_mid = 0;
                let last_mid = 0;
                let first_flag = true;
                let first_flag2 = true;
                for(let child of node.children) {
                    if(first_flag) {
                        child._x = last + child.data.left_width;
                    }
                    else {
                        child._x = last + child.data.left_width;
                        // child._x = last + child.data.left_width + min_weight;
                    }
                    first_flag = false;

                    if(first_flag2){
                        if(child.data.class != "empty") {
                            first_mid = child._x;
                            first_flag2 = false;
                        }
                    }
                    if(child.data.class != "empty") {
                        if(first_flag2){
                            first_mid = child._x;
                        }
                        last_mid = child._x;
                        first_flag2 = false;
                    }
                    last = child._x + child.data.right_width;
                }
                let tmp_width = node.data.separation_weight[0]+node.data.separation_weight[1]*min_weight;
                let tmp_mid = (first_mid+last_mid)/2;
                node.data.left_width = Math.max(tmp_width/2, tmp_mid);
                node.data.right_width = Math.max(tmp_width/2, last-tmp_mid);

                // console.log("mid")
                for(let child of node.children) {
                    child.x = child._x - tmp_mid;
                    // console.log("mid", child.x);
                }
            }
        },
        getTreelayoutDown(node, scale) {
            let that = this;
            if(node.children != null && node.children.length>0) {
                for(let child of node.children) {
                    child.x = node.x+child.x*scale;
                    that.getTreelayoutDown(child, scale);
                }
            }
        },
        updateConfideceRange(data) {
            let that = this;
            that.confidence_range[0] = Math.max(that.default_confidence_range[0], Math.min(that.confidence_range[0], data.score));
            that.confidence_range[1] = Math.min(that.default_confidence_range[1], Math.max(that.confidence_range[1], data.score));
            let tmp_children = data.children;
            if(tmp_children != null)
            for(let sub_data of tmp_children) {
                that.updateConfideceRange(sub_data);
            }
        },
        updateTreeLayout(is_zoom=false, fixed_range=false) {
            let that = this;
            
            that.click_ids = [];
            that.click_score = -1;
            let tmp_ids = that.getClickIds(that.click_id);
            if(tmp_ids != null)
                that.click_ids = tmp_ids;
            if(that.click_ids.length>0)that.click_ids = that.click_ids.concat(that.getFocusIds(that.click_id));
            
            if(!fixed_range) {
                // 更新confidence range
                that.confidence_range = [that.default_confidence_range[1], that.default_confidence_range[0]];
                that.hard_confidence_range = [that.default_confidence_range[1], that.default_confidence_range[0]];
                if(that.h_data != null) {
                    that.updateConfideceRange(that.h_data);
                    that.confidence_range[1] = Math.min(1, that.confidence_range[1]+0.1);
                    that.confidence_range[0] = Math.max(0, that.confidence_range[0]-0.1);
                    that.hard_confidence_range = [that.confidence_range[0], that.confidence_range[1]];
                    that.confidence_range[1] += 0.05 * (that.confidence_range[1]-that.confidence_range[0]);
                }
            }
            
            // 计算原上界线位置、对应的confidence，svg底部对应的confidence
            let tmp_top = (that.context_ratio*that.calc_size[1]*that.scale+that.yshift-that.ori_yshift) / (that.calc_size[1]*that.ori_scale);
            that.now_context_ratio = Math.max(0, Math.min(1, tmp_top-0.00001));
            let bottom_value = -(that.calc_size[1]*that.ori_scale-that.calc_size[1]*that.scale+that.ori_yshift-that.yshift)/(that.scale/that.ori_scale*that.calc_size[1]*(1-that.context_ratio));
            let top_value = bottom_value+that.calc_size[1] * (1-that.now_context_ratio) / (that.scale/that.ori_scale*that.calc_size[1]*(1-that.context_ratio));
            // 转换到新confidence范围
            // console.log("y value", bottom_value, top_value);
            bottom_value = bottom_value * (that.confidence_range[1] - that.confidence_range[0]) + that.confidence_range[0];
            top_value = top_value * (that.confidence_range[1] - that.confidence_range[0]) + that.confidence_range[0];

            let top_pos = 0;
            let bottom_pos = that.calc_size[1]*(1-that.now_context_ratio);
            // 底部对应confidence小于0时，提高底部线
            if(bottom_value < 0){
                let tmp = min(-0.00001, top_value-0.00001);
                bottom_pos = bottom_pos * (top_value-tmp) / Math.max(0.00001, (top_value-bottom_value));
                bottom_value = tmp;
            }

            // console.log("y value", bottom_value, top_value, that.ori_scale, that.scale, that.ori_yshift, that.yshift);
            const yScale = d3.scaleLinear()
                .domain([bottom_value, top_value])
                .range([bottom_pos, top_pos]);

            // let lines_data = yScale.ticks(10);
            // let lines_data = yScale.ticks(Math.round(10*(bottom_pos-top_pos)/(that.calc_size[1]*(1-that.context_ratio))));
            let lines_data = yScale.ticks(10*(bottom_pos-top_pos)/(that.calc_size[1]*(1-that.context_ratio)));
            lines_data = lines_data.filter(d => d >= 0 && d <= 1);

            if((that.click_score>=bottom_value)&&(that.click_score<=top_value)){
                lines_data = lines_data.filter(item => Math.abs(that.click_score-item)>(top_value-bottom_value)*0.015);
                lines_data.push(that.click_score);
            }

            // console.log("line_data", lines_data);

            this.svg.select(".y-axis")
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("transform", `translate(${that.padding+24+20}, ${that.ori_yshift+that.calc_size[1]*that.now_context_ratio})`)
            
            let ticks = this.svg.select(".y-axis").selectAll(".tick")
                .data(lines_data, d => d)
            
            ticks.select("text")
                .text(d => {
                    if(d == that.click_score)return d.toFixed(3);
                    return d.toFixed(2);
                })
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("y", d => yScale(d))
                .attr("opacity", 1);
            
            ticks.exit()
                .transition()
                .duration(is_zoom?0:that.remove_time)
                .attr("opacity", 0)
                .remove();
            
            let new_ticks = ticks.enter()
                .append("g")
                .attr("class", "tick");
            
            new_ticks
                .append("text")
                .attr("fill", "black")
                .attr("y", d => yScale(d))
                .attr("dy", "0.32em")
                .attr("opacity", 0)
                .text(d => {
                    if(d == that.click_score)return d.toFixed(3);
                    return d.toFixed(2);
                })
                .transition()
                .duration(is_zoom?0:that.create_time)
                .delay(is_zoom?0:that.remove_time+that.update_time)
                .attr("opacity", 1);
            
            let lines = this.svg.selectAll(".grid-line")
                .data(lines_data, d => d);

            lines
                .transition()
                .duration(is_zoom?0:that.update_time)
                .delay(is_zoom?0:that.remove_time)
                .attr("transform", `translate(${0}, ${that.ori_yshift+that.calc_size[1]*that.now_context_ratio})`)
                .attr("y1", d => yScale(d))
                .attr("y2", d => yScale(d))
                .attr("opacity", 0.5);
            
            lines.enter()
                .append("line")
                .attr("transform", `translate(${0}, ${that.ori_yshift+that.calc_size[1]*that.now_context_ratio})`)
                .attr("class", "grid-line")
                .attr("x1", that.padding+10+24+20)
                .attr("x2", that.svg_width-that.padding-5) 
                .attr("y1", d => yScale(d))
                .attr("y2", d => yScale(d))
                .attr("stroke", "gray") 
                .attr("stroke-dasharray", function(d) {
                    if(d == that.click_score)return "4 4";
                    return "none"
                }) 
                // .attr("stroke-width", 1);
                .attr("stroke-width", 0.5)
                .attr("opacity", 0)
                .transition()
                .duration(is_zoom?0:that.create_time)
                .delay(is_zoom?0:that.remove_time+that.update_time)
                .attr("opacity", 0.5);
            
            lines.exit()
                .transition()
                .duration(is_zoom?0:that.remove_time)
                .attr("opacity", 0)
                .remove();
            
            // that.svg.select(".confidence-area")
            //     .attr("transform", `translate(${0.5}, ${that.ori_yshift+that.calc_size[1]*that.now_context_ratio-0.5})`)
            //     .attr("width", that.svg_width-1)
            //     .attr("height", bottom_pos-top_pos+(that.svg_height-that.ori_yshift-that.calc_size[1]));

            let h_data = that.h_data;
            if(h_data != null) {
                const root = d3.hierarchy(h_data);

                let calc_size = that.calc_size;

                that.getTreelayoutUp(root, h_data.min_weight);

                // if(!fixed_range) {
                if(true) {
                    that.width_ratio = calc_size[0]/(root.data.left_width+root.data.right_width);
                }

                // console.log("width_ratio", that.width_ratio, root.data.left_width+root.data.right_width);

                root.x = root.data.left_width*that.width_ratio;
                that.getTreelayoutDown(root, that.width_ratio);
                
                that.leaf_list = [];
                that.preAdjustTree(root);
                that.initialAdjustTree(root, calc_size);
                that.secondAdjustTree(root);
                that.checkChildOrder(root);

                that.root = root;
                
                // console.log('root', root.descendants());
                that.node_data = root.descendants();
                // console.log("root", that.node_data);
                const node = that.svg_g.selectAll(".node")
                    .data(that.node_data, d=>d.data.name);
                
                that.level_dist = that.calc_size[1];
                that.level_dist = Math.min(that.level_dist, 100);
                for(let node of that.node_data) {
                    if ((node.data.class != "empty") && (node.parent)) {
                        node.parent.level_dist = Math.min(node.parent.level_dist?node.parent.level_dist:that.calc_size[1], Math.abs(node.y - node.parent.y));
                        that.level_dist = Math.min(that.level_dist, Math.abs(node.y - node.parent.y));
                    }
                }

                // if(!fixed_range) {
                if(true) {
                    for(let node of that.node_data) {
                        if(node.children != null && node.children.length>0) {

                        }else if (node.data.class != "empty") {
                            that.width_ratio = min(that.width_ratio, that.svg_width*0.3/node.data.width_weight_focus);

                            let tmp_y = Math.abs(node.y - (calc_size[1] * that.context_ratio - that.axis_top_padding + that.area_padding))
                            // if(!fixed_range) {
                            if(true) {
                                that.width_ratio = min(that.width_ratio, tmp_y/(node.data.width_weight_focus/2));
                            }else {
                                node.data.width_weight_focus = min(node.data.width_weight_focus, tmp_y*2/that.width_ratio);
                            }
                        }
                    }

                    let parent_scale = 1;
                    for(let node of that.node_data) {
                        if(node.children != null && node.children.length>0) {
                            if(false) {
                                that.width_ratio = min(that.width_ratio, that.svg_width*0.3/node.data.width_weight_focus);
                            } else {
                                parent_scale = min(parent_scale, that.svg_width*0.3/that.width_ratio/node.data.width_weight_focus);
                            }

                            let tmp_y = Math.abs(node.y - (calc_size[1] * that.context_ratio - that.axis_top_padding - that.area_padding - that.between_area_padding))
                            if(false) {
                                that.width_ratio = min(that.width_ratio, tmp_y/(node.data.width_weight_focus/2));
                            }else {
                                // node.data.width_weight_focus = min(node.data.width_weight_focus, tmp_y*2/that.width_ratio);
                                parent_scale = min(parent_scale, tmp_y*2/that.width_ratio/node.data.width_weight_focus);
                            }
                        }
                    }
                    for(let node of that.node_data) {
                        if ((node.data.class != "empty") && (node.parent)) {
                            let tmp_y = Math.abs(node.y - node.parent.y);
                            if(!(node.children != null && node.children.length>0)) {
                                continue;
                                // tmp_y = Math.abs(node.parent.y - (node.y - that.area_padding*2 - that.between_area_padding));
                            }
                            if(false) {
                                that.width_ratio = min(that.width_ratio, tmp_y/(node.data.width_weight_focus/2+node.parent.data.width_weight_focus/2));
                            }else {
                                parent_scale = min(parent_scale, tmp_y*2/that.width_ratio/(node.data.width_weight_focus+node.parent.data.width_weight_focus));
                            }
                        }
                    }
                    for(let node of that.node_data) {
                        if(node.children != null && node.children.length>0) {
                            node.data.width_weight_focus *= parent_scale;
                        }
                    }
                }

                that.node_basesize = 0;
                // that.width_ratio = Math.min(that.width_ratio, that.svg_width/h_data.min_weight);
                let node_basesize = that.node_basesize;

                that.confidence_area_top_y1 = that.calc_size[1]*that.context_ratio;
                let tmp_top_pos1 = that.confidence_area_top_y1*that.scale + that.yshift - that.axis_top_padding;
                let tmp_top_pos2 = tmp_top_pos1;
                for(let node of that.node_data) {
                    if(!(node.children != null && node.children.length>0)) {
                        // console.log("???", node.y - node.data.width_weight_focus);
                        let tmp = node.y*that.scale - that.width_ratio*node.data.width_weight_focus/2*Math.sqrt(that.scale) + that.yshift - that.area_padding;
                        tmp_top_pos2 = Math.min(tmp_top_pos2, tmp);
                    }
                }
                
                let tmp_top_pos = Math.min(tmp_top_pos1, tmp_top_pos2);
                tmp_top_pos = Math.max(tmp_top_pos, that.ori_yshift);

                that.svg.select(".confidence-area")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    .attr("transform", `translate(${0.5}, ${tmp_top_pos-0.5})`)
                    .attr("width", that.svg_width-1)
                    .attr("height", bottom_pos-tmp_top_pos+that.ori_yshift+that.calc_size[1]*that.now_context_ratio+(that.svg_height-that.ori_yshift-that.calc_size[1]));

                that.svg.select(".y-axis-title")
                    .transition()
                    .duration(is_zoom?0:that.update_time)
                    .delay(is_zoom?0:that.remove_time)
                    // .attr("transform", `translate(${that.padding+5}, ${tmp_top_pos+10}) rotate(270, 0, 0)`)
                    .attr("transform", `translate(${that.padding+5}, ${bottom_pos+that.ori_yshift+that.calc_size[1]*that.now_context_ratio}) rotate(270, 0, 0)`)
                    .attr("fill", "rgb(140, 155, 180")
                    .text("Confidence score")
                    .attr("opacity", 1);

                // console.log("tree layout", root);

                let lineGenerator = d3.line().curve(d3.curveBasis);

                that.link_data = root.links();

                let links = that.svg_back_g.selectAll(".link")
                    .data(that.link_data, d => { return String(d.source.data.name)+"&"+String(d.target.data.name); });
                
                that.old_links = links;
                // console.log("links", links, root.links());
                links.enter()
                    .append("path")
                    .attr("class", "link")
                    .attr("opacity", 0)
                    .attr("stroke", "#ccc")
                    .attr("fill", "none")
                    .attr("visibility", function(d) {
                        if(d.source.data.class == "empty")return "hidden";
                        if(d.target.data.class == "empty")return "hidden";
                        return null;
                    })
                    .transition()
                    .duration(that.create_time)
                    .delay(that.remove_time+that.update_time)
                    .attrTween("d", d => {
                        let f_data = d.source, c_data = d.target;
                        if(f_data.y > c_data.y) { c_data = d.source; f_data = d.target; }
                        let f_bias = 0;
                        // let f_bias = node_basesize;
                        let c_bias = 0;
                        // let c_bias = node_basesize;
                        const source = [f_data.x*that.scale, f_data.y*that.scale+f_bias*Math.sqrt(that.scale)];
                        const target = [c_data.x*that.scale, c_data.y*that.scale-c_bias*Math.sqrt(that.scale)];
                        // return lineGenerator([source, [source[0], (source[1]*2+target[1])/3], [target[0], (source[1]+target[1]*2)/3], target]);
                        let corner = (that.level_dist-2*that.node_basesize)/2*Math.pow(0.9, d.target.order);
                        let old_path = that.old_last_path[d.target.data.name];
                        that.last_path[d.target.data.name] = [source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3];
                        // console.log("change", old_path, that.last_path[d.target.data.name]);
                        return function(t) {
                            if(old_path == null)
                                return that.generatePathWithArcs(source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3);
                            let new_path = [source[0], source[1], source[0], source[1]+corner, target[0], source[1]+corner, target[0], target[1], (that.level_dist-2*node_basesize)/3];
                            // if((d.target.data._children.length == 2)&&(d.target.depth==1))
                            //     console.log("change", old_path, new_path);
                            for(let i=0;i<new_path.length;i++)
                                new_path[i] = new_path[i]*t + old_path[i]*(1-t);
                            return that.generatePathWithArcs(...new_path);
                        }
                    })
                    .attr("stroke-width", function(d) {
                        if(d.source.data.is_focus) return 4;
                        return 1.5;
                    })
                    .attr("stroke-dasharray", function(d) {
                        let dash = 4;
                        // TODO 修改判定规则
                        if(d.target.data.unselected)
                            return `${dash} ${dash}`
                        return "none";
                    })
                    .attr("opacity", 1);
                
                links.exit()
                    .transition()
                    .duration(that.remove_time)
                    .attr("opacity", 0)
                    .remove();

                const new_node = node.enter()
                    .append("g")
                    .attr("class", "node")
                    .attr("opacity", 0)
                    .attr("transform", d => `translate(${d.x*that.scale},${d.y*that.scale})`)
                    .on('mouseenter', function(e, d) {
                        that.hover_id = d.data.name;

                        that.updateSector(d3.select(this));

                        // that.$emit('click-node', d.data.name);
                        that.emitHover(d.data.name, 500);
                        // that.updateTree();
                    })
                    .on('mouseleave', function(e, d) {
                        that.hover_id = -1;
                        // if((d.data.name==that.click_id)&&(d.data._children==null||d.data._children.length==0))
                        //     that.click_id = -1;

                        that.updateSector(d3.select(this));

                        // that.$emit('click-node', that.click_id);
                        if((d.data.name==that.click_id)&&(d.data._children==null||d.data._children.length==0))
                            that.emitHover(-1);
                        else
                            that.emitHover(that.click_id);
                        
                        // that.updateTree();
                    })
                    .on('click', function(e, d) {
                        that.updateClick(d.data.name);
                    })
                    .on('dblclick', function(e, d) {
                        that.updateDoubleClick(d.data.name);
                    })
                    .style("cursor", "pointer");
                
                new_node.transition()
                    .duration(that.create_time)
                    .delay(that.remove_time+that.update_time)
                    .attr("opacity", 1);

                let circle_g = new_node.append("g")
                    .attr("class", "circle_g")
                    .attr("opacity", 0)
                circle_g.append("circle")
                    .attr("class", "circle-middle");
                circle_g.append("circle")
                    .attr("class", "circle-outer");
                
                circle_g.each(function(d) {
                    // console.log("circle", d);
                    let now_group = d3.select(this);

                    let sector_g = now_group.selectAll(".sector_g")
                        .data(d.data.all_children, d2 => d2.node.name);
                    let new_sector_g = sector_g.enter()
                        .append("g")
                        .attr("class", "sector_g");
                    new_sector_g.append("path")
                        .attr("class", "sector")
                        .on('mouseenter', function(e, d2) {
                            e.preventDefault();
                            e.stopPropagation();
                            that.hover_id = d2.node.name;

                            that.updateSector(d3.select(this.parentNode.parentNode.parentNode));
                            // console.log(d3.select(this.parentNode.parentNode.parentNode));

                            // that.$emit('click-node', d2.node.name);
                            that.emitHover(d2.node.name, 500);
                        })
                        .on('mouseleave', function(e, d2) {
                            e.preventDefault();
                            e.stopPropagation();
                            that.hover_id = d.data.name;
                            
                            that.updateSector(d3.select(this.parentNode.parentNode.parentNode));
                            // console.log(d3.select(this.parentNode.parentNode.parentNode));

                            // that.$emit('click-node', d.data.name);
                            that.emitHover(d.data.name, 500);
                        })
                        .on('click', function(e, d2) {
                            // console.log("click", d2.node.name);
                            e.preventDefault();
                            e.stopPropagation();

                            that.updateClick(d2.node.name, d.data.name);
                        });
                    
                    new_sector_g.append("circle")
                        .attr("class", "sector_circle")
                        .on('mouseenter', function(e, d2) {
                            e.preventDefault();
                            e.stopPropagation();
                            that.hover_id = d2.node.name;

                            that.updateSector(d3.select(this.parentNode.parentNode.parentNode));

                            that.emitHover(d2.node.name, 500);
                        })
                        .on('mouseleave', function(e, d2) {
                            e.preventDefault();
                            e.stopPropagation();
                            that.hover_id = d.data.name;
                            
                            that.updateSector(d3.select(this.parentNode.parentNode.parentNode));

                            that.emitHover(d.data.name, 500);
                        })
                        .on('click', function(e, d2) {
                            e.preventDefault();
                            e.stopPropagation();

                            that.updateClick(d2.node.name, d.data.name);
                        });

                    let tmp_d = [0, 0.25, 0.50, 0.75, that.thres];
                    // let tmp_d = [0, 0.25, 0.50, 0.75];
                    let axis_g = now_group.selectAll(".axis_g")
                        .data(tmp_d);
                    let new_axis_g = axis_g.enter()
                        .append("g")
                        .attr("class", (d2, i) => `axis_g axis-${i}`);
                    new_axis_g.append("circle")
                        .attr("class", (d2, i) => `axis-circle circle-${i}`)
                        .attr("fill", "none")
                        .attr("stroke", "gray")
                        .attr("opacity", 0.5)
                        .attr("stroke-width", (d) => d==that.thres?1.5:0.5);
                    new_axis_g.append("text")
                        .attr("class", (d2, i) => `axis-text text-${i}`)
                        .attr("color", "black")
                        .attr("text-anchor", "middle")
                        .attr("dy", ".35em")
                        .text(d2 => d2==0?d2:d2.toFixed(2))
                        .attr("visibility", "hidden");
                })

                let edit_group = new_node
                    .append('g')
                    .attr("class", "edit_g")
                    .attr("opacity", 0);
                
                edit_group
                    .append('path')
                    .attr("class", "inc")
                    .style("cursor", "pointer")
                    .attr("d", "M512 0C230.4 0 0 230.4 0 512s230.4 512 512 512 512-230.4 512-512S793.6 0 512 0z m224 544h-192v192c0 19.2-12.8 32-32 32s-32-12.8-32-32v-192H288c-19.2 0-32-12.8-32-32s12.8-32 32-32h192V288c0-19.2 12.8-32 32-32s32 12.8 32 32v192h192c19.2 0 32 12.8 32 32s-12.8 32-32 32z")
                    // .attr("fill", "rgb(9, 69, 254")
                    .attr("fill", "#838383")
                    .attr("stroke", function(d) {
                        return "white";
                    })
                    .attr("stroke-width", 0.1*1024)
                    .on('click', (e, d) => {
                        e.stopPropagation();
                        that.scoreEdit(e, d, 3/2);
                    })
                    .attr("transform", function(d) {
                        let tmp = 16;
                        return `scale(${tmp/1024}) translate(${0*1024}, ${-1*1024})`;
                    });
                
                edit_group
                    .append('path')
                    .attr("class", "dec")
                    .style("cursor", "pointer")
                    .attr("d", "M512 0C230.4 0 0 230.4 0 512s230.4 512 512 512 512-230.4 512-512S793.6 0 512 0z m204.8 563.2H307.2c-30.72 0-51.2-20.48-51.2-51.2s20.48-51.2 51.2-51.2h409.6c30.72 0 51.2 20.48 51.2 51.2s-20.48 51.2-51.2 51.2z m0 0")
                    // .attr("fill", "rgb(9, 69, 254")
                    .attr("fill", "#838383")
                    .attr("stroke", function(d) {
                        return "white";
                    })
                    .attr("stroke-width", 0.1*1024)
                    .on('click', (e, d) => {
                        e.stopPropagation();
                        that.scoreEdit(e, d, 2/3);
                    })
                    .attr("transform", function(d) {
                        let tmp = 16;
                        return `scale(${tmp/1024}) translate(${1.2*1024}, ${-1*1024})`;
                    });
                
                node.exit()
                    .transition()
                    .duration(that.remove_time)
                    .attr("opacity", 0)
                    .remove();

                that.svg.on("click", function(event) {
                    const rect = that.svg.node().getBoundingClientRect();
                    const x = event.clientX - rect.left;
                    const y = event.clientY - rect.top;
                    if(that.is_zoom!=0) {
                        that.ImageZoom(x, y, 2*that.is_zoom);
                        return;
                    }
                    if (event.target.tagName === "svg") {
                        that.click_id = -1;
                        // that.$emit('click-node', -1);
                        that.emitClick(-1);

                        that.updateTree();
                    }
                });
            }
        },
        nodeExpand(node, name) {
            let find = false;
            if(node.name == name)
                find = true
            for(let child of node._children) {
                if(this.nodeExpand(child, name))
                    find = true;
            }
            if(find) {
                node.expand = true;
            }
            return find;
        },
        nodeFullExpand(node, name, father_find=false) {
            if(node.name == name)
                father_find = true
            let find = father_find;
            for(let child of node._children) {
                if(this.nodeFullExpand(child, name, father_find))
                    find = true;
            }
            if(find) {
                node.expand = true;
            }
            return find;
        },
        nodeFullTmpExpand(node, name, father_find=false) {
            if(node.name == name)
                father_find = true
            let find = father_find;
            for(let child of node._children) {
                if(this.nodeFullTmpExpand(child, name, father_find))
                    find = true;
            }
            if(find) {
                node.tmp_expand = true;
            }else {
                node.tmp_expand = false;
            }
            return find;
        },
        nodeClose(node, name, find=false) {
            if(node.name == name)
                find = true;
            for(let child of node._children) {
                this.nodeClose(child, name, find);
            }
            if(find) {
                node.expand = false;
            }
        },
        resetNode(){
            let that = this;
            that.tot_weight = 0;
            that.focus_weight = 0;
            that.max_focus_weight = 0;
            that.resetNodeFocus(that.h_data, false, that.click_parent_id, false);
            that.resetNodeExpand(that.h_data);
            let tmp_r = 2/3, tmp_r2 = 1/3;
            that.focus_ratio = 4;
            that.focus_ratio = Math.max(that.focus_ratio, tmp_r*(that.tot_weight-that.focus_weight)/Math.max(0.000001, that.focus_weight*(1-tmp_r)));
            that.focus_ratio = Math.max(2, Math.min(that.focus_ratio, tmp_r2*(that.tot_weight-that.max_focus_weight)/Math.max(0.000001, that.max_focus_weight*(1-tmp_r2))));
            
            // console.log("focus_ratio", that.focus_ratio, that.tot_weight, that.focus_weight, that.max_focus_weight);
            that.resetWeight(that.h_data);
        },
        resetNodeFocus(node, father_find=false, pid=-1, father_find2=false) {
            if(node.name == this.focus_id)
                father_find = true;
            if(node.name == pid)
                father_find2 = true;
            let find = father_find;
            for(let child of node._children) {
                if(this.resetNodeFocus(child, father_find, pid, father_find2)) {
                    if(father_find2)
                        find = true;
                }
            }
            if(find) {
                node.is_focus = true;
            }else {
                node.is_focus = false;
            }
            return find;
        },
        resetWeight(node){
            let that = this;

            node.width_weight_focus = node.width_weight;
            if(node.is_focus)node.width_weight_focus *= that.focus_ratio;
            // if(node.children != null && node.children.length>0) node.width_weight_focus /= 2;

            node.separation_weight = [node.width_weight_focus, 0];
            node.min_weight = node.width_weight_focus;

            node.all_children = [{"node": node, "ratio": 1, "bias": 0, "parent": node}];

            for(let child of node._children) {
                this.resetWeight(child);
            }

            if(node._children != null && node._children.length>0) {

                node.all_children = [];
                let max_ratio = 0, min_ratio = 10000000;
                let scale_min = 1/5;
                for(let child of node._children) {
                    for(let obj of child.all_children) {
                        node.all_children.push({"node": obj.node, "ratio": obj.node.width_weight, "bias": 0, "parent": node});
                        max_ratio = Math.max(max_ratio, obj.node.width_weight);
                        min_ratio = Math.min(min_ratio, obj.node.width_weight);
                    }
                }
                
                for(let i=0;i<node.all_children.length;i++)
                for(let j=i+1;j<node.all_children.length;j++) {
                    let order1 = that.class_order[node.all_children[i].node.class];
                    let order2 = that.class_order[node.all_children[j].node.class];
                    let flag = false;
                    if(order1 > order2) flag = true;
                    if(!that.isShowInfluence) {
                        if((order1 == order2)&&(node.all_children[i].node.score<node.all_children[j].node.score)) flag = true;
                    } else {
                        if((order1 == order2)&&(node.all_children[i].node.influence<node.all_children[j].node.influence)) flag = true;
                    }
                    if(flag) {
                        let tmp = node.all_children[i];
                        node.all_children[i] = node.all_children[j];
                        node.all_children[j] = tmp;
                    }
                }

                let tot_ratio = 0, bias = 0;
                for(let obj of node.all_children){
                    if(min_ratio/max_ratio < scale_min) {
                        obj.ratio = (obj.ratio-min_ratio)/(max_ratio-min_ratio)*(1-scale_min) + scale_min;
                    }
                    tot_ratio += obj.ratio;
                }
                // console.log("all_children", node.all_children, tot_ratio, max_ratio, min_ratio);
                
                let padding_ratio = min(0.5, 0.04*node.all_children.length);
                for(let obj of node.all_children){
                    obj.ratio = obj.ratio/tot_ratio*(1-padding_ratio);
                    obj.bias = bias;
                    bias += obj.ratio + padding_ratio/Math.max(1, node.all_children.length);
                }
            }
            if(node.children != null && node.children.length>0) {
                node.separation_weight = [0, 0];
                let first_flag = true;
                for(let child of node.children) {
                    node.min_weight = min(node.min_weight, child.min_weight);
                }
            }
        },
        resetNodeExpand(node, parent_expand=true) {
            let that = this;

            node.width_weight_o = node.area;
            node.width_weight = Math.sqrt(Math.sqrt(node.width_weight_o));
            
            let expand = node.expand||node.tmp_expand;
            if(expand) {
                node.children = node._children;
            }else {
                node.children = null;
            }
            for(let child of node._children) {
                this.resetNodeExpand(child, expand);
            }

            if(node._children != null && node._children.length>0) {
                let tmp_weight_o = 0;
                for(let child of node._children) {
                    tmp_weight_o += child.width_weight_o;
                }
                // node.width_weight_o = max(node.width_weight_o, tmp_weight_o);
                node.width_weight_o = tmp_weight_o;

                node.width_weight = Math.sqrt(Math.sqrt(node.width_weight_o));
            }
            
            if((parent_expand)&&(node.children == null || node.children.length==0)) {
                if(node.is_focus) {
                    that.focus_weight += node.width_weight;
                    that.max_focus_weight = Math.max(that.max_focus_weight, node.width_weight);
                }
                that.tot_weight += node.width_weight;
            }
        },
        nodeDistUp(node, name) {
            node.dist = 10000;
            if(node.name == name) {
                node.dist = 0;
            }
            for(let child of node._children) {
                let child_dist = this.nodeDistUp(child, name)
                node.dist = min(node.dist, child_dist+1);
            }
            return node.dist;
        },
        nodeDistDown(node, father_dist) {
            node.dist = min(node.dist, father_dist+1);
            for(let child of node._children) {
                this.nodeDistDown(child, node.dist)
            }
        },
        nodeDfs(node, name) {
            let find = false;
            if(node.name == name)
                find = true;
            let node_list = [];
            let expanded_node_list = [];
            if(node.expand) {
                for(let child of node._children) {
                    let [child_node_list, child_expanded_node_list, child_find] = this.nodeDfs(child, name);
                    node_list = node_list.concat(child_node_list);
                    expanded_node_list = expanded_node_list.concat(child_expanded_node_list);
                    if(child_find)
                        find = true;
                }
                if(!find)
                    expanded_node_list.push(node)
            }
            node_list.push(node)
            return [node_list, expanded_node_list, find];
        },
        nodeTrim(h_data, name, max_cnt=5) {
            this.nodeDistUp(h_data, name);
            this.nodeDistDown(h_data, 10000);
            while(true) {
                let [node_list, expanded_node_list, find] = this.nodeDfs(h_data, name);
                // console.log("node number", node_list, expanded_node_list);
                if((node_list.length>max_cnt)&&(expanded_node_list.length>0)) {
                    let now_node = null;
                    for(let node of expanded_node_list) {
                        if((now_node == null)||(node.dist>now_node.dist)||((node.dist==now_node.dist)&&(node.child_names.length<now_node.child_names.length)))
                            now_node = node;
                    }
                    this.nodeClose(now_node, now_node.name);
                }else break;
            }
        },
        ImageZoom(x, y, zoom) {
            // let that = this;
            // const scaleBefore = that.scale;
            // const zoomFactor = 0.2;
            // that.scale *= 1+zoom*zoomFactor;
            // that.scale = Math.max(1, that.scale);

            // that.xshift = x + (that.xshift - x)*that.scale/scaleBefore;
            // that.yshift = y + (that.yshift - y)*that.scale/scaleBefore; 

            // that.updateTree(true);
        },
        newLayout(item) {
            let that = this;
            that.old_last_path = {};
            that.last_path = {};
            that.selectedCategory = item.category;
            if(that.svg == null)return;

            that.scale = 1;
            that.xshift = that.ori_xshift;
            that.yshift = that.ori_yshift;
            this.svg_g.attr("transform", "translate("+this.xshift+","+this.yshift+")");
            
            that.confidence_range = [that.default_confidence_range[0], that.default_confidence_range[1]];
            that.hard_confidence_range = [that.confidence_range[0], that.confidence_range[1]];

            that.svg.on("wheel", (event) => {
                const rect = that.svg.node().getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                that.ImageZoom(x, y, event.deltaY<0 ? 1 : -1);
            });

            let drag_offsetX = 0;
            let drag_offsetY = 0;

            const ImageMoveStartEnd = function(e, d) {
                if(that.no_drag) return;
                if(e.type=='start') {
                    drag_offsetX = e.x - that.xshift;
                    drag_offsetY = e.y - that.yshift;
                }
            };

            const ImageMoving = function(e, d) {
                if(that.no_drag) return;
                that.xshift = e.x - drag_offsetX;
                that.yshift = e.y - drag_offsetY;
                that.updateTree();
            };

            that.svg.call(d3.drag()
                .container(that.svg.node())
                .on('start end', ImageMoveStartEnd)
                .on('drag', ImageMoving),
            );

            // console.log("item", item);

            let id_cnt = 0;
            let boxes = item.boxes.map(function(d) {
                id_cnt += 1;
                return {
                    id: id_cnt-1,
                    area: d.width*d.height,
                    bbox: [d.x, d.y, d.width, d.height],
                    type: 'pred',
                    class: d.class,
                    score: d.score,
                    iscrowd: 0,
                    unselected: d.unselected
                };
            });
            that.max_deep = 0;

            // let max_influence = 0;
            // if("influence_within" in item) {
            //     for(let i=0;i<item["influence_within"].length;i++)
            //         max_influence = Math.max(max_influence, item["influence_within"][i].length)
            // }

            let h_data = null;
            id_cnt = 10000;
            function dfs(hierarchy, deep) {
                if(typeof hierarchy === 'number') {
                    // if(["text", "Annotation", "Title", "Source"].includes(boxes[hierarchy].class))return null;
                    if(!that.show_node[that.categories_dict[boxes[hierarchy].class].super]["show"])return null;

                    boxes[hierarchy].deep = deep;
                    let category_cnt = {};
                    let category_area = {};
                    for(let key in that.categories_dict){
                        category_cnt[key] = 0;
                        category_area[key] = 0;
                    }
                    category_cnt[boxes[hierarchy].class] = 1;
                    category_area[boxes[hierarchy].class] = Math.sqrt(boxes[hierarchy].area);
                    let category_weight = category_area;
                    let tmp_cnt = Object.values(category_weight).reduce((acc, val) => acc + val, 0);
                    let result = {"name": boxes[hierarchy].id, "area": boxes[hierarchy].area, "bbox": boxes[hierarchy].bbox, "deep": deep, "class": boxes[hierarchy].class, "child_index": [hierarchy], "child_names": [boxes[hierarchy].id], "child_names2": [boxes[hierarchy].id], "expand": false, "_children": [], "tmp_expand": false, "category_cnt": category_cnt, "category_area": category_area, "layers": 0, "category_weight": category_weight, "cnt": tmp_cnt};
                    result["score"] = boxes[hierarchy].score;
                    result["unselected"] = boxes[hierarchy].unselected;
                    result["influence"] = Math.random();
                    // if("influence_within" in item) {
                    //     result["influence"] = item["influence_within"][hierarchy].length/Math.max(max_influence, 1);
                    // }
                    // console.log("?", that.$parent.$parent.selectedInfluence, hierarchy);
                    result["influence"] = that.$parent.$parent.selectedInfluence[hierarchy]?that.$parent.$parent.selectedInfluence[hierarchy].quantile:0;
                    return result;
                }
                id_cnt += 1;
                let tmp = {
                    name: id_cnt-1,
                    area: hierarchy.width*hierarchy.height,
                    bbox: [hierarchy.x, hierarchy.y, hierarchy.width, hierarchy.height],
                    deep: hierarchy.deep,
                    class: 'group',
                    _children: [],
                    children: null,
                    expand: false,
                    tmp_expand: false,
                    child_index: [],
                    child_names: [id_cnt-1],
                    child_names2: [],
                    category_cnt: {},
                    category_area: {},
                    category_weight: {},
                    layers: 0,
                }
                for(let key in that.categories_dict){
                    tmp.category_cnt[key] = 0;
                    tmp.category_area[key] = 0;
                    tmp.category_weight[key] = 0;
                }
                that.max_deep = Math.max(that.max_deep, hierarchy.deep);
                for(let child of hierarchy.children) {
                    let tmp_child = dfs(child, hierarchy.deep-1);
                    if(tmp_child == null) continue;
                    tmp._children.push(tmp_child);
                    tmp.child_index = tmp.child_index.concat(tmp_child.child_index);
                    tmp.child_names = tmp.child_names.concat(tmp_child.child_names);
                    tmp.child_names2 = tmp.child_names2.concat(tmp_child.child_names2);
                    for(let key in tmp_child.category_cnt) {
                        tmp.category_cnt[key] += tmp_child.category_cnt[key];
                        tmp.category_area[key] += tmp_child.category_area[key];
                        tmp.category_weight[key] += tmp_child.category_weight[key];
                    }
                    tmp.layers = max(tmp.layers, tmp_child.layers+1);
                    tmp.cnt = Object.values(tmp.category_weight).reduce((acc, val) => acc + val, 0);
                }
                
                if(tmp._children.length == 0) return null;
                if(tmp._children.length == 1) return tmp._children[0];

                let score_avg = 0;
                for(let i=0;i<tmp.child_index.length;i++) {
                    score_avg += boxes[tmp.child_index[i]].score;
                }
                tmp.score = score_avg / Math.max(1, tmp.child_index.length);

                // tmp.influence = Math.random();

                tmp.unselected = true;
                for(let i=0;i<tmp.child_index.length;i++) {
                    if(!boxes[tmp.child_index[i]].unselected)tmp.unselected = false;
                }

                for(let i=0;i<tmp._children.length-1;i++)
                for(let j=i+1;j<tmp._children.length;j++){
                    let flag = false;
                    if((tmp._children[i].unselected)&&(!tmp._children[j].unselected))
                        flag = true;
                    else if (((!tmp._children[i].unselected)&&(!tmp._children[j].unselected))||((tmp._children[i].unselected)&&(tmp._children[j].unselected))) {
                        let box1 = tmp._children[i].bbox;
                        let box2 = tmp._children[j].bbox;
                        // console.log("sort", box1, box2);
                        // if((box1[1]>box2[1])||((box1[1]==box2[1])&&(box1[0]>box2[0]))||((box1[1]==box2[1])&&(box1[0]==box2[0])&&(box1[3]<box2[3]))) {
                        if(box1[0]+box1[1]>box2[0]+box2[1]) {
                            flag = true;
                        }
                    }
                    if(flag) {
                        let t = tmp._children[i];
                        tmp._children[i] = tmp._children[j];
                        tmp._children[j] = t;
                    }
                }
                return tmp;
            }
            if(item.hierarchy != null) {
                h_data = dfs(item.hierarchy, item.hierarchy.deep);
            }
            if((h_data == null)&&(boxes.length >= 1)) {
                let category_cnt = {};
                let category_area = {};
                for(let key in that.categories_dict){
                    category_cnt[key] = 0;
                    category_area[key] = 0;
                }
                category_cnt[boxes[0].class] = 1;
                category_area[boxes[0].class] = Math.sqrt(boxes[0].area);
                let category_weight = category_area;
                let tmp_cnt = Object.values(category_weight).reduce((acc, val) => acc + val, 0);
                h_data = {"name": boxes[0].id, "area": boxes[0].area, "bbox": boxes[0].bbox, "deep": 0, "class": boxes[0].class, "child_index": [0], "child_names": [boxes[0].id], "child_names2": [boxes[0].id], "expand": false, "_children": [], "tmp_expand": false, "category_cnt": category_cnt, "category_area": category_area, "category_weight": category_weight, "layers": 0, "cnt": tmp_cnt}
                h_data["score"] = boxes[0].score;
                h_data["influence"] = Math.random();
                // if("influence_within" in item) {
                //     h_data["influence"] = item["influence_within"][0].length/Math.max(max_influence, 1);
                // }
                h_data["influence"] = that.$parent.$parent.selectedInfluence[0].quantile;
                h_data["unselected"] = boxes[0].unselected;
            }

            // that.nodeExpand(h_data, h_data.name);
            that.nodeFullExpand(h_data, h_data.name);
            that.nodeTrim(h_data, h_data.name);

            that.h_data = h_data;
            that.boxes = boxes;

            that.resetNode();
            // console.log("hierarchy", h_data);
            
            that.svg_back_g.selectAll(".link").remove();

            that.svg_g.selectAll(".node").remove();

            that.updateTree();
        },
        drawLegend() {
            let that = this;
            that.color_legend_svg = d3.select(".color-legend");
            that.legend_svg = d3.select(".tree-legend");

            let color_legend_svgsize = that.color_legend_svg.node().getBoundingClientRect();
            let stroke_width = 0;
            let check_stroke_width = 1;
            let legend_size = 20;
            legend_size = min(min(20, color_legend_svgsize.height/3), color_legend_svgsize.width/17);

            that.show_node = {};
            for(let i=0;i<that.categories_super.length;i++) {
                that.show_node[that.categories_super[i]["text"]] = that.categories_super[i];
            }

            for(let i=0;i<that.categories_super.length;i++) {
                that.categories_super[i].tree_y = i/(that.categories_super.length-1)*(color_legend_svgsize.height - stroke_width - legend_size);
            }
            const legend = that.color_legend_svg.selectAll(".legend")
                .data(that.categories_super)
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", (d, i) => `translate(0, ${d.tree_y})`);

            const group = legend.append("g");
            group.append("rect")
                .attr("x", check_stroke_width/2)
                .attr("y", legend_size-1/3*legend_size-legend_size*3/5/2)
                .attr("class", "box")
                .attr("width", legend_size*3/5)
                .attr("height", legend_size*3/5)
                .attr("rx", legend_size*3/20)
                .attr("ry", legend_size*3/20)
                .attr("fill", "white")
                .attr("stroke", "#444")
                .attr("stroke-width", check_stroke_width);
            const check = group.append("path")
                .attr("class", "check")
                .attr("transform", function(d) {
                    let tmp = legend_size*3/5;
                    return `scale(${tmp/1024}) translate(${(check_stroke_width/2)/(legend_size*3/5)*1024}, ${(legend_size-1/3*legend_size-legend_size*3/5/2)/(legend_size*3/5)*1024})`;
                })
                .attr("d", "M479.287 761.117c-28.762 28.039-75.489 28.039-104.251 0l-234.739-229.703c-28.762-28.039-28.762-74.052 0-102.087s75.489-28.039 104.251 0l182.615 178.658 351.927-344.736c28.762-28.039 75.489-28.039 104.251 0s28.762 74.052 0 102.087l-404.048 395.781z")
                .attr("stroke", "#0074D9")
                .attr("stroke-width", check_stroke_width)
                .attr("stroke-linecap", "round")
                .attr("stroke-linejoin", "round")
                .style("display", d => that.show_node[d.text]["show"] ? null : "none");
            group.on("click", function(event, d) {
                that.show_node[d.text]["show"] = !that.show_node[d.text]["show"];
                d3.select(this)
                    .select(".check")
                    .style("display", d2 => that.show_node[d2.text]["show"] ? null : "none");
                that.load(that.item);
            });

            legend.append("circle")
                .attr("cx", (stroke_width+legend_size)*1/3 + 1*legend_size)
                .attr("cy", stroke_width+legend_size-1/3*legend_size-stroke_width/2)
                .attr("r", legend_size*1/3)
                .attr("fill", d => d.color)
                .attr("stroke-width", stroke_width)
                .attr("stroke", d => d.color)
                .attr("opacity", 0.9);
            legend.append("circle")
                .attr("cx", (stroke_width+legend_size)*1/3 + legend_size + 1*legend_size)
                .attr("cy", stroke_width+legend_size-1/3*legend_size-stroke_width/2)
                .attr("r", legend_size*1/3)
                .attr("fill", d => d.color)
                .attr("stroke-width", stroke_width)
                .attr("stroke", d => d.color)
                .attr("opacity", 0.5);
            legend.append("text")
                .attr("x", stroke_width/2 + 2*legend_size + 1*legend_size)
                .attr("y", stroke_width+legend_size-1/3*legend_size-stroke_width/2)
                .attr("dy", '.35em')
                .text(d => "Selected / Unselected "+d.text)
                .attr("font-size", legend_size*4/5);
            
            that.legend_svg.append("defs").selectAll("marker")
                .data(["arrow-start", "arrow-end"])
                .enter().append("marker")
                .attr("id", d => d)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", d => d === "arrow-start" ? 0 : 10)
                .attr("refY", 0)
                .attr("markerWidth", 5)
                .attr("markerHeight", 5)
                .attr("orient", "auto")
                .append("path")
                .attr("d", d => d === "arrow-start" ? "M10,-5 L00,0 L10,5" :"M0,-5 L10,0 L0,5")
                .style("fill", "black");
            
            that.legend_svgsize = that.legend_svg.node().getBoundingClientRect();
            that.legend_svg_width = that.legend_svgsize.width;
            that.legend_svg_height = that.legend_svgsize.height;

            let full_radius = Math.min(that.legend_svg_width*2/5, that.legend_svg_height*0.95);
            let parent_radius = that.circle_ratio*full_radius;
            let middle_radius = Math.min(3, parent_radius/6)

            let legend_start_points = [null, null, null, null];
            let legend_end_points = [null, null, null, null];
            for(let i=0;i<4;i++) {
                legend_end_points[i] = {x: full_radius*2, y: that.legend_svg_height*(i*2+1)/8};
            }

            let legend_circle_g = that.legend_svg.append("g")
                .attr("class", "legend_circle_g")
                .attr("transform", d => `translate(${full_radius},${that.legend_svg_height})`)

            legend_circle_g.append("circle")
                .attr("class", "circle-middle")
                .attr("fill", "gray")
                .attr("stroke", function() {
                    return "gray";
                })
                .attr("stroke-width", function() {
                    return 1;
                })
                .attr("r", middle_radius)

            legend_circle_g.append("circle")
                .attr("class", "circle-outer").attr("fill", "transparent")
                .attr("stroke", function() {
                    return "gray";
                })
                .attr("stroke-width", function() {
                    return 1;
                })
                .attr("r", parent_radius);
            
            let r_bias = middle_radius + (parent_radius-middle_radius)*0.1;
            let a_bias = 0;

            const arcGenerator = d3.arc()
                .innerRadius(r_bias);

            let legend_sector_g = legend_circle_g.selectAll(".legend_sector_g")
                .data([{node: {name: 0, score: 0.45, influence: 0.9}, bias: 0.925, ratio: 0.15}], d2 => d2.node.name);
            
            let new_legend_sector_g = legend_sector_g.enter()
                .append("g")
                .attr("class", "legend_sector_g");

            new_legend_sector_g
                .append("path")
                .attr("class", "sector")
                .attr("fill", function(d2) {
                    let cls = Object.keys(that.categories_dict)[Object.keys(that.categories_dict).length-1];
                    let color = d3.color(that.categories_dict[cls]["color"]);
                    color.opacity = 0.9;
                    let tmp_thres = that.thres;
                    if("thres" in that.categories_dict[cls]) tmp_thres = that.categories_dict[cls]["thres"];
                    if(d2.node.score<tmp_thres)
                        color.opacity = 0.5;
                    return color.toString();
                })
                .attr("stroke", function(d2) {
                    let color = d3.color("black");
                    return color.toString();
                })
                .attr("stroke-dasharray", function(d2) {
                    return "none";
                })
                .attr("stroke-width", function(d2) {
                    let stroke = 0.75;
                    return stroke;
                })
                .attr("d", function(d2) {
                    let tmp_score = d2.node.score;
                    return arcGenerator
                        .outerRadius(parent_radius*tmp_score+r_bias*(1-tmp_score))
                        .startAngle(2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio)))
                        .endAngle(2*Math.PI*(1-a_bias-(1-2*a_bias)*d2.bias))();
                });
            
            function getArc(radius, startAngle, endAngle) {
                const polarToCartesian = (centerX, centerY, radius, angle) => ({
                    x: centerX + radius * Math.cos(-Math.PI/2+angle),
                    y: centerY + radius * Math.sin(-Math.PI/2+angle)
                });
                const start = polarToCartesian(0, 0, radius, startAngle);
                const end = polarToCartesian(0, 0, radius, endAngle);
                const middle = polarToCartesian(0, 0, radius, (startAngle+endAngle)/2);

                const arcPath = `
                    M ${start.x} ${start.y}
                    A ${radius} ${radius} 0 0 1 ${end.x} ${end.y}
                `;
                return { arcPath, middle };
            }
            
            const polarToCartesian = (centerX, centerY, radius, angle) => ({
                x: centerX + radius * Math.cos(-Math.PI/2+angle),
                y: centerY + radius * Math.sin(-Math.PI/2+angle)
            });
            
            function getRadius(radius1, radius2, startAngle, maxR) {
                const start = polarToCartesian(0, 0, radius1, startAngle);
                const end = polarToCartesian(0, 0, radius2, startAngle);

                let dir = [-(end.y-start.y), (end.x-start.x)];
                let length = Math.sqrt(dir[0]*dir[0]+dir[1]*dir[1]);
                dir[0] /= length; dir[1] /= length;
                start.x += dir[0] * 0.1 * maxR;
                start.y += dir[1] * 0.1 * maxR;
                end.x += dir[0] * 0.1 * maxR;
                end.y += dir[1] * 0.1 * maxR;
                const middle = {x: (start.x+end.x)/2, y: (start.y+end.y)/2};

                const linePath = `
                    M ${start.x} ${start.y}
                    L ${end.x} ${end.y}
                `;
                return { linePath, middle };
            }

            new_legend_sector_g
                .append("path")
                .attr("class", "sector-arc")
                .attr("stroke", function(d2) {
                    let color = d3.color("black");
                    return color.toString();
                })
                .attr("stroke-width", function(d2) {
                    return 0.67;
                })
                .attr("d", function(d2) {
                    let tmp_score = d2.node.score+0.1;
                    let result = getArc(parent_radius*tmp_score+r_bias*(1-tmp_score), 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio)),2*Math.PI*(1-a_bias-(1-2*a_bias)*d2.bias));
                    legend_start_points[1] = {x: result.middle.x+full_radius, y: result.middle.y+that.legend_svg_height};
                    return result.arcPath;
                })
                .attr("fill", "none")
                .attr("marker-start", "url(#arrow-start)")
                .attr("marker-end", "url(#arrow-end)");
            
            new_legend_sector_g
                .append("path")
                .attr("class", "sector-radius")
                .attr("stroke", function(d2) {
                    let color = d3.color("black");
                    return color.toString();
                })
                .attr("stroke-width", function(d2) {
                    return 0.67;
                })
                .attr("d", function(d2) {
                    let tmp_score = d2.node.score;
                    let result = getRadius(r_bias, parent_radius*tmp_score+r_bias*(1-tmp_score), 2*Math.PI*(1-a_bias-(1-2*a_bias)*d2.bias), parent_radius-r_bias);
                    legend_start_points[2] = {x: result.middle.x+full_radius, y: result.middle.y+that.legend_svg_height};
                    return result.linePath;
                })
                .attr("fill", "none")
                .attr("marker-start", "url(#arrow-start)")
                .attr("marker-end", "url(#arrow-end)");
            
            new_legend_sector_g.append("circle")
                .attr("class", "sector_circle")
                .attr("fill", function(d2) {
                    let cls = Object.keys(that.categories_dict)[Object.keys(that.categories_dict).length-1];
                    let color = d3.color(that.categories_dict[cls]["color"]);
                    color.opacity = 0.9;
                    let tmp_thres = that.thres;
                    if("thres" in that.categories_dict[cls]) tmp_thres = that.categories_dict[cls]["thres"];
                    if(d2.node.score<tmp_thres)
                        color.opacity = 0.4;
                    return color.toString();
                })
                .attr("stroke", function(d2) {
                    let color = d3.color("black");
                    return color.toString();
                })
                .attr("stroke-dasharray", function(d2) {
                    return "none";
                })
                .attr("stroke-width", function(d2) {
                    let stroke = 0.75
                    return stroke;
                })
                .attr("transform", function(d2) {
                    let angle = 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio/2));
                    let tmp_score = d2.node.influence;
                    let r = full_radius - (full_radius-parent_radius)/2*tmp_score;
                    let x = r * Math.sin(angle);
                    let y = -r * Math.cos(angle);
                    return `translate(${x},${y})`
                })
                .attr("r", function(d2) {
                    let tmp_score = d2.node.influence;
                    return (full_radius-parent_radius)/2 * tmp_score;
                });
            
            new_legend_sector_g
                .append("path")
                .attr("class", "sector-circle-line")
                .attr("stroke", function(d2) {
                    let color = d3.color("black");
                    return color.toString();
                })
                .attr("stroke-width", function(d2) {
                    return 0.67;
                })
                .attr("d", function(d2) {
                    let angle = 2*Math.PI*(1-a_bias-(1-2*a_bias)*(d2.bias+d2.ratio/2));
                    let tmp_score = d2.node.influence;
                    let r = full_radius - (full_radius-parent_radius)/2*tmp_score;
                    let x = r * Math.sin(angle);
                    let y = -r * Math.cos(angle);
                    legend_start_points[0] = {x: x+full_radius, y: y+that.legend_svg_height};
                    let Path = `M ${x} ${y-(full_radius-parent_radius)/2*tmp_score} L ${x} ${y+(full_radius-parent_radius)/2*tmp_score}`
                    return Path;
                })
                .attr("fill", "none")
                .attr("marker-start", "url(#arrow-start)")
                .attr("marker-end", "url(#arrow-end)");

            let tmp_d = [0, 0.25, 0.50, 0.75, that.thres];
            // let tmp_d = [0, 0.25, 0.50, 0.75];
            let legend_axis_g = legend_circle_g.selectAll(".axis_g")
                .data(tmp_d);
            
            let new_legend_axis_g = legend_axis_g.enter()
                .append("g")
                .attr("class", (d2, i) => `axis_g axis-${i}`);
            
            new_legend_axis_g.append("circle")
                .attr("class", (d2, i) => `axis-circle circle-${i}`)
                .attr("fill", "none")
                .attr("stroke", "gray")
                .attr("opacity", 0.5)
                .attr("stroke-width", (d) => d==that.thres?1.5:0.5)
                .attr("r", d2 => parent_radius*d2+r_bias*(1-d2));
            
            legend_start_points[3] = polarToCartesian(full_radius, that.legend_svg_height, parent_radius*that.thres+r_bias*(1-that.thres), Math.PI*5/12);
            
            let legend_texts = ["Influence Score", "Bounding Box Area", "Confidence Score", "Confidence Threshold"];
            let legend_lines = [];
            for(let i=0;i<4;i++) {
                legend_lines.push({start: legend_start_points[i], end: legend_end_points[i], text: legend_texts[i]});
            }

            let legend_line_g = that.legend_svg.selectAll(".legend_line_g")
                .data(legend_lines);
            
            let new_legend_line_g = legend_line_g
                .enter()
                .append("g")
                .attr("class", "legend_line_g");
            
            function legendLineGenerator(start, end) {
                let dir = {x: Math.sqrt(3)/2, y: 1/2};
                if(end.y<start.y) dir.y = -dir.y;
                let middle = {x: (end.y-start.y)/dir.y*dir.x+start.x, y: end.y};
                const Path = `
                    M ${start.x} ${start.y}
                    L ${middle.x} ${middle.y} L ${end.x} ${end.y}
                `;
                return Path;
            }
            new_legend_line_g.append("path")
                .attr("d", d => legendLineGenerator(d.start, d.end))
                .attr("fill", "none")
                .attr("stroke", "black")
                .attr("stroke-width", 0.5);
            
            let legend_font_size = Math.min(that.legend_svg_height/5, (that.legend_svg_width-2*full_radius)/10);
            new_legend_line_g.append("text")
                .attr("x", d => d.end.x)
                .attr("y", d => d.end.y)
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .text(d => d.text)
                .attr("font-size", legend_font_size);
        },
        load(item) {
            this.click_id = -1;
            this.click_parent_id = -1;
            this.focus_id = -1;
            this.click_ids = [];
            this.newLayout(item);

            this.$parent.$parent.wait_cnt += 1;
            console.log("tree add wait cnt", this.$parent.$parent.wait_cnt);
        }
    },
    computed: {
    },
    watch: {
        item: function(item) {
            this.load(item);
        }
    },
    mounted() {
        this.class_order = {};
        for(let i=0;i<this.$parent.$parent.categories.length;i++) {
            this.class_order[this.$parent.$parent.categories[i]["name"]] = i;
        }
        console.log("order", this.class_order);

        let card = document.querySelector('.svg-info')
        let tmp = card.style.maxHeight;
        card.style.maxHeight = 'none';

        this.svg = d3.select("#meta-svg2");
        this.svgsize = this.svg.node().getBoundingClientRect();
        this.svg_width = this.svgsize.width;
        this.svg_height = this.svgsize.height;

        card.style.maxHeight = tmp;

        let legend_size = 20;
        legend_size = min(20, this.svg_height/10);
        // this.title_yshift = Math.max(legend_size*1.8, 24+legend_size)+2;
        // this.title_yshift = legend_size*2;
        // this.title_yshift = 35;
        this.title_yshift = legend_size;

        this.scale = 1;
        this.xshift = 0.15*this.svg_width;
        this.yshift = this.title_yshift+12+this.svg_width/25;

        this.calc_size = [0.8*this.svg_width, this.svg_height-this.yshift-15];

        this.ori_scale = this.scale;
        this.ori_xshift = this.xshift;
        this.ori_yshift = this.yshift;

        this.svg_g = this.svg.select(".tree-g")
            .attr("transform", "translate("+this.xshift+","+this.yshift+")");

        this.svg_back_g = this.svg.select(".tree-back-g");

        this.categories_super = this.$parent.$parent.categories_super;
        this.categories_super2 = this.$parent.$parent.categories_super2;
        this.categories = this.$parent.$parent.categories;
        this.categories2 = this.$parent.$parent.categories2;

        this.categories_dict = {};
        for(let item of this.categories) {
            this.categories_dict[item["name"]] = item;
        }
        this.categories_dict2 = {};
        for(let item of this.categories2) {
            this.categories_dict2[item["name"]] = item;
        }

        let that = this;

        let padding = 0;
        that.padding = padding;
        let legend_stroke = 2;

        that.svg.append("text")
            .attr("transform", `translate(${padding}, ${that.title_yshift})`)
            .attr("font-size", legend_size*1)
            .attr("font-weight", "bold")
            .attr("fill", "#344461")
            .text("Scene tree");

        const yScale = d3.scaleLinear()
            .domain([0, 1.05])
            .range([that.calc_size[1]*(1-that.context_ratio), 0]);

        const lines_data = d3.range(0, 1+0.00001, 0.1);

        this.svg.append("g")
            .attr("class", "y-axis")
            .attr("transform", `translate(${padding+24+20}, ${that.ori_yshift+that.calc_size[1]*that.context_ratio})`)
            .attr("font-family", "sans-serif")
            .attr("font-size", 10)
            .attr("text-anchor", "end");

        that.svg.append("text")
            .attr("class", "y-axis-title")
            .attr("text-anchor", "start")
            .attr("dy", "0.8em")
            .attr("transform", `translate(${padding+5}, ${that.ori_yshift+that.calc_size[1]*that.context_ratio-that.axis_top_padding+10}) rotate(270, 0, 0)`)
            .text("Confidence score")
            .attr("opacity", 0);
        
        that.svg.append("rect")
            .attr("class", "confidence-area")
            // .attr("fill", "rgba(255, 255, 255, 0.5)")
            .attr("fill", "url(#myGradient)")
            .attr("rx", 20)
            .attr("ry", 20)
            .style("pointer-events", "none")
            .attr("transform", `translate(${0.5}, ${that.ori_yshift+that.calc_size[1]*that.context_ratio-that.axis_top_padding-0.5})`)
            .attr("width", that.svg_width-1)
            .attr("height", that.calc_size[1]*(1-that.context_ratio)+that.axis_top_padding+(that.svg_height-that.ori_yshift-that.calc_size[1]))
            .lower();
        // console.log("?", that.ori_yshift, that.calc_size[1], that.context_ratio, that.axis_top_padding);

        that.drawLegend();
    },
};
</script>

<style scoped>

.tool-title {
    pointer-events: auto;
    /* color: rgb(204, 204, 204); */
    background-color: rgb(204, 204, 204);
    font-weight: bold;
    font-size: 16px;
    border-bottom: 1px solid #ddd;
    text-align: left;
    border-radius: 4px;
    display: flex;
    text-align: center;
    align-items: center;
}

.arrow {
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
    font-size: 20px;
    padding-left: 8px;
    padding-right: 8px;
    transition: transform 0.5s ease;
}

.arrow.expanded {
    transform: rotate(90deg);
}

.svg-info {
    pointer-events: auto;
    /* background-color: rgba(255, 255, 255, 0.75); */
    /* background-color: rgb(244, 244, 244); */
    height: 100%;
    width: 100%;
    /* border: 2px solid #aaa; */
}

.tree-box {
    position: relative;
    width: 100%;
    height: 100%;
    /* flex-shrink: 100; */
}

.datainfo-svg {
    display: block;
    width: 100%;
    height: calc(100% - 80px);
}

#control-tree {
    width: 100%;
    height: 80px;
    display: flex;
}

.datainfo-bar {
    height: 10%;
    width: 90%;
}

.meta-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.V-centered {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.H-centered {
    align-items: center;
    text-align: center;
}

.TreeFlex {
    display: flex;
    height: 100%;
    width: calc(100% - 15px);
    margin-left: 10px;
    margin-right: 5px;
    flex-direction: column;
}

.sector_switch {
    position: absolute;
    right: 0px;
    top: 20px;
    transition: opacity 0.5s ease;
    opacity: 1;
    display: flex;
    height: 20px;
    z-index: 99;
}

.control{
    display: flex;
    width: 50%;
    height: 100%;
    justify-content: center;
    align-items: end;
}

.color-legend-div{
    display: flex;
    width: 50%;
    height: 100%;
    justify-content: center;
    align-items: end;
}
.color-legend{
    width: 100%;
    height: 90%;
}

.tree-legend-div {
    display: flex;
    width: 50%;
    height: 100%;
    align-items: end;
}
.tree-legend{
    width: 100%;
    height: 90%;
}

.rect-button {
    align-items: center;
    position: static;
    /* cursor: pointer; */
    overflow: hidden;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    vertical-align: middle;
    color: #fff;
    z-index: 1;
    width: 31%;
    margin-left: 2%;
    margin-right: 2%;
    height: 30px;
    line-height: 30px;
    padding: 0;
    /*background-color: #0660FE;*/
    background-color: #838383;
    border-radius: 5px;
    /*box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),*/
    /*    0 3px 1px -2px rgba(0, 0, 0, 0.12), 0 1px 5px 0 rgba(0, 0, 0, 0.2);*/
    font-size: 12px;
}
.rect-button.icon-rect-button {
    width: 12%;
}

.rect-button:disabled {
    /*background-color: #BFCFEB;*/
    background-color: #d9d9d9;
}
</style>
