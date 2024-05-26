<template>
  <div ref="treeSvgDiv" class="treeSvgDiv">

    <svg class="treeSvg">

    </svg>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import NewsEText from './NewsEText.vue';
import { tree } from 'd3';
export default {
  name: 'NewsNodeTree',
  props: {



  },
  components: {
    // NewsEText,

  },
  data() {
    return {
      evi_show_data: null,


      marge: { top: 10, bottom: 60, left: 800, right: 60 },
      tree_height_r: 0.95,

      tree_width_r: 0.25,
      tree_inter: 5,
      tree_head_inter: null,
      tree_left_inter: null,
      tree_height: null,
      tree_width: null,




    }

  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },
    claimMarkFList: function () {
      // console.log('claimMarkFList', this.claimMarkFList)
      let vuethis = this
      d3.select("body").select(".treeSvg").selectAll(".treeNodeGroup").classed("highLighted", function (d) {

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
        if (d.type === "diamond") {
          var c_index = parseInt(d.index) - 1
          if (vuethis.claimMarkFList[c_index] == 1) {
            return false;
          }
        }
        return true;

      })
    }

  },
  computed: {
    ...mapState([
      'displayMode',
      'eNodeYControlArray',
      'claimMarkFList',
    ])
  },
  beforeMount: function () {
    var claim_list = window.sysDatasetObj.jsonData.children
    var claim_markF_list = this.claim_markF_list
    var evi_show_data = []




  },
  mounted: function () {
    const divW = this.$refs.treeSvgDiv.clientWidth
    const divH = this.$refs.treeSvgDiv.clientHeight
    console.log("div w h ", divW, divH)
    d3.select(".treeSvg").attr("width", divW)
    d3.select(".treeSvg").attr("height", divH)

    this.tree_height = this.tree_height_r * divH
    this.tree_width = this.tree_width_r * divW
    this.tree_left_inter = (divW - this.tree_width) / 2
    this.tree_head_inter = (divH - this.tree_height) / 2
    console.log("sele treeSvg ", divW, this.tree_width, this.tree_left_inter)
    this.drawTree()

  },
  methods: {
    drawTree() {
      var tree_height = this.tree_height
      var word_len_list = []
      var tree_data = window.sysDatasetObj.jsonData.children
      var total_length = 0;
      for (var i = 0; i < tree_data.length; i++) {
        var word_len = tree_data[i].name.length
        word_len_list.push(word_len)
        total_length += word_len
        for (var j = 0; j < tree_data[i].children.length; j++) {
          total_length += tree_data[i].children[j].name.length
          word_len_list.push(tree_data[i].children[j].name.length)
        }
      }

      var h_r = (tree_height - (word_len_list.length - 1) * this.tree_inter) / total_length

      // begin draw tree
      var cur_y = this.tree_head_inter
      var cur_x = this.tree_left_inter
      // 创建一个新的数据数组，包含菱形和矩形的信息
      const node_data = [];
      for (let i = 0; i < tree_data.length; i++) {
        const node = tree_data[i];
        const nodeWidth = this.tree_width;
        const nodeHeight = node.name.length * h_r;

        // 菱形信息
        node_data.push({
          type: 'diamond',
          index: node.index,
          x: nodeWidth / 2 + cur_x,
          y: cur_y,
          width: nodeWidth,
          height: nodeHeight,
          fill: '#1b9e77',
          text: 'C' + node.index,
          textX: cur_x + nodeWidth / 2,
          textY: cur_y + nodeHeight / 2,
        });

        cur_y += nodeHeight + this.tree_inter;

        for (let j = 0; j < node.children.length; j++) {
          const child = node.children[j];
          const childWidth = this.tree_width;
          const childHeight = child.name.length * h_r;

          // 矩形信息
          node_data.push({
            type: 'rect',
            index: j,
            x: cur_x,
            y: cur_y,
            width: childWidth,
            height: childHeight,
            fill: this.eNodeColor(child.type),
            opacity: 0.8,
            text: child.type.slice(-1),
            textX: cur_x + childWidth / 2,
            textY: cur_y + childHeight / 2,
          });

          cur_y += childHeight + this.tree_inter;
        }
      }

      // 数据绑定
      const svg = d3.select("body").select(".treeSvg");
      // console.log("tree svg", svg)
      const nodeGroups = svg.selectAll(".treeNodeGroup")
        .data(node_data)
        .enter()
        .append("g")
        .attr('class', 'treeNodeGroup');
      nodeGroups.append(
        // function (d) {
        //   return document.createElementNS('http://www.w3.org/2000/svg', 'rect')
        // }

        function (d) {
          // return document.createElement("rect")
          if (d.type === 'diamond') {
            return document.createElementNS('http://www.w3.org/2000/svg', 'path')
          } else {
            return document.createElementNS('http://www.w3.org/2000/svg', 'rect')
          }
        }
      )
        .attr('class', 'treeNode')
        // .merge(nodes)
        .attr('d', function (d) {
          if (d.type === 'diamond') {
            return `M ${d.x},${d.y}
               L ${d.x + d.width / 2},${d.y + d.height / 2}
               L ${d.x},${d.y + d.height}
               L ${d.x - d.width / 2},${d.y + d.height / 2}
               Z`;
          }
        })
        .attr("fill", function (d) { return d.fill; })
        .attr("x", function (d) { return d.x; })
        .attr("y", function (d) { return d.y; })
        .attr("width", function (d) { return d.type === 'diamond' ? null : d.width; }) // 对菱形忽略宽度
        .attr("height", function (d) { return d.type === 'diamond' ? null : d.height; }) // 对菱形忽略高度
        // .attr("width", function (d) { return d.width; }) // 对菱形忽略宽度
        // .attr("height", function (d) { return d.height; }) // 对菱形忽略高度
        .attr("opacity", function (d) { return d.opacity; });

      // // 文本
      nodeGroups.selectAll("text")
        .data(function (d) { return [d]; }) // 为每个节点绑定自身数据
        .enter().append("text")
        // .merge(nodes.select("text"))
        .attr("x", function (d) { return d.textX; })
        .attr("y", function (d) { return d.textY; })
        .text(function (d) { return d.text; })
        .style("font-size", "8px")
        .style("fill", "white")
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .style("font-family", "sans-serif")
        .style("dominant-baseline", "middle");







      // for (var i = 0; i < tree_data.length; i++) {
      //   word_len = tree_data[i].name.length
      //   // 添加菱形图形
      //   var node_width = this.tree_width
      //   var node_height = word_len * h_r
      //   var svg = d3.select(".treeSvg")
      //   svg.append('path')
      //     .attr('class', 'diamond')
      //     .attr('d', `M ${node_width / 2 + cur_x},${cur_y}
      //                    L ${node_width + cur_x},${node_height / 2 + cur_y}
      //                    L ${node_width / 2 + cur_x},${node_height + cur_y}
      //                    L ${cur_x},${node_height / 2 + cur_y}
      //                    Z`)
      //     .attr("fill", "#1b9e77")

      //   svg.append("text")
      //     // .attr("x", cur_x - 20)
      //     .attr("x", cur_x + node_width / 2)
      //     .attr("y", cur_y + node_height / 2)
      //     .text("C" + tree_data[i].index)
      //     .style("font-size", "8px")
      //     .style("fill", "white")
      //     .style("text-anchor", "middle")
      //     .style("font-weight", "bold")
      //     .style("font-family", "sans-serif")
      //     // .style("font-style", "italic")
      //     .style("dominant-baseline", "middle")


      //   cur_y += node_height + this.tree_inter
      //   for (var j = 0; j < tree_data[i].children.length; j++) {
      //     word_len = tree_data[i].children[j].name.length
      //     var node_width = this.tree_width
      //     var node_height = word_len * h_r
      //     svg.append('rect')
      //       .attr("width", node_width)
      //       .attr("height", node_height)
      //       .attr("x", cur_x)
      //       .attr("y", cur_y)
      //       .attr("fill", this.eNodeColor(tree_data[i].children[j].type))
      //       .attr("opacity", "0.8")

      //     svg.append("text")
      //       // .attr("x", cur_x - 20)
      //       .attr("x", cur_x + node_width / 2)
      //       .attr("y", cur_y + node_height / 2)
      //       .text(tree_data[i].children[j].type.slice(-1))
      //       .style("font-size", "8px")
      //       .style("fill", "white")
      //       .style("text-anchor", "middle")
      //       .style("font-weight", "bold")
      //       .style("font-family", "sans-serif")
      //       // .style("font-style", "italic")
      //       .style("dominant-baseline", "middle")

      //     cur_y += node_height + this.tree_inter
      //   }

      // }



    },
    eNodeColor(e_type) {
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


  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style lang="less">
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.treeSvgDiv {
  position: absolute;
  top: 0%;
  left: 0%;
  bottom: 0%;
  right: 0%;

  .treeNodeGroup {
    text {
      font-size: 8px;
      fill: white;
      text-anchor: middle;
      fold-weight: bold;
      font-family: "sans-serif";
      dominant-baseline: middle;
      // .style("font-size", "8px") .style("fill", "white") .style("text-anchor", "middle") .style("font-weight", "bold") .style("font-family", "sans-serif") .style("dominant-baseline", "middle");
    }

    &.highLighted {
      opacity: 0.2;
    }
  }
}
</style>
