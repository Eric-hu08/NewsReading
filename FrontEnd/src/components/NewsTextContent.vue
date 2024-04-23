<template>
  <div class="mainTextDiv">
    <el-switch v-model="mainText_mode" class="mainText-switch"
      style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" active-text="text mode"
      inactive-text="node mode" />
    <div class="mainText-content" ref="mainTextContent">
      <el-card class="mainTextCard">
        <span v-for="(claim, c_index) in claim_list" :key="claim.name" :id="'C' + c_index" @mouseover="textMouseOver"
          @mouseout="textMouseOut" @click="textClick">
          {{ claim.name + ". " }}
        </span>
      </el-card>
    </div>
    <div class="eviView">
      <NewsEviPro :claim_markF_list="claim_markF_list"></NewsEviPro>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import { ref } from 'vue';

import NewsEviPro from './NewsEviPro.vue';


export default {
  name: 'NewsTextContent',
  components: {
    NewsEviPro,
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
    }
  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    }
  },
  computed: {
    ...mapState([
      'displayMode'
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
    textMouseOver(event) {
      // console.log("mouse in!!")
      // console.log(event.target.tagName)
      if (event.target.tagName == 'SPAN') {
        var mark_text = document.createElement("mark")
        mark_text.onclick = this.onClick
        mark_text.id = event.target.id
        mark_text.style.backgroundColor = "blue"
        var text_content = event.target.textContent
        mark_text.innerHTML = text_content
        event.target.textContent = ""
        event.target.appendChild(mark_text)
      }

    },
    textMouseOut(event) {
      // console.log("mouse in!!")
      // console.log(event.target.firstElementChild)
      var id_str = event.target.id
      var c_index = parseInt(id_str.slice(1, id_str.length))
      var f_mark = this.claim_markF_list[c_index]
      // console.log("mouse out", event.target, event.target.parentElement)
      if (f_mark == 0) {
        var mark_node, span_node
        if (event.target.tagName == "SPAN") {
          mark_node = event.target.firstElementChild
          span_node = event.target
        }
        else {
          mark_node = event.target
          span_node = event.target.parentElement
        }

        var text_content = mark_node.innerHTML
        span_node.removeChild(mark_node)
        span_node.textContent = text_content
      }


    },
    textClick(event) {
      let vuethis = this
      var id_str = event.target.id
      var c_index = parseInt(id_str.slice(1, id_str.length))
      var f_mark = vuethis.claim_markF_list[c_index]
      var f_list = vuethis.claim_markF_list

      f_list.splice(c_index, 1, 1 - f_mark)
      vuethis.claim_markF_list = lodash.cloneDeep(f_list)
      // alert("mouseclcik")
      console.log(event.target)
      console.log(f_mark, vuethis.claim_markF_list[c_index], id_str, c_index)
      console.log(vuethis.claim_markF_list)

      // if (f_mark == 0) {//unfold
      //   // this.show
      // }
      // else {// to fold

      // }
    }
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
    right: 50%;
    text-align: left;

    .mainTextCard {
      max-width: v-bind(card_width);

    }


  }

  .eviView {
    position: absolute;
    top: 0%;
    left: 50%;
    bottom: 0%;
    right: 0%;
    text-align: left;

  }
}
</style>
