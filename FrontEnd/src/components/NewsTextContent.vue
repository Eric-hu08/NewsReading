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
      <NewsEviPro :claim_markF_list="claim_markF_list"></NewsEviPro>
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
    }
  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },
    mainText_mode: function () {

    },
    claim_markF_list: function () {
      // this.getNodeCoor()
    },
    eviIndexArray: function () {
      console.log("watch change ", this.eviIndexArray)
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
      d3.select(".linkSvg").selectAll(".cardLink").remove()
      for (i = 0; i < claim_index_list.length; i++) {
        var claim_i = claim_index_list[i]
        // draw path
        d3.select(".linkSvg").append("path")
          .attr("class", "cardLink")
          // .attr("id", "p" + i).attr("class", "nodeLink")
          .attr("d", "M " + (claim_coor_list[claim_i].x - svg_attr.x + claim_coor_list[claim_i].width) + " " + (claim_coor_list[claim_i].y - svg_attr.y) + " L " + (eviIndexArray[i].x - svg_attr.x) + " " + (eviIndexArray[i].y - svg_attr.y + eviIndexArray[i].height / 2))
          .attr("stroke", "black")
      }

    }
  },
  computed: {
    ...mapState([
      'displayMode',
      'eviIndexArray',
    ])
  },
  beforeMount: function () {
    this.claim_list = this.jsonData.children
    // console.log(this.claim_list.length)
    var claim_markF_list = []
    for (var i = 0; i < this.claim_list.length; i++) {
      claim_markF_list.push(0);
    }
    this.claim_markF_list = claim_markF_list
  },
  mounted: function () {
    const divW = this.$refs.mainTextContent.clientWidth
    const divH = this.$refs.mainTextContent.clientHeight
    this.card_width = divW + 'px';


  },
  methods: {
    getNodeCoor() {
      let vuethis = this
      var marks = vuethis.$refs.mainMark
      console.log("coord test ", marks)
      var mainMarkCoorArray = []
      for (var i = 0; i < marks.length; i++) {
        mainMarkCoorArray.push(marks[i].getBoundingClientRect())
      }
      console.log("coord test ", mainMarkCoorArray)
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
      vuethis.claim_markF_list = lodash.cloneDeep(f_list)

      // alert("mouseclcik")
      // console.log(event.target)
      // console.log(f_mark, vuethis.claim_markF_list[c_index], id_str, c_index)
      // console.log(vuethis.claim_markF_list)

      if (f_mark == 0) {//unfold
        // this.show
        event.target.style.background = "grey"
      }
      else {// to fold
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
    }

    .paragraphHighlight {
      background: grey;
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

  }
}
</style>
