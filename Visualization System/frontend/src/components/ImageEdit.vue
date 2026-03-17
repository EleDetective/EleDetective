<template>
    <div class="ImageEdit">
<!--        <div>-->
<!--            <p style="text-align: left;">-->
<!--                <span class="sub-title" style="color: #4e4e4e;"> Infographic Chart </span>-->
<!--            </p>-->
<!--        </div>-->
        <p class="sub-title" style="color: #4e4e4e;">Infographic</p>
        <div class="sample-panel-content">
            <div style="width: 52.5%; height: calc(100% - 25px); margin-top: 10px; display: inline-block;">
                <TreeView
                    ref="child_tree"
                    :item="item"
                    :imageSrc="imageSrc"
                    @click-node="setClick"
                    @hover-node="setHover"
                />
            </div>
            <div class="ImageInlineBlock" style="display: inline-block;">
                <div class="ImageFlex" @mouseenter="showButton" @mouseleave="hideButton">
                    <div style="position: relative;">
                        <p class="sub-sub-title" style="color: #4e4e4e;">Detection Boxes</p>
                    </div>

                    <div class="QA-block" v-bind:style="QAStyle">
                        <div class="QA-outer">
                            <div class="QA-inner">
                                <div class="QA-title">
                                    <p> Question </p>
                                </div>
                                <div class="QA-content">
                                    <p> {{ QA_question }} </p>
                                </div>
                            </div>
                        </div>
                        <div class="QA-outer2">
                            <div class="QA-inner">
                                <div class="QA-title">
                                    <p> Golden Answer </p>
                                </div>
                                <div class="QA-content">
                                    <p> {{ QA_answer }} </p>
                                </div>
                            </div>
                        </div>
                        <div class="reply-outer">
                            <div class="reply-inner">
                                <div class="reply-title">
                                    <p> Thinking-with-Boxes Reply </p>
                                </div>
                                <div class="reply-content">
                                    <p> {{ QA_reply }} </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    
                    <div class="svg-outer" v-bind:style="ImageSvgStyle">
                        <div id='image_buttons' class='buttons hidden' style='top: 20px; right: 20px'>
                            <div id='image_prop' title='Check propagation' @click='checkWithinInfluenceExcute' v-ripple class='small-button' v-show="can_prop || prop_showed">
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M830.60526 1006.455055V298.915417l111.015651 41.404245c50.601962 0 68.354343-33.973884 39.429454-75.510888l-163.982384-217.065282c-28.933187-41.532856-76.270104-41.532856-105.186697 0l-163.986533 217.065282c-28.929038 41.532856-11.172508 98.5197 39.437751 75.510888l111.007354-41.404245v371.584431c-77.593547-105.373389-200.889415-196.16402-396.783769-222.823708l78.141179-81.850135c19.05508-44.424515-4.09064-72.789327-51.435855-63.043979l-247.969112 96.748196C32.947084 409.283867 15.124175 450.829169 40.692748 491.855881l150.374576 191.148215c25.568573 41.035009 82.273305 46.909599 81.132407-6.181596l-20.449051-113.027781s397.252574 39.836028 446.589176 443.614542" fill="#ffffff" p-id="10420"></path>
                                </svg>
                            </div>
                            <div class='gap' v-show="can_prop || prop_showed"></div>
                            <div id='image_only_drag' title='Only Drag' @click='buttonDrag' v-ripple class='small-button' v-show="only_drag">
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M236.8 620.8c12.8 12.8 12.8 25.6 0 38.4-6.4 6.4-25.6 12.8-32 0h-6.4l-128-128V512H64V492.8l128-128c12.8-12.8 25.6-12.8 38.4 0 6.4 6.4 12.8 25.6 0 32v6.4L153.6 486.4h332.8V153.6L403.2 236.8c-12.8 12.8-25.6 12.8-38.4 0-6.4-6.4-12.8-25.6 0-32v-6.4l128-128h12.8L512 64H531.2l128 128c12.8 12.8 12.8 25.6 0 38.4-6.4 6.4-25.6 12.8-32 0h-6.4L537.6 153.6v332.8h332.8l-83.2-83.2c-12.8-12.8-12.8-25.6 0-38.4 6.4-6.4 25.6-12.8 32 0h6.4l128 128V512h6.4V531.2l-128 128c-12.8 12.8-25.6 12.8-38.4 0-6.4-6.4-12.8-25.6 0-32v-6.4l83.2-83.2H537.6v332.8l83.2-83.2c12.8-12.8 25.6-12.8 38.4 0 6.4 6.4 12.8 25.6 0 32v6.4l-128 128H512v6.4H492.8l-128-128c-12.8-12.8-12.8-25.6 0-38.4 6.4-6.4 25.6-12.8 32 0h6.4l83.2 83.2V537.6H153.6l83.2 83.2z" fill="white" p-id="10244"></path>
                                </svg>
                            </div>
                            <div id='image_drag' title='Hover and Drag' @click='buttonDrag' v-ripple class='small-button' v-show="!only_drag">
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M402.112 821.024l140.448-208.544a63.36 63.36 0 0 1 48.992-28.16l250.56-17.344c0.224 0 0.192 0 0.128-0.064L342.624 209.952c0.096 0.064 0 0.096 0.032 0.16l59.296 610.72 0.064 0.32z m53.152 35.648c-33.536 50.24-111.68 30.272-116.992-29.632L278.912 215.904c-4.96-54.4 56.128-89.696 100.928-58.08L879.008 514.56c49.536 34.752 27.776 112.416-32.48 116.32l-251.136 17.344c0.16 0 0.32-0.096 0.256 0l-140.48 208.608z" fill="white" p-id="13044"></path>
                                </svg>
                            </div>
                            <div class='gap'></div>
                            <div id='image_zoom_in' title='Zoom in' @click='buttonZoomIn' v-ripple class='small-button'>
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M754.2 151.5h-89.5v42.7h89.5c59.5 0 108 48.4 108 108v67.6h42.7v-67.6c0-83.1-67.6-150.7-150.7-150.7zM862.2 737.3c0 59.5-48.4 108-108 108h-89.5V888h89.5c83.1 0 150.7-67.6 150.7-150.7v-67.6h-42.7v67.6zM166.3 737.8v-67.6h-42.7v67.6c0 83.1 67.6 150.7 150.7 150.7h89.5v-42.7h-89.5c-59.5 0-108-48.4-108-108zM416.3 261.8h-42.8v126H247.6v42.7h125.9V556h42.8V430.5h125.4v-42.7H416.3z" fill="white" p-id="1775"></path><path d="M773.6 789.4l30.2-30.2-190.1-190.6c32.7-44.8 52-99.9 52-159.5 0-149.7-121.6-271.3-271.3-271.3-149.3 0-271.3 121.6-271.3 271.3 0 149.3 121.5 271.3 271.3 271.3 74.5 0 142.3-30.3 191.4-79.3l187.8 188.3zM394.4 637.7c-126 0-228.6-102.5-228.6-228.6s102.5-228.6 228.6-228.6S623 283.1 623 409.2 520.5 637.7 394.4 637.7z" fill="white" p-id="1776"></path>
                                </svg>
                            </div>
                            <div class='gap'></div>
                            <div id='image_zoom_out' title='Zoom out' @click='buttonZoomOut' v-ripple class='small-button'>
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M754.2 151.5h-89.5v42.7h89.5c59.5 0 108 48.4 108 108v67.6h42.7v-67.6c0-83.1-67.6-150.7-150.7-150.7zM862.2 737.3c0 59.5-48.4 108-108 108h-89.5V888h89.5c83.1 0 150.7-67.6 150.7-150.7v-67.6h-42.7v67.6zM166.3 737.8v-67.6h-42.7v67.6c0 83.1 67.6 150.7 150.7 150.7h89.5v-42.7h-89.5c-59.5 0-108-48.4-108-108zM247.6 387.8h294.2v42.7H247.6z" p-id="1938" fill="white"></path><path d="M773.6 789.4l30.2-30.2-190.1-190.6c32.7-44.8 52-99.9 52-159.5 0-149.7-121.6-271.3-271.3-271.3-149.3 0-271.3 121.6-271.3 271.3 0 149.3 121.6 271.3 271.3 271.3 74.5 0 142.3-30.3 191.4-79.3l187.8 188.3zM394.4 637.7c-126 0-228.6-102.5-228.6-228.6s102.5-228.6 228.6-228.6S623 283.1 623 409.2 520.5 637.7 394.4 637.7z" p-id="1939" fill="white"></path>
                                </svg>
                            </div>
                            <div class='gap'></div>
                            <div id='image_add' title='Add box' @click='addBox' v-ripple class='small-button'>
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M896 704h-192V512H640v192H448v64h192v192h64v-192h192v-64z" fill="white" p-id="7056"></path><path d="M448 960H64V64h832v448h-64V128H128v768h320v64z" fill="white" p-id="7057"></path>
                                </svg>
                            </div>
                            <div class='gap'></div>
                            <div id='image_delete' title='Delete box' @click='enableDelete' v-ripple class='small-button'>
                                <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                                    <path d="M607.897867 768.043004c-17.717453 0-31.994625-14.277171-31.994625-31.994625L575.903242 383.935495c0-17.717453 14.277171-31.994625 31.994625-31.994625s31.994625 14.277171 31.994625 31.994625l0 351.94087C639.892491 753.593818 625.61532 768.043004 607.897867 768.043004z" fill="white" p-id="2351"></path><path d="M415.930119 768.043004c-17.717453 0-31.994625-14.277171-31.994625-31.994625L383.935495 383.935495c0-17.717453 14.277171-31.994625 31.994625-31.994625 17.717453 0 31.994625 14.277171 31.994625 31.994625l0 351.94087C447.924744 753.593818 433.647573 768.043004 415.930119 768.043004z" fill="white" p-id="2352"></path><path d="M928.016126 223.962372l-159.973123 0L768.043004 159.973123c0-52.980346-42.659499-95.983874-95.295817-95.983874L351.94087 63.989249c-52.980346 0-95.983874 43.003528-95.983874 95.983874l0 63.989249-159.973123 0c-17.717453 0-31.994625 14.277171-31.994625 31.994625s14.277171 31.994625 31.994625 31.994625l832.032253 0c17.717453 0 31.994625-14.277171 31.994625-31.994625S945.73358 223.962372 928.016126 223.962372zM319.946246 159.973123c0-17.545439 14.449185-31.994625 31.994625-31.994625l320.806316 0c17.545439 0 31.306568 14.105157 31.306568 31.994625l0 63.989249L319.946246 223.962372 319.946246 159.973123 319.946246 159.973123z" fill="white" p-id="2353"></path><path d="M736.048379 960.010751 288.123635 960.010751c-52.980346 0-95.983874-43.003528-95.983874-95.983874L192.139761 383.591466c0-17.717453 14.277171-31.994625 31.994625-31.994625s31.994625 14.277171 31.994625 31.994625l0 480.435411c0 17.717453 14.449185 31.994625 31.994625 31.994625l448.096758 0c17.717453 0 31.994625-14.277171 31.994625-31.994625L768.215018 384.795565c0-17.717453 14.277171-31.994625 31.994625-31.994625s31.994625 14.277171 31.994625 31.994625l0 479.231312C832.032253 916.835209 789.028725 960.010751 736.048379 960.010751z" fill="white" p-id="2354"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="show_hierarchy_switch">
                            <!-- <el-switch
                                v-model="isShowHierarchy"
                                :disabled="(node == null)||(node.groups == null)||(node.groups.length == 0)"
                                active-text="show hierarchy"
                                inactive-text="hide hierarchy"
                                @change="showHierarchyChange"
                                >
                            </el-switch> -->
                        </div>
                        <!-- <div class="show_hierarchy_switch2">
                            <p style="font-size: 14px; height: 20px; margin-right: 10px;"> hierarchy </p>
                            <el-switch
                                v-model="isShowHierarchy"
                                :disabled="(node == null)||(node.groups == null)||(node.groups.length == 0)"
                                active-text="show"
                                inactive-text="hide"
                                @change="showHierarchyChange"
                                style="height: 20px;"
                                >
                            </el-switch>
                        </div> -->
                        <div class="show_boxes_switch">
                            <p style="font-size: 14px; height: 20px; margin-right: 10px;"> Show all boxes </p>
                            <el-switch
                                v-model="isShowAll"
                                :disabled="(node == null)||(selectedLayer != 'Origin')"
                                active-text=""
                                inactive-text=""
                                @change="showBoxesChange"
                                style="height: 20px;"
                                >
                            </el-switch>
                        </div>
                        <select class="layer-dropdown" v-model="selectedLayer" @change="updateLayer" v-if="show_QA">
                            <option v-for="option in layer_options" :key="option" :value="option">
                                {{ option }}
                            </option>
                        </select>
                        <div id="svg-container">
                            <div class="tool-windows" style="display: none;">
                                <!-- <div style="height: 5px"></div> -->
                                <SampleView
                                    ref="child_sample"
                                    :item="item"
                                    :selectedItemIndex="selectedItemIndex"
                                    @categroy-selected="updateCategory"
                                />
                            </div>
                            <div id="svg-and-dropdown">
                                <svg id="svg" ref="svg">
                                    <image class="widget-image" x="0" y="0"
                                                    :xlink:href="nowImageSrc"></image>
                                    <g id="box-back-group" v-show="selectedLayer=='Origin'">
                                    </g>
                                    <g id="image-flow-group" v-show="selectedLayer=='Origin'">
                                    </g>
                                    <g id="box-group" v-show="selectedLayer=='Origin'">
                                    </g>
                                    <mask class="widget-mask" id="hover-mask">
                                        <rect class="black-rect" x="0" y="0" fill="#777777"></rect>
                                        <rect class="white-rect" x="0" y="0" fill="white"></rect>
                                    </mask>
                                </svg>
                                <svg id="legend-svg-image">
                                </svg>
                                <!-- <svg id="image-flow">
                                </svg> -->
                                <div id="image-dropdown" v-show="selectedLayer=='Origin'">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="control-tree2">
                    <div class="control-padding">
                    </div>
                    <div class="control2">
                        <button id='apply_bottom' title='Apply' :disabled="!$parent.can_apply" @click='buttonApply' v-ripple class='rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M1004.50304 266.82624l-587.072 594.16064-17.1904 16.19328-17.1904-16.19328L19.49696 493.03808l118.53696-119.9872 262.17856 265.37984 485.7536-491.6096L1004.50304 266.82624 1004.50304 266.82624zM1004.50304 266.82624" fill="white"></path>
                            </svg>
                            Apply
                        </button>
                        <button id='undo_bottom' title='Undo' :disabled="!$parent.can_undo" @click='buttonUndo' v-ripple class='rect-button icon-rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M223.300267 221.320533h410.555733c214.493867 0 388.437333 173.192533 388.437333 386.798934 0 213.674667-173.943467 386.8672-388.437333 386.8672H116.053333a64.580267 64.580267 0 0 1-64.7168-64.512c0-35.566933 29.013333-64.443733 64.7168-64.443734h517.802667a258.389333 258.389333 0 0 0 258.935467-257.911466 258.389333 258.389333 0 0 0-258.935467-257.8432h-415.061333L293.546667 424.823467a64.3072 64.3072 0 0 1-28.672 108.7488 64.853333 64.853333 0 0 1-62.941867-17.6128L19.114667 333.687467a64.375467 64.375467 0 0 1 0-91.204267L201.9328 60.074667a64.9216 64.9216 0 0 1 91.613867 0c25.258667 25.122133 25.258667 65.9456 0 91.136l-70.314667 70.0416z" fill="white"></path>
                            </svg>
                        </button>
                        <button id='redo_bottom' title='Redo' :disabled="!$parent.can_redo" @click='buttonRedo' v-ripple class='rect-button icon-rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M828.893867 220.091733H418.338133C203.844267 220.091733 29.969067 393.216 29.969067 606.890667c0 213.674667 173.8752 386.798933 388.369066 386.798933h517.802667a64.580267 64.580267 0 0 0 64.7168-64.443733 64.580267 64.580267 0 0 0-64.7168-64.443734H418.338133A258.389333 258.389333 0 0 1 159.402667 606.890667a258.389333 258.389333 0 0 1 258.935466-257.911467h415.1296l-74.888533 74.615467a64.3072 64.3072 0 0 0 28.672 108.7488 64.853333 64.853333 0 0 0 62.941867-17.6128l183.022933-182.272a64.375467 64.375467 0 0 0 0-91.272534L850.193067 58.914133a64.9216 64.9216 0 0 0-91.5456 0 64.3072 64.3072 0 0 0 0 91.136l70.314666 70.0416z" fill="white"></path>
                            </svg>
                        </button>
                        <button id='cancel_bottom' title='Cancel' :disabled="!$parent.can_undo" @click='buttonCancel' v-ripple class='rect-button'>
                            <svg class='icon' width='18px' height='18px' transform='translate(0, 5)' viewBox='0 0 1024 1024'>
                                <path d="M617.92 516.096l272 272-101.824 101.824-272-272-272 272-101.856-101.824 272-272-275.008-275.04L241.056 139.2l275.04 275.04 275.04-275.04 101.824 101.824-275.04 275.04z" fill="white"></path>
                            </svg>
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import * as d3 from 'd3';
import TreeView from './TreeView_circle_without_text.vue'
import SampleView from './SampleView.vue';
import MapRender from '../plugins/image_render_map';

