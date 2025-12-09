<template>
    <div class='view' id='grid-container'>
<!--        <div>-->
<!--            <p style="text-align: left;">-->
<!--                <span class="sub-title" style="color: #4e4e4e;"> Layout Template </span>-->
<!--            </p>-->
<!--        </div>-->
        <div id='loading-background-grid' class="my-loading" style="display: block;"></div>
        <svg id='loading-svg-grid' version="1.1" width="40px" height="40px" style="enable-background:new 0 0 512 512; display: block;" xml:space="preserve"
            class="my-loading-svg">
            <symbol id="static-update-icon" viewBox="-150 -150 812 812">
                <g>
                    <g>
                        <path
                            d="M463.702,162.655L442.491,14.164c-1.744-12.174-16.707-17.233-25.459-8.481l-30.894,30.894
                                C346.411,12.612,301.309,0,254.932,0C115.464,0,3.491,109.16,0.005,248.511c-0.19,7.617,5.347,14.15,12.876,15.234l59.941,8.569
                                c8.936,1.304,17.249-5.712,17.125-15.058C88.704,165.286,162.986,90,254.932,90c22.265,0,44.267,4.526,64.6,13.183l-29.78,29.78
                                c-8.697,8.697-3.761,23.706,8.481,25.459l148.491,21.211C456.508,181.108,465.105,172.599,463.702,162.655z" />
                    </g>
                </g>
                <g>
                    <g>
                        <path d="M499.117,249.412l-59.897-8.555c-7.738-0.98-17.124,5.651-17.124,16.143c0,90.981-74.019,165-165,165
                                c-22.148,0-44.048-4.482-64.306-13.052l28.828-28.828c8.697-8.697,3.761-23.706-8.481-25.459L64.646,333.435
                                c-9.753-1.393-18.39,6.971-16.978,16.978l21.21,148.492c1.746,12.187,16.696,17.212,25.459,8.481l31.641-31.626
                                C165.514,499.505,210.587,512,257.096,512c138.794,0,250.752-108.618,254.897-247.28
                                C512.213,257.088,506.676,250.496,499.117,249.412z" />
                    </g>
                </g>
            </symbol>
            <symbol id="animate-update-icon" viewBox="0 0 60 60">
                <g transform="translate(30,30)">
                    <path class="circle-path"
                        d="M1.2246467991473533e-15,-20A20,20,0,1,1,-20,2.4492935982947065e-15L-16,1.959434878635765e-15A16,16,0,1,0,9.797174393178826e-16,-16Z">
                    </path>
                </g>
            </symbol>
            <use xlink:href="#animate-update-icon" x="0" y="0" width="40px" height="40px"></use>
        </svg>
        <p class="sub-title" style="color: #4e4e4e;">Clusters</p>
        <div class="grid-panel-content">
            <div class="gap15"></div>
            <div class="meta-info">
                <MetaView
                    :items_len="items_len"
                />
            </div>
            <div id='main-gridlayout' class='gridlayout' @mouseenter="showButton" @mouseleave="hideButton">
                <div id='grid-top-legend' class='grid-top-legend' style="left: 10px; height:24px; width:60%">
                    <svg id='grid-top-legend-svg' style='width: 100%; height: 100%'/>
                </div>
                <div id='buttons' class='buttons hidden' style="right: 10px">
                    <div id='prop' title='Check propagation' @click='onPropClick' v-ripple class='small-button' v-show="can_prop || prop_showed">
                        <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                            <path d="M830.60526 1006.455055V298.915417l111.015651 41.404245c50.601962 0 68.354343-33.973884 39.429454-75.510888l-163.982384-217.065282c-28.933187-41.532856-76.270104-41.532856-105.186697 0l-163.986533 217.065282c-28.929038 41.532856-11.172508 98.5197 39.437751 75.510888l111.007354-41.404245v371.584431c-77.593547-105.373389-200.889415-196.16402-396.783769-222.823708l78.141179-81.850135c19.05508-44.424515-4.09064-72.789327-51.435855-63.043979l-247.969112 96.748196C32.947084 409.283867 15.124175 450.829169 40.692748 491.855881l150.374576 191.148215c25.568573 41.035009 82.273305 46.909599 81.132407-6.181596l-20.449051-113.027781s397.252574 39.836028 446.589176 443.614542" fill="#ffffff" p-id="10420"></path>
                        </svg>
                    </div>
                    <div class='gap' v-show="can_prop || prop_showed"></div>
                    <div id='cropping' title='Zoom in' @click='onCrop1Click' v-ripple class='small-button'>
                        <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 1024 1024'>
                            <path d="M477.663 848v64h-177v-64h177z m-235 0v64h-39.858C153.759 912 114 872.24 114 823.195v-48.044h64v48.044c0 13.7 11.105 24.805 24.805 24.805h39.858zM178 717.15h-64v-177h64v177z m0-235h-64v-177h64v177z m0-235h-64v-43.345C114 154.759 153.76 115 202.805 115h44.556v64h-44.556c-13.7 0-24.805 11.105-24.805 24.805v43.346zM305.36 179v-64h177v64h-177z m235 0v-64h177v64h-177z m235 0v-64h46.835C871.241 115 911 154.76 911 203.805v41.068h-64v-41.068c0-13.7-11.105-24.805-24.805-24.805h-46.834zM847 302.873h64v174.962h-64V302.873z m-57.059 439.485l112.271 112.271c12.497 12.497 12.497 32.758 0 45.255l-2.828 2.828c-12.497 12.497-32.758 12.497-45.255 0l-113-113L692.01 912.3 571.095 573.595 909.8 694.51l-119.858 47.848z" fill="white" p-id="1479"></path>
                        </svg>
                    </div>
                    <div class='gap' v-show="!in_overview"></div>
                    <div id='cropping2' title='Zoom in without expansion' @click='onCrop2Click' v-ripple class='small-button' v-show="!in_overview">
                        <svg class='icon' width='18px' height='18px' transform='translate(3, 3)' viewBox='0 0 200 200'>
                            <path d="M93.3,165.6v12.5H47.4v-12.5H93.3z M47.4,165.6v12.5h-7.8c-9.6,0-17.3-7.8-17.3-17.3v-9.4h12.5v9.4c0,2.7,2.2,4.8,4.8,4.8H47.4z M34.8,151.4H22.3v-45.9h12.5V151.4z M34.8,105.5H22.3V48.3l12.5,0V105.5z M34.8,48.3H22.3v-8.5c0-9.6,7.8-17.3,17.3-17.3h8.7V35h-8.7c-2.7,0-4.8,2.2-4.8,4.8V48.3L34.8,48.3z M48.3,35V22.5h57.2V35H48.3z M105.5,35V22.5h45.9l0,12.5H105.5z M151.4,35V22.5h9.1c9.6,0,17.3,7.8,17.3,17.3v8h-12.5v-8c0-2.7-2.2-4.8-4.8-4.8H151.4L151.4,35z M165.4,47.8h12.5v45.5h-12.5V47.8z M154.3,145l21.9,21.9c2.4,2.4,2.4,6.4,0,8.8l-0.6,0.6c-2.4,2.4-6.4,2.4-8.8,0l-22.1-22.1l-9.6,23.9L111.5,112l66.2,23.6L154.3,145L154.3,145z" fill="white" p-id="1479"></path>
                        </svg>
                    </div>
                    <div class='gap' v-show="allow_zoomout"></div>
                    <div id='zoomout' title='Zoom out' @click='onZoomOutClick' v-ripple v-show="allow_zoomout" class='small-button'>
                        <svg t="1685968804315" class="icon" viewBox="0 0 1024 1024" width='18px' height='18px'
                            transform='translate(3, 3)'>
                            <path
                                d="M312.533333 320l109.226667-109.226667-60.373333-60.373333L149.333333 362.666667l211.2 211.2 61.226667-61.866667-106.666667-106.666667A512 512 0 0 1 789.333333 874.666667h85.333334a597.333333 597.333333 0 0 0-562.133334-554.666667z"
                                p-id="13973" fill="#ffffff"></path>
                        </svg>
                    </div>
                    <div class='gap' v-show="allow_details"></div>
                    <div id='details' title='Show/hide details' @click='onDetailsClick' v-ripple v-show="allow_details"
                        class='small-button'>
                        <svg t="1685968804315" class="icon" viewBox="0 0 1024 1024" width='18px' height='18px'
                            transform='translate(3, 3)'>
                            <path
                                d="M131.84 698.221714h189.44v186.002286c0 20.992 12.434286 33.846857 32.585143 33.846857 19.712 0 32.128-12.854857 32.128-33.865143V698.221714H635.428571v186.002286c0 20.992 12.434286 33.846857 32.566858 33.846857 19.712 0 32.146286-12.854857 32.146285-33.865143V698.221714h192.420572c21.010286 0 33.865143-12.434286 33.865143-32.585143 0-20.132571-12.854857-32.146286-33.865143-32.146285H700.16V392.228571h192.420571c21.010286 0 33.865143-12.434286 33.865143-32.146285 0-20.132571-12.854857-32.548571-33.865143-32.548572H700.16V140.196571c0-21.010286-12.434286-34.285714-32.146286-34.285714-20.132571 0-32.566857 13.275429-32.566857 34.285714V327.497143H386.011429V140.214857c0-21.010286-12.434286-34.285714-32.146286-34.285714-20.150857 0-32.585143 13.275429-32.585143 34.285714V327.497143H131.84c-21.412571 0-34.267429 12.434286-34.267429 32.566857 0 19.730286 12.854857 32.146286 34.285715 32.146286h189.44v241.28H131.84c-21.430857 0-34.285714 12.013714-34.285714 32.146285 0 20.150857 12.854857 32.585143 34.285714 32.585143z m254.171429-64.731428V392.228571h249.417142v241.28z"
                                p-id="13973" fill="#ffffff"></path>
                        </svg>
                    </div>
                    <div class='gap' v-show="use_image"></div>
                    <div id='images' title='Show/hide images' @click='onImageButtonClick' v-ripple v-show="use_image"
                        class='small-button'>
                        <svg t="1685968804315" class="icon" viewBox="0 0 1024 1024" width='18px' height='18px'
                            transform='translate(3, 3)'>
                            <path
                                d="M831.792397 82.404802 191.548594 82.404802c-60.676941 0-110.042255 49.364291-110.042255 110.042255l0 640.245849c0 60.677964 49.364291 110.042255 110.042255 110.042255l640.244826 0c60.677964 0 110.042255-49.364291 110.042255-110.042255L941.835675 192.447057C941.834652 131.769093 892.470361 82.404802 831.792397 82.404802zM191.548594 122.420167l640.244826 0c38.612413 0 70.02689 31.414477 70.02689 70.02689l0 134.349871c-144.759965 4.953825-280.06151 63.59234-382.864898 166.396751-48.28061 48.28061-86.814228 103.732549-114.628714 163.962306-80.588433-68.744687-197.638289-73.051783-282.803971-12.938684L121.522728 192.447057C121.521704 153.834644 152.935158 122.420167 191.548594 122.420167zM121.521704 832.691883l0-136.601144c74.040297-72.025407 192.529945-71.925123 266.451538 0.301875-23.496134 62.998823-35.762505 130.383536-35.762505 199.672622 0 2.336208 0.420579 4.569062 1.157359 6.652514L191.548594 902.717749C152.935158 902.718773 121.521704 871.304296 121.521704 832.691883zM831.792397 902.718773 391.068743 902.718773c0.735757-2.084475 1.157359-4.317329 1.157359-6.652514 0-141.581576 55.054897-274.608312 155.023726-374.578164 95.245248-95.245248 220.499973-149.720953 354.570481-154.655336l0 465.860147C901.819287 871.304296 870.40481 902.718773 831.792397 902.718773z"
                                fill="#ffffff" p-id="1590"></path>
                                <path d="M349.471346 477.533001c75.04723 0 136.102794-61.054541 136.102794-136.101771s-61.055564-136.102794-136.102794-136.102794-136.102794 61.055564-136.102794 136.102794S274.424116 477.533001 349.471346 477.533001zM349.471346 245.343801c52.982702 0 96.087429 43.104727 96.087429 96.087429 0 52.982702-43.104727 96.087429-96.087429 96.087429-52.982702 0-96.087429-43.104727-96.087429-96.087429C253.383918 288.448528 296.488645 245.343801 349.471346 245.343801z"
                                fill="#ffffff" p-id="1591"></path>
                        </svg>
                    </div>
                </div>
                <div class="svg-outer">
                    <div class="grid-outer">
                        <svg class='grid-svg'>
                            <g class='grid-group'></g>
                            <g class='boundary-group'></g>
                            <g class='grid-group2'></g>
                            <g class='highlight-group'>
                                <defs>
                                    <filter id="dropShadow" x="-50%" y="-50%" width="200%" height="200%" filterUnits="userSpaceOnUse">
                                        <feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.25" flood-color="rgba(0, 0, 0, 1)"/>
                                    </filter>
                                </defs>
                                <g class="highlight" opacity="0" visibility="hidden"> 
                                    <rect class="highlight_rect"/>
                                    <path style="display: none" class="highlight_icon" d="M895.384423 127.91206H127.91206v767.472363h319.780152v127.912061H0V0h1023.296484v447.692212h-127.912061V127.91206zM287.802136 286.203235a325.60015 325.60015 0 0 1 501.351321 410.34189l234.590719 235.230279-92.032728 92.16064-234.590719-235.230279a325.728062 325.728062 0 0 1-409.318593-502.50253z m224.933358 416.417713a192.315783 192.315783 0 1 0-191.420398-192.315783 191.868091 191.868091 0 0 0 191.612266 192.315783z"/>
                                </g>
                            </g>
                            <g class='overview-group'></g>
                            <g class='map-group'>
                                <filter id="strokeFilter" x="-50%" y="-50%" width="200%" height="200%" filterUnits="userSpaceOnUse">
                                    <feMorphology operator="dilate" radius="2" in="SourceAlpha" result="thicker" />
                                    <feFlood flood-color="white" result="flood" />
                                    <feComposite in="flood" in2="thicker" operator="in" result="stroke" />
                                    <feMerge>
                                        <feMergeNode in="stroke" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>
                            </g>
                            <g class='confirm-group'></g>
                        </svg>
                    </div>
                    <svg class="legend-svg">
                    </svg>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { VContainer, VRow, VCol } from 'vuetify/components'; 
