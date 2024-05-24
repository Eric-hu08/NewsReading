<template>
  <div class="mainTextDiv">
    <el-switch v-model="mainText_mode" class="mainText-switch"
      style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" active-text="text mode"
      inactive-text="node mode" />
    <div class="mainText-content" ref="mainTextContent">
      <el-card class="mainTextCard" v-if="mainText_mode">
        <mark class="mainMark" :class="{ 'paragraphHighlight': ifMark(c_index) }" ref="mainMark"
          v-for="(claim, c_index) in claim_list" :key="claim.name" :id="'C' + c_index" @mouseover="textMouseOver"
          @mouseout="textMouseOut" @click="textClick">
          {{ claim.name + ". " }}

        </mark>
        <!-- <el-icon @click="foldClick(c_index)">
          <Sort />
        </el-icon> -->
      </el-card>
      <div class="node_card" v-if="!mainText_mode">
        <el-card class="mainTextCard" v-for="(claim, c_index) in claim_list" :key="claim.name" :id="'C' + c_index">
          <mark class="mainMark" :class="{ 'paragraphHighlight': ifMark(c_index) }" ref="mainMark" :id="'C' + c_index"
            @mouseover="textMouseOver" @mouseout="textMouseOut" @click="textClick">
            {{ claim.name + ". " }}
          </mark>

        </el-card>
      </div>
    </div>
    <div class="linkDiv" ref="linkDiv">
      <NewsLink>
      </NewsLink>
    </div>
    <div class="eviView" ref="eviView">
      <NewsEviPro :claim_markF_list="claim_markF_list" :evi_mode_list="evi_mode_list"></NewsEviPro>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import { ref } from 'vue';

import NewsEviPro from './NewsEviPro.vue';
import NewsLink from './NewsLink.vue';


