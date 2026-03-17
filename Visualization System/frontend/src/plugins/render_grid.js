/* eslint-disable */
import * as d3 from "d3";
import { GridLayout } from "./layout_grid";

const GridRender = function(parent) {
  let that = this;
  that.parent = parent;
  that.layout = new GridLayout(this);
  that.init = true;
  that.in_update = true;
  that.is_zoomout = false;
  that.render_image = false;
  that.image_border = 4;
  that.image_history = new Set();
  that.image_records = new Set();
  that.boundary_border = 100;
  that.mode = ["alpha", "isolate_label", 'boundary']; // 'alpha', 'boundary', 'isolate_label';
  // that.pboundary_stroke = "gray";
  that.pboundary_stroke = "white";
  that.pboundary_stroke_width = 1;
  that.one_partition = false;
  that.hide_opacity = 0.4;
  // that.min_image_size = 44;
  // that.min_image_size2 = 80;
  that.min_image_size = 36;
  that.min_image_size2 = 50;
  
  that.current_click = -1;

  that.current_hover = -1;

  let dark_bias = 0;
  let dark_rate = 0.33;
  let light_bias = 255;
  let light_rate = 0;
  let bar_rate = 1;

  // let color_dict = {"good": "lightgreen", "normal": "rgb(255, 242, 0)", 'normal-only-image': "rgb(255, 242, 0)", 'normal-only-small-image': "rgb(255, 242, 0)", "bad": "rgb(244, 115, 121)"}
  // let color_dict = {"good": "rgba(80, 80, 80, 0)", "normal": "rgba(80, 80, 80, 0.2)", 'normal-only-image': "rgba(80, 80, 80, 0.2)", 'normal-only-small-image': "rgba(80, 80, 80, 0.2)", "bad": "rgba(80, 80, 80, 0.4)"}
  // let color_dict = {"good": "rgba(219, 245, 251, 1.0)", "normal": "rgba(198, 237, 248, 1.0)", 'normal-only-image': "rgba(198, 237, 248, 1.0)", 'normal-only-small-image': "rgba(198, 237, 248, 1.0)", "bad": "rgba(158, 224, 243, 1.0)"}
  let color_dict = {"good": "rgb(240, 240, 240)", "normal": "rgb(200, 200, 200)", 'normal-only-image': "rgb(200, 200, 200)", 'normal-only-small-image': "rgb(200, 200, 200)", "bad": "rgb(160, 160, 160)"}
  let color_dict2 = ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373"].reverse();
  // let color_dict2 = ["rgba(6, 96, 254, 1)", "rgba(6, 96, 254, 0.75)", "rgba(6, 96, 254, 0.5)", "rgba(6, 96, 254, 0.25)", "rgba(6, 96, 254, 0.15)"]

  that.getBoxColor = function(d) {
    if (d.detection_category != null) {
      return color_dict[d.detection_category];
    }

    // if(d.detection_boxes != null) {
    //   if(d.detection_boxes.length >= 5*color_dict2.length) {
    //     return color_dict2[color_dict2.length-1];
    //   }
    //   return color_dict2[Math.floor(d.detection_boxes.length/5)];
    // }
    
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

    if(d.detection_boxes != null) {
      for(let i=0;i<that.parent.categories.length-1;i++)
      // if(d.detection_boxes.length <= that.parent.categories[i].max) {
      // if(getAvgConfidence(d.detection_boxes) <= that.parent.categories[i].max) {
        if(getAvgConfidence(d.detection_boxes, true) <= that.parent.categories[i].max) {
      // if(getClassAvgConfidence(d.detection_boxes) <= that.parent.categories[i].max) {
        return that.parent.categories[i].color;
      }
      return that.parent.categories[that.parent.categories.length-1].color;
    }
    return "transparent";
  }

  that.update_detection_grids = function(sample_id=null){
    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);
    if(sample_id == null) {
      that.e_grids
        .select("rect.category")
        .attr("fill", function(d) {
          // if(d.detection_category in color_dict)
          //   return color_dict[d.detection_category];
          // return "transparent";
          // // return "black";
          return that.getBoxColor(d);
        })
        .attr("stroke", function(d) {
          if((d.detection_category!=null)&&(d.detection_category!=""))
            // return "white";
            // return "rgb(80, 80, 80)";
            return "transparent";
          else
            return "transparent";
        })
        .attr("width", d => d.width)
        .attr("height", d => d.height)
        .attr("x", d => d.width*0)
        .attr("y", d => d.height*0);
    } else {
      that.e_grids
        .select("rect.category")
        .filter(d => d.sample_id == sample_id)
        .attr("fill", function(d) {
          // if(d.detection_category in color_dict)
          //   return color_dict[d.detection_category];
          // return "transparent";
          // // return "black";
          return that.getBoxColor(d);
        })
        .attr("stroke", function(d) {
          if((d.detection_category!=null)&&(d.detection_category!=""))
            // return "white";
            // return "rgb(80, 80, 80)";
            return "transparent";
          else
            return "transparent";
        })
        .attr("width", d => d.width)
        .attr("height", d => d.height)
        .attr("x", d => d.width*0)
        .attr("y", d => d.height*0);
    }
    // console.log("end");
    // console.log(that.e_grids.select("rect.category").filter(d => d.sample_id == sample_id).attr("fill"));
  }

  that.update_detections = function(sample_id) {
    // console.log("update grid", sample_id, item.category);
    console.log("grid render update detections", sample_id, that.detection_items[sample_id]);
    that.grids.forEach(grid => {
      if ((sample_id == null) || (grid.sample_id == sample_id)) {
        grid.detection_category = that.detection_items[grid.sample_id].category;
        grid.detection_boxes = that.detection_items[grid.sample_id].boxes;
      }
    });
    that.update_detection_grids(sample_id);
  };

  that.update_info_from_parent = function() {
    that.svg = that.parent.svg;
    that.grid_group = that.parent.grid_group;
    that.grid_group2 = that.parent.grid_group2;
    that.map_group = that.parent.map_group;
    that.boundary_group = that.parent.boundary_group;
    that.highlight_group = that.parent.highlight_group;
    that.render_image = that.parent.use_image;

    that.grid_margin = that.parent.grid_margin;
    that.top_margin = that.parent.top_margin;

    that.create_ani = that.parent.create_ani;
    that.update_ani = that.parent.update_ani;
    that.remove_ani = that.parent.remove_ani;
    that.fast_ani = 400;
    that.colorinter = d3.interpolateHcl;
    that.svg_width = that.parent.svg_width;
    that.svg_height = that.parent.svg_height;
    that.gridstack = that.parent.gridstack;
    that.detection_items = that.parent.items;
  };

  that.update_info_from_parent();

  that.render = function(grid_info, color_set = null, two_stage = false) {
    that.parent.addOnLoadingFlag();
    // that.parent.addGridLoadingFlag();
//    console.log("+1");
    if (two_stage && color_set !== null) {
      that.grids = that.layout.update_color(that.grids, color_set);
    } else {
      // update info
      that.update_info_from_parent();

      // update state
      let [meta, grids] = that.layout.update_layout(grid_info, color_set);
      that.meta = meta;
      that.grids = grids;
//      console.log("render_", that.meta.max_pid);
      if (two_stage) return [meta, grids];
    }
    that.grid_width = that.layout.cell - 2 * that.layout.stroke_width
    that.image_border = max(4, 0.1*that.grid_width);
    if(that.grid_width - 2*that.image_border >= that.min_image_size)that.image_width = that.grid_width - 2*that.image_border;
    else that.image_width = that.min_image_size2;
    if(that.grid_width-2*that.image_border<that.image_width*0.9)that.image_has_stroke=true;
    else that.image_has_stroke=false;

//    console.log("render", that.meta);
    if (that.meta.max_pid === 1) {
      that.one_partition = true;
      that.parent.allow_details = false;
      // that.one_partition = false;
    } else {
      that.one_partition = false;
      that.parent.allow_details = true;
      // that.one_partition = true;
    }

    // update view
    that.grid_group
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.init ? 0 : that.update_ani)
      .attr(
      "transform",
      `translate(${that.meta.delta_x}, ${that.meta.delta_y})`
    );
    that.grid_group2
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.init ? 0 : that.update_ani)
      .attr(
      "transform",
      `translate(${that.meta.delta_x}, ${that.meta.delta_y})`
    );
    that.map_group
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.init ? 0 : that.update_ani)
      .attr(
      "transform",
      `translate(${that.meta.delta_x}, ${that.meta.delta_y})`
    );
    that.boundary_group
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.init ? 0 : that.update_ani)
      .attr(
      "transform",
      `translate(${that.meta.delta_x}, ${that.meta.delta_y})`
    );
    that.highlight_group
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.init ? 0 : that.update_ani)
      .attr(
      "transform",
      `translate(${that.meta.delta_x}, ${that.meta.delta_y})`
    );
    that.init_recall();
    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);
    that.e_paths = that.boundary_group
      .selectAll(".partition_boundary")
      .data(that.meta.paths, d => d.name);
    that.e_cpaths = that.boundary_group
      .selectAll(".class_boundary")
      .data(that.meta.cpaths, d => d.name);

    that.create();
    that.update();
    that.remove();
    if (that.init) that.init = false;