import * as d3 from 'd3';
import * as Global from '../plugins/global';
import GridRender from '../plugins/render_grid';
import MapRender from '../plugins/render_map';
import MetaView from './MetaView.vue';
import { mapState, mapActions } from 'vuex';
window.d3 = d3;

export default {
    name: 'GridView',
    components: {
        VContainer,
        VRow,
        VCol,
        MetaView
    },
    emits: ['item-selected'],
    data: function() {
        return {
            items: null,
            items_len: 0,
            use_image: true,
            allow_zoomout: false,
            allow_details: false,
            show_details: false,
            show_images: false,
            svg_width: 1920,
            svg_height: 1080,
            create_ani: 500,
            update_ani: 500,
            remove_ani: 500,
            mode: 'scan', // 'zoom'
            sample_area: { x1: 0, y1: 0, x2: 0, y2: 0 },
            sample_nodes: [],
            delta: 1e-5,
            in_overview: false,
            mouse_pos: {},
            mouse_pressed: false,
            data_driven: true,
            data_driven_type: 'similar', // 'discri' // 'similar'
            color_part: 'backend', // 'backend' // 'frontend'
            test: false,
            zoom_without_expand: false,
            first_flag: true,
            can_prop: false,
            prop_showed: false,
        };
    },
    methods: {
        ...mapActions(['fetchGridLayout', 'resetGridSize', 'fetchZoomOutGridLayout', 'fetchImages', 'addOnLoadingFlag', 'decOnLoadingFlag', 'addGridLoadingFlag', 'decGridLoadingFlag']),
        showButton: function() {
            let buttons = document.querySelector('#buttons');
            buttons.classList.remove('hidden');
        },
        hideButton: function() {
            let buttons = document.querySelector('#buttons');
            buttons.classList.add('hidden');
        },
        child_test: function() {
            console.log("child test");
        },
        update_detections: function(sample_id) {
            // console.log("grid view update detections", sample_id, item, this.items[sample_id]);
            this.grid_render.update_detections(sample_id);
        },
        update_detection_grids: function(sample_id) {
            this.grid_render.update_detection_grids(sample_id);
        },
        click_grid: function(sample_id) {
            console.log("click", sample_id);
            this.map_render.render(this.map_info);
            this.$emit('item-selected', sample_id);
        },
        render_influence_map: function() {
            this.map_render.render(this.map_info);
        },
        // zoom in overview
        overview_recall_mousedown: function (ev) {
            this.mouse_pos = {
                x: ev.offsetX,
                y: ev.offsetY
            };
            this.mouse_pressed = true;
            this.adjustSamplingArea(this.mouse_pos.x, this.mouse_pos.y, this.mouse_pos.x, this.mouse_pos.y);
            this.confirm_group.style('visibility', 'hidden');
        },
        overview_recall_mousemove: function (ev) {
            if (!this.mouse_pressed) {
                return;
            }
            this.adjustSamplingArea(this.mouse_pos.x, this.mouse_pos.y, ev.offsetX, ev.offsetY);
        },
        overview_recall_mouseup: function (ev) {
            if (!this.mouse_pressed) {
                return;
            }
            this.mouse_pressed = false;
            this.sample_area = {
                x1: this.mouse_pos.x,
                y1: this.mouse_pos.y,
                x2: ev.offsetX,
                y2: ev.offsetY
            };
            if (Math.abs(this.sample_area.x1 - this.sample_area.x2) < this.delta && Math.abs(this.sample_area.y1 - this.sample_area.y2) < this.delta) {
                this.confirm_group.style('visibility', 'hidden');
                return;
            }
            this.confirm_group
                .attr('transform', 'translate(' + (ev.offsetX) + ',' + (ev.offsetY) + ')')
                .style('visibility', 'visible');
        },
        initOverview: function () {
            this.overview_group
                .attr('transform', 'translate(0, 0)')
                .style('visibility', 'hidden');
            this.overview_group
                .append('rect')
                .attr('id', 'overview')
                .attr('class', 'overview-box');
            this.overview_group
                .selectAll('.overview-box')
                .attr('x', 0)
                .attr('y', 0)
                .style('fill', 'white')
                .style('stroke', 'grey')
                .style('stroke-width', 5)
                .style('opacity', 0.3);
            this.overview_group
                .append('rect')
                .attr('id', 'viewbox')
                .style('stroke-dasharray', '5, 5')
                .style('fill', 'white')
                .style('stroke', 'grey')
                .style('stroke-width', 5)
                .style('opacity', 0.5);

            this.overview_group
                .style('pointer-events', 'none');
            // .on('mousedown', this.overview_recall_mousedown)
            // .on('mousemove', this.overview_recall_mousemove)
            // .on('mouseup', this.overview_recall_mouseup);

            this.confirm_group
                .attr('id', 'confirm-zoom')
                .style('visibility', 'hidden')
                .style('cursor', 'pointer')
                .on('click', this.onZoomInClick);
            this.confirm_group.append('circle')
                .attr('r', 20)
                .attr('fill', 'grey');
            let box = this.confirm_group.append('g')
                .attr('class', 'confirm-icon')
                .attr('transform', `scale(${26 / 1024}) translate(${-512}, ${-512})`);
            box.append('path')
                .attr('d', Global.d_confirm1)
                .attr('fill', 'white')
                .attr('stroke', 'black')
                .attr('stroke-width', 2);
            box.append('path')
                .attr('d', Global.d_confirm2)
                .attr('fill', 'white')
                .attr('stroke', 'black')
                .attr('stroke-width', 2);
        },
        enterOverview: function () {
            this.mode = 'zoom';
            this.allow_zoomout = false;
            d3.select('#cropping').select('path').attr('d', Global.d_rollback);
            let meta = this.grid_render.meta;
            this.overview_group.select('#overview')
                .attr('x', meta.delta_x)
                .attr('y', meta.delta_y)
                .attr('width', meta.grid_width)
                .attr('height', meta.grid_height);
            this.overview_group.style('visibility', 'visible');
            this.in_overview = true;
        },
        exitOverview: function () {
            this.mode = 'scan';
            if (this.gridstack.length > 2) this.allow_zoomout = true;
            d3.select('#cropping').select('path').attr('d', Global.d_scan);
            this.overview_group.style('visibility', 'hidden');
            this.in_overview = false;
            this.overview_group.select('#viewbox')
                .attr('width', 0)
                .attr('height', 0);
            this.confirm_group.style('visibility', 'hidden');
        },

        // zoom in sampling
        adjustSamplingArea: function (x1, y1, x2, y2) {
            if (x1 > x2) { let tmp = x1; x1 = x2; x2 = tmp; }
            if (y1 > y2) { let tmp = y1; y1 = y2; y2 = tmp; }
            this.overview_group.select('#viewbox')
                .attr('x', x1)
                .attr('y', y1)
                .attr('width', x2 - x1)
                .attr('height', y2 - y1);
        },
        filterSamples: function () {
            this.sample_nodes = this.grid_render.filter_grids(this.sample_area);
            // console.log('zoom in', this.sample_nodes);
        },

        // buttons click apis
        onCropClick: function () {
            if (this.mode === 'scan') {
                this.enterOverview();
            } else {
                this.exitOverview();
            }
        },
        onPropClick: function () {
            this.$parent.$parent.checkCrossInfluenceExcute(this.prop_showed);
            this.prop_showed = !this.prop_showed;
        },
        onCrop1Click: function () {
            this.zoom_without_expand = false;
            this.onCropClick();
        },
        onCrop2Click: function () {
            this.zoom_without_expand = true;
            this.onCropClick();
        },
        onZoomInClick: function () {
            this.filterSamples();
            this.grid_render.in_update = true;
            let args = {
                samples: this.sample_nodes,
                zoom_without_expand: this.zoom_without_expand
            };
            this.fetchGridLayout(args);
        },
        onZoomOutClick: function () {
            this.grid_render.in_update = true;
            this.grid_render.is_zoomout = true;
            this.fetchZoomOutGridLayout();
        },
        onDetailsClick: function () {
            this.show_details = !this.show_details;
            if (this.show_details) this.grid_render.show_details();
            else this.grid_render.hide_details();
        },
        onImageButtonClick: function () {
            this.show_images = !this.show_images;
            if(!this.use_image) {
                this.show_images = false;
            }
            if (this.show_images) this.grid_render.show_images();
            else this.grid_render.hide_images();
        },
        checkCrossInfluence: function(influenceDict, representDict) {
            this.grid_render.checkCrossInfluence(influenceDict, representDict);
        },
        drawLegend: function() {
            let grid_margin = 10+3;
            let legend_size = 20;
            legend_size = min(20, (this.svg_width-grid_margin*2)/30);

            // let color_dict2 = ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373"];
            let color_dict2 = ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373"].reverse();
            // let color_dict2 = ["rgba(6, 96, 254, 1)", "rgba(6, 96, 254, 0.75)", "rgba(6, 96, 254, 0.5)", "rgba(6, 96, 254, 0.25)", "rgba(6, 96, 254, 0.15)"]

            const categories = [
                { name: "1~5 Boxes", color: color_dict2[0], x: 0, max: 5},
                { name: "6~10 Boxes", color: color_dict2[1], x: 0.25*((this.svg_width-grid_margin*2) - legend_size*5), max: 10},
                { name: "11~15 Boxes", color: color_dict2[2],  x: 0.5*((this.svg_width-grid_margin*2) - legend_size*5), max: 15},
                { name: "16~20 Boxes", color: color_dict2[3],  x: 0.75*((this.svg_width-grid_margin*2) - legend_size*5), max: 20},
                { name: ">20 Boxes", color: color_dict2[4],  x: 1*((this.svg_width-grid_margin*2) - legend_size*5)},
            ];
            this.quantiles = this.$parent.$parent.quantiles;
            let tmp_cnt = 0, last_cnt=0;
            for(let quantile of this.quantiles) {
                categories[tmp_cnt].max = quantile.value;

                // categories[tmp_cnt].name = `${last_cnt+1}~${categories[tmp_cnt].max} Boxes`;
                categories[tmp_cnt].name = `${last_cnt.toFixed(2)}~${categories[tmp_cnt].max.toFixed(2)}`;

                last_cnt = categories[tmp_cnt].max;
                tmp_cnt += 1;
            }

            // categories[tmp_cnt].name = `>${last_cnt+1} Boxes`;
            categories[tmp_cnt].name = `${last_cnt.toFixed(2)}~1.00`;

            this.categories = categories;

            let legend_svgsize = this.legend_svg.node().getBoundingClientRect();

            const legend = this.legend_svg.selectAll(".legend")
                .data(categories)
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", (d, i) => `translate(${d.x}, 0)`);
            legend.append("rect")
                .attr("x", grid_margin)
                .attr("y", legend_svgsize.height-2/3*legend_size-0.5)
                .attr("width", legend_size*2/3)
                .attr("height", legend_size*2/3)
                .attr("fill", d => d.color)
                .attr("stroke", "black");
            legend.append("text")
                .attr("x", grid_margin + legend_size)
                .attr("y", legend_svgsize.height-1/3*legend_size-0.5)
                .attr("dy", '.35em')
                .text(d => d.name)
                .attr("font-size", legend_size*4/5);
            this.legend = legend;
        }, 
        drawLegend2: function() {
            let grid_margin = 10+3;
            let legend_svgsize = this.legend_svg.node().getBoundingClientRect();
            let legend_size = legend_svgsize.height;
            let text_margin = legend_size*4;
            let middle_margin = legend_size*0.5;

            let color_dict2 = ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373"].reverse();

            let categories = [
                {color: color_dict2[0], idx: 0},
                {color: color_dict2[1], idx: 1},
                {color: color_dict2[2], idx: 2},
                {color: color_dict2[3], idx: 3},
                {color: color_dict2[4], idx: 4},
            ];
            this.quantiles = this.$parent.$parent.quantiles;
            let tmp_cnt = 0, last_cnt=0;
            for(let quantile of this.quantiles) {
                categories[tmp_cnt].min = last_cnt;
                categories[tmp_cnt].max = quantile.value;

                // categories[tmp_cnt].name = `${last_cnt+1}~${categories[tmp_cnt].max} Boxes`;
                categories[tmp_cnt].name = `${categories[tmp_cnt].max.toFixed(2)}`;

                last_cnt = categories[tmp_cnt].max;
                tmp_cnt += 1;
            }

            categories[tmp_cnt].min = last_cnt;
            categories[tmp_cnt].max = 1;
            categories[tmp_cnt].name = "1";

            let ori_categories = categories
            categories = [{color: categories[0].color, min: 0, max: 0, name: "0"}].concat(categories);

            this.categories = categories;

            let rect_size = Math.min(text_margin/(ori_categories.length+1), (1/2-1/12)*legend_size);
            this.legend_svg.selectAll(".legend_rect")
                .data(ori_categories)
                .enter().append("rect")
                .attr("class", "legend_rect")
                .attr("x", d => grid_margin+(text_margin-rect_size)*d.idx/(ori_categories.length-1))
                .attr("y", 1/12*legend_size)
                .attr("width", rect_size)
                .attr("height", rect_size)
                .attr("fill", d => d.color)
                .attr("stroke", "black");

            this.legend_svg.append("text")
                .attr("x", grid_margin)
                .attr("y", 3/4*legend_size)
                .attr("dy", '.35em')
                .text("Avg Confidence Score:")
                .attr("font-size", legend_size*2/5);

            const legend = this.legend_svg.selectAll(".legend")
                .data(categories)
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", (d, i) => `translate(${grid_margin+text_margin+middle_margin+(this.svg_width-grid_margin*2-text_margin-middle_margin)*d.min}, 0)`);
            legend.append("rect")
                .attr("x", 0)
                .attr("y", 1/6*legend_size)
                .attr("width", d => (this.svg_width-grid_margin*2-text_margin-middle_margin)*(d.max-d.min))
                .attr("height", legend_size*1/3)
                .attr("fill", d => d.color)
                .attr("stroke", "black");
            legend.append("line")
                .attr("x1", d => (this.svg_width-grid_margin*2-text_margin-middle_margin)*(d.max-d.min))
                .attr("y1", 1/12*legend_size)
                .attr("x2", d => (this.svg_width-grid_margin*2-text_margin-middle_margin)*(d.max-d.min))
                .attr("y2", 7/12*legend_size)
                .attr("stroke", "black")
            legend.append("text")
                .attr("x", d => (this.svg_width-grid_margin*2-text_margin-middle_margin)*(d.max-d.min))
                .attr("y", 2/3*legend_size)
                .attr("dy", '.75em')
                .attr("text-anchor", "middle")
                .text(d => d.name)
                .attr("font-size", legend_size*1/4);
            this.legend = legend;
        },
        drawTopLegend: function() {
            let legend_svg = d3.select("#grid-top-legend-svg");
            let legend_svgsize = legend_svg.node().getBoundingClientRect();

            let stroke_width = 2;
            let legend_size = 20;
            legend_size = min(20, legend_svgsize.width/23);

            let categories_super2 = this.$parent.$parent.categories_super2;
            for(let i=0;i<categories_super2.length;i++) {
                categories_super2[i].image_x = i/(categories_super2.length-1)*(legend_svgsize.width - stroke_width - legend_size*(2+categories_super2[0].text.length*2/3));
            }
            const legend = legend_svg.selectAll(".legend")
                .data(categories_super2)
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
            legend.append("text")
                .attr("x", stroke_width/2 + 1*legend_size)
                .attr("y", legend_svgsize.height-1/3*legend_size-stroke_width/2)
                .attr("dy", '.35em')
                .text(d => d.text)
                .attr("font-size", legend_size*4/5);
            this.legend = legend;
        },
        drawGridLayout(grid_info) {
            if (this.in_overview) this.exitOverview();

            if (this.color_part === 'backend') {
                this.grid_render.render(grid_info);
                if(this.first_flag) {
                    this.grid_render.grid_click(this.grid_render.grids[0]);
                }
                this.map_info = null;
                this.map_render.render(this.map_info, true);

                if (this.test) {
                    let refresh_times = localStorage.getItem('refresh_times');
                    if (refresh_times === null) {
                        localStorage.setItem('refresh_times', 1);
                    } else {
                        refresh_times = parseInt(refresh_times);
                        // console.log('refresh_times', refresh_times);
                        if (refresh_times >= 10) {
                            localStorage.setItem('refresh_times', 0);
                        } else {
                            localStorage.setItem('refresh_times', refresh_times + 1);
                            setTimeout(() => {
                                window.location.reload();
                            }, 5000);
                        }
                    }
                }
                return;
            }
        },
    },
    computed: {
        ...mapState(['gridlayout', 'images', 'chosen_ids', 'gridstack', 'colorstack', 'evaluations', 'eval_mode', 'thresholdValue', 'on_loading_flag', 'grid_loading_flag', 'setting_loading_flag']),
        svg: function () {
            return d3.select('.grid-svg');
        },
        legend_svg: function() {
            return d3.select('.legend-svg');
        },
        grid_group: function () {
            return d3.select('.grid-group');
        },
        grid_group2: function () {
            return d3.select('.grid-group2');
        },
        boundary_group: function () {
            return d3.select('.boundary-group');
        },
        highlight_group: function () {
            return d3.select('.highlight-group');
        },
        overview_group: function () {
            return d3.select('.overview-group');
        },
        map_group: function () {
            return d3.select('.map-group');
        },
        confirm_group: function () {
            return d3.select('.confirm-group');
        }
    },
    watch: {
        on_loading_flag: function (on_loading_flag) {
            // document.getElementById('setting-title').innerHTML = 'Settings_' + on_loading_flag;
            if (on_loading_flag > 0) {
                d3.select('#main-gridlayout').classed('pointer-disabled', true);
                document.getElementById('loading-background').style.visibility = 'visible';
                document.getElementById('loading-svg').style.visibility = 'visible';
            } else {
                d3.select('#main-gridlayout').classed('pointer-disabled', false);
                document.getElementById('loading-background').style.visibility = 'hidden';
                document.getElementById('loading-svg').style.visibility = 'hidden';
            }
        },
        grid_loading_flag: function (grid_loading_flag) {
            if (grid_loading_flag > 0) {
                // console.log('show');
                document.getElementById('loading-background-grid').style.visibility = 'visible';
                document.getElementById('loading-svg-grid').style.visibility = 'visible';
                // document.getElementById('loading-svg').style.opacity = '0.7';
                // console.log('show end', d3.select('#loading-background-grid').style('display'));
            } else {
                // console.log('hide');
                document.getElementById('loading-background-grid').style.visibility = 'hidden';
                document.getElementById('loading-svg-grid').style.visibility = 'hidden';
                // console.log('hide end', d3.select('#loading-background-grid').style('display'));
            }
        },
        setting_loading_flag: function (setting_loading_flag) {
            /* if (setting_loading_flag > 0) {
                document.getElementById('loading-background-setting').style.visibility = 'visible';
                document.getElementById('loading-svg-setting').style.visibility = 'visible';
                // d3.select('#loading-background-setting')
                //         .style('display', 'block');
                // d3.select('#loading-svg-setting')
                //         .style('display', 'block');
            } else {
                document.getElementById('loading-background-setting').style.visibility = 'hidden';
                document.getElementById('loading-svg-setting').style.visibility = 'hidden';
                // d3.select('#loading-background-setting')
                //         .style('display', 'none');
                // d3.select('#loading-svg-setting')
                //         .style('display', 'none');
            } */
        },
        evaluations: function (evaluations) {
        },
        gridlayout: async function (grid_info) {
            let new_ids = [];
            for(let id of grid_info.sample_ids) {
                if((this.items == null)||(!(id in this.items))) new_ids.push(id);
            }
            this.$parent.$parent.fetchDataIds(new_ids)
                .then(response => {
                    if(this.first_flag) {
                        this.drawLegend2();
                        this.drawTopLegend();
                    }
                    this.items = this.$parent.$parent.items;
                    this.items_len = this.$parent.$parent.items_len;
                    console.log("items len", this.items_len);
                    this.drawGridLayout(grid_info);
                    this.first_flag = false;
                })
        },
        images: function (images) {
            this.grid_render.render_images(images, this.chosen_ids);
        },
        gridstack: {
            handler: function (gridstack) {
                // console.log("gridstack", gridstack);
                if (gridstack.length > 2) {
                    this.allow_zoomout = true;
                } else {
                    this.allow_zoomout = false;
                }
                this.show_details = false;
            },
            deep: true,
        },
    },
    mounted() {
        // console.log('grid mounted');
        document.getElementById('loading-background-grid').style.visibility = 'hidden';
        document.getElementById('loading-svg-grid').style.visibility = 'hidden';

        let container = d3.select('.grid-outer');
        let bbox = container.node().getBoundingClientRect();
        this.svg_width = bbox.width;
        this.svg_height = bbox.height;
        // this.svg.attr('width', this.svg_width);
        // this.svg.attr('height', this.svg_height);
        // console.log("width", this.svg_width, "height", this.svg_height);

        // this.create_ani = Global.Animation;
        // this.update_ani = Global.Animation;
        // this.remove_ani = Global.Animation;

        let that = this;
        this.grid_render = new GridRender(that);
        this.map_render = new MapRender(that);
        this.initOverview();
        
        this.grid_margin = 10;
        this.top_margin = 2 + 24 + 6;
        this.grid_size = [30, 30]
        this.grid_size[0] = Math.max(1, Math.round((this.svg_height-this.top_margin)/(this.svg_width-2*this.grid_margin)*this.grid_size[1]));

        console.log("grid fetch");
        // this.$parent.$parent.fetchData()
        //     .then(response => {
        //         this.drawLegend2();

        //         this.items = response.data.data;
        //         this.resetGridSize(this.grid_size)
        //             .then(() => {
        //                 this.fetchGridLayout([]);
        //                 // this.$parent.$parent.selectItem(4);
        //             })
        //     })
        
        this.resetGridSize(this.grid_size)
            .then(() => {
                this.fetchGridLayout([]);
                // this.$parent.$parent.selectItem(4);
            })
    },
};
</script>

