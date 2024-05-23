<template>
  <div class="EviDiv" v-on:scroll="eviScroll">
    <div class="eviNodeDiv" v-for="(evi_data) in evi_show_data" :key="evi_data.name" ref="eviDivs"
      :id="'DC' + (evi_data.index - 1)">
      <el-card class="EviCard" :id="'EC' + (evi_data.index - 1)" ref="eviCard" v-if="evi_if_show(evi_data.index - 1, 0)"
        shadow="hover">

        <mark v-for="(evi, e_index) in evi_data.children" :key="evi.name" :id="'E' + e_index" @mouseover="textMouseOver"
          @mouseout="textMouseOut">
          {{ evi.name + ". " }}
        </mark>

      </el-card>
      <div class="nodeCardDiv" v-if="evi_if_show(evi_data.index - 1, 1)" :id="'EC' + (evi_data.index - 1)">

        <el-card class="EviCard" v-for="(evi, e_index) in evi_data.children" :key="evi.name" :id="'E' + e_index"
          shadow="hover">
          <circle r="5"></circle>
          <mark>{{ evi.name + ". " }}</mark>
        </el-card>

      </div>
      <!-- <div class="EviUnfoldDiv">
      <el-card class="EviCard" v-for="(evi_data) in evi_show_data" :key="evi_data.name" :id="'EC' + (evi_data.index - 1)"
      ref="eviCard">
      <mark v-for="(evi, e_index) in evi_data.children" :key="evi.name" :id="'E' + e_index" @mouseover="textMouseOver"
        @mouseout="textMouseOut">
        {{ evi.name + ". " }}
      </mark>
      </el-card>
      </div> -->
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import NewsEText from './NewsEText.vue';
export default {
  name: 'NewsEviPro',
  props: {
    claim_markF_list: Object,
    evi_mode_list: Object,


  },
  components: {
    // NewsEText,

  },
  data() {
    return {
      evi_show_data: null,
      evi_mode: false,


      marge: { top: 10, bottom: 60, left: 800, right: 60 },

      eCRInter: 80,
      eTextWidth: 600,
      ebarHeight: 50,
      ebarWidth: 600,

      e_text_dx: 5,

      eRCRW: 3,
      eRRInter: 2,



    }

  },
  watch: {
    displayMode: function () {
      // console.log('displayMode')
    },
    claim_markF_list: function () {
      // console.log("claimF change!")
      var claim_list = window.sysDatasetObj.jsonData.children
      var claim_markF_list = this.claim_markF_list
      var evi_show_data = []
      for (var i = 0; i < claim_markF_list.length; i++) {
        if (claim_markF_list[i] == 1) {
          if (claim_list[i].children.length > 0) {
            evi_show_data.push(claim_list[i])
          }

        }
      }
      this.evi_show_data = evi_show_data
      // console.log(this.evi_show_data)
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
    for (var i = 0; i < claim_markF_list.length; i++) {
      if (claim_markF_list[i] == 1) {
        evi_show_data.push(claim_list[i])
      }
    }
    // console.log("claimFlist in evi", this.claim_markF_list)



  },
  mounted: function () {
    // this.drawCRLink
    // this.changeEText()
    // console.log("e_dict", this.e_dict)
    // console.log("eviPro mounted!!")
    const EviDiv = this.$refs.EviDiv


  },
  updated() {
    this.updateEviCoor()


  },
  methods: {
    eviScroll(event) {
      this.updateEviCoor()

    },
    updateEviCoor() {
      // console.log("eviPro updateed!!")
      var eviDivs = this.$refs.eviDivs
      var eviCard = this.$refs.eviCard

      var attr_list = []
      var attr_index_list = []
      var evi_mode_list = this.evi_mode_list
      if (eviDivs == null) {
        return
      }
      // console.log("cur evimode", evi_mode_list)
      for (var i = 0; i < eviDivs.length; i++) {
        var eviDiv = eviDivs[i]
        var evi_div_id_str = eviDiv.id
        var evi_div_index = evi_div_id_str.slice(2)
        var temp_list = []
        console.log('eviDiv id', evi_div_id_str, evi_div_index, evi_mode_list[evi_div_index])
        // if (evi_mode_list[evi_div_index] == 0) {//one evi one card
        if (false) {//one evi one card
          console.log("in if")
          var card_ele = eviDiv.firstElementChild
          var id_str = card_ele.id
          var id_c_index = parseInt(id_str.slice(2))
          temp_list.push(card_ele.getBoundingClientRect())
          attr_list.push([id_c_index, temp_list])
          // console.log("evi idstr", id_str, card_ele.getBoundingClientRect())
        }
        else { //one evi multi card
          console.log("in else")
          var div_ele = eviDiv.firstElementChild

          id_str = div_ele.id
          id_c_index = parseInt(id_str.slice(2))
          var card_eles = div_ele.children
          // console.log("card ele", card_eles)
          console.log("in div_ele", div_ele, card_eles)
          for (var j = 0; j < card_eles.length; j++) {
            temp_list.push([card_eles[j].getBoundingClientRect()])

          }
          attr_list.push([id_c_index, temp_list])

        }
      }
      // for (var i = 0; i < eviCard.length; i++) {
      //   console.log("evicard ele ", eviCard[i].$el.id)
      //   var id_str = eviCard[i].$el.id
      //   var id_c_index = id_str.slice(2)
      //   console.log("coor ", eviCard[i].$el.getBoundingClientRect(), id_c_index)
      //   attr_index_list.push(id_c_index)
      //   attr_list.push([id_c_index, eviCard[i].$el.getBoundingClientRect()])

      // }
      attr_list.sort(function (a, b) {
        if (a[0] < b[0]) {
          return -1
        }
        if (a[0] > b[0]) {
          return 1
        }
        return 0
      })
      console.log("attrlist", attr_list)
      this.$store.commit("setEviIndexArray", attr_list)
    },
    evi_if_show(c_index, e_type) {
      var temp = this.evi_mode_list[c_index]
      // console.log("if show", c_index, temp)
      if (temp == e_type) {
        return true

      }
      else {
        return false
      }

    }


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

.EviDiv {
  height: 95vh;
  overflow-y: scroll;
}

.EviDiv::-webkit-scrollbar {
  display: none;
  width: 10px;
}

.EviDiv::-webkit-scrollbar-track {
  background-color: #f1f1f1;
  opacity: 0.2;
}

.EviDiv::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 5px;
}

.EviDiv::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}


.EviCard {



  mark {
    background: white;
  }

  mark:hover {
    background: grey;
  }
}
</style>
