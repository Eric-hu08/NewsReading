<template>
  <div id="app" v-if="!loadingData">
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#676767"
        text-color="#fff"
        :default-active="activeIndex"
        active-text-color="#ffd04b">
        <el-menu-item class='labelIcon' id="title">
          {{appName}}
        </el-menu-item>
        <el-tooltip class='labelIcon' v-for="operation in operationArray" :key="operation" :content="operation" effect="light">
          <el-menu-item :index="operation">
            {{operation}}
          </el-menu-item>
        </el-tooltip>
    </el-menu>
    <div class = "content-container">
      <NewsMP></NewsMP>
    </div>
  </div>
</template>

<script>

import HelloWorld from './components/HelloWorld.vue'
import { getTabularDataset } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
import NewsMP from './components/NewsMP.vue'

export default {
  name: 'app',
  components: {
    HelloWorld,
    NewsMP
},
  data() {
    return {
      appName: "News Reader",
      operationArray: ['#operation1', '#operation2'],
      activeIndex: '',
      loadingData: true
    }
  },
  beforeMount: function() {
    let self = this
    window.sysDatasetObj = new Dataset()
    let tabularDataDeferObj = $.Deferred()
    $.when(tabularDataDeferObj).then(function() {
      self.loadingData = false
    })
    let tabularDataList = ['*']
    // initialize the tabular dataset
    getTabularDataset(tabularDataList, function(processed_tabular_datalist_str) {
      let processed_tabular_datalist = JSON.parse(processed_tabular_datalist_str)
      console.log('processed_tabular_datalist', processed_tabular_datalist)
      sysDatasetObj.updateTabularDatasetList(processed_tabular_datalist)
      tabularDataDeferObj.resolve()
    })
  },
  methods: {
    iconClass(operation) {
      return 'icon-' + operation
    }
  }
}
</script>

<style lang="less">
html {
  font-size: 100%;
}
@menu-height: 2.5rem;
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .icon {
        color: #dadada !important;
      }
    }
  }
  .labelIcon {
    font-size: 1rem;
  }
  .content-container {
    position: absolute;
    top: @menu-height;
    left: 0%;
    bottom: 0%;
    right: 0%;
  }
}
</style>
