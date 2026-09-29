<template>
    <div class="grid-panel">
        <GridView
            ref="child_grid"
            @item-selected="selectItem"
        />
        <!-- <ListView
            ref="child_grid"
            :items="items"
            :selectedItemIndex="selectedItemIndex"
            @item-selected="selectItem"
        /> -->
        <!-- <SampleView
            ref="child_sample"
            :item="item"
            :selectedItemIndex="selectedItemIndex"
            @categroy-selected="updateCategory"
            @click-node="clickNode"
        /> -->
    </div>
</template>

<script>
import { VContainer, VRow, VCol } from 'vuetify/components'; 
import * as d3 from 'd3';
import * as Global from '../plugins/global';
import { mapState, mapActions } from 'vuex';
import GridView from './GridView.vue';
import SampleView from './SampleView.vue';
window.d3 = d3;

export default {
    name: 'GridPanel',
    components: {
        VContainer,
        VRow,
        VCol,
        GridView,
        SampleView,
    },
    // props: ['item', 'items', 'selectedItemIndex'],
    props: ['item', 'selectedItemIndex'],
    emits: ['item-selected', 'categroy-selected', 'click-node'],
    data: function() {
        return {
        };
    },
    methods: {
        child_test: function() {
            console.log("child test");
        },
        update_detections: function(sample_id) {
            this.$refs.child_grid.update_detections(sample_id);
        },
        update_detection_grids: function(sample_id) {
            this.$refs.child_grid.update_detection_grids(sample_id);
        },
        selectItem: function(sample_id) {
            this.$emit('item-selected', sample_id);
        },
        updateCategory: function() {
            if (this.item !== null) {
                this.$emit('categroy-selected');
            }
        },
        clickNode: function(id) {
            this.$emit('click-node', id);
        },
        setClick: function(id) {
            if(this.$refs.child_sample != null)
                this.$refs.child_sample.setClick(id);
        },
        setShowHierarchy: function(show) {
            if(this.$refs.child_sample != null)
                this.$refs.child_sample.setShowHierarchy(show);
        },
    },
    computed: {
    },
    watch: {
    },
    mounted() {
    },
};
</script>

<style scoped>

.pointer-disabled {
    pointer-events: none;
}

.label-text {
  color: rgb(78, 78, 78);
  font-weight: bold;
  font-size: 18px;
}

.grid-panel {
  display: inline-block;
  vertical-align: top;
}
</style>
