<template>
  <div class="EviDiv">
    <el-card class="EviCard" v-for="(evi_data) in evi_show_data" :key="evi_data.name" :id="'EC' + (evi_data.index - 1)"
      ref="eviCard">
      <mark v-for="(evi, e_index) in evi_data.children" :key="evi.name" :id="'E' + e_index" @mouseover="textMouseOver"
        @mouseout="textMouseOut">
        {{ evi.name + ". " }}
      </mark>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import NewsEText from './NewsEText.vue';
export default {
  name: 'NewsEviPro',
  props: {
    claim_markF_list: Object,


  },
  components: {
    // NewsEText,

  },
  data() {
    return {
      evi_show_data: null,


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
      console.log('displayMode')
    },
    claim_markF_list: function () {
      console.log("claimF change!")
      var claim_list = window.sysDatasetObj.jsonData.children
      var claim_markF_list = this.claim_markF_list
      var evi_show_data = []
      for (var i = 0; i < claim_markF_list.length; i++) {
        if (claim_markF_list[i] == 1) {
          evi_show_data.push(claim_list[i])
        }
      }
      this.evi_show_data = evi_show_data
      console.log(this.evi_show_data)
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
    console.log("claimFlist in evi", this.claim_markF_list)



  },
  mounted: function () {
    // this.drawCRLink
    // this.changeEText()
    // console.log("e_dict", this.e_dict)
    // console.log("eviPro mounted!!")

  },
  updated() {
    // console.log("eviPro updateed!!")
    var eviCard = this.$refs.eviCard
    console.log("evicard ele ", eviCard)
    var attr_list = []
    for (var i = 0; i < eviCard.length; i++) {
      console.log("coor ", eviCard[i].$el.getBoundingClientRect())
      attr_list.push(eviCard[i].$el.getBoundingClientRect())

    }
    console.log("attrlist", attr_list)
    this.$store.commit("setEviIndexArray", attr_list)


  },
  methods: {



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

.EviCard {
  mark {
    background: white;
  }

  mark:hover {
    background: grey;
  }
}
</style>
