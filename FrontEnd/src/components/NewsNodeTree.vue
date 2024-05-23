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
    claim_markF_list: function () {

    },

  },
  computed: {
    ...mapState([
      'displayMode',
      'eNodeYControlArray'
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

      for (var i = 0; i < tree_data.length; i++) {
        word_len = tree_data[i].name.length
        // 添加菱形图形
        var node_width = this.tree_width
        var node_height = word_len * h_r
        var svg = d3.select(".treeSvg")
        svg.append('path')
          .attr('class', 'diamond')
          .attr('d', `M ${node_width / 2 + cur_x},${cur_y}
                         L ${node_width + cur_x},${node_height / 2 + cur_y}
                         L ${node_width / 2 + cur_x},${node_height + cur_y}
                         L ${cur_x},${node_height / 2 + cur_y}
                         Z`)
          .attr("fill", "#1b9e77")

        svg.append("text")
          // .attr("x", cur_x - 20)
          .attr("x", cur_x + node_width / 2)
          .attr("y", cur_y + node_height / 2)
          .text("C" + tree_data[i].index)
          .style("font-size", "8px")
          .style("fill", "white")
          .style("text-anchor", "middle")
          .style("font-weight", "bold")
          .style("font-family", "sans-serif")
          // .style("font-style", "italic")
          .style("dominant-baseline", "middle")


        cur_y += node_height + this.tree_inter
        for (var j = 0; j < tree_data[i].children.length; j++) {
          word_len = tree_data[i].children[j].name.length
          var node_width = this.tree_width
          var node_height = word_len * h_r
          svg.append('rect')
            .attr("width", node_width)
            .attr("height", node_height)
            .attr("x", cur_x)
            .attr("y", cur_y)
            .attr("fill", this.eNodeColor(tree_data[i].children[j].type))
            .attr("opacity", "0.8")

          svg.append("text")
            // .attr("x", cur_x - 20)
            .attr("x", cur_x + node_width / 2)
            .attr("y", cur_y + node_height / 2)
            .text(tree_data[i].children[j].type.slice(-1))
            .style("font-size", "8px")
            .style("fill", "white")
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("font-family", "sans-serif")
            // .style("font-style", "italic")
            .style("dominant-baseline", "middle")

          cur_y += node_height + this.tree_inter
        }

      }



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
}
</style>