export default {
    name: 'ImageEdit',
    components: {
        TreeView,
        SampleView,
    },
    props: ['imageSrc', 'item', 'inputBoxes', 'inputHierarchy', 'selectedItemIndex'],
    emits: ['hover-box', 'show-hierarchy-change', 'categroy-selected', 'score-edit', 'score-edit2', 'class-edit', 'class-edit2'],
    data: function() {
        return {
            // URL_GET_IMAGE: (imageId) => `http://166.111.80.25:6010/api/image?imageId=${imageId}`,
            // URL_GET_IMAGEBOX: `http://166.111.80.25:6010/api/imagebox`,
            // URL_RESTORE_IMAGEBOX: `http://166.111.80.25:6010/api/restore`,
            // URL_SAVE: `http://166.111.80.25:6010/api/save`,
            isCrowd: false,
            curBox: null,
            imagesize: [],
            raw_boxes: [],
            boxes: [],
            node: null,
            isDelete: false,
            svgsize: null,
            scale: 1,
            ori_scale: 1,
            realWidth: null,
            realHeight: null,
            xshift: 0,
            yshift: 0,
            isShowHierarchy: false,
            isShowAll: false,
            hover_ids: [],
            hover_id: -1,
            click_id: -1,
            hover_box: [0, 0, 0, 0],
            color_list: ['rgb(255, 23, 23)', 'rgb(255, 139, 23)', 'rgb(255, 238, 23)', 'rgb(180, 255, 23)', 'rgb(23, 255, 35)', 'rgb(23, 255, 255)', 'rgb(23, 64, 255)', 'rgb(168, 23, 255)', 'rgb(255, 83, 247)'],
            max_deep: 0,
            on_draging: false,
            is_zoom: 0,
            only_drag: false,
            HANDLE_R: 2,
            HANDLE_R_ACTIVE: 5,
            HANDLE_R_new: 3.5,
            HANDLE_R_ACTIVE_new: 8,
            unselected_dict: {},
            map_info: null,
            can_prop: false,
            prop_showed: false,
            show_QA: false,
            QA_question: "",
            QA_answer: "",
            QA_reply: "",
            nowImageSrc: "",
            selectedLayer: 'Origin',
            layer_options: ['Origin', 'Layer1', 'Layer2'],
        }
    },
    computed: {
        QAStyle: function() {
            if(!this.show_QA)return {
            }
            return {
                display: "flex"
            }
        },
        ImageSvgStyle: function() {
            if(!this.show_QA)return {}
            return {
                height: "58.3%"
            }
        }, 
        map_group: function () {
            return d3.select('#image-flow-group');
        },
    },
    watch: {
        item: function(item) {
            // this.selectedLayer = "Origin";
            this.updateLayer();
            if(this.show_QA) {
                let str = item["other_info"]["question"];
                let lastColonIndex = str.lastIndexOf("Question:");
                if (lastColonIndex === -1) {
                    this.QA_question = str;
                }else this.QA_question = str.slice(lastColonIndex + 10);
                this.QA_answer = item["other_info"]["Goldon"];
                this.QA_reply = JSON.parse(item["other_info"]["response"])["Steps"];
            }
            this.hover_ids = [];
            this.hover_id = -1;
            this.click_id = -1;
            this.hover_box = [0, 0, 0, 0];
            this.map_info = null;
            this.can_prop = false;
            this.prop_showed = false;
            this.fetchAndDrawWidgetBox();
        }
    },
    methods: {
        updateLayer: function() {
            if(this.selectedLayer == "Origin") {
                this.nowImageSrc = this.imageSrc;
            } else if (this.selectedLayer == "Layer1") {
                this.nowImageSrc = "layer1_" + this.imageSrc;
            } else if (this.selectedLayer == "Layer2") {
                this.nowImageSrc = "layer2_" + this.imageSrc;
            }
        },
        buttonApply: function() {
            this.$parent.buttonApply();
        },
        buttonUndo: function() {
            // console.log("buttonUndo", this.$parent.$parent.tmp_edit_record);
            this.$parent.buttonUndo();
        },
        buttonRedo: function() {
            this.$parent.buttonRedo();
        },
        buttonCancel: function() {
            // console.log("buttonCancel", this.$parent.$parent.tmp_edit_record);
            this.$parent.buttonCancel();
        },
        showButton: function() {
            let buttons = document.querySelector('#image_buttons');
            buttons.classList.remove('hidden');
        },
        hideButton: function() {
            let buttons = document.querySelector('#image_buttons');
            buttons.classList.add('hidden');
        },
        updateCategory: function() {
            this.$emit('categroy-selected');
        },
        test: function() {
            console.log("test");
        },
        checkWithinInfluencePre(id) {
            let that = this;
            that.can_prop = false;
            that.prop_bid = id;
            if(id>=0) that.can_prop = true;
        },
        getWithinInfluenceInfo() {
            let that = this;
            let box_dict = {};
            if(that.prop_showed) {
                for(let box of that.boxes) box_dict[box.id] = box;
                let source = box_dict[that.prop_bid];
                // console.log("box_dict", box_dict, id, source);
                if(source == null) {
                    that.map_info = null;
                } else {
                    let pairs = [];
                    for(let id2 in that.$parent.selectedWithinInfluence[that.prop_bid][that.$parent.selectedItemIndex]) {
                        if(id2 == that.prop_bid) continue;
                        pairs.push({"source": source, "target": box_dict[id2]});
                    }
                    that.map_info = {"source": source, "pairs": pairs };
                }
            } else {
                that.map_info = null;
            }
        },
        checkWithinInfluenceExcute() {
            let that = this;
            that.prop_showed = !that.prop_showed;
            that.updateFlow();
        },
        updateFlow() {
            let that = this;
            that.getWithinInfluenceInfo();
            that.map_render.render(that.map_info);
        },
        setClick: function(id) {
            this.checkWithinInfluencePre(id);
            this.setHover(id);
            this.$parent.checkCrossInfluencePre(id);
        },
        setHover: function(id) {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            const that = this;

            that.hover_ids = [];
            that.hover_id = -1;
            that.click_id = -1;
            if(id != -1){
                that.hover_ids = [id];
                that.hover_id = id;
            }

            d3.selectAll("g.imagebox rect").classed('hovering', false);
            const el = d3.selectAll("g.imagebox rect").filter((d) => d.id == id);
            if(el.size()>0) {
                el.classed('hovering', true)
                d3.select(el.node().parentNode).raise();

                let ori_width = d3.select(el.node().parentNode).datum().ori_width;
                let ori_height = d3.select(el.node().parentNode).datum().ori_height;
                let ori_x = d3.select(el.node().parentNode).datum().ori_x;
                let ori_y = d3.select(el.node().parentNode).datum().ori_y;
                let scaleBefore = that.scale;
                that.scale = min(that.scale, that.svgsize.width*1/ori_width/that.imagesize[0]);
                that.scale = min(that.scale, that.svgsize.height*0.95/ori_height/that.imagesize[1]);
                let x = that.svgsize.width/2;
                let y = that.svgsize.height/2;
                that.xshift = x + (that.xshift - x)*that.scale/scaleBefore;
                that.yshift = y + (that.yshift - y)*that.scale/scaleBefore; 
                // console.log(that.scale, that.svgsize.height*0.95, ori_height*that.imagesize[1]);
                that.xshift = max(that.xshift, -ori_x*that.imagesize[0]*that.scale+0*that.svgsize.width);
                that.xshift = min(that.xshift, -(ori_x+ori_width)*that.imagesize[0]*that.scale+1*that.svgsize.width);
                that.yshift = max(that.yshift, -ori_y*that.imagesize[1]*that.scale+0.025*that.svgsize.height);
                that.yshift = min(that.yshift, -(ori_y+ori_height)*that.imagesize[1]*that.scale+0.975*that.svgsize.height);
            }
            
            d3.selectAll("g.imagegroup rect").classed('hovering', false);
            const g_el = d3.selectAll("g.imagegroup rect").filter((d) => d.id == id);
            if(g_el.size()>0) {
                g_el.classed('hovering', true)
                that.hover_ids = d3.select(g_el.node().parentNode).datum().children;
                that.hover_id = d3.select(g_el.node().parentNode).datum().id;

                let ori_width = d3.select(g_el.node().parentNode).datum().ori_width;
                let ori_height = d3.select(g_el.node().parentNode).datum().ori_height;
                let ori_x = d3.select(g_el.node().parentNode).datum().ori_x;
                let ori_y = d3.select(g_el.node().parentNode).datum().ori_y;
                let scaleBefore = that.scale;
                that.scale = min(that.scale, that.svgsize.width*1/ori_width/that.imagesize[0]);
                that.scale = min(that.scale, that.svgsize.height*0.95/ori_height/that.imagesize[1]);
                let x = that.svgsize.width/2;
                let y = that.svgsize.height/2;
                that.xshift = x + (that.xshift - x)*that.scale/scaleBefore;
                that.yshift = y + (that.yshift - y)*that.scale/scaleBefore;
                that.scale = min(that.scale, that.svgsize.width*1/ori_width/that.imagesize[0]);
                that.scale = min(that.scale, that.svgsize.height*0.95/ori_height/that.imagesize[1]);
                that.xshift = max(that.xshift, -ori_x*that.imagesize[0]*that.scale+0*that.svgsize.width);
                that.xshift = min(that.xshift, -(ori_x+ori_width)*that.imagesize[0]*that.scale+1*that.svgsize.width);
                that.yshift = max(that.yshift, -ori_y*that.imagesize[1]*that.scale+0.025*that.svgsize.height);
                that.yshift = min(that.yshift, -(ori_y+ori_height)*that.imagesize[1]*that.scale+0.975*that.svgsize.height);
            }
            that.click_id = id;

            that.realWidth = that.scale*that.imagesize[0];
            that.realHeight = that.scale*that.imagesize[1];
            for(let box of that.boxes){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }
            for(let box of that.groups){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }

            that.updateBackBoxes();
            that.updateBoxes();
            that.updateGroupBoxes();
            that.updateImageAndMask();
            that.updateFlow();
        },
        showHierarchyChange: function() {
            if(this.node != null)console.log(this.node);
            if(this.node != null) {
                // this.drawWidgetBox(this.node);
                this.update();
                this.$refs.child_tree.setShowHierarchy(this.isShowHierarchy);
                this.$emit('show-hierarchy-change', this.isShowHierarchy);
            }
        },
        showBoxesChange: function() {
            if(this.node != null)console.log(this.node);
            if(this.node != null) {
                // this.drawWidgetBox(this.node);
                this.update();
            }
        },
        getSvgImageSize: function(node) {
            const svg = d3.select('#svg');
            const that = this;
            that.imagesize = node.imagesize;
            that.svgsize = that.$refs['svg'].getBoundingClientRect();
            that.scale = Math.min(that.svgsize.width*1/that.imagesize[0], that.svgsize.height*0.95/that.imagesize[1]);
            that.ori_scale = that.scale;
            that.realWidth = that.scale*that.imagesize[0];
            that.realHeight = that.scale*that.imagesize[1];
            that.xshift = (that.svgsize.width-that.realWidth)/2;
            that.yshift = (that.svgsize.height-that.realHeight)/2;
        },
        updateImageAndMask: function() {
            const svg = d3.select('#svg');
            const that = this;

            const image = svg.select('image');
            image.attr('width', that.realWidth);
            image.attr('height', that.realHeight);
            image.attr('x', that.xshift-0*that.scale);
            image.attr('y', that.yshift-0*that.scale);
            
            const mask = svg.select('mask');
            const black_mask = svg.select('.black-rect');
            black_mask.attr('width', that.realWidth);
            black_mask.attr('height', that.realHeight);
            black_mask.attr('x', that.xshift-0*that.scale);
            black_mask.attr('y', that.yshift-0*that.scale);
            const white_mask = svg.select('.white-rect');
            if(that.hover_id != -1){
                black_mask.transition()
                        .duration(200)
                        .attr('fill', "rgb(32, 32, 32)");
                if(that.on_draging) {
                    white_mask
                        .attr('x', that.hover_box[0])
                        .attr('y', that.hover_box[1])
                        .attr('width', that.hover_box[2])
                        .attr('height', that.hover_box[3]);
                } else {
                    white_mask.transition()
                        .duration(200)
                        .attr('x', that.hover_box[0])
                        .attr('y', that.hover_box[1])
                        .attr('width', that.hover_box[2])
                        .attr('height', that.hover_box[3]);
                }
            }else{
                black_mask.transition()
                        .duration(200)
                        .attr('fill', "rgb(255, 255, 255)");
            }
            image.lower();
        },
        updateBackBoxes: function() {
            const svg = d3.select('#svg');
            const box_back_g = d3.select('#box-back-group');
            const that = this;
            const boxes = that.boxes;
            boxes.sort((a, b) => d3.descending(a.width*a.height*100+a.id, b.width*b.height*100+b.id));
            let allBackRects = box_back_g.selectAll('g.imageback').data(boxes, (d) => d.id);

            
            allBackRects
                .attr("visibility", function(d) {
                    if(d.unselected) {
                        // TODO
                        if(that.isShowAll) return "visible";
                        // console.log("unselected", that.unselected_dict, that.hover_id, that.click_id);
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) return "visible";
                            }
                        }
                        return d3.select(this).attr("visibility");
                    }
                    return "visible";
                })
                .transition()
                .duration(200)
                .attr("bid", d => d.id)
                .attr("opacity", function(d) {
                    if(d.unselected) {
                        // TODO
                        let tmp_flag = false;
                        if(that.isShowAll) tmp_flag = true;
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) tmp_flag = true;
                            }
                        }
                        if(!tmp_flag) return 0;
                    }
                    if(that.hover_ids.length>0){
                        if(that.hover_ids.includes(d.id))
                            return 1;
                        else return 0.15;
                    }
                    return 1;
                })
                .on('end', function(d) {
                    if(d.unselected) {
                        // TODO
                        if(that.isShowAll) return;
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) return;
                            }
                        }
                        d3.select(this).attr("visibility", "hidden");
                    }
                });

            allBackRects
                .attr('transform', function(d) {
                    return 'translate(' + d.x + ',' + d.y + ')';
                })
                .style("display", function() {
                    if(!that.isShowHierarchy) return null;
                    else return 'none';
                })
                // .lower();

            allBackRects
                .select('rect.bg')
                .attr('height', function(d) {
                    return d.height;
                })
                .attr('width', function(d) {
                    return d.width;
                });
        },
        updateBoxes: function() {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            const that = this;
            const boxes = that.boxes;
            boxes.sort((a, b) => d3.descending(a.width*a.height*100+a.id, b.width*b.height*100+b.id));
            const allRects = box_g.selectAll('g.imagebox').data(boxes, (d) => d.id);
            const allDropdown = d3.select("#image-dropdown").selectAll(".dropdown-group");

            allDropdown
                // .style("left", d => `${d.x + d.width/2 - 172/2}px`)
                // .style("bottom", d => `calc(100% - ${d.y - 10}px`)
                .style("left", d => {
                    let width = 172;
                    let left = d.x + d.width/2 - width/2;
                    left = Math.max(left, 0);
                    left = Math.min(left, that.svgsize.width-width);
                    return `${left}px`
                })
                .style("top", d => {
                    let height = 29+41;
                    let top = d.y - height - 10;
                    top = Math.max(top, 0);
                    top = Math.min(top, that.svgsize.height-height);
                    return `${top}px`
                })
                .style("visibility", function(d) {
                    const rect = box_g.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return "hidden";
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return "visible";
                    if(d.score < 100)
                        return d3.select(this).style("visibility");
                    return "visible";
                })
                .transition()
                .duration(200)
                .style("opacity", function(d) {
                    const rect = box_g.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return 0;
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return 1;
                    if(d.score < 100)
                        return 0;
                    return 1;
                })
                .on('end', function(d) {
                    const rect = box_g.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return;
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return;
                    if(d.score < 100)
                        d3.select(this).style("visibility", "hidden");
                });

            allDropdown.select(".image-dropdown-title")
                .style("background-color", (d) => {
                    if(d.class in that.categories_dict)
                        return that.categories_dict[d.class]["color"];
                    else return "#999";
                })

            allDropdown.select(".image-dropdown-body .text-div p")
                .text((d) => d.score.toFixed(4))

            const select = allDropdown.select(".categories-select")
            select.each(function (d) {
                const sel = d3.select(this);
                sel.selectAll("option")
                    .attr("value", d2 => d2)
                    .text(d2 => ((d.type=="new")?"New ":"") + that.categories_dict[d2]["text"])
                    .property("selected", d2 => d2 === d.class);
            });

            allRects.each(function(d) {
                if((d.id == that.hover_id) && (that.hover_ids.length > 0)) {
                    that.hover_box = [d.x, d.y, d.width, d.height];
                    // console.log("hover box", that.hover_box);
                }
            });

            allRects
                .attr('transform', function(d) {
                    return 'translate(' + d.x + ',' + d.y + ')';
                })
                // .lower();
            // console.log("??", allRects)

            allRects
                .attr("visibility", function(d) {
                    if(d.unselected) {
                        // TODO
                        if(that.isShowAll) return "visible";
                        // console.log("unselected", that.unselected_dict, that.hover_id, that.click_id);
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) return "visible";
                            }
                        }
                        return d3.select(this).attr("visibility");
                    }
                    return "visible";
                })
                .transition()
                .duration(200)
                .attr("bid", d => d.id)
                .attr("opacity", function(d) {
                    if(d.unselected) {
                        // TODO
                        let tmp_flag = false;
                        if(that.isShowAll) tmp_flag = true;
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) tmp_flag = true;
                            }
                        }
                        if(!tmp_flag) return 0;
                    }
                    if(that.hover_ids.length>0){
                        if(that.hover_ids.includes(d.id))
                            return 1;
                        else return 0.15;
                    }
                    return 1;
                })
                .on('end', function(d) {
                    if(d.unselected) {
                        // TODO
                        if(that.isShowAll) return;
                        if(that.unselected_dict[that.hover_id]||that.unselected_dict[that.click_id]) {
                            if(that.hover_ids.length>0) {
                                if(that.hover_ids.includes(d.id)) return;
                            }
                        }
                        d3.select(this).attr("visibility", "hidden");
                    }
                });

            allRects
                .select('rect.bg')
                .attr('height', function(d) {
                    return d.height;
                })
                .attr('width', function(d) {
                    return d.width;
                })
                .attr('stroke-width', function(d) {
                    const rect = d3.select(this);
                    if(rect.classed('hovering')||that.click_id==d.id) {
                        if(d.type == "new") return that.HANDLE_R_ACTIVE_new;
                        return that.HANDLE_R_ACTIVE;
                    } else if(that.hover_ids.includes(d.id)) {
                        if(d.type == "new") return (that.HANDLE_R_ACTIVE_new+that.HANDLE_R_new)/2;
                        return (that.HANDLE_R_ACTIVE+that.HANDLE_R)/2;
                    } else {
                        if(d.type == "new") return that.HANDLE_R_new;
                        return that.HANDLE_R;
                    }
                });

            allRects
                .select('circle.bottomright')
                .attr('cx', function(d) {
                    return d.width;
                })
                .attr('cy', function(d) {
                    return d.height;
                });

            // console.log("?", that.node.boxes);
        },
        updateGroupBoxes: function() {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            const that = this;
            const groups = that.groups;
            const allDropdown = d3.select("#image-dropdown").selectAll(".groupdropdown-group");

            allDropdown
                // .style("left", d => `${d.x + d.width/2 - 172/2}px`)
                // .style("bottom", d => `calc(100% - ${d.y - 10}px`)
                .style("left", d => {
                    let width = 172;
                    let left = d.x + d.width/2 - width/2;
                    left = Math.max(left, 0);
                    left = Math.min(left, that.svgsize.width-width);
                    return `${left}px`
                })
                .style("top", d => {
                    let height = 29;
                    let top = d.y - height - 10;
                    top = Math.max(top, 0);
                    top = Math.min(top, that.svgsize.height-height);
                    return `${top}px`
                })
                .style("visibility", function(d) {
                    const rect = box_g.selectAll("g.imagegroup rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return "hidden";
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return "visible";
                    // if(d.score < 100)
                    if(true)
                        return d3.select(this).style("visibility");
                    return "visible";
                })
                .transition()
                .duration(200)
                .style("opacity", function(d) {
                    const rect = box_g.selectAll("g.imagegroup rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return 0;
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return 1;
                    // if(d.score < 100)
                    if(true)
                        return 0;
                    return 1;
                })
                .on('end', function(d) {
                    const rect = box_g.selectAll("g.imagegroup rect").filter((d2) => d2.id == d.id);
                    if(rect.empty()){
                        return;
                    }
                    if(rect.classed('hovering')||that.click_id==d.id)
                        return;
                    // if(d.score < 100)
                    if(true)
                        d3.select(this).style("visibility", "hidden");
                });

            allDropdown.select(".image-dropdown-title2")
                .style("background-color", (d) => {
                    if(d.class in that.categories_dict)
                        return that.categories_dict[d.class]["color"];
                    else return "#999";
                })

            const select = allDropdown.select(".categories-select")
            select.each(function (d) {
                const sel = d3.select(this);
                sel.selectAll("option")
                    .attr("value", d2 => d2)
                    .text(d2 => d2 in that.categories_dict?that.categories_dict[d2]["text"]:"Group")
                    .property("selected", d2 => d2 === d.class);
            });

            groups.sort((a, b) => d3.descending(a.deep, b.deep));
            let allGroupRects = box_g.selectAll('g.imagegroup').data(groups, (d) => d.id);

            allGroupRects.each(function(d) {
                if(d.id == that.hover_id) {
                    let rect = d;
                    if(that.isShowAll) {
                        rect = {
                            x: (d.ori_box2.ori_x)*that.realWidth+that.xshift,
                            y: (d.ori_box2.ori_y)*that.realHeight+that.yshift,
                            width: (d.ori_box2.ori_width)*that.realWidth,
                            height: (d.ori_box2.ori_height)*that.realHeight,
                        }
                    }
                    that.hover_box = [rect.x-d.max_deep*(that.HANDLE_R_ACTIVE), rect.y-d.max_deep*(that.HANDLE_R_ACTIVE), rect.width+2*d.max_deep*(that.HANDLE_R_ACTIVE), rect.height+2*d.max_deep*(that.HANDLE_R_ACTIVE)];
                    // console.log("hover group box", that.hover_box);
                }
            });

            allGroupRects
                .attr('transform', function(d) {
                    return 'translate(' + (d.x-d.max_deep*(that.HANDLE_R_ACTIVE)) + ',' + (d.y-d.max_deep*(that.HANDLE_R_ACTIVE)) + ')';
                })
                .style("display", function() {
                    if(that.isShowHierarchy) return null;
                    else return 'none';
                })
                // .lower();
            
            allGroupRects
                .transition()
                .duration(200)
                .attr("opacity", function(d) {
                    if(that.hover_ids.length>0){
                        if(that.hover_ids.includes(d.id))
                            return 1;
                        else return 0.15;
                    }
                    return 1;
                });

            allGroupRects
                .selectAll('rect')
                .attr('height', function(d) {
                    return d.height + 2*d.max_deep*(that.HANDLE_R_ACTIVE);
                })
                .attr('width', function(d) {
                    return d.width + 2*d.max_deep*(that.HANDLE_R_ACTIVE);
                })
                .attr('stroke-width', function(d) {
                    const rect = d3.select(this);
                    if(rect.classed('hovering'))
                        return that.HANDLE_R_ACTIVE;
                    else if(that.hover_ids.includes(d.id))
                        return (that.HANDLE_R_ACTIVE+that.HANDLE_R)/2;
                    else return that.HANDLE_R;
                })
                .attr("stroke-dasharray", "8,4");

            allGroupRects
                .select('circle.bottomright')
                .attr('cx', function(d) {
                    return d.width + 2*d.max_deep*(that.HANDLE_R_ACTIVE);
                })
                .attr('cy', function(d) {
                    return d.height + 2*d.max_deep*(that.HANDLE_R_ACTIVE);
                });
        },
        tmpEdit: function(update_dict, key=null, key2=null) {
            // console.log("image update_dict", update_dict, key);
            if(update_dict == null) return;
            let that = this;
            for(let item of that.node.boxes) {
                if(item.id in update_dict) {
                    item.score = update_dict[item.id][key];
                    item.class = update_dict[item.id][key2];
                }
            }
            // console.log("image updated", that.node.boxes);
            that.drawWidgetBox(that.node);
        },
        scoreEdit: function(e, d, scale) {
            let that = this;
            // // console.log(e, d, scale);
            // for(let i=0;i<that.inputBoxes.length;i++){
            //     let box = that.inputBoxes[i];
            //     if((Math.abs(d.ori_width*that.imagesize[0]-box.width)<0.2*box.width)&&(Math.abs(d.ori_height*that.imagesize[1]-box.height)<0.2*box.height)) {
            //         console.log("update box", d.ori_width*that.imagesize[0], d.ori_height*that.imagesize[1], box.width, box.height);
            //         that.inputBoxes[i].score *= scale;
            //         console.log("inputBoxes", that.inputBoxes);
            //     }
            // }
            // that.fetchAndDrawWidgetBox();
            // that.$refs.child_tree.newLayout(that.item);

            // let tmp_box = {"class": d.class, "x": d.ori_x*that.imagesize[0], "y": d.ori_y*that.imagesize[1], "width": d.ori_width*that.imagesize[0], "height": d.ori_height*that.imagesize[1]}
            // that.$emit('score-edit', tmp_box, scale);
            that.$emit('score-edit', d.id, scale);
        },
        drawWidgetBox: function(node) {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            const box_back_g = d3.select('#box-back-group');
            const that = this;

            that.svg = svg;
            let boxes = node.boxes;
            let groups = node.groups;
            
            that.MAP_HEIGHT = 10000;
            that.MAP_WIDTH = that.MAP_HEIGHT * Math.sqrt(2);

            that.MAX_TRANSLATE_X = that.MAP_WIDTH / 2;
            that.MIN_TRANSLATE_X = -that.MAX_TRANSLATE_X;

            that.MAX_TRANSLATE_Y = that.MAP_HEIGHT / 2;
            that.MIN_TRANSLATE_Y = -that.MAX_TRANSLATE_Y;

            that.MIN_RECT_WIDTH = 0;
            that.MIN_RECT_HEIGHT = 0;

            boxes = boxes.map(function(d) {
                let box = [
                    Math.round(d.bbox[0])/that.imagesize[0],
                    Math.round(d.bbox[1])/that.imagesize[1],
                    (Math.round(d.bbox[0]+d.bbox[2])-Math.round(d.bbox[0]))/that.imagesize[0],
                    (Math.round(d.bbox[3]+d.bbox[1])-Math.round(d.bbox[1]))/that.imagesize[1],
                ]
                return {
                    id: d.id,
                    ori_x: box[0],
                    ori_y: box[1],
                    ori_width: box[2],
                    ori_height: box[3],
                    box: d.bbox,
                    x: (box[0])*that.realWidth+that.xshift,
                    y: (box[1])*that.realHeight+that.yshift,
                    width: box[2]*that.realWidth,
                    height: box[3]*that.realHeight,
                    ispred: d.type==='pred',
                    class: d.class,
                    type: d.type,
                    score: d.score,
                    iscrowd: d.iscrowd===1,
                    deep: d.deep,
                    unselected: d.unselected,
                };
            });
            that.boxes = boxes;
            // console.log("draw boxes", boxes);
            box_g.selectAll('g.imagebox').remove();

            box_back_g.selectAll('g.imageback').remove();

            groups = groups.map(function(d) {
                let box = [
                    Math.round(d.bbox[0])/that.imagesize[0],
                    Math.round(d.bbox[1])/that.imagesize[1],
                    (Math.round(d.bbox[0]+d.bbox[2])-Math.round(d.bbox[0]))/that.imagesize[0],
                    (Math.round(d.bbox[3]+d.bbox[1])-Math.round(d.bbox[1]))/that.imagesize[1],
                ]
                let box2 = box;
                if("bbox2" in d) {
                    box2 = [
                        Math.round(d.bbox2[0])/that.imagesize[0],
                        Math.round(d.bbox2[1])/that.imagesize[1],
                        (Math.round(d.bbox2[0]+d.bbox2[2])-Math.round(d.bbox2[0]))/that.imagesize[0],
                        (Math.round(d.bbox2[3]+d.bbox2[1])-Math.round(d.bbox2[1]))/that.imagesize[1],
                    ]
                }
                return {
                    id: d.id,
                    ori_x: box[0],
                    ori_y: box[1],
                    ori_width: box[2],
                    ori_height: box[3],
                    ori_box2: {
                        ori_x: box2[0],
                        ori_y: box2[1],
                        ori_width: box2[2],
                        ori_height: box2[3],
                    },
                    box: d.bbox,
                    x: (box[0])*that.realWidth+that.xshift,
                    y: (box[1])*that.realHeight+that.yshift,
                    width: box[2]*that.realWidth,
                    height: box[3]*that.realHeight,
                    ispred: d.type==='pred',
                    class: d.class,
                    deep: d.deep,
                    max_deep: d.max_deep,
                    children: d.children,
                    child_index: d.child_index,
                    unselected: d.unselected,
                };
            });
            that.groups = groups;
            box_g.selectAll('g.imagegroup').remove();
            let group_rects = box_g.selectAll('g.imagegroup').data(groups);


            const image = svg.select('image');
            // image.style('width', svgsize.width);
            // image.style('height', svgsize.height);

            image.attr('width', that.realWidth);
            image.attr('height', that.realHeight);
            image.attr('x', that.xshift-0*that.scale);
            image.attr('y', that.yshift-0*that.scale);
            // image.attr('transform', 'translate(' + that.xshift + ',' + that.yshift + ')');

            const mask = svg.select('mask');
            const black_mask = svg.select('.black-rect');
            black_mask.attr('width', that.realWidth);
            black_mask.attr('height', that.realHeight);
            black_mask.attr('x', that.xshift-0*that.scale);
            black_mask.attr('y', that.yshift-0*that.scale);
            image.attr('mask', "url(#hover-mask)");

            svg.on("wheel", (event) => {
                const rect = svg.node().getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                that.ImageZoom(x, y, event.deltaY<0 ? 1 : -1);
            });

            svg.on('click', function(e) {
                const rect = svg.node().getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                if(that.is_zoom!=0)
                    that.ImageZoom(x, y, 2*that.is_zoom);
            })

            that.image_drag_offsetX = 0;
            that.image_drag_offsetY = 0;

            image.call(d3.drag()
                .container(svg.node())
                .on('start end', that.ImageMoveStartEnd)
                .on('drag', that.ImageMoving),
            );

            that.update();
        },
        ImageZoom: function(x, y, zoom) {
            let that = this;

            const scaleBefore = that.scale;
            const zoomFactor = 0.2;
            that.scale *= 1+zoom*zoomFactor;
            that.scale = Math.max(0.1, that.scale);
            // console.log(event.clientX, event.clientX, that.scale);
            that.realWidth = that.scale*that.imagesize[0];
            that.realHeight = that.scale*that.imagesize[1];

            that.xshift = x + (that.xshift - x)*that.scale/scaleBefore;
            that.yshift = y + (that.yshift - y)*that.scale/scaleBefore; 

            for(let box of that.boxes){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }
            for(let box of that.groups){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }
            
            that.update();
        },
        ImageMoveStartEnd: function(e, d, now) {
            let that = this;

            d3.select(now).classed('moving', e.type === 'start');
            if(e.type=='start') {
                that.on_draging = true;
                that.image_drag_offsetX = e.x - that.xshift;
                that.image_drag_offsetY = e.y - that.yshift;
            } else {
                that.on_draging = false;
            }
        },
        ImageMoving: function(e, d, now) {
            let that = this;

            that.xshift = e.x - that.image_drag_offsetX;
            that.yshift = e.y - that.image_drag_offsetY;

            //console.log(that.boxes);
            for(let box of that.boxes){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }
            for(let box of that.groups){
                box.x = box.ori_x*that.realWidth+that.xshift;
                box.y = box.ori_y*that.realHeight+that.yshift;
                box.width = box.ori_width*that.realWidth;
                box.height = box.ori_height*that.realHeight;
            }
            
            that.update();
        }, 
        resizerHover: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            const el = d3.select(now);
            const isEntering = e.type === 'mouseenter';
            if(that.on_draging) {
                return;
            }
            el.classed('hovering', isEntering)
                .attr(
                    'r',
                    isEntering || el.classed('resizing') ?
                        that.HANDLE_R_ACTIVE_new : that.HANDLE_R_new,
                );
            if(isEntering) {
                const tmp = d3.select(now.parentNode).datum();
                if((tmp.children != null)&&(tmp.children.length>0)) {
                    that.hover_ids = tmp.children;
                    that.hover_id = tmp.id;
                }
            }else {
                if(that.hover_id === d3.select(now.parentNode).datum().id) {
                    that.hover_ids = [];
                    that.hover_id = -1;
                }
            }
            
            that.update();
        },
        rectClick: function(e, d, now) {
            let that = this;

            // console.log("rectClick", d.id);
            if(that.only_drag) {
                return;
            }
            that.click_id = d.id;
            that.$emit('hover-box', d.id);
            that.$refs.child_tree.setClick2(d.id);
            this.checkWithinInfluencePre(d.id);
            that.update();
            this.$parent.checkCrossInfluencePre(d.id);
        },
        rectHover: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }

            const el = d3.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
            const isEntering = e.type === 'mouseenter';
            if(that.on_draging) {
                return;
            }
            el.classed('hovering', isEntering)
                // .attr(
                //     'stroke-width',
                //     isEntering || el.classed('resizing') ?
                //         that.HANDLE_R_ACTIVE : that.HANDLE_R,
                // );
            d3.select(el.node().parentNode).raise();
            // console.log("max deep", d.max_deep);
            // console.log("box", Math.round(d.box[0]), Math.round(d.box[1]), Math.round(d.box[0]+d.box[2])-Math.round(d.box[0]), Math.round(d.box[3]+d.box[1])-Math.round(d.box[1]));
            if(isEntering) {
                that.$emit('hover-box', d.id);
                // console.log("emit click", d.id);
                that.$refs.child_tree.setClick(d.id);
            }else {
                that.$emit('hover-box', -1);
                // console.log("emit click", -1);
                that.$refs.child_tree.setClick(-1);
            }

            that.update();
        },
        groupRectHover: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            // eslint-disable-next-line no-invalid-this
            const el = d3.select(now);
            const isEntering = e.type === 'mouseenter';
            if(that.on_draging) {
                return;
            }
            el.classed('hovering', isEntering)

            if(isEntering) {
                that.hover_ids = d3.select(now.parentNode).datum().children;
                that.hover_id = d3.select(now.parentNode).datum().id;
            }else {
                if(that.hover_id === d3.select(now.parentNode).datum().id)
                    that.hover_ids = [];
                    that.hover_id = -1;
            }
            // console.log("max deep", d.max_deep);
            // console.log("box", Math.round(d.box[0]), Math.round(d.box[1]), Math.round(d.box[0]+d.box[2])-Math.round(d.box[0]), Math.round(d.box[3]+d.box[1])-Math.round(d.box[1]));
            if(isEntering) {
                that.$emit('hover-box', d.id);
                that.$refs.child_tree.setClick(d.id);
            }else {
                that.$emit('hover-box', -1);
                that.$refs.child_tree.setClick(-1);
            }

            that.update();
        },
        rectResizeStartEnd: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            that.isCrowd = d.iscrowd;
            that.curBox = d;
            // eslint-disable-next-line no-invalid-this
            const el = d3.select(now);
            const isStarting = e.type === 'start';
            // eslint-disable-next-line no-invalid-this
            d3.select(now)
                .classed('resizing', isStarting)
                .attr(
                    'r',
                    isStarting || el.classed('hovering') ?
                        that.HANDLE_R_ACTIVE : that.HANDLE_R,
                );
            
            if(e.type=='start') {
                that.on_draging = true;
            } else {
                that.on_draging = false;
            }
        },
        rectResizing: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            const dragX = Math.max(
                Math.min(e.x, that.MAX_TRANSLATE_X),
                that.MIN_TRANSLATE_X,
            );

            const dragY = Math.max(
                Math.min(e.y, that.MAX_TRANSLATE_Y),
                that.MIN_TRANSLATE_Y,
            );

            // eslint-disable-next-line no-invalid-this
            if (d3.select(now).classed('topleft')) {
                const newWidth = Math.max(d.width + d.x - dragX, that.MIN_RECT_WIDTH);
                d.x += d.width - newWidth;
                d.width = newWidth;
                const newHeight = Math.max(d.height + d.y - dragY, that.MIN_RECT_HEIGHT);
                d.y += d.height - newHeight;
                d.height = newHeight;
            } else {
                d.width = Math.max(dragX - d.x, that.MIN_RECT_WIDTH);
                d.height = Math.max(dragY - d.y, that.MIN_RECT_HEIGHT);
            }
            d.ori_x = (d.x-that.xshift)/that.realWidth;
            d.ori_y = (d.y-that.yshift)/that.realHeight;
            d.ori_width = d.width/that.realWidth;
            d.ori_height = d.height/that.realHeight;
            
            // const el2 = d3.selectAll("imageback.rect").filter((d2) => d2.id == d.id);
            // el2.each(function(d2) {
            //     d2.x = d.x;
            //     d2.y = d.y;
            //     d2.ori_x = (d.x-that.xshift)/that.realWidth;
            //     d2.ori_y = (d.y-that.yshift)/that.realHeight;
            //     d2.ori_width = d.width/that.realWidth;
            //     d2.ori_height = d.height/that.realHeight;
            // });

            that.update();
        },
        rectMoveStartEnd: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            that.isCrowd = d.iscrowd;
            that.curBox = d;
            // const el = d3.select(this);
            const el = d3.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
            el.classed('moving', e.type === 'start');
            if(e.type=='start') {
                that.on_draging = true;
            } else {
                that.on_draging = false;
            }
        },
        rectMoving: function(e, d, now) {
            let that = this;

            if(that.only_drag) {
                return;
            }
            if(d.ispred) {
                return;
            }
            const dragX = Math.max(
                Math.min(e.x, that.MAX_TRANSLATE_X - d.width),
                that.MIN_TRANSLATE_X,
            );

            const dragY = Math.max(
                Math.min(e.y, that.MAX_TRANSLATE_Y - d.height),
                that.MIN_TRANSLATE_Y,
            );
            
            const el1 = d3.selectAll("g.imagebox rect").filter((d2) => d2.id == d.id);
            el1.each(function(d1) {
                d1.x = dragX;
                d1.y = dragY;
                d1.ori_x = (d.x-that.xshift)/that.realWidth;
                d1.ori_y = (d.y-that.yshift)/that.realHeight;
                d1.ori_width = d.width/that.realWidth;
                d1.ori_height = d.height/that.realHeight;
            });
            const el2 = d3.selectAll("g.imageback rect").filter((d2) => d2.id == d.id);
            el2.each(function(d2) {
                d2.x = dragX;
                d2.y = dragY;
                d2.ori_x = (d.x-that.xshift)/that.realWidth;
                d2.ori_y = (d.y-that.yshift)/that.realHeight;
                d2.ori_width = d.width/that.realWidth;
                d2.ori_height = d.height/that.realHeight;
            });

            that.update();
        },
        update_back_boxes: function() {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            const box_back_g = d3.select('#box-back-group');

            let that = this;

            let boxes = that.boxes;
            boxes.sort((a, b) => d3.descending(a.width*a.height*100+a.id, b.width*b.height*100+b.id));
            let back_rects = box_back_g.selectAll('g.imageback').data(boxes, (d) => d.id);
            back_rects.exit().remove();

            const newBackRects = back_rects.enter()
                .append('g')
                .classed('imageback', true);
            
            newBackRects
                .append('rect')
                .classed('bg', true)
                .attr('fill', 'transparent')
                .on('mouseenter mouseleave', function(e, d) {
                    that.rectHover(e, d, this);
                })
                .on('click', function(e, d) {
                    that.rectClick(e, d, this);
                    // console.log('click')
                    if(that.isDelete) {
                        that.deleteBox(d.id);
                    }
                })
                .call(d3.drag()
                    .container(that.svg.node())
                    .on('start end', function(e, d) {
                        that.ImageMoveStartEnd(e, d, this);
                    })
                    .on('drag', function(e, d) {
                        that.ImageMoving(e, d, this);
                    }),
                );

            that.updateBackBoxes();
        }, 
        update_boxes: function() {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');

            let that = this;

            let boxes = that.boxes;
            boxes.sort((a, b) => d3.descending(a.width*a.height*100+a.id, b.width*b.height*100+b.id));
            let rects = box_g.selectAll('g.imagebox').data(boxes, (d) => d.id);
            rects.exit().remove();

            const newRects = rects.enter()
                .append('g')
                .classed('imagebox', true);
            
            newRects
                .append('rect')
                .classed('bg', true)
                .attr('fill', 'none')
                .attr('stroke', (d) => {
                    // if((that.isShowHierarchy)&&('deep' in d)) 
                    //     return that.color_list[(that.max_deep-d.deep)%that.color_list.length];
                    if(d.class in that.categories_dict2)
                        return that.categories_dict2[d.class]["color"];
                    else return "transparent";
                })
                .attr("stroke-dasharray", (d) => {
                    // TODO
                    let tmp_thres = 0.3;
                    if((d.class in that.categories_dict2) && ("thres" in that.categories_dict2[d.class]))
                        tmp_thres = that.categories_dict2[d.class]["thres"];
                    if(d.score < tmp_thres)
                        return "4 4"
                    else return "none";
                })
                .attr('stroke-width', (d) => {
                    if(d.type == "new") return 4;
                    return 2;
                })
                .on('mouseenter mouseleave', function(e, d) {
                    that.rectHover(e, d, this);
                })
                .on('click', function(e, d) {
                    that.rectClick(e, d, this);
                    // console.log('click')
                    if(that.isDelete) {
                        that.deleteBox(d.id);
                    }
                })
                .call(d3.drag()
                    .container(that.svg.node())
                    .on('start end', function(e, d) {
                        that.rectMoveStartEnd(e, d, this);
                    })
                    .on('drag', function(e, d) {
                        that.rectMoving(e, d, this);
                    }),
                );
            
            const container = d3.select("#image-dropdown");
            const dropdowns = container.selectAll(".dropdown-group")
                .data(boxes, (d) => d.id);

            const newDropdowns = dropdowns.enter()
                .append("div")
                .attr("class", "dropdown-group")
                .style("position", "absolute")
                // .style("left", d => `${d.x + d.width/2 - 172/2}px`)
                // .style("bottom", d => `calc(100% - ${d.y - 10}px`)
                .style("left", d => {
                    let width = 172;
                    let left = d.x + d.width/2 - width/2;
                    left = Math.max(left, 0);
                    left = Math.min(left, that.svgsize.width-width);
                    return `${left}px`
                })
                .style("top", d => {
                    let height = 29+41;
                    let top = d.y - height - 10;
                    top = Math.max(top, 0);
                    top = Math.min(top, that.svgsize.height-height);
                    return `${top}px`
                })
                .style("visibility", "hidden")
                .style("opacity", 0);

            const newTitles = newDropdowns
                .append("div")
                .attr("class", "image-dropdown-title");

            const newBodies = newDropdowns
                .append("div")
                .attr("class", "image-dropdown-body");

            const select = newTitles.append("select")
                .attr("class", "categories-select")
                .attr("id", d => `select-${d.id}`)
                .on("change", function (event, d) {
                    that.changeBox(d.id, event.target.value, d);
                    // console.log("Updated data:", d.id, event.target.value);
                });

            select.each(function (d) {
                const sel = d3.select(this);
                sel.selectAll("option")
                    .data(Object.keys(that.categories_dict))
                    .enter()
                    .append("option")
                    .attr("value", d2 => d2)
                    .text(d2 => ((d.type=="new")?"New ":"") + that.categories_dict[d2]["text"])
                    .property("selected", d2 => d2 === d.class);
                });

            newBodies.append("div")
                .attr("class", "text-div")
                .append("p");

            let new_edit_div = newBodies.append("div")
                .attr("class", "edit-div")
                .style("visibility", d => {
                    // console.log("d", d);
                    if(d.type == "new") return "hidden";
                    return null;
                });

            new_edit_div
                .append('div')
                .append('svg')
                .append('path')
                .attr("class", "inc")
                .attr("d", "M512 0C230.4 0 0 230.4 0 512s230.4 512 512 512 512-230.4 512-512S793.6 0 512 0z m224 544h-192v192c0 19.2-12.8 32-32 32s-32-12.8-32-32v-192H288c-19.2 0-32-12.8-32-32s12.8-32 32-32h192V288c0-19.2 12.8-32 32-32s32 12.8 32 32v192h192c19.2 0 32 12.8 32 32s-12.8 32-32 32z")
                .style("cursor", "pointer")
                // .attr("fill", "rgb(9, 69, 254")
                .attr("fill", "#838383")
                .attr("stroke", "white")
                .attr("stroke-width", 0.1*1024)
                .on('click', (e, d) => that.scoreEdit(e, d, 3/2))
                .attr("transform", function(d) {
                    let tmp = 20;
                    return `scale(${tmp/1024})`;
                });

            new_edit_div
                .append('div')
                .append('svg')
                .append('path')
                .attr("class", "dec")
                .attr("d", "M512 0C230.4 0 0 230.4 0 512s230.4 512 512 512 512-230.4 512-512S793.6 0 512 0z m204.8 563.2H307.2c-30.72 0-51.2-20.48-51.2-51.2s20.48-51.2 51.2-51.2h409.6c30.72 0 51.2 20.48 51.2 51.2s-20.48 51.2-51.2 51.2z m0 0")
                .style("cursor", "pointer")
                // .attr("fill", "rgb(9, 69, 254")
                .attr("fill", "#838383")
                .attr("stroke", "white")
                .attr("stroke-width", 0.1*1024)
                .on('click', (e, d) => that.scoreEdit(e, d, 2/3))
                .attr("transform", function(d) {
                    let tmp = 20;
                    return `scale(${tmp/1024})`;
                });


            dropdowns.exit().remove();

            newRects
                .append('g')
                .classed('circles', true)
                // .attr("visibility", (d) => {
                //     if(!d.ispred)return "visible";
                //     return "hidden";
                // })
                .attr("opacity", (d) => {
                    if(!d.ispred)return 1;
                    return 0;
                })
                .each(function() {
                    // eslint-disable-next-line no-invalid-this
                    const circleG = d3.select(this);

                    circleG
                        .append('circle')
                        .classed('topleft', true)
                        .attr('r', that.HANDLE_R_new)
                        .on('mouseenter mouseleave', function(e, d) {
                            that.resizerHover(e, d, this);
                        })
                        .call(d3.drag()
                            .container(that.svg.node())
                            .subject(function(e) {
                                return {x: e.x, y: e.y};
                            })
                            .on('start end', function(e, d) {
                                that.rectResizeStartEnd(e, d, this);
                            })
                            .on('drag', function(e, d) {
                                that.rectResizing(e, d, this);
                            }),
                        );

                    circleG
                        .append('circle')
                        .classed('bottomright', true)
                        .attr('r', that.HANDLE_R_new)
                        .on('mouseenter mouseleave', function(e, d) {
                            that.resizerHover(e, d, this);
                        })
                        .call(d3.drag()
                            .container(that.svg.node())
                            .subject(function(e) {
                                return {x: e.x, y: e.y};
                            })
                            .on('start end', function(e, d) {
                                that.rectResizeStartEnd(e, d, this);
                            })
                            .on('drag', function(e, d) {
                                that.rectResizing(e, d, this);
                            }),
                        );
                });
            
            that.updateBoxes();
        },
        update_groups: function() {
            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');
            let that = this;

            let groups = that.groups;
            let group_rects = box_g.selectAll('g.imagegroup').data(groups, (d) => d.id);
            group_rects.exit().remove();

            const newGroupRects = group_rects.enter()
                .append('g')
                .classed('imagegroup', true);
            
            newGroupRects
                .append('rect')
                .classed('bg', true)
                .attr('fill', 'none')
                .attr('stroke', (d) => {
                    return 'gray';
                    // return that.color_list[(that.max_deep-d.deep)%that.color_list.length];
                })
                .attr('stroke-width', 2)
                .on('mouseenter mouseleave', function(e, d) {
                    that.groupRectHover(e, d, this);
                })
                .call(d3.drag()
                    .container(that.svg.node())
                    .on('start end', function(e, d) {
                        that.rectMoveStartEnd(e, d, this);
                    })
                    .on('drag', function(e, d) {
                        that.rectMoving(e, d, this);
                    }),
                );

            newGroupRects
                .append('rect')
                .classed('transparent_fill', true)
                .attr('fill', 'transparent')
                .on('mouseenter mouseleave', function(e, d) {
                    that.groupRectHover(e, d, this);
                })
                .call(d3.drag()
                    .container(that.svg.node())
                    .on('start end', function(e, d) {
                        that.ImageMoveStartEnd(e, d, this);
                    })
                    .on('drag', function(e, d) {
                        that.ImageMoving(e, d, this);
                    }),
                );

            const container = d3.select("#image-dropdown");
            const dropdowns = container.selectAll(".groupdropdown-group")
                .data(groups, (d) => d.id);

            const newDropdowns = dropdowns.enter()
                .append("div")
                .attr("class", "groupdropdown-group")
                .style("position", "absolute")
                // .style("left", d => `${d.x + d.width/2 - 172/2}px`)
                // .style("bottom", d => `calc(100% - ${d.y - 10}px`)
                .style("left", d => {
                    let width = 172;
                    let left = d.x + d.width/2 - width/2;
                    left = Math.max(left, 0);
                    left = Math.min(left, that.svgsize.width-width);
                    return `${left}px`
                })
                .style("top", d => {
                    let height = 29;
                    let top = d.y - height - 10;
                    top = Math.max(top, 0);
                    top = Math.min(top, that.svgsize.height-height);
                    return `${top}px`
                })
                .style("visibility", "hidden")
                .style("opacity", 0);

            const newTitles = newDropdowns
                .append("div")
                .attr("class", "image-dropdown-title2");

            const select = newTitles.append("select")
                .attr("class", "categories-select")
                .attr("id", d => `select-${d.id}`)
                .on("change", function (event, d) {
                    that.changeBox2(d.child_index, event.target.value);
                });

            select.each(function (d) {
                const sel = d3.select(this);
                sel.selectAll("option")
                    .data(["group"].concat(Object.keys(that.categories_dict)))
                    .enter()
                    .append("option")
                    .attr("value", d2 => d2)
                    .text(d2 => d2 in that.categories_dict?that.categories_dict[d2]["text"]:"Group")
                    .property("selected", d2 => d2 === d.class);
                });

            dropdowns.exit().remove();

            newGroupRects
                .append('g')
                .classed('circles', true)
                .each(function() {
                    // eslint-disable-next-line no-invalid-this
                    const circleG = d3.select(this);

                    circleG
                        .append('circle')
                        .classed('topleft', true)
                        .attr('r', that.HANDLE_R)
                        .on('mouseenter mouseleave', function(e, d) {
                            that.resizerHover(e, d, this);
                        })
                        .call(d3.drag()
                            .container(that.svg.node())
                            .subject(function(e) {
                                return {x: e.x, y: e.y};
                            })
                            .on('start end', function(e, d) {
                                that.rectResizeStartEnd(e, d, this);
                            })
                            .on('drag', function(e, d) {
                                that.rectResizing(e, d, this);
                            }),
                        );

                    circleG
                        .append('circle')
                        .classed('bottomright', true)
                        .attr('r', that.HANDLE_R)
                        .on('mouseenter mouseleave', function(e, d) {
                            that.resizerHover(e, d, this);
                        })
                        .call(d3.drag()
                            .container(that.svg.node())
                            .subject(function(e) {
                                return {x: e.x, y: e.y};
                            })
                            .on('start end', function(e, d) {
                                that.rectResizeStartEnd(e, d, this);
                            })
                            .on('drag', function(e, d) {
                                that.rectResizing(e, d, this);
                            }),
                        );
                });

            that.updateGroupBoxes();
        },
        update: function() {
            let that = this;

            let tmp_dict = {};
            for(let box of that.node.boxes) {
                tmp_dict[box.id] = box;
            }
            for(let d of that.boxes) {
                let new_class = d.class;
                let new_bbox = [d.ori_x*that.imagesize[0], d.ori_y*that.imagesize[1], d.ori_width*that.imagesize[0], d.ori_height*that.imagesize[1]];
                tmp_dict[d.id].class = new_class;
                tmp_dict[d.id].bbox = new_bbox;
            }

            that.saveNewBox();

            that.update_back_boxes();
            that.update_boxes();
            that.update_groups();
            
            that.updateImageAndMask();
            that.updateFlow();
        },
        fetchAndDrawWidgetBox: function() {
            // console.log("start image");
            const that = this;
            
            that.unselected_dict = {};

            const svg = d3.select('#svg');
            const box_g = d3.select('#box-group');

            box_g.selectAll('g').remove();

            let input_boxes = that.inputBoxes;
            let id_cnt = 0;
            let boxes = input_boxes.map(function(d) {
                id_cnt += 1;
                that.unselected_dict[id_cnt-1] = d.unselected;
                return {
                    id: id_cnt-1,
                    bbox: [d.x, d.y, d.width, d.height],
                    type: 'pred',
                    class: d.class,
                    score: d.score,
                    iscrowd: 0,
                    unselected: d.unselected,
                };
            });

            that.max_deep = 0;

            let groups = [];
            id_cnt = 10000;

            function dfs(hierarchy, deep) {
                if(typeof hierarchy === 'number') {
                    boxes[hierarchy].deep = deep;
                    return {"children": [boxes[hierarchy].id], "child_index": [hierarchy]};
                }
                id_cnt += 1;
                let tmp = {
                    id: id_cnt-1,
                    bbox: [hierarchy.x, hierarchy.y, hierarchy.width, hierarchy.height],
                    deep: hierarchy.deep,
                    max_deep: hierarchy.max_deep,
                    type: 'pred',
                    class: 'group',
                    children: [],
                    child_index: [],
                }
                if("box2" in hierarchy) {
                    tmp.bbox2 = [hierarchy.box2.x, hierarchy.box2.y, hierarchy.box2.width, hierarchy.box2.height];
                }

                that.max_deep = Math.max(that.max_deep, hierarchy.deep);
                tmp.children.push(tmp.id);
                for(let child of hierarchy.children) {
                    let tmp_child = dfs(child, hierarchy.deep-1)
                    tmp.children = tmp.children.concat(tmp_child.children);
                    tmp.child_index = tmp.child_index.concat(tmp_child.child_index);
                }

                tmp.unselected = true;
                for(let i=0;i<tmp.child_index.length;i++) {
                    if(!boxes[tmp.child_index[i]].unselected)tmp.unselected = false;
                }

                that.unselected_dict[tmp.id] = tmp.unselected;

                groups.push(tmp);
                return tmp;
            }
            if(that.inputHierarchy != null) {
                dfs(that.inputHierarchy, that.inputHierarchy.deep);
            }
            // console.log("groups", groups);
            if(groups.length == 0) {
                that.isShowHierarchy = false;
                that.$emit('show-hierarchy-change', that.isShowHierarchy);
            }

            const image = new Image();
            image.src = that.imageSrc;
            image.onload = () => {
                console.log(that.imageSrc, image);
                let node = {
                    boxes: boxes,
                    groups: groups,
                    imagesize: [image.width, image.height],
                }
                // console.log(node);
                that.node = node;
                that.raw_boxes = node.boxes;
                that.raw_groups = node.groups;
                that.getSvgImageSize(node);
                that.loadNewBox();
                that.drawWidgetBox(node);
                
                this.$parent.wait_cnt += 1;
                console.log("image add wait cnt", this.$parent.wait_cnt);
            };
        },
        restore: function(want_new) {
        },
        changeIsCrowd: function() {
            this.curBox.iscrowd = this.isCrowd;
        },
        save: function() {
        },
        addBox: function() {
            this.node.boxes.push({
                bbox: [
                    this.node.imagesize[0]/4,
                    this.node.imagesize[1]/4,
                    this.node.imagesize[0]/4,
                    this.node.imagesize[1]/4,
                ],
                iscrowd: 0,
                score: 1,
                class: this.$parent.categories[0]["name"],
                type: 'new',
                deep: 0,
                id: Math.floor(Math.random() * 100000000),
            })
            this.drawWidgetBox(this.node);
        },
        loadNewBox: function() {
            if(this.selectedItemIndex in this.$parent.new_boxes_record) {
                for(let box of this.$parent.new_boxes_record[this.selectedItemIndex]) {
                    this.node.boxes.push({
                        bbox: [
                            box.bbox[0],
                            box.bbox[1],
                            box.bbox[2],
                            box.bbox[3],
                        ],
                        iscrowd: 0,
                        score: box.score,
                        class: box.class,
                        type: 'new',
                        deep: 0,
                        id: box.id,
                    })
                }
            }
        },
        saveNewBox: function() {
            let save_boxes = [];
            // console.log(this.node.boxes);
            for(let box of this.node.boxes) {
                if(box.type != "new") continue;
                save_boxes.push({
                    bbox: [
                        box.bbox[0],
                        box.bbox[1],
                        box.bbox[2],
                        box.bbox[3],
                    ],
                    score: box.score,
                    class: box.class,
                    id: box.id,
                })
            }
            if(save_boxes.length==0) return;
            this.$parent.new_boxes_record[this.selectedItemIndex] = save_boxes;
        },
        deleteBox: function(id) {
            if(this.isDelete) {
                let indexes = this.node.boxes.findIndex(d => d.id===id);
                this.node.boxes.splice(indexes, 1);
                this.disableDelete();
                this.drawWidgetBox(this.node);
            }
        },
        enableDelete: function() {
            if(this.isDelete){
                this.isDelete = false;
                return
            }
            this.isDelete = true;
        },
        disableDelete: function() {
            this.isDelete = false;
        },
        changeBox: function(id, cls, d=null) {
            let that = this;
            let new_flag = false;
            if((d!=null)&&(d.type=="new")) { 
                let tmp_update_dict = {};
                tmp_update_dict[id] = {"new_score": d.score, "new_class": cls};
                that.tmpEdit(tmp_update_dict, "new_score", "new_class");
                return;
            }
            that.$emit('class-edit', id, cls);
        },
        changeBox2: function(ids, cls) {
            let that = this;
            that.$emit('class-edit2', ids, cls);
        },
        buttonDrag: function() {
            let tmp = document.getElementById('svg');
            if(this.is_zoom == 1) {
                tmp.classList.remove('magnifier-cursor');
                if(this.only_drag)
                    tmp.classList.add('drag-cursor');
                this.is_zoom = 0;
            }else if(this.is_zoom == -1) {
                tmp.classList.remove('shrink-cursor');
                if(this.only_drag)
                    tmp.classList.add('drag-cursor');
                this.is_zoom = 0;
            }else {
                this.only_drag = !this.only_drag;
                if(this.only_drag)
                    tmp.classList.add('drag-cursor');
                else
                    tmp.classList.remove('drag-cursor');
            }
        },
        buttonZoomIn: function() {
            let tmp = document.getElementById('svg');
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
            let tmp = document.getElementById('svg');
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
        }
    },
    mounted: function() {
        // this.fetchAndDrawWidgetBox();
        let tmp = document.getElementById('svg');
        // tmp.classList.add('drag-cursor');

        this.categories_super = this.$parent.categories_super;
        this.categories_super2 = this.$parent.categories_super2;
        this.categories = this.$parent.categories;
        this.categories2 = this.$parent.categories2;

        this.categories_dict = {};
        for(let item of this.categories) {
            this.categories_dict[item["name"]] = item;
        }
        this.categories_dict2 = {};
        for(let item of this.categories2) {
            this.categories_dict2[item["name"]] = item;
        }

        let legend_svg = d3.select("#legend-svg-image");
        let legend_svgsize = legend_svg.node().getBoundingClientRect();

        let stroke_width = 2;
        let legend_size = 20;
        legend_size = min(20, legend_svgsize.width/27);

        for(let i=0;i<this.categories_super2.length;i++) {
            // this.categories_super2[i].image_x = i/(this.categories_super2.length-1)*(legend_svgsize.width - stroke_width - legend_size*8);
            this.categories_super2[i].image_x = i/(this.categories_super2.length-1)*(legend_svgsize.width - stroke_width - legend_size*(2+this.categories_super2[0].text.length*2/3));
            // this.categories_super2[i].image_x = i/(this.categories_super2.length-1)*(legend_svgsize.width - stroke_width - legend_size*4);
        }
        const legend = legend_svg.selectAll(".legend")
            .data(this.categories_super2)
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", (d, i) => `translate(${d.image_x}, 0)`);
        legend.append("rect")
            .attr("x", stroke_width/2)
            .attr("y", legend_svgsize.height-2/3*legend_size-stroke_width/2)
            .attr("width", legend_size*2/3)
            .attr("height", legend_size*2/3)
            .attr("fill", "transparent")
            .attr("stroke-width", stroke_width)
            .attr("stroke", d => d.color);
        legend.append("rect")
            .attr("x", stroke_width/2 + legend_size)
            .attr("y", legend_svgsize.height-2/3*legend_size-stroke_width/2)
            .attr("width", legend_size*2/3)
            .attr("height", legend_size*2/3)
            .attr("fill", "transparent")
            .attr("stroke-width", stroke_width)
            .attr("stroke-dasharray", "1.5 1.5")
            .attr("stroke", d => d.color);
        legend.append("text")
            .attr("x", stroke_width/2 + 2*legend_size)
            .attr("y", legend_svgsize.height-1/3*legend_size-stroke_width/2)
            .attr("dy", '.35em')
            .text(d => d.text)
            .attr("font-size", legend_size*4/5);
        this.legend = legend;

        this.map_render = new MapRender(this);
    }
}
</script>


