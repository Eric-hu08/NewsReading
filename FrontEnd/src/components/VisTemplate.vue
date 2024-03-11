<template>
  <svg class="canvas">
    <rect class="bar" v-for="obj in objList" :x="obj.x" :y="obj.y" :width="obj.w" :height="obj.h">
    </rect>
  </svg>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      objList: [
        {'x': 400, 'y': 100, 'w': 100, 'h': 100}, 
        {'x': 200, 'y': 200, 'w': 100, 'h': 100}, 
        {'x': 300, 'y': 300, 'w': 100, 'h': 100}
      ]
    }
  },
  watch: {
      displayMode: function() {
        console.log('displayMode')
      }
  },
  computed: {
    ...mapState([
        'displayMode'
      ])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.canvas {
  width: 100%;
  height: 100%;
  .bar {
    fill: steelblue;
  }
}
</style>