//    console.log("render_image", that.render_image, that.grids.length);
    if (that.render_image) {
      let chosen_names = [];
      let chosen_ids = [];
      that.grids.forEach(grid => {
        if (grid.show_image) {
          chosen_names.push(grid.name);
          chosen_ids.push(grid.index);
        }
      });
      // console.log(chosen_names, chosen_ids);
      that.parent.fetchImages({names: chosen_names, ids: chosen_ids, batch: true});
    } else that.image_history = that.image_records;

    setTimeout(function() {
      that.parent.decOnLoadingFlag();
      // that.parent.decGridLoadingFlag();
//      console.log("-1");
    }, (that.init ? that.create_ani : that.remove_ani + that.update_ani + that.create_ani) + 100);
  };

  that.filter_grids = function(filter_area) {
    let filter_grids = that.grids.filter(grid => {
      let center_x = that.meta.delta_x + grid.x + grid.width / 2;
      let center_y = that.meta.delta_y + grid.y + grid.height / 2;
      return (
        center_x >= filter_area.x1 &&
        center_x <= filter_area.x2 &&
        center_y >= filter_area.y1 &&
        center_y <= filter_area.y2
      );
    });
    return filter_grids.map(d => d.name);
  };

  that.render_images = function(images, chosen_ids) {
    that.image_records = new Set();
    if (chosen_ids === null) {
      that.grids.forEach(grid => {
        grid.img = `data:image/jpeg;base64,${images[grid.name]}`;
        that.image_records.add(grid.sample_id);
      });
    } else {
      chosen_ids.forEach((id, i) => {
        that.grids[that.layout.id_map[id]].img = `data:image/jpeg;base64,${images[i]}`;
        that.image_records.add(that.grids[that.layout.id_map[id]].sample_id);
      });
      if (images.length === 1 && that.current_hover === that.grids[that.layout.id_map[chosen_ids[0]]].name) {
        let meta_image = document.querySelector('#meta-image');
        let image_container = document.querySelector('#meta-image-container');
//        meta_image.style.width = 'auto';
//        meta_image.style.height = 'auto';
        if(meta_image != null) {
          meta_image.src = `data:image/jpeg;base64,${images[0]}`;
          let containerRatio = image_container.clientWidth / image_container.clientHeight;
          let imageRatio = meta_image.naturalWidth / meta_image.naturalHeight;
          if (containerRatio < imageRatio) {
              meta_image.style.width = '100%';
              meta_image.style.height = 'auto';
          } else {
              meta_image.style.width = 'auto';
              meta_image.style.height = '100%';
          }
        }
      }
    }

    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
        .selectAll(".grid-cell2")
        .data(that.grids, d => d.sample_id);

    that.e_grids2
      .select(".image_g")
      .filter(d => that.image_records.has(d.sample_id))
      .attr("opacity", 0)
      .style("visibility", "hidden")
      .filter(d => d.show_image)
      .transition()
      .ease(d3.easeSin)
      .delay(function (d) {
        let tmp = (that.init ? 0 : that.remove_ani);
        if(!(("show_before" in d)&&(d.show_before)))
          tmp += that.update_ani;
        return tmp;
      })
      .duration(function (d) {
        if(!(("show_before" in d)&&(d.show_before)))
          return that.create_ani;
        return that.update_ani;
      })
      .attr("opacity", that.parent.show_images ? 1 : 0)
      .style("visibility", that.parent.show_images ? "visible" : "hidden");

    that.e_grids2
      .select("image")
      .filter(d => that.image_records.has(d.sample_id))
      .filter(d => d.show_image)
      .attr("xlink:href", d => d.img);

    that.image_history = that.image_records;
  };

  that.click_render_images = function(boxes) {
    for(let d of that.grids) {
      // console.log("d", d);
      if(!d.o_show_image)continue;
      d.show_image = d.o_show_image;
      let image_box = {
        "x": d.x+d.image_bias[0]+(d.width-that.image_width*d.image_ratio[0])/2,
        "y": d.y+d.image_bias[1]+(d.width-that.image_width*d.image_ratio[1])/2,
        "width": that.image_width*d.image_ratio[0], 
        "height": that.image_width*d.image_ratio[1]
      };
      for(let box of boxes) {
        if(Math.max(box.x-image_box.x-image_box.width, image_box.x-box.x-box.width)<0)
        if(Math.max(box.y-image_box.y-image_box.height, image_box.y-box.y-box.height)<0){
          d.show_image = false;
          break;
        }
      }
      // console.log("d.show_image", d.show_image);
    }

    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);

    that.e_grids2
      .select(".image_g")
      .filter(d => d.o_show_image)
      .style("visibility", "visible")
      .transition()
      .duration(that.update_ani)
      .attr("opacity", d => (that.parent.show_images && d.show_image) ? 1 : 0)
      .on("end", function() {
        d3.select(this).style("visibility", d => (that.parent.show_images && d.show_image) ? "visible" : "hidden")
      });

    that.e_grids2
      .select(".grid-bar")
      .filter(d => d.o_show_image)
      .style("visibility", "visible")
      .transition()
      .duration(that.update_ani)
      .attr("opacity", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0)
      .on("end", function() {
        d3.select(this).style("visibility", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden");
      });

    that.e_grids2
      .select(".image-bar")
      .filter(d => d.o_show_image)
      .style("visibility", "visible")
      .transition()
      .duration(that.update_ani)
      .attr("opacity", d => (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0)
      .on("end", function() {
        d3.select(this).style("visibility", d => (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden");
      });
  };

  that.init_recall = function() {
    that.grid_group
      .on("mousedown", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mousedown(ev);
      })
      .on("mousemove", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mousemove(ev);
      })
      .on("mouseup", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mouseup(ev);
      });
    that.grid_group2
      .on("mousedown", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mousedown(ev);
      })
      .on("mousemove", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mousemove(ev);
      })
      .on("mouseup", ev => {
        if (!that.parent.in_overview) return;
        that.parent.overview_recall_mouseup(ev);
      });
  };

  that.cropImage = function(imageSrc, cropX, cropY, cropWidth, cropHeight) {
    // console.log("crop", imageSrc, cropX, cropY, cropWidth, cropHeight);
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            canvas.width = cropWidth;
            canvas.height = cropHeight;
            ctx.drawImage(img, cropX, cropY, cropWidth, cropHeight, 0, 0, cropWidth, cropHeight);
            const croppedImageUrl = canvas.toDataURL("image/png");
            resolve(croppedImageUrl);
        };
        img.onerror = (err) => reject(err);
        img.src = imageSrc;
    });
  };

  that.checkCrossInfluence = async function(influenceDict, representDict) {
    console.log("influenceDict", influenceDict, representDict);
    
    that.parent.addGridLoadingFlag();
    
    let source = that.meta.index_dict[that.current_click];

    let id_list = [];
    for(let id in influenceDict) {
      if((parseInt(id)===Number(id))&&(id!=that.current_click)) id_list.push(id);
    }

    // class Random {
    //   constructor(seed) {
    //     this.seed = seed || Date.now();
    //   }
    //   next() {
    //     this.seed = (this.seed * 9301 + 49297) % 233280;
    //     return this.seed / 233280.0;
    //   }
    // }
    // function shuffleArray(array, random) {
    //   for (let i = array.length - 1; i > 0; i--) {
    //     const j = Math.floor(random.next() * (i + 1));
    //     [array[i], array[j]] = [array[j], array[i]];
    //   }
    // }
    // const random = new Random(seed);
    // shuffleArray(id_list, random);

    for(let i=0;i<id_list.length;i++)
      for(let j=i+1;j<id_list.length;j++)
        if(influenceDict[id_list[i]]<influenceDict[id_list[j]]) {
          let tmp = id_list[i];
          id_list[i] = id_list[j];
          id_list[j] = tmp;
        }
    // let thres = Math.max(1, influenceDict[id_list[Math.floor(id_list.length/30)]]);
    let thres = Math.max(1, influenceDict[id_list[Math.min(20, id_list.length-1)]]);

    let tmp_pairs = [];
    for(let id of id_list) {
      if(influenceDict[id]<thres) continue;
      if(tmp_pairs.length>=25) break;
      let item = that.meta.index_dict[id];
      
      let tmp_pair = {"source": source, "target": item, "flow": influenceDict[id], "imageSrc": that.parent.items[id]['image'], "represent": that.parent.items[id]['boxes'][representDict[id]]};

      // let idx = 0;
      // let confidence = { min: 0.2+0.02, q1: 0.3+0.02, median: 0.45+0.02*idx, q3: 0.65+0.02*idx, max: 0.75+0.02*idx, outliers: [0.15+0.02*idx, 0.8+0.02*idx] }
      // tmp_pair["confidence"] = confidence;
      // // let bin = [0.2, 0.4, 0.1, 0.1, 0];
      // let bin = [0, 0, 0, 0, 0];
      // let scores = [];
      // let boxes = that.parent.items[item.sample_id].boxes;
      // for(let box of boxes) {
      //   scores.push(box.score);
      //   for(let i=0;i<5;i++) {
      //     if(box.score<(i+1)*0.2) {
      //       bin[i] += 1/boxes.length;
      //       break;
      //     }
      //   }
      // }
      // tmp_pair["bin"] = bin;
      // tmp_pair["scores"] = scores;

      tmp_pairs.push(tmp_pair);
    }

    async function batchCropImages(cropParamsList) {
      const cropPromises = cropParamsList.map((params, index) =>
          that.cropImage(params.imageSrc, params.represent.x, params.represent.y, params.represent.width, params.represent.height)
              .then(croppedImage => ({ index, croppedImage }))
      );
      const results = await Promise.all(cropPromises);
      return results.sort((a, b) => a.index - b.index).map(item => item.croppedImage);
    }

    let result = await batchCropImages(tmp_pairs);
    // console.log("crop result", result);
    for(let i=0;i<result.length;i++)tmp_pairs[i]['image'] = result[i];

    that.parent.map_info = {
      "source": source,
      "pairs": tmp_pairs,
    }
    if(source == null) that.parent.map_info = null;

    that.parent.render_influence_map();

    that.parent.decGridLoadingFlag();
  };

  that.grid_click = function(d) {
    let new_click = true;
    if(that.current_click == d.sample_id)
      new_click = false;

    console.log('click grid', d.label_name, d.bottom_label_name)
    console.log('cluster acc', d.acc);
    console.log("other info", that.detection_items[d.sample_id].other_info)
    that.current_click = d.sample_id;
    let highlight = that.svg.select("g.highlight")
    let highlight_rect = highlight.select("rect.highlight_rect");
    let highlight_icon = highlight.select("path.highlight_icon");
    let tmp_width = d.width;
    let tmp_height = d.height;
    let tmp_x = d.x;
    let tmp_y = d.y;
    let find_flag = true;
    highlight
      .style("visibility", find_flag ? "visible" : "hidden")
      .attr("transform", d => `translate(${tmp_x}, ${tmp_y})`)
      .attr("opacity", find_flag ? 1 : 0);
    highlight_rect
      .attr("width", tmp_width)
      .attr("height", tmp_height)
      .attr("fill", "none")
      .attr("stroke", "white")
      // .attr("stroke-width", 2*that.layout.stroke_width);
      .attr("stroke-width", 5)
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("filter", "url(#dropShadow)");
    highlight_icon
      .attr("transform", `scale(${tmp_width/1024*2/3}) translate(${1024*(1/(2/3)-1)/2}, ${1024*(1/(2/3)-1)/2})`)
      .attr("fill", "black")
      .attr("stroke", "white")
      // .attr("stroke-width", 2*that.layout.stroke_width/tmp_width*1024);
      .attr("stroke-width", 75);
    highlight.raise();
    
    // let tmp_pairs = [];
    // function getRandomItems(arr, num) {
    //   const shuffled = arr.slice();
    //   for (let i = shuffled.length - 1; i > 0; i--) {
    //     const j = Math.floor(Math.random() * (i + 1));
    //     [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    //   }
    //   return shuffled.slice(0, num);
    // }
    // let filter_list = [];
    // for(let item of that.grids) {
    //   if((Math.abs(d.x-item.x)<=d.width*4)&&(Math.abs(d.y-item.y)<=d.height*4)) {
    //     if(d.sample_id == item.sample_id) continue;
    //     filter_list.push(item);
    //   }
    // }
    // // let tmp_list = getRandomItems(that.grids, 10);
    // let tmp_list = getRandomItems(filter_list, 10);
    // // for(let item of that.grids.slice(0, 10)) {
    // for(let idx=0;idx<10;idx++) {
    //   let item = tmp_list[idx];
    //   let confidence = { min: 0.2+0.02*idx, q1: 0.3+0.02*idx, median: 0.45+0.02*idx, q3: 0.65+0.02*idx, max: 0.75+0.02*idx, outliers: [0.15+0.02*idx, 0.8+0.02*idx] }
    //   let bin = [0, 0, 0, 0, 0];
    //   let scores = [];
    //   let boxes = that.parent.items[item.sample_id].boxes;
    //   for(let box of boxes) {
    //     scores.push(box.score);
    //     for(let i=0;i<5;i++) {
    //       if(box.score<(i+1)*0.2) {
    //         bin[i] += 1/boxes.length;
    //         break;
    //       }
    //     }
    //   }
    //   // let bin = [0.2, 0.4, 0.1, 0.1, 0];
    //   tmp_pairs.push({"source": d, "target": item, "confidence": confidence, "bin": bin, "scores": scores});
    // }

    // that.parent.map_info = {
    //   "source": d,
    //   "pairs": tmp_pairs,
    // }
    
    if(new_click)that.parent.map_info = null;

    that.parent.click_grid(d.sample_id);
    
    if(that.render_image) {
      if (d.img === '') {
        that.parent.fetchImages({names: [d.name], ids: [d.index]});
      }
      else {
        let meta_image = document.querySelector('#meta-image');
        let image_container = document.querySelector('#meta-image-container');
        if(meta_image != null) {
          meta_image.src = d.img;
          let containerRatio = image_container.clientWidth / image_container.clientHeight;
          let imageRatio = meta_image.naturalWidth / meta_image.naturalHeight;
          if (containerRatio < imageRatio) {
              meta_image.style.width = '100%';
              meta_image.style.height = 'auto';
          } else {
              meta_image.style.width = 'auto';
              meta_image.style.height = '100%';
          }
        }
      }
    }
  };

  that.create = function() {
    that.cur_pclass = null;
    // grid partition boundary
    that.e_paths
      .enter()
      .append("path")
      .attr("class", "partition_boundary")
      .attr("d", d => d.path)
      // .attr('stroke', d => `rgb(${d.pcolor[0]},${d.pcolor[1]},${d.pcolor[2]})`)
      .attr("stroke", that.pboundary_stroke)
      // .attr("stroke-width", that.pboundary_stroke_width)
      .attr("stroke-width", that.layout.partition_width*2)
      .attr("opacity", 0)
      .attr("fill", "none");

    that.e_cpaths
      .enter()
      .append("path")
      .attr("class", "class_boundary")
      .attr("d", d => d.path)
      .attr("stroke", that.pboundary_stroke)
      .attr("stroke-width", that.layout.extra_width*2)
      .attr("opacity", 0)
      .attr("fill", "none")
      .transition()
      .delay(that.init ? 0 : that.remove_ani + that.update_ani)
      .duration(that.create_ani)
      .attr("opacity", 1);

    // grid group boundary
    let boundary_group = that.grid_group
      .selectAll(".grid_boundary")
      .data([that.meta]);
    boundary_group
      .enter()
      .append("g")
      .attr("class", "grid_boundary")
      .on("mouseenter", () => {
        // console.log("grid boundary enter");
        if (that.in_update || that.one_partition || that.parent.show_details)
          return;
        if (that.cur_pclass !== null) {
          if (that.mode.indexOf("boundary") !== -1) {
            that.e_paths = that.boundary_group
              .selectAll(".partition_boundary")
              .data(that.meta.paths, d => d.name);
            that.e_paths
              .filter(e => e.pclass === that.cur_pclass)
              .transition()
              .duration(that.fast_ani)
              .attr("opacity", 0);
          }

          that.e_grids = that.grid_group
            .selectAll(".grid-cell")
            .data(that.grids, d => d.sample_id);
          that.e_grids2 = that.grid_group2
            .selectAll(".grid-cell2")
            .data(that.grids, d => d.sample_id);
          // console.log(that.cur_pclass, that.e_grids.filter(e => e.pclass === that.cur_pclass));
          that.e_grids
            // .filter(e => e.pclass === that.cur_pclass)
            .transition()
            .duration(that.fast_ani)
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
          that.e_grids2
            // .filter(e => e.pclass === that.cur_pclass)
            .transition()
            .duration(that.fast_ani)
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
          that.e_grids
            // .filter(e => e.pclass === that.cur_pclass)
            .select("rect.main")
            .transition()
            .duration(that.fast_ani)
            .attr("fill-opacity", 1)
            .attrTween("fill", that.colorinter)
            .attr(
              "fill",
              e => `rgba(${e.pcolor[0]},${e.pcolor[1]},${e.pcolor[2]},${e.pcolor[3]})`
            )
            .attr("width", d => d.width)
            .attr("height", d => d.height);

          that.e_grids2
            .selectAll("rect.confuse-1")
            .transition()
            .duration(that.fast_ani)
            .attrTween("fill", that.colorinter)
            .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
//            .attr("stroke", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`);
//            .attr("stroke", "white");

          that.e_grids2
            .selectAll("rect.confuse0")
            .transition()
            .duration(that.fast_ani)
            .attrTween("fill", that.colorinter)
//            .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
            .attr("fill", 'none')
            .attr("stroke", e => `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})`);

          that.e_grids2
            .selectAll("rect.confuse1")
            .transition()
            .duration(that.fast_ani)
            .attrTween("fill", that.colorinter)
            .attr("fill", e => `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})`);

          that.cur_pclass = null;
        }
      })
      .append("rect")
      .attr("x", d => d.minx - that.boundary_border)
      .attr("y", d => d.miny - that.boundary_border)
      .attr("width", d => d.maxx - d.minx + 2 * that.boundary_border)
      .attr("height", d => d.maxy - d.miny + 2 * that.boundary_border)
      .attr("fill", "transparent")
      .attr("stroke", "gray")
      .attr("stroke-width", that.boundary_border * 2 - 0.5)
      .attr("opacity", 0);
    // .transition()
    // .duration(that.create_ani)
    // .attr('opacity', 1);

    function extractString(str) {
      const regex = /\+(.*?)\./;
      const match = str.match(regex);
      let s = (match ? match[1] : str).replace(/_/g, ' ');
      let i, ss = s.toLowerCase().split(/\s+/);
      for (i = 0; i < ss.length; i++) {
        ss[i] = ss[i].slice(0, 1).toUpperCase() + ss[i].slice(1);
      }
      return ss.join(' ');
    }

    function grid_mouseover(ev, d){
      // let ss = `${extractString(d.label_name)}`;
      // if(d.label!=d.bottom_label) {
      //   ss = ss + ` (${extractString(d.bottom_label_name)})`
      // }
      // d3.select("#meta1t").text(`${extractString(d.label_name)}`)
      //   .attr("title", ss);
      // let gt_ss = `${extractString(d.gt_label_name)}`;
      // if(d.gt_label!=d.bottom_gt_label) {
      //   gt_ss = gt_ss + ` (${extractString(d.bottom_gt_label_name)})`
      // }
      // d3.select("#meta2t").text(`${extractString(d.gt_label_name)}`)
      //   .attr("title", gt_ss);

      that.current_hover = d.name;

      // if(that.render_image) {
      //   if (d.img === '') {
      //     that.parent.fetchImages({names: [d.name], ids: [d.index]});
      //   }
      //   else {
      //     let meta_image = document.querySelector('#meta-image');
      //     let image_container = document.querySelector('#meta-image-container');
      //     meta_image.src = d.img;
      //     let containerRatio = image_container.clientWidth / image_container.clientHeight;
      //     let imageRatio = meta_image.naturalWidth / meta_image.naturalHeight;
      //     if (containerRatio < imageRatio) {
      //         meta_image.style.width = '100%';
      //         meta_image.style.height = 'auto';
      //     } else {
      //         meta_image.style.width = 'auto';
      //         meta_image.style.height = '100%';
      //     }
      //   }
      // }

      // let meta_bar = d3.select("#meta-bar");

      // let svgElement = document.getElementById('meta-bar');
      // let svgWidth = svgElement.clientWidth;
      // let svgHeight = svgElement.clientHeight;
      // svgElement.setAttribute('viewBox', `0 0 ${svgWidth} ${svgHeight}`);

      // meta_bar = meta_bar.select("g");

      // meta_bar.select(".bar-boundary")
      //   .attr("width", svgWidth)
      //   .attr("height", svgHeight);


      if (that.in_update || that.one_partition || that.parent.show_details)
        return;
      if (d.pclass !== that.cur_pclass) {
        // console.log('over', d);
        if (that.mode.indexOf("boundary") !== -1) {
          that.e_paths = that.boundary_group
            .selectAll(".partition_boundary")
            .data(that.meta.paths, d => d.name);
          that.e_paths
            .filter(e => e.pclass === d.pclass)
            .raise()
            .transition()
            .duration(that.fast_ani)
            .attr("opacity", 1);
          that.e_paths
            .filter(e => e.pclass === that.cur_pclass)
            .transition()
            .duration(that.fast_ani)
            .attr("opacity", 0);
        }

        that.e_grids = that.grid_group
          .selectAll(".grid-cell")
          .data(that.grids, d => d.sample_id);
        that.e_grids2 = that.grid_group2
          .selectAll(".grid-cell2")
          .data(that.grids, d => d.sample_id);
        // if (that.cur_pclass !== null) {
        //     that.e_grids
        //         .filter(e => e.pclass === that.cur_pclass)
        //         .select('rect')
        //         .transition()
        //         .duration(that.fast_ani)
        //         .attrTween('fill', that.colorinter)
        //         .attr('fill', e => `rgb(${e.pcolor[0] * 255},${e.pcolor[1] * 255},${e.pcolor[2] * 255}), 0.5`);
        // }
        that.e_grids
          .transition()
          .duration(that.fast_ani)
          .attr(
            "transform",
            e => `translate(${e.px[d.pclass]}, ${e.py[d.pclass]})`
          );
        that.e_grids2
          .transition()
          .duration(that.fast_ani)
          .attr(
            "transform",
            e => `translate(${e.px[d.pclass]}, ${e.py[d.pclass]})`
          );

        that.e_grids
          .filter(e => e.pclass === d.pclass)
          .select("rect.main")
          .transition()
          .duration(that.fast_ani)
          .attr("fill-opacity", 1)
          .attrTween("fill", that.colorinter)
          .attr(
            "fill",
            e => `rgba(${e.color[0]},${e.color[1]},${e.color[2]},${e.color[3]})`
          )
          .attr("width", e => e.pwidth[d.pclass])
          .attr("height", e => e.pheight[d.pclass]);

        if (that.mode.indexOf("alpha") !== -1) {
          that.e_grids
            .filter(e => e.pclass !== d.pclass)
            .select("rect.main")
            .transition()
            .duration(that.fast_ani)
            .attr("fill-opacity", that.hide_opacity)
            .attrTween("fill", that.colorinter)
            .attr(
              "fill",
              e => `rgba(${e.pcolor[0]},${e.pcolor[1]},${e.pcolor[2]},${e.pcolor[3]})`
            )
            .attr("width", e => e.pwidth[d.pclass])
            .attr("height", e => e.pheight[d.pclass]);
        } else {
          that.e_grids
            .filter(e => e.pclass !== d.pclass)
            .select("rect.main")
            .transition()
            .duration(that.fast_ani)
            .attrTween("fill", that.colorinter)
            .attr(
              "fill",
              e => `rgba(${e.pcolor[0]},${e.pcolor[1]},${e.pcolor[2]},${e.pcolor[3]})`
            )
            .attr("width", e => e.pwidth[d.pclass])
            .attr("height", e => e.pheight[d.pclass]);
        }

        that.e_grids2
          .filter(e => e.pclass === d.pclass)
          .selectAll("rect.confuse-1")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
          .attr("fill", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//            .attr("stroke", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`);
//            .attr("stroke", "white");

        that.e_grids2
          .filter(e => e.pclass === d.pclass)
          .selectAll("rect.confuse0")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
//            .attr("fill", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
          .attr("fill", 'none')
          .attr("stroke", e => `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`);

        that.e_grids2
          .filter(e => e.pclass === d.pclass)
          .selectAll("rect.confuse1")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
          .attr("fill", e => `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);

        that.e_grids2
          .filter(e => e.pclass !== d.pclass)
          .selectAll("rect.confuse-1")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
          .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
//            .attr("stroke", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`);
//            .attr("stroke", "white");

        that.e_grids2
          .filter(e => e.pclass !== d.pclass)
          .selectAll("rect.confuse0")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
//            .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
          .attr("fill", 'none')
          .attr("stroke", e => `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})`);

        that.e_grids2
          .filter(e => e.pclass !== d.pclass)
          .selectAll("rect.confuse1")
          .transition()
          .duration(that.fast_ani)
          .attrTween("fill", that.colorinter)
          .attr("fill", e => `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})`);

        that.cur_pclass = d.pclass;
      }
    }

    // grid layouts
    let e_grid_groups = that.e_grids
      .enter()
      .append("g")
      .attr("class", "grid-cell")
      .attr("transform", d =>
        that.one_partition || that.is_zoomout
          ? `translate(${d.px[d.pclass]}, ${d.py[d.pclass]})`
          : `translate(${d.x}, ${d.y})`
      )
      .on("click", function(ev, d) {
        that.grid_click(d);
      })
      .on("mouseover", function(ev, d) {
        grid_mouseover(ev, d);
      })
//      .on("click", function(ev, d) {
//        // console.log("click", d);
//        if (that.in_update || that.one_partition || that.parent.show_details)
//          return;
//        that.in_update = true;
//        let sample_ids = that.grids
//          .filter(e => e.pclass === d.pclass)
//          .map(e => e.name);
//        console.log("zoom in", sample_ids);
//        let args = {
//          samples: sample_ids,
//          zoom_without_expand: false,
//        };
//        that.parent.fetchGridLayout(args);
//      })
      .style("cursor", "pointer")
      .attr("opacity", 0);

    let e_grid_groups2 = that.e_grids2
      .enter()
      .append("g")
      .attr("class", "grid-cell2")
      .attr("transform", d =>
        that.one_partition || that.is_zoomout
          ? `translate(${d.px[d.pclass]}, ${d.py[d.pclass]})`
          : `translate(${d.x}, ${d.y})`
      )
      .on("click", function(ev, d) {
        that.grid_click(d);
      })
      .on("mouseover", function(ev, d) {
        grid_mouseover(ev, d);
      })
      .style("cursor", "pointer")
      .attr("opacity", 0);

    e_grid_groups
      .transition()
      .delay(that.init ? 0 : that.remove_ani + that.update_ani)
      .duration(that.create_ani)
      .attr("opacity", 1)
      .on("end", () => {
        that.in_update = false;
      });
    e_grid_groups2
      .transition()
      .delay(that.init ? 0 : that.remove_ani + that.update_ani)
      .duration(that.create_ani)
      .attr("opacity", 1);

//    console.log("ani time", that.create_ani);

    if (!that.one_partition && !that.is_zoomout) {
      e_grid_groups
        .append("rect")
        .attr("class", "main")
        .attr("width", d => d.width)
        .attr("height", d => d.height)
        .attr("fill-opacity", 1)
        .attr("fill", d => `rgba(${d.pcolor[0]},${d.pcolor[1]},${d.pcolor[2]},${d.pcolor[3]})`)
        .attr("stroke", "white")
        // .attr("stroke", "rgb(80, 80, 80)")
        // .attr("stroke", "transparent")
        .attr("stroke-width", d => d.stroke_width);
    } else {
      e_grid_groups
        .append("rect")
        .attr("class", "main")
        .attr("fill-opacity", 1)
        .attr("fill", e => `rgba(${e.color[0]},${e.color[1]},${e.color[2]},${e.color[3]})`)
        .attr("width", e => e.pwidth[e.pclass])
        .attr("height", e => e.pheight[e.pclass])
        .attr("stroke", "white")
        // .attr("stroke", "rgb(80, 80, 80)")
        // .attr("stroke", "transparent")
        .attr("stroke-width", d => d.stroke_width);
    }

    e_grid_groups
      .append("rect")
      .attr("class", "category")
      .attr("fill-opacity", 1)
      .attr("fill", function(d) {
        // if(d.detection_category in color_dict)
        //   return color_dict[d.detection_category];
        // return "transparent";
        // // return "black";
        return that.getBoxColor(d);
      })
      .attr("stroke", function(d) {
        if((d.detection_category!=null)&&(d.detection_category!=""))
          // return "white";
          // return "rgb(80, 80, 80)";
          return "transparent";
        else
          return "transparent";
      })
      .attr("width", d => d.width)
      .attr("height", d => d.height)
      .attr("x", d => d.width*0)
      .attr("y", d => d.height*0);

    let e_grid_bar = e_grid_groups2
      .append("g")
      .attr("class", "confuse-bar grid-bar");

    e_grid_bar
      .style("visibility", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden")
      .attr("opacity", 0)
      .transition()
      .delay(that.init ? 0 : that.remove_ani + that.update_ani)
      .duration(that.create_ani)
      .attr("opacity", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0);

    e_grid_bar
      .append("rect")
      .attr("class", "confuse-1")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
//      .attr("width", d => d.width * 0.9)
//      .attr("height", d => d.width * 0.9)
//      .attr("x", d => d.width * 0.05)
//      .attr("y", d => d.width * 0.05)
//      .attr("rx", d => d.width * 0.05)
//      .attr("ry", d => d.width * 0.05)
      .attr("width", d => d.width)
      .attr("height", d => d.width)
      .attr("x", 0)
      .attr("y", 0)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//      .attr("stroke", "white")
//      .attr("stroke-width", d => d.width * 0.08);

    e_grid_bar
      .append("rect")
      .attr("class", "confuse1")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => d.width * 0.9)
      .attr("height", d => (d.confuse_values[0]) * (d.width * 0.9))
      .attr("x", d => d.width * 0.05)
      .attr("y", d => d.width * 0.05 + d.width*0.9*(1-d.confuse_values[0]))
      .attr("rx", d => d.width * 0.05)
      .attr("ry", d => d.width * 0.05)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})` : `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);

    e_grid_bar
      .append("rect")
      .attr("class", "confuse0")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => d.width * 0.9)
      .attr("height", d => d.width * 0.9)
      .attr("x", d => d.width * 0.05)
      .attr("y", d => d.width * 0.05)
      .attr("rx", d => d.width * 0.05)
      .attr("ry", d => d.width * 0.05)
      .attr("fill-opacity", 1)
      .attr("fill", 'none')
      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})` : `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`)
      .attr("stroke-width", d => d.width * 0.03);

    if (that.render_image) {
      let image_g = e_grid_groups2
        .append("g")
        .attr("class", "image_g")
        .attr("opacity", 0)
        .style("visibility", "hidden");

      image_g
        .append("rect")
        .attr("class", "image_rect")
        .attr("fill", "none")
        .attr("x", d => d.image_bias[0] + (d.width-that.image_width*d.image_ratio[0])/2)
        .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2)
        .attr("width", d => that.image_width*d.image_ratio[0])
        .attr("height", d => that.image_width*d.image_ratio[1])
        .attr("stroke", that.image_has_stroke ? "black" : null)
        .attr("stroke-width", that.image_has_stroke ? 0.025*that.image_width : null);

      image_g
        .append("image")
        .attr("x", d => d.image_bias[0] + (d.width-that.image_width*d.image_ratio[0])/2)
        .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2)
        .attr("width", d => that.image_width*d.image_ratio[0])
        .attr("height", d => that.image_width*d.image_ratio[1])
        .attr("preserveAspectRatio", "none");

      image_g
        .append("path")
        .attr("class", "pin")
        .attr("d", "M512 64.383234c-189.077206 0-342.355289 153.643944-342.355289 343.172854S512 959.616766 512 959.616766s342.355289-362.531768 342.355289-552.060679S701.077206 64.383234 512 64.383234zM512 497.079441c-65.76594 0-119.080367-53.44115-119.080367-119.364471S446.23406 258.350499 512 258.350499s119.080367 53.44115 119.080367 119.364471S577.76594 497.079441 512 497.079441z")
        .attr("fill", "#2c2c2c")
        .attr("stroke", "white")
        .attr("stroke-width", 100)
        .attr("transform", d => `scale(${d.width/1024*2/3}) translate(${1024*(1/(2/3)-1)/2}, ${1024*(1/(2/3)-1)/2})`)
        .attr("opacity", d => d.use_image_bias ? 1 : 0);
    }

    let e_image_bar = e_grid_groups2
      .append("g")
      .attr("class", "confuse-bar image-bar");

    e_image_bar
      .style("visibility", d => (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden")
      .attr("opacity", 0)
      .transition()
      .delay(that.init ? 0 : that.remove_ani + that.update_ani)
      .duration(that.create_ani)
      .attr("opacity", d => (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0);

    e_image_bar
      .append("rect")
      .attr("class", "confuse-1")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => that.image_width*0.6)
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.05*that.image_width)
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
      .attr("stroke", "white")
      .attr("stroke-width", d => that.image_width*0.08);

    e_image_bar
      .append("rect")
      .attr("class", "confuse1")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
//      .attr("width", d => that.image_width*0.17)
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => (d.confuse_values[0]) * (that.image_width*0.57))
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.035*that.image_width + that.image_width*0.57*(1-d.confuse_values[0]))
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})` : `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);

    e_image_bar
      .append("rect")
      .attr("class", "confuse0")
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => that.image_width*0.6)
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.05*that.image_width)
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
      .attr("fill-opacity", 1)
//      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
      .attr("fill", 'none')
      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})` : `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`)
      .attr("stroke-width", d => that.image_width*0.03);
  };

  that.update = function() {
    if (!that.one_partition && !that.is_zoomout) {
      that.e_grids
        .transition()
        .ease(d3.easeSin)
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr("transform", d => `translate(${d.x}, ${d.y})`);
      that.e_grids2
        .transition()
        .ease(d3.easeSin)
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr("transform", d => `translate(${d.x}, ${d.y})`);
      that.e_grids
        .select("rect.main")
        .transition()
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr("width", d => d.width)
        .attr("height", d => d.height)
        .attrTween("fill", that.colorinter)
        .attr("fill", d => `rgba(${d.pcolor[0]},${d.pcolor[1]},${d.pcolor[2]},${d.pcolor[3]})`)
        .on("end", () => {
          that.in_update = false;
        });
    } else {
      that.e_grids
        .transition()
        .ease(d3.easeSin)
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr(
          "transform",
          d => `translate(${d.px[d.pclass]}, ${d.py[d.pclass]})`
        );
      that.e_grids2
        .transition()
        .ease(d3.easeSin)
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr(
          "transform",
          d => `translate(${d.px[d.pclass]}, ${d.py[d.pclass]})`
        );
      that.e_grids
        .select("rect.main")
        .transition()
        .ease(d3.easeSin)
        .duration(that.update_ani)
        .delay(that.init ? 0 : that.remove_ani)
        .attr("width", e => e.pwidth[e.pclass])
        .attr("height", e => e.pheight[e.pclass])
        .attrTween("fill", that.colorinter)
        .attr("fill", d => `rgba(${d.color[0]},${d.color[1]},${d.color[2]},${d.color[3]})`)
        .on("end", () => {
          that.in_update = false;
          if (that.is_zoomout) that.is_zoomout = false;
        });
    }

    let highlight = that.svg.select("g.highlight");
    let highlight_rect = highlight.select("rect.highlight_rect");
    let highlight_icon = highlight.select("path.highlight_icon");

    let tmp_width = highlight_rect.attr("width");
    let tmp_height = highlight_rect.attr("height");
    let tmp_transfrom = highlight_rect.attr("transfrom");
    let tmp_x = 0;
    let tmp_y = 0;
    let find_flag = false;
    // console.log("current click", that.current_click);
    that.e_grids.each(function(d) {
      if(d.sample_id == that.current_click) {
        tmp_width = d.width;
        tmp_height = d.height;
        tmp_x = d.x;
        tmp_y = d.y;
        find_flag = true;
      }
    })
    if(find_flag) tmp_transfrom = `translate(${tmp_x}, ${tmp_y})`;
    // console.log("find", find_flag);
    highlight
      .style("visibility", "visible")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("transform", tmp_transfrom)
      .attr("opacity", find_flag ? 1 : 0)
      .on("end", function() {
        d3.select(this)
          .style("visibility", find_flag ? "visible" : "hidden");
      });
    highlight_rect
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("width", tmp_width)
      .attr("height", tmp_height)
      .attr("fill", "none")
      .attr("stroke", "white")
      // .attr("stroke-width", 2*that.layout.stroke_width);
      .attr("stroke-width", 5)
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("filter", "url(#dropShadow)");
    highlight_icon
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("transform", `scale(${tmp_width/1024*2/3}) translate(${1024*(1/(2/3)-1)/2}, ${1024*(1/(2/3)-1)/2})`)
      .attr("fill", "black")
      .attr("stroke", "white")
      // .attr("stroke-width", 2*that.layout.stroke_width/tmp_width*1024);
      .attr("stroke-width", 75);

    that.e_grids
      .select("rect.category")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("fill", function(d) {
        // if(d.detection_category in color_dict)
        //   return color_dict[d.detection_category];
        // return "transparent";
        // // return "black";
        return that.getBoxColor(d);
      })
      .attr("stroke", function(d) {
        if((d.detection_category!=null)&&(d.detection_category!=""))
          // return "white";
          // return "rgb(80, 80, 80)";
          return "transparent";
        else
          return "transparent";
      })
      .attr("width", d => d.width)
      .attr("height", d => d.height)
      .attr("x", d => d.width*0)
      .attr("y", d => d.height*0);

    let e_grid_bar = that.e_grids2
      .select(".grid-bar");

    if(!that.init) {
      e_grid_bar
        .transition()
        .duration(that.remove_ani)
        .attr("opacity", 0)
        .on("end", function(d) {
          d3.select(this)
            .style("visibility", (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden")
            .transition()
            .duration(that.create_ani)
            .delay(that.update_ani)
            .attr("opacity", (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0)
            .attr("attr", (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)));
        });
    }else {
      e_grid_bar
        .style("visibility", "visible")
        .transition()
        .duration(that.create_ani)
        .delay(that.init ? 0 : that.remove_ani+that.update_ani)
        .attr("opacity", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0)
        .on("end", function(d) {
          d3.select(this)
            .style("visibility", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden");
        });
    }

    e_grid_bar
      .select("rect.confuse-1")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
//      .attr("width", d => d.width * 0.9)
//      .attr("height", d => d.width * 0.9)
//      .attr("x", d => d.width * 0.05)
//      .attr("y", d => d.width * 0.05)
//      .attr("rx", d => d.width * 0.05)
//      .attr("ry", d => d.width * 0.05)
      .attr("width", d => d.width)
      .attr("height", d => d.width)
      .attr("x", 0)
      .attr("y", 0)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate}),${e.pcolor[3]}` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate,${e.color[3]}})`)
//      .attr("stroke", "white")
//      .attr("stroke-width", d => d.width * 0.08);

    e_grid_bar
      .select("rect.confuse0")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => d.width * 0.9)
      .attr("height", d => d.width * 0.9)
      .attr("x", d => d.width * 0.05)
      .attr("y", d => d.width * 0.05)
      .attr("rx", d => d.width * 0.05)
      .attr("ry", d => d.width * 0.05)
      .attr("fill", 'none')
      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})` : `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`)
      .attr("stroke-width", d => d.width * 0.03);

    e_grid_bar
      .select("rect.confuse1")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => d.width * 0.9)
      .attr("height", d => (d.confuse_values[0]) * (d.width * 0.9))
      .attr("x", d => d.width * 0.05)
      .attr("y", d => d.width * 0.05 + d.width*0.9*(1-d.confuse_values[0]))
      .attr("rx", d => d.width * 0.05)
      .attr("ry", d => d.width * 0.05)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})` : `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);

    let e_image_bar = that.e_grids2
      .select(".image-bar");

    if(!that.init) {
      e_image_bar
        .transition()
        .ease(d3.easeSin)
        .duration(that.remove_ani)
        .attr("opacity", 0)
        .on("end", function(d) {
          d3.select(this)
            .style("visibility", (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden")
            .transition()
            .duration(that.create_ani)
            .delay(that.update_ani)
            .attr("opacity", (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0);
        });
    }else {
      e_image_bar
        .style("visibility", "visible")
        .transition()
        .ease(d3.easeSin)
        .duration(that.create_ani)
        .delay(that.init ? 0 : that.remove_ani+that.update_ani)
        .attr("opacity", d => (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0)
        .on("end", function(d) {
          d3.select(this)
            .style("visibility", (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden");
        });
    }

    e_image_bar
      .select("rect.confuse-1")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => that.image_width*0.6)
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.05*that.image_width)
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
      .attr("stroke", "white")
      .attr("stroke-width", d => that.image_width*0.08);

    e_image_bar
      .select("rect.confuse0")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => that.image_width*0.6)
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.05*that.image_width)
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
//      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})` : `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
      .attr("fill", 'none')
      .attr("stroke", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})` : `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`)
      .attr("stroke-width", d => that.image_width*0.03);

    e_image_bar
      .select("rect.confuse1")
      .transition()
      .ease(d3.easeSin)
      .duration(that.update_ani)
      .delay(that.init ? 0 : that.remove_ani)
      .attr("opacity", d => (d.is_confused ? 1 : 0))