<style scoped>
.el-switch {
    /*--el-switch-on-color: #789FE2;*/
    /* --el-switch-on-color: #838383; */
}

.ImageEdit {
    display: inline-block;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

.sample-panel-content {
    display: flex;
    /*border-top: 2px solid #ddd;*/
    width: 100%;
    height: 94%;
    /*background-color: rgb(237, 242, 254);*/
    background-color: rgba(255, 255, 255, 0.5);
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
    /*box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.3); */
}

.ImageInlineBlock {
    width: 47.5%;
    height: calc(100% - 25px);
    margin-top: 10px;
}

.ImageFlex {
    display: flex;
    height: calc(100% - 60px);
    flex-direction: column;
}

#controls {
    display: flex;
}

.QA-block {
    display: none;
    flex-direction: column;
    height: calc(41.7% - 1.2vh);
    width: calc(100% - 15px);
    margin-left: 5px;
    margin-right: 10px;
    margin-bottom: 1.2vh;
    position: relative;
}

.QA-outer {
    height: 7vh;
    margin-bottom: 1.2vh;
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
}

.QA-outer2 {
    height: 6vh;
    margin-bottom: 1.2vh;
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
}

.QA-inner {
    height: calc(100% - 1.5vh);
    width: calc(100% - 30px);
    margin-left: 15px;
    margin-top: 0.75vh;
}

