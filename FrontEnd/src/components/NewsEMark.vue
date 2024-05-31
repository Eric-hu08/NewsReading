<template>
  <el-slider class="evi-slider" :max="5" :min="0" v-model="evi_sum" :step="1" show-stops v-if="elShow(el_show)" />
  <mark :id="'E' + e_index">{{ sumContent(evi, evi_sum, evi_sum_exter) }}</mark>
  <span>&nbsp</span>

</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'NewsEText',
  props: {
    evi: Object,
    el_show: Number,
    e_index: Number,
    evi_sum_exter: Number,

  },
  data() {
    return {
      evi_sum: 0,




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

    // console.log("cnodename", this.cNodeName)

  },
  mounted: function () {


  },
  methods: {
    elShow() {
      if (this.el_show == 1) {
        return true
      }
      else {
        return false
      }
    },
    sumContent(evi, evi_sum, evi_sum_exter) {
      if (this.el_show == 0) {
        evi_sum = evi_sum_exter
      }
      if (evi_sum == 0) {
        return (evi.name + ".")
      }
      else {
        var sum_str = "sum" + (evi_sum - 1)
        return (evi[sum_str] + ".")
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