<style scoped>

#grid-container {
    width: 100%;
    /* height: 65%; */
    height: 100%;
    /* max-width: calc(98% - 380px); */
    position: relative;
}

.grid-panel-content{
    /*border-top: 2px solid #ddd;*/
    width: 100%;
    height: 94%;
    /*background-color: rgb(237, 242, 254);*/
    background-color: rgba(255, 255, 255, 0.5);
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
    /*box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.3); */
}

.gap15 {
    width: 100%;
    height: 10px;
}
.meta-info {
    width: 100%;
    height: 16%;
    /*margin-top: 20px;*/
    /* margin: 0.5%; */
    position: relative;
}

.gridlayout {
    /* width: 99%; */
    width: 100%;
    /* height: 89%; */
    height: calc(84% - 20px);
    margin-bottom: 10px;
    /* margin: 0.5%; */
    position: relative;
}

.svg-outer {
    width: 100%;
    /* height: 95.5%; */
    height: 100%;
    /* border: 2px solid #aaa; */
}

.grid-outer {
    width: 100%;
    height: calc(100% - 35px);
}

.legend-svg {
    margin-top: 5px;
    width: 100%;
    height: 30px;
}

.grid-svg {
    height: 100%;
    width: 100%;
}

.MetaView {
    width: 100%;
    /* height: 80%; */
    height: 100%;
    /* border: 2px solid #aaa; */
}
</style>