.QA-title {
    font-size: 1.25vh;
    height: 1.6vh;
    width: 100%;
    font-weight: bold;
    text-align: left;
    margin-bottom: 0.75vh;
}

.QA-content {
    height: calc(100% - 2.4vh);
    width: 100%;
    font-size: 1vh;
    font-weight: bold;
    color: #697283;
    /* display: flex; */
    align-items: center;
    vertical-align: top;
    overflow-y: auto;
}

.reply-outer {
    height: calc(100% - 15.4vh);
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
}

.reply-inner {
    height: calc(100% - 1.5vh);
    width: calc(100% - 30px);
    margin-left: 15px;
    margin-top: 0.75vh;
}

.reply-title {
    font-size: 1.25vh;
    height: 1.6vh;
    width: 100%;
    font-weight: bold;
    text-align: left;
    margin-bottom: 0.75vh;
}

.reply-content {
    white-space: pre-wrap;
    height: calc(100% - 2.4vh);
    width: 100%;
    font-size: 1vh;
    font-weight: bold;
    color: #697283;
    /* display: flex; */
    align-items: center;
    overflow-y: auto;
}

.svg-outer {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: calc(100% - 15px);
    margin-left: 5px;
    margin-right: 10px;
    /* border: 2px solid #aaa; */
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
    position: relative;
}