export default {
  name: 'NewsTextContent',
  components: {
    NewsEviPro,
    NewsLink,
  },
  props: {
    msg: String,
    jsonData: Object,
  },
  data() {
    return {
      mainText_mode: ref(true),
      card_width: '480px',
      claim_list: [],
      claim_markF_list: [],
      activeIndex: null,
      evi_mode_list: [],

      pathRect_width: 0.05,
      pathRect_end_h_r: 0.99,
    }
  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },
    claimMarkFList: function () {
      this.claim_markF_list = this.claimMarkFList
    },
    eviModeList: function () {
      this.evi_mode_list = this.eviModeList
    },
    eviIndexArray: function () {
      console.log("watch change ", this.eviIndexArray)
      this.genLink()

    }
  },
  computed: {
    ...mapState([
      'displayMode',
      'eviIndexArray',
      'claimMarkFList',
      'eviModeList',
    ])
  },
  beforeMount: function () {
    this.claim_list = this.jsonData.children
    // console.log(this.claim_list.length)
    var claim_markF_list = []
    var evi_mode_list = []
    for (var i = 0; i < this.claim_list.length; i++) {
      claim_markF_list.push(0);
      evi_mode_list.push(0)
    }
    this.claim_markF_list = claim_markF_list
    this.$store.commit('setCMFArray', claim_markF_list)
    this.evi_mode_list = evi_mode_list
    this.$store.commit('setEviModeList', evi_mode_list)

  },
  mounted: function () {
    const divW = this.$refs.mainTextContent.clientWidth
    const divH = this.$refs.mainTextContent.clientHeight
    this.card_width = divW + 'px';


  },
  updated: function () {
    this.genLink()
  },
  methods: {
    foldClick(event) {
      console.log("foldclick!!", event.target)
      var id_str = event.target.id
      var claim_i = parseInt(id_str.slice(3))
      // console.log("fold click", claim_i)
      var evi_mode_list = this.evi_mode_list
      var temp = evi_mode_list[claim_i]
      evi_mode_list[claim_i] = 1 - temp
      this.evi_mode_list = lodash.cloneDeep(evi_mode_list)
      // TODO:evi unfold the evi_mode_list should to reset to 0!!

    },
    genLink() {
      // return
      var eviIndexArray = this.eviIndexArray
      var claim_coor_list = this.getNodeCoor()
      var claim_markF_list = this.claim_markF_list
      var claim_index_list = []
      for (var i = 0; i < claim_markF_list.length; i++) {
        if (claim_markF_list[i] == 1) {
          claim_index_list.push(i)
        }
      }

      var svg_attr = this.$refs.linkDiv.getBoundingClientRect()
      var mainCard_attr = this.$refs.mainTextContent.getBoundingClientRect()
      d3.select(".linkSvg").selectAll(".linkG").remove()

      var pathRect_width = this.pathRect_width * this.$refs.linkDiv.clientWidth
      let vuethis = this
      var claim_list = vuethis.claim_list
      for (i = 0; i < claim_index_list.length; i++) {
        var claim_i = claim_index_list[i]
        if (eviIndexArray[i] == null) continue
        // draw path
        var rect_x = mainCard_attr.x - svg_attr.x + mainCard_attr.width
        console.log("evi Array", eviIndexArray[i], eviIndexArray[i][1])
        var rect_end_x = eviIndexArray[i][1][0][0].x - pathRect_width - svg_attr.x
        // var rect_end_x = eviIndexArray[i][1][0][0].x - pathRect_width - svg_attr.x
        // TODO: evi i?
        var evi_coor_list = eviIndexArray[i][1]
        var g = d3.select(".linkSvg").append("g").attr("class", "linkG")

        g.append("rect")
          .attr("x", rect_x).attr("y", claim_coor_list[claim_i].y - svg_attr.y + 10)
          .attr("width", pathRect_width)
          .attr("height", claim_coor_list[claim_i].height - 10)
          .attr("rx", 1).attr("ry", 2)
          .attr("stroke", "grey")
          .attr("fill", "grey")

        g.append("text")
          .attr("x", rect_x + pathRect_width / 2).attr("y", claim_coor_list[claim_i].y - svg_attr.y + claim_coor_list[claim_i].height / 2)
          .text("C" + claim_list[claim_i].index)
          .style("font-size", "8px")
          .style("fill", "white")
          .style("text-anchor", "middle")
          .style("font-weight", "bold")
          .style("font-family", "sans-serif")
          // .style("font-style", "italic")
          .style("dominant-baseline", "middle")


        if (claim_list[claim_i].children.length > 1) {
          g.append("circle")
            .attr("class", "fold_button")
            .attr("cx", rect_x + pathRect_width * 2 + 5).attr("cy", claim_coor_list[claim_i].y - svg_attr.y + claim_coor_list[claim_i].height)
            .attr("r", 9)
            .attr("id", "Cir" + claim_i)
            .attr("fill", "white")
            .on('click', function () {
              vuethis.foldClick(d3.event)
            })
          var tran_x = rect_x + pathRect_width * 2 - 5
          var tran_y = claim_coor_list[claim_i].y - svg_attr.y + claim_coor_list[claim_i].height - 10
          // g.append(<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" ><path fill="currentColor" d="M118.656 438.656a32 32 0 0 1 0-45.248L416 96l4.48-3.776A32 32 0 0 1 461.248 96l3.712 4.48a32.064 32.064 0 0 1-3.712 40.832L218.56 384H928a32 32 0 1 1 0 64H141.248a32 32 0 0 1-22.592-9.344zM64 608a32 32 0 0 1 32-32h786.752a32 32 0 0 1 22.656 54.592L608 928l-4.48 3.776a32.064 32.064 0 0 1-40.832-49.024L805.632 640H96a32 32 0 0 1-32-32"></path></svg>)

          var button_g = g.append("g").attr("class", "fold_button")


          button_g.on('click', function () {
            vuethis.foldClick(d3.event)
          })
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .attr("transform", "translate(" + (tran_x) + "," + (tran_y) + ")scale(0.02)")
          button_g.append("path")
            .attr("id", "Cir" + claim_i)
            .attr("d", "M118.656 438.656a32 32 0 0 1 0-45.248L416 96l4.48-3.776A32 32 0 0 1 461.248 96l3.712 4.48a32.064 32.064 0 0 1-3.712 40.832L218.56 384H928a32 32 0 1 1 0 64H141.248a32 32 0 0 1-22.592-9.344zM64 608a32 32 0 0 1 32-32h786.752a32 32 0 0 1 22.656 54.592L608 928l-4.48 3.776a32.064 32.064 0 0 1-40.832-49.024L805.632 640H96a32 32 0 0 1-32-32")
            .attr("fill", "currentColor")
        }






        // console.log("evi_coorlist", evi_coor_list)
        var Bézier_curve_generator = d3.linkHorizontal()
          .x(function (d) { return d.x; })
          .y(function (d) { return d.y; });


        // gen evi color list
        var evi_color_list = []
        var evi_list = claim_list[claim_i].children
        for (var z = 0; z < evi_list.length; z++) {
          evi_color_list.push(this.eNodeColor(evi_list[z].type))
        }
        var evi_mode_list = vuethis.evi_mode_list
        var evi_mode = evi_mode_list[i]


        for (var j = 0; j < evi_coor_list.length; j++) {
          var evi_attr = evi_coor_list[j][0]
          // var e_type = claim_list[claim_i].children[j].type
          // console.log("evi attr", evi_attr)
          var start_x = rect_x + pathRect_width
          var start_y = claim_coor_list[claim_i].y - svg_attr.y + claim_coor_list[claim_i].height / 2
          var end_x = evi_attr.x - svg_attr.x
          var end_y = evi_attr.y - svg_attr.y + evi_attr.height / 2
          var start = { x: end_x, y: end_y }
          var end = { x: start_x, y: start_y }
          g.append("path")
            .attr("class", "cardLink")
            // .attr("id", "p" + i).attr("class", "nodeLink")
            .attr("d", Bézier_curve_generator({ source: start, target: end }))
            // .attr("d", "M " + (rect_x + pathRect_width) + " " + (claim_coor_list[claim_i].y - svg_attr.y + claim_coor_list[claim_i].height / 2) + " L " + (evi_attr.x - svg_attr.x) + " " + (evi_attr.y - svg_attr.y + evi_attr.height / 2))
            .attr("stroke", "black")
            .attr("fill", "none")




          if (evi_coor_list.length == 1) {//fold
            var rect_h = evi_attr.height * this.pathRect_end_h_r
            var rect_y = evi_attr.y - svg_attr.y + evi_attr.height * (1 - this.pathRect_end_h_r) / 2
            for (var z = 0; z < evi_color_list.length; z++) {
              g.append("rect")
                .attr("x", rect_end_x).attr("y", rect_y + rect_h / evi_color_list.length * z)
                .attr("width", pathRect_width)
                .attr("height", rect_h / evi_color_list.length)
                .attr("rx", 1).attr("ry", 2)
                .attr("stroke", "grey")
                .attr("fill", evi_color_list[z])
              g.append("text")
                .attr("x", rect_end_x + pathRect_width / 2).attr("y", rect_y + rect_h / evi_color_list.length * z + rect_h / evi_color_list.length / 2)
                .text(evi_list[z].type.slice(-1))
                .style("font-size", "8px")
                .style("fill", "white")
                .style("text-anchor", "middle")
                .style("font-weight", "bold")
                .style("font-family", "sans-serif")
                // .style("font-style", "italic")
                .style("dominant-baseline", "middle")


            }
          }
          else { //unfold
            g.append("rect")
              .attr("x", rect_end_x).attr("y", evi_attr.y - svg_attr.y + evi_attr.height * (1 - this.pathRect_end_h_r) / 2)
              .attr("width", pathRect_width)
              .attr("height", evi_attr.height * this.pathRect_end_h_r)
              .attr("rx", 1).attr("ry", 2)
              .attr("stroke", "grey")
              .attr("fill", evi_color_list[j])
            g.append("text")
              .attr("x", rect_end_x + pathRect_width / 2).attr("y", evi_attr.y - svg_attr.y + evi_attr.height * (1 - this.pathRect_end_h_r) / 2 + evi_attr.height * this.pathRect_end_h_r / 2)
              .text(evi_list[j].type.slice(-1))
              .style("font-size", "8px")
              .style("fill", "white")
              .style("text-anchor", "middle")
              .style("font-weight", "bold")
              .style("font-family", "sans-serif")
              // .style("font-style", "italic")
              .style("dominant-baseline", "middle")
          }




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
    getNodeCoor() {
      let vuethis = this
      var marks = vuethis.$refs.mainMark
      // console.log("coord test ", marks)
      var mainMarkCoorArray = []
      for (var i = 0; i < marks.length; i++) {
        mainMarkCoorArray.push(marks[i].getBoundingClientRect())
      }
      // console.log("coor d test ", mainMarkCoorArray)
      return mainMarkCoorArray

    },
    textMouseOver(event) {
      // console.log("mouse in!!")

      event.target.style.background = "grey"
      // console.log(event.target)
      // if (event.target.tagName == 'SPAN') {
      //   var mark_text = document.createElement("mark")
      //   mark_text.onclick = this.onClick
      //   mark_text.id = event.target.id
      //   mark_text.style.backgroundColor = "blue"
      //   var text_content = event.target.textContent
      //   mark_text.innerHTML = text_content
      //   event.target.textContent = ""
      //   event.target.appendChild(mark_text)
      // }

    },
    textMouseOut(event) {
      // console.log("mouse in!!")

      // console.log(event.target.firstElementChild)
      var id_str = event.target.id
      var c_index = parseInt(id_str.slice(1, id_str.length))
      var f_mark = this.claim_markF_list[c_index]
      if (f_mark == 0) {
        console.log("white move out")
        event.target.style.background = "white"
      }
      // // console.log("mouse out", event.target, event.target.parentElement)
      // if (f_mark == 0) {
      //   var mark_node, span_node
      //   if (event.target.tagName == "SPAN") {
      //     mark_node = event.target.firstElementChild
      //     span_node = event.target
      //   }
      //   else {
      //     mark_node = event.target
      //     span_node = event.target.parentElement
      //   }

      //   var text_content = mark_node.innerHTML
      //   span_node.removeChild(mark_node)
      //   span_node.textContent = text_content
      // }


    },
    textClick(event) {
      let vuethis = this
      var id_str = event.target.id
      var c_index = parseInt(id_str.slice(1, id_str.length))
      var f_mark = vuethis.claim_markF_list[c_index]
      var f_list = vuethis.claim_markF_list
      vuethis.activeIndex = c_index
      f_list.splice(c_index, 1, 1 - f_mark)
      vuethis.$store.commit("setCMFArray", lodash.cloneDeep(f_list))
      vuethis.claim_markF_list = lodash.cloneDeep(f_list)


      // alert("mouseclcik")
      // console.log(event.target)
      // console.log(f_mark, vuethis.claim_markF_list[c_index], id_str, c_index)
      // console.log(vuethis.claim_markF_list)
      var evi_mode_list = this.evi_mode_list
      var temp = evi_mode_list[c_index]
      if (temp == 1) {
        evi_mode_list[c_index] = 1 - temp
        this.evi_mode_list = lodash.cloneDeep(evi_mode_list)
      }

      if (f_mark == 0) {//unfold
        // this.show
        event.target.style.background = "grey"
      }
      else {// to fold
        console.log("white click")

        event.target.style.background = "white"
      }

    },

    ifMark(c_index) {
      let vuethis = this
      var f_mark = vuethis.claim_markF_list[c_index]
      if (f_mark == 1) {
        return true
      }
      else {
        return false
      }
    }
    // genMarkColor(event) {
    //   let vuethis = this

    //   console.log("ele ", vuethis.$el, vuethis, this)
    //   var id_str = event.id
    //   var c_index = parseInt(id_str.slice(1, id_str.length))
    //   var f_mark = vuethis.claim_markF_list[c_index]
    //   if (f_mark == 0) {
    //     return "white"
    //   }
    //   else {
    //     return "grey"
    //   }
    // }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.mainTextDiv {
  position: absolute;
  top: 0%;
  left: 0%;
  bottom: 0%;
  right: 0%;

  .mainText-switch {
    position: absolute;
    top: 0%;
    left: 0%;
    bottom: 95%;
    right: 50%;
  }

  .mainText-content {
    position: absolute;
    top: 5%;
    left: 0%;
    bottom: 0%;
    right: 60%;
    text-align: left;

    .mainTextCard {
      max-width: v-bind(card_width);

    }

    mark {
      background: white;
      cursor: pointer;

      &.paragraphHighlight {
        background: grey !important;
      }
    }



    .el-icon {
      float: none;
    }




  }

  .linkDiv {
    position: absolute;
    top: 0%;
    left: 40%;
    bottom: 0%;
    right: 45%;
  }

  .eviView {
    position: absolute;
    top: 0%;
    left: 55%;
    bottom: 0%;
    right: 0%;
    text-align: left;

    // mark {
    //   transition: background 10s;
    //   background: white;


    // }
  }
}
</style>
