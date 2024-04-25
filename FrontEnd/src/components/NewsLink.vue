<template>
  <div ref="linkSvgDiv" class="linkSvgDiv">
    <svg class="linkSvg">

    </svg>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import NewsEText from './NewsEText.vue';
export default {
  name: 'NewsLink',
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
    const divW = this.$refs.linkSvgDiv.clientWidth
    const divH = this.$refs.linkSvgDiv.clientHeight
    console.log("div w h ", divW, divH)
    d3.select(".linkSvg").attr("width", divW)
    d3.select(".linkSvg").attr("height", divH)

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

.linkSvgDiv {
  position: absolute;
  top: 0%;
  left: 0%;
  bottom: 0%;
  right: 0%;
}
</style>