#svg-container {
    position: relative;
    /* border: 1px solid #ddd; */
    height: calc(100%);
    /* margin-bottom: 16px; */
    flex-shrink: 100;
    /* background-color: rgb(246, 249, 255); */
    /* border: 2px solid #aaa; */
    overflow: hidden;
}

#svg-and-dropdown {
    width: calc(100% - 40px);
    height: calc(100% - 50px);
    margin-left: 20px;
    margin-right: 20px;
    margin-top: 30px;
    margin-bottom: 20px;
    position: relative;
}

#svg {
    display: block;
    width: 100%;
    height: calc(100% - 21px);
}

#image-flow {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: calc(100% - 21px);
    pointer-events: none;
}

#legend-svg-image {
    width: 100%;
    height: 21px;
}

#category-label {
  font-size: larger;
}

#category {
  font-size: larger;
}

.tool-windows {
    position: absolute;
    pointer-events: none;
    top: 0;
    right: 0;
    z-index: 90;
    height: 100%;
    width: 25%;
}

</style>

<style>

.image-dropdown-title{
    width: 172px;
    height: 29px;
    border-radius: 5px 5px 0 0;
    background: #000;
    display: flex;
    align-items: center;
    /* justify-content: center; */
    box-shadow: 4px 4px 12px 0 rgba(105, 114, 131, 0.3);
}

