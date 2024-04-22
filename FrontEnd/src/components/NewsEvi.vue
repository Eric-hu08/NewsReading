<template>

  <g class="Evi" :id="('E' + e_dict.c_index + '_' + e_dict.e_index)" :transform="EviTran()">
    <g class="EviN">
      <circle class="EviC" cx="0" cy="0" :r="eNodeR" :fill="eNodeColor()" @click="eNodeClick()" opacity="0.7">
      </circle>
      <text text-anchor="middle" class="enodeText" dy="3">{{ eNodeName }}</text>
    </g>
    <g class="EviT" v-if="f_eviT()" :transform="EviTTran()">
      <rect class="eviR" :y="-ebarHeight / 2" :height="ebarHeight" :width="ebarWidth" :fill="eNodeColor()">
      </rect>
      <NewsEText :e_content="e_dict.e_content"></NewsEText>
    </g>


  </g>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import NewsEText from './NewsEText.vue';
export default {
  name: 'NewsEvi',
  props: {
    e_dict: Object,
    e_node_y_array: Object,
    e_render_index: Number,
    e_index_map_array: Object,

    eNodeR: Number,

  },
  components: {
    NewsEText,

  },
  data() {
    return {
      marge: { top: 10, bottom: 60, left: 800, right: 60 },

      eCRInter: 80,
      eTextWidth: 600,
      ebarHeight: 50,
      ebarWidth: 600,
      e_text_dy: -10,  //不管用
      e_text_dx: 5,

      eRCRW: 3,
      eRRInter: 2,



    }

  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },

  },
  computed: {
    ...mapState([
      'displayMode',
      'eNodeYControlArray'
    ])
  },
  beforeMount: function () {
    this.eNodeName = "E" + String(this.e_dict.e_type)
    // console.log("cnodename", this.cNodeName)

  },
  mounted: function () {
    // this.drawCRLink
    // this.changeEText()
    // console.log("e_dict", this.e_dict)

  },
  methods: {
    drawCRLink(cur_v) {
      let vuethis = this
      if (cur_v == 1) {
        var rect_x = vuethis.eCRInter
        var rect_y = vuethis.e_node_y_array[vuethis.e_dict.c_index - 1][vuethis.e_index_map_array[vuethis.e_render_index]] + vuethis.marge.top
        var link_g = d3.select(vuethis.$el).append("g").attr("class", "eCRLink")
        link_g.append("path")
          .attr("d", "M" + vuethis.eNodeR + " 0L" + (rect_x - vuethis.eRCRW - vuethis.eRRInter) + " " + "0")
          .attr("stroke", "#c8ccc6")
        link_g.append("rect")
          .attr("y", -(vuethis.ebarHeight) / 2)
          .attr("x", rect_x - vuethis.eRCRW - vuethis.eRRInter)
          .attr("height", vuethis.ebarHeight)
          .attr("width", vuethis.eRCRW)
          .attr("rx", 1).attr("ry", 2)
          .attr("stroke", "#c8ccc6")
          .attr("fill", "#c8ccc6")
      }
      else {
        d3.select(vuethis.$el).select(".eCRLink").remove()
      }



    },
    EviTran() {
      let vuethis = this
      // get C and Y index
      let e_dict = vuethis.e_dict
      var c_index = e_dict.c_index
      var e_index = vuethis.e_render_index
      var e_index_map_array = vuethis.e_index_map_array
      // console.log("e_index map", e_index_map_array)

      // get Y tran
      var e_node_y_array = vuethis.e_node_y_array
      // console.log("enodeyraaar", e_node_y_array, c_index, e_index)
      var y_tran = e_node_y_array[c_index - 1][e_index_map_array[e_index]]
      // console.log("y_tran", y_tran, typeof y_tran)

      return "translate(" + vuethis.marge.left + "," + (y_tran + vuethis.marge.top) + ")"


    },
    f_eviT() {
      let vuethis = this
      var eNodeYControlArray = vuethis.eNodeYControlArray
      var e_dict = vuethis.e_dict
      var c_index = e_dict.c_index - 1
      var e_index = vuethis.e_index_map_array[vuethis.e_render_index]
      // console.log("enodeYc:", eNodeYControlArray, c_index, e_index)
      // return true
      if (eNodeYControlArray[c_index][e_index] == 1) {
        return true
      }
      else {
        return false
      }
    },
    EviTTran() {
      return "translate(" + this.eCRInter + ",0)"
    },
    changeEText() {
      let vuethis = this

      // console.log("e select ", d3.select(vuethis.$el))
      d3.select(vuethis.$el).select(".eText").text("")
      console.log("d3 select changeetset", d3.select(vuethis.$el).select(".eText")._groups[0][0])
      if (d3.select(vuethis.$el).select(".eText")._groups[0][0] == undefined) {
        d3.select(vuethis.$el).select(".EviT").append("text")
          .attr("class", "eText")
          .attr("dx", vuethis.e_text_dx)
        console.log("d3 select changeetset", d3.select(vuethis.$el).select(".EviT"))
      }

      d3.select(vuethis.$el).select(".eText").call(wrapText, vuethis.e_dict.e_content, vuethis.eTextWidth)




      function wrapText(text, getcontent, width) {
        // console.log("getcontent: ", getcontent)
        var content = getcontent

        var words = content.split(/\s+/);
        var lineHeight = 1; // 行高
        var line = [];
        var lineNumber = 0;
        var tspan = text.append("tspan")
          .attr("x", 0)
          .attr("y", vuethis.e_text_dy)
          .attr("dy", 0);

        words.forEach(function (word) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan")
              .attr("x", 5)
              .attr("y", vuethis.e_text_dy)
              // .attr("dy", 3)
              .attr("dy", lineHeight * ++lineNumber + "em")
              .text(word)
            // .style("text-anchor", "middle")
          }
        });
      }
    },
    eNodeClick() {
      // alert("node click")
      let vuethis = this
      var eNodeYControlArray = vuethis.eNodeYControlArray
      var e_dict = vuethis.e_dict
      var c_index = e_dict.c_index - 1
      var e_index = vuethis.e_index_map_array[vuethis.e_render_index]
      // console.log("enodeYc:", eNodeYControlArray, c_index, e_index)
      var cur_v = eNodeYControlArray[c_index][e_index]
      cur_v = 1 - cur_v
      console.log("enode click!", cur_v, c_index, e_index)

      vuethis.$store.commit('editENodeYControlArray', [c_index, e_index, cur_v])
      console.log("after clcik: ", vuethis.eNodeYControlArray)

      vuethis.drawCRLink(cur_v)

      // vuethis.$nextTick(() => {
      //   vuethis.changeEText()
      // })
      // vuethis.changeEText()
      // vuethis.$forceUpdate()

    },
    eNodeColor() {

      // console.log("e color", this.e_dict.e_type)

      // alert("e circle color")
      if (this.e_dict.e_type.indexOf('S') != -1) {
        return "#8dd3c7"
      }
      else if (this.e_dict.e_type.indexOf('P') != -1) {
        return "#ffffb3"
      }
      else if (this.e_dict.e_type.indexOf('O') != -1) {
        return "#bebada"
      }
      else {
        return "#fb8072"
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

text.enodeText {
  font: 8px sans-serif;
  font-weight: bold;
  pointer-events: none;
}
</style>