//      .attr("width", d => that.image_width*0.17)
      .attr("width", d => that.image_width*0.2)
      .attr("height", d => (d.confuse_values[0]) * (that.image_width*0.57))
      .attr("x", d => d.image_bias[0] + (d.image_bias[0]<=0 ? min(0, (d.width-that.image_width*d.image_ratio[0])/2)-0.07*that.image_width : d.width - min(0, (d.width-that.image_width*d.image_ratio[0])/2)-that.image_width*0.2+0.07*that.image_width))
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2-0.035*that.image_width + that.image_width*0.57*(1-d.confuse_values[0]))
      .attr("rx", d => that.image_width*0.05)
      .attr("ry", d => that.image_width*0.05)
      .attr("fill-opacity", 1)
      .attr("fill", e => (!that.one_partition && !that.is_zoomout) ? `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})` : `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);
    
    that.e_grids2
      .select(".image_g")
      .each(function(d) {
        if(d3.select(this).style("visibility") == "visible")
          d.show_before = true;
        else {
          d.show_before = false;
        }
      })

    that.e_grids2
      .select(".image_g")
      .attr("opacity", 0)
      .style("visibility", "hidden");
      
    that.e_grids2
      .select("image")
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.update_ani)
      .attr("x", d => d.image_bias[0] + (d.width-that.image_width*d.image_ratio[0])/2)
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2)
      .attr("width", d => that.image_width*d.image_ratio[0])
      .attr("height", d => that.image_width*d.image_ratio[1]);

    that.e_grids2
      .select("rect.image_rect")
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.update_ani)
      .attr("x", d => d.image_bias[0] + (d.width-that.image_width*d.image_ratio[0])/2)
      .attr("y", d => d.image_bias[1] + (d.width-that.image_width*d.image_ratio[1])/2)
      .attr("width", d => that.image_width*d.image_ratio[0])
      .attr("height", d => that.image_width*d.image_ratio[1])
      .attr("stroke", that.image_has_stroke ? "black" : null)
      .attr("stroke-width", that.image_has_stroke ? 0.025*that.image_width : null);;

    that.e_grids2
      .select("path.pin")
      .transition()
      .ease(d3.easeSin)
      .delay(that.init ? 0 : that.remove_ani)
      .duration(that.update_ani)
      .attr("transform", d => `scale(${d.width/1024*2/3}) translate(${1024*(1/(2/3)-1)/2}, ${1024*(1/(2/3)-1)/2})`)
      .attr("opacity", d => d.use_image_bias ? 1 : 0);

    if (!(that.render_image)) {
      that.e_grids2
        .select(".image_g")
        .attr("opacity", 0)
        .style("visibility", "hidden");
    }

    let selection = that.grid_group2
      .selectAll(".grid-cell")
      .filter(d => d.show_image);

    selection = selection.sort(function(a, b) {
      return a.order - b.order;
    });

    selection
      .each(function(d) {
//        console.log(d.order, d.x, d.y);
        d3.select(this).raise();
      });
    
    highlight.raise();
  };

  that.remove = function() {
    that.e_paths
      .exit()
      .transition()
      .duration(that.remove_ani)
      .attr("opacity", 0)
      .remove();

    that.e_cpaths
      .exit()
      .transition()
      .duration(that.remove_ani)
      .attr("opacity", 0)
      .remove();

    that.e_grids
      .exit()
      .transition()
      .duration(that.remove_ani)
      .attr("opacity", 0)
      .remove();
    that.e_grids2
      .exit()
      .transition()
      .duration(that.remove_ani)
      .attr("opacity", 0)
      .remove();
  };

  that.show_images = function() {
//    console.log("show", that.parent.show_images);

    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);

    that.e_grids2
      .select(".image_g")
      .filter(d => d.show_image)
      .style("visibility", "visible")
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", 1);

    that.e_grids2
      .select(".grid-bar")
      .filter(d => d.show_image)
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0)
      .on("end", function() {
        d3.select(this).style("visibility", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden");
      });

    that.e_grids2
      .select(".image-bar")
      .filter(d => d.show_image)
      .style("visibility", d => (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden")
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", d => (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0);
  }

  that.hide_images = function() {
//    console.log("hide", that.parent.show_images);

    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);

    that.e_grids2
      .select(".image_g")
      .filter(d => d.show_image)
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", 0)
      .on("end", function() {
        d3.select(this).style("visibility", "hidden");
      });

    that.e_grids2
      .select(".grid-bar")
      .filter(d => d.show_image)
      .style("visibility", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? "visible" : "hidden")
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", d => (d.is_confused && (!that.parent.show_images || !d.show_image || d.use_image_bias)) ? 1 : 0);

    that.e_grids2
      .select(".image-bar")
      .filter(d => d.show_image)
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", d => (d.is_confused && d.show_image && that.parent.show_images) ? 1 : 0)
      .on("end", function() {
        d3.select(this).style("visibility", d => (d.is_confused && d.show_image && that.parent.show_images) ? "visible" : "hidden");
      });
  }

  that.show_details = function() {
    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);

    that.e_grids
      .select("rect.main")
      .transition()
      .duration(that.update_ani)
      .attr("fill-opacity", 1)
      .attr("fill", e => `rgba(${e.color[0]},${e.color[1]},${e.color[2]},${e.color[3]})`)
      .attr("stroke", "white")
      // .attr("stroke", "rgb(80, 80, 80)")
      // .attr("stroke", "transparent")
      .attr("stroke-width", d => d.stroke_width);

    that.e_grids2
      .selectAll("rect.confuse-1")
      .transition()
      .duration(that.update_ani)
      .attr("fill", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
//      .attr("stroke", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`);
//      .attr("stroke", "white");

    that.e_grids2
      .selectAll("rect.confuse0")
      .transition()
      .duration(that.update_ani)
//      .attr("fill", e => `rgba(${light_bias+e.color[0]*light_rate},${light_bias+e.color[1]*light_rate},${light_bias+e.color[2]*light_rate},${e.color[3]})`)
      .attr("fill", 'none')
      .attr("stroke", e => `rgba(${dark_bias+e.color[0]*dark_rate},${dark_bias+e.color[1]*dark_rate},${dark_bias+e.color[2]*dark_rate},${e.color[3]})`);

    that.e_grids2
      .selectAll("rect.confuse1")
      .transition()
      .duration(that.update_ani)
      .attr("fill", e => `rgba(${e.color[0]*bar_rate},${e.color[1]*bar_rate},${e.color[2]*bar_rate},${e.color[3]})`);

  //  that.e_grids
  //    .transition()
  //    .duration(that.update_ani)
  //    .attr(
  //      "transform",
  //      d => `translate(${d.px[d.pclass]}, ${d.py[d.pclass]})`
  //    );

    that.e_paths = that.boundary_group
      .selectAll(".partition_boundary")
      .data(that.meta.paths, d => d.name);
    that.e_paths
      .raise()
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", 1);
  };

  that.hide_details = function() {
    that.e_grids = that.grid_group
      .selectAll(".grid-cell")
      .data(that.grids, d => d.sample_id);
    that.e_grids2 = that.grid_group2
      .selectAll(".grid-cell2")
      .data(that.grids, d => d.sample_id);

    that.e_grids
      .select("rect.main")
      .transition()
      .duration(that.update_ani)
      .attr("width", d => d.width)
      .attr("height", d => d.height)
      .attr("fill-opacity", 1)
      .attr("fill", d => `rgba(${d.pcolor[0]},${d.pcolor[1]},${d.pcolor[2]},${d.pcolor[3]})`)
      .attr("stroke", "white")
      // .attr("stroke", "rgb(80, 80, 80)")
      // .attr("stroke", "transparent")
      .attr("stroke-width", d => d.stroke_width);

    that.e_grids2
      .selectAll("rect.confuse-1")
      .transition()
      .duration(that.update_ani)
      .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
//      .attr("stroke", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`);
//      .attr("stroke", "white");

    that.e_grids2
      .selectAll("rect.confuse0")
      .transition()
      .duration(that.update_ani)
//      .attr("fill", e => `rgba(${light_bias+e.pcolor[0]*light_rate},${light_bias+e.pcolor[1]*light_rate},${light_bias+e.pcolor[2]*light_rate},${e.pcolor[3]})`)
      .attr("fill", 'none')
      .attr("stroke", e => `rgba(${dark_bias+e.pcolor[0]*dark_rate},${dark_bias+e.pcolor[1]*dark_rate},${dark_bias+e.pcolor[2]*dark_rate},${e.pcolor[3]})`);

    that.e_grids2
      .selectAll("rect.confuse1")
      .transition()
      .duration(that.update_ani)
      .attr("fill", e => `rgba(${e.pcolor[0]*bar_rate},${e.pcolor[1]*bar_rate},${e.pcolor[2]*bar_rate},${e.pcolor[3]})`);

    // that.e_grids
    //   .transition()
    //   .duration(that.update_ani)
    //   .attr("transform", d => `translate(${d.x}, ${d.y})`);
        
    that.e_paths = that.boundary_group
      .selectAll(".partition_boundary")
      .data(that.meta.paths, d => d.name);
    that.e_paths
      .raise()
      .transition()
      .duration(that.fast_ani)
      .attr("opacity", 0);
  };
};

export default GridRender;