.image-dropdown-title2{
    width: 172px;
    height: 29px;
    border-radius: 5px 5px 5px 5px;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 4px 4px 12px 0 rgba(105, 114, 131, 0.3);
}

.image-dropdown-body{
    width: 172px;
    height: 41px;
    border-radius: 0 0 5px 5px;
    background: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 4px 4px 12px 0 rgba(105, 114, 131, 0.3);
}

.categories-select {
    /*border-style: solid;*/
    /*border-radius: 2px;*/
    color: white;
    background-color: transparent;
    padding-left: 3px;
    width: calc(100% - 3px);
    -webkit-appearance: auto;
}

.categories-select:focus {
    outline: none;
}

.image-dropdown-body .text-div {
    width: 60%;
    height: 100%;
    font-size: 25px;
    font-weight: bold;
    display: flex;
    align-items: center;
}

.image-dropdown-body .edit-div {
    width: 30%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-dropdown-body .edit-div div {
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-dropdown-body .edit-div div svg{
    width: 20px;
    height: 20px;
}

.categories-select option {
  background-color: #f9f9f9;
  color: #333;
}

.categories-select option:hover {
  background-color: #f9f9f9;
  color: #333;
}

.show_hierarchy_switch {
    height: 20px;
}

.show_hierarchy_switch2 {
    position: absolute;
    left: 20px;
    top: 20px;
    transition: opacity 0.5s ease;
    opacity: 1;
    display: flex;
    height: 20px;
    z-index: 99;
}

.show_boxes_switch {
    position: absolute;
    left: 20px;
    top: 20px;
    transition: opacity 0.5s ease;
    opacity: 1;
    display: flex;
    height: 20px;
    z-index: 99;
}

.layer-dropdown {
    position: absolute;
    height: 20px;
    font-size: 14px;
    border-radius: 5px;
    background-color: #E9EFFB;
    /* appearance: none; */
    cursor: pointer;
    -webkit-appearance: auto;
    z-index: 99;
    top: 20px;
    left: 50%;
    transform: translate(-50%, 0);
}

#control-tree2 {
    width: calc(100% - 15px);
    margin-left: 5px;
    margin-right: 10px;
    height: 60px;
    display: flex;
}

.control2{
    display: flex;
    width: 50%;
    height: 100%;
    justify-content: center;
    align-items: end;
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

.control-padding {
    display: flex;
    width: 50%;
    height: 100%;
    align-items: end;
}
</style>