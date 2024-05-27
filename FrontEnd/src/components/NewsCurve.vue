<template>
  <div class="curve-container" ref="curveContainer">
    <svg class="curve-svg">
    </svg>
    <div id="tooltip" style="position: absolute;display: none;"></div> <!-- 添加这个元素 -->
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'NewsCurve',
  props: {
    msg: String
  },
  data() {
    return {
      emo_flat_list: [],
      divW: 0,
      divH: 0,

      curve_width_r: 0.8,
      curve_height_r: 0.95,
      tree_inter: 5,
    }
  },
  watch: {
    displayMode: function () {
      console.log('displayMode')

    },
    claimMarkFList: function () {
      // console.log('claimMarkFList', this.claimMarkFList)
      let vuethis = this
      d3.select("body").select(".curve-svg").selectAll(".cNode").classed("highLighted", function (d) {

        var f_0 = 0
        for (var i = 0; i < vuethis.claimMarkFList.length; i++) {
          if (vuethis.claimMarkFList[i] != 0) {
            f_0 = 1
            break;
          }
        }
        if (f_0 == 0) {
          return false;
        }
        if (vuethis.HLEList.length == 0) { //click claim
          if (d.id.indexOf("C") != -1) {
            var c_index = parseInt(d.id.slice(1)) - 1
            if (vuethis.claimMarkFList[c_index] == 1) {
              return false;
            }
          }
          return true;
        }
        else {   //click evidence
          var c_index = vuethis.HLEList[0].c_index
          var e_index = vuethis.HLEList[0].e_index
          if (d.id.indexOf("C") != -1) return true;
          var cur_c_i = parseInt(d.id.split("-")[0])
          var cur_e_i = parseInt(d.id.split("-")[1])
          console.log("cur_c_i", c_index, cur_c_i, "cur_e_i", e_index, cur_e_i)
          if ((cur_c_i == c_index) && (cur_e_i == e_index)) {
            return false;
          }
          return true;

        }


      })
    }
  },
  computed: {
    ...mapState([
      'displayMode',
      'claimMarkFList',
      'HLEList',
    ])
  },
  beforeMount: function () {
    this.emo_flat_list = window.sysDatasetObj.emoFlatData
    console.log("emo_flat_list", this.emo_flat_list)

  },
  mounted: function () {
    const divW = this.$refs.curveContainer.clientWidth
    const divH = this.$refs.curveContainer.clientHeight
    this.divH = divH
    this.divW = divW
    // console.log("div w h ", divW, divH)
    d3.select(".curve-svg").attr("width", divW)
    d3.select(".curve-svg").attr("height", divH)
    this.drawCurve()

  },
  methods: {
    drawCurve() {
      let vuethis = this
      // gen curve coordinates
      var coor_list = []
      var line = d3.line()
        .x(function (d) { return d.y; })
        .y(function (d) { return d.x; })
        .curve(d3.curveCardinal);
      // curveMonotoneY
      // curveCardinal +


      var word_len_list = []
      var tree_data = window.sysDatasetObj.jsonData.children
      var total_length = 0;

      var node_type_list = []
      var flat_c_mark_list = []
      var flat_type_list = []

      for (var i = 0; i < tree_data.length; i++) {
        var word_len = tree_data[i].name.length
        word_len_list.push(word_len)
        total_length += word_len
        node_type_list.push(tree_data[i].type)
        flat_c_mark_list.push(1)
        flat_type_list.push("C" + tree_data[i].index)

        for (var j = 0; j < tree_data[i].children.length; j++) {
          total_length += tree_data[i].children[j].name.length
          word_len_list.push(tree_data[i].children[j].name.length)
          node_type_list.push(tree_data[i].children[j].type)
          flat_c_mark_list.push(0)
          flat_type_list.push(i + "-" + j + "-" + tree_data[i].children[j].type.slice(-1))

        }
      }
      var tree_height = vuethis.divH * vuethis.curve_height_r




      var emo_flat_list = vuethis.emo_flat_list

      var x_start = vuethis.divH * (1 - vuethis.curve_height_r) / 2
      // var x_end=vuethis.divH*(1-vuethis.curve_width_r)/2+vuethis.divH*vuethis.curve_width_r
      var y_start = vuethis.divW * (1 - vuethis.curve_width_r) / 2
      // var y_end=vuethis.divW*(1-vuethis.curve_height_r)/2+vuethis.curve_height_r)

      var h_r = (tree_height - (emo_flat_list.length - 1) * vuethis.tree_inter) / total_length

      var x_inter = vuethis.divH * (vuethis.curve_height_r) / emo_flat_list.length
      var y_max = vuethis.divW * (vuethis.curve_width_r) / 2
      var y_cur_list = []
      var x_cur_list = []

      var x_cur_inter = 0
      for (var i = 0; i < emo_flat_list.length; i++) {

        var x_cur = x_start + word_len_list[i] * h_r / 2 + x_cur_inter
        x_cur_inter += word_len_list[i] * h_r + vuethis.tree_inter
        var y_i = 1
        // if (i % 2 == 0) {
        //   y_i = -1
        // }
        var y_cur = (emo_flat_list[i]) * y_i * y_max + vuethis.divW / 2
        x_cur_list.push(x_cur)
        // y_cur_list.push((emo_flat_list[i] + 1) * y_i * y_max / 2)
        y_cur_list.push(y_cur)

        coor_list.push({ x: x_cur, y: y_cur })
        if ((i == emo_flat_list.length - 1) || (((i + 1) < emo_flat_list.length) && (flat_c_mark_list[i + 1] == 1))) {
          var svg = d3.select("body").select(".curve-svg")
          svg.append("path")
            .datum(coor_list)
            .attr("d", line)
            .attr("stroke", "black")
            .attr("fill", "none");

          // x_cur_inter=0
          coor_list = []
        }



      }
      console.log("x_cur_list", x_cur_list)
      var svg = d3.select("body").select(".curve-svg")
      svg.append("path")
        .datum(coor_list)
        .attr("d", line)
        .attr("stroke", "black")
        .attr("fill", "none");

      //参照线 
      svg.append("path")

        .attr("d", "M" + vuethis.divW / 2 + "," + x_start + "L" + vuethis.divW / 2 + "," + tree_height)
        .attr("stroke", "black")
        .attr("fill", "none");

      const node_bind_data = emo_flat_list.map((item, index) => ({
        cy: x_cur_list[index],
        cx: y_cur_list[index],
        r: Math.log10(word_len_list[index] * h_r) * 5,
        fill: vuethis.eNodeColor(node_type_list[index]),
        id: flat_type_list[index],
        node_type: node_type_list[index],
        // node_index: function () {
        //   if (this.id.indexOf("C") != -1) {
        //     var index_str = parseInt(this.id.slice(1))
        //     return index_str - 1
        //   }
        //   else{

        //   }
        // }
        // 可以根据需要添加更多数据属性
      }));
      svg.selectAll(".cNode")
        .data(node_bind_data)
        .enter()
        .append("circle")
        .attr("cy", d => d.cy)
        .attr("cx", d => d.cx)
        .attr("r", d => d.r)
        .attr("fill", d => d.fill)
        .attr("class", "cNode")
        .attr("id", d => d.id)
        .on("mouseover", function (d) {
          // console.log("mouse over!", event)
          var id_str = event.target.id
          // console.log("id str!!", id_str)
          if (id_str.indexOf("C") == -1) {
            id_str = id_str.slice(-1)
          }
          document.getElementById("tooltip").innerText = `${id_str}`;
          var tooltip = document.getElementById("tooltip");
          // 获取提示框的尺寸


          var curveContainer = vuethis.$refs.curveContainer
          var curveContainerRect = curveContainer.getBoundingClientRect();
          var mainDiv_top = curveContainerRect.top
          var mainDiv_left = curveContainerRect.left

          // 计算提示框的初始位置
          var top = event.clientY;
          var left = event.clientX;
          top -= 30
          left -= 20
          top -= mainDiv_top
          left -= mainDiv_left

          tooltip.style.top = top + 'px';
          tooltip.style.left = left + 'px';
          document.getElementById("tooltip").style.display = "block";
        })


        .on("mouseout", function () {
          // 当鼠标离开时清除提示
          document.getElementById("tooltip").innerText = "";
          document.getElementById("tooltip").style.display = "none";
        })

        .on("click", function () {
          var id_str = event.target.id
          var node_index = parseInt(event.target.id.slice(0))
          var node_type = parseInt(event.target.id.slice(-1))
          if (id_str.indexOf('C') != -1) {//click claim!
            var c_index = parseInt(event.target.id.slice(-1)) - 1
            // var temp_value = vuethis.claimMarkFList[c_index]
            // console.log("temp value", temp_value, vuethis.claimMarkFList)
            var zero_list = []
            vuethis.$store.commit("setHLEList", lodash.cloneDeep(zero_list))
            vuethis.$store.commit("editCMFArray", { index: c_index, value: 1 })
          }
          else {  //click evi
            var str_list = id_str.split('-')
            c_index = parseInt(str_list[0])


            var e_index = parseInt(str_list[1])
            vuethis.$store.commit("updateHLEList", { c_index: c_index, e_index: e_index })
            vuethis.$store.commit("editCMFArray", { index: c_index, value: 1 })
            // vuethis.$store.commit("editEviModeList", { index: c_index, value: 1 })
            vuethis.$nextTick(() => {
              var eviDivs = d3.select("body").selectAll(".eviNodeDiv")
              // console.log("evi divs ", eviDivs)
              eviDivs.each(function (d, i) {
                var div_id = this.getAttribute("id")
                var s_start = div_id.indexOf("C")
                var c_index_str = div_id.slice(s_start + 1)
                var div_c_id = parseInt(c_index_str)
                // console.log("id com", div_c_id, c_index)
                if (div_c_id == c_index) {
                  var e_index_str = "E" + e_index
                  var dst_mark = d3.select(this).select("#" + e_index_str)
                  // console.log("select divs", dst_mark)

                  dst_mark.style("background", "grey")
                  setTimeout(function () {
                    dst_mark.transition().duration(2000)
                      .style("background", "white")
                    //   d3.select(self.frameElement).transition()
                    // .duration(duration)
                    // .style("height", height + "px");
                  }, 200)

                }
              })

            })
          }

        })




    },
    eNodeColor(e_type) {
      if (e_type.indexOf('C') != -1) {
        return "#1b9e77"
      }
      if (e_type.indexOf('S') != -1) {
        return "#66a61e"
      }
      else if (e_type.indexOf('P') != -1) {
        return "#7570b3"
      }
      else if (e_type.indexOf('O') != -1) {
        return "#d95f02"
      }
      else {
        return "#e7298a"
      }


    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
.curve-container {
  position: absolute;
  top: 0%;
  left: 0%;
  bottom: 0%;
  right: 0%;

  #tooltip {
    background-color: black;
    color: white;
    padding: 5px;
    border-radius: 3px;
    font-size: 14px;
    position: absolute;
    width: 20px;
    height: 10px;
    /* 确保它在其他元素之上 */
  }

  .cNode {
    stroke-width: 1;
    stroke: black;
    opacity: 1;

    &.highLighted {
      opacity: 0.2;
    }
  }
}
</style>
