<template>
  <div id="app" v-if="!loadingData">
    <el-menu class="el-menu-demo" mode="horizontal" background-color="#676767" text-color="#fff"
      :default-active="activeIndex" active-text-color="#ffd04b">
      <el-menu-item class='labelIcon' id="title">
        {{ appName }}
      </el-menu-item>
      <el-tooltip class='labelIcon' v-for="(operation, i) in operationArray" :key="operation" :content="operation"
        effect="light">
        <el-menu-item :index="operation" @click="menuItemClick(operation)">
          {{ operation }}
        </el-menu-item>
      </el-tooltip>
    </el-menu>
    <div class="content-container">
      <div class="nodeView">
        <NewsNodeTree></NewsNodeTree>
      </div>
      <div class="curveView">
        <NewsCurve></NewsCurve>
      </div>
      <div class="textView">
        <NewsTextContent :jsonData="jsonData"></NewsTextContent>
      </div>

    </div>
  </div>
</template>

<script>


import { getTabularDataset, getJsonData, getTextData, getRelationData, getEmoVal } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'

import NewsS from './components/NewsS.vue'
import NewsTextContent from './components/NewsTextContent.vue';
import NewsNodeTree from './components/NewsNodeTree.vue';
import NewsCurve from './components/NewsCurve.vue';

export default {
  name: 'app',
  components: {

    NewsTextContent,
    NewsNodeTree,
    NewsCurve
  },
  data() {
    return {
      appName: "News Reader",
      operationArray: ['News1', 'News2', 'News3', 'News4', 'News5', 'News6', 'News7', 'T7', 'T8'],
      cur_news_i: 1,
      cur_i_change: 1,
      activeIndex: '',
      loadingData: true,
      jsonData: null,
      f_y_change: 0,



    }
  },
  beforeMount: function () {
    let self = this
    window.sysDatasetObj = new Dataset()
    let tabularDataDeferObj = $.Deferred()
    let jsonDataDeferObj = $.Deferred()
    let textDataDeferObj = $.Deferred()
    let relationDataDeferObj = $.Deferred()
    let emoValDataDeferObj = $.Deferred()
    $.when(tabularDataDeferObj, jsonDataDeferObj, textDataDeferObj, relationDataDeferObj, emoValDataDeferObj).then(function () {
      self.loadingData = false
    })
    let tabularDataList = ['*']
    // initialize the tabular dataset
    getTabularDataset(tabularDataList, function (processed_tabular_datalist_str) {
      let processed_tabular_datalist = JSON.parse(processed_tabular_datalist_str)
      console.log('processed_tabular_datalist', processed_tabular_datalist)
      sysDatasetObj.updateTabularDatasetList(processed_tabular_datalist)
      tabularDataDeferObj.resolve()
    })

    getJsonData(self.cur_news_i, 1, function (processed_json_data) {
      sysDatasetObj.updateJsonData(processed_json_data)
      jsonDataDeferObj.resolve()
      self.jsonData = processed_json_data
    })
    getTextData(self.cur_news_i, function (processed_json_data) {
      sysDatasetObj.updateTextData(processed_json_data)
      textDataDeferObj.resolve()

    })
    getRelationData(self.cur_news_i, function (processed_json_data) {
      sysDatasetObj.updateRelationData(processed_json_data)
      relationDataDeferObj.resolve()

    })
    getEmoVal(self.cur_news_i, function (processed_json_data) {
      sysDatasetObj.updateEmoFlatList(processed_json_data)
      emoValDataDeferObj.resolve()

    })






  },
  watch: {
    cur_news_i: function () {
      let vuethis = this;
      console.log("in change", this.cur_news_i)
      let jsonDataDeferObj = $.Deferred()
      let textDataDeferObj = $.Deferred()
      $.when(jsonDataDeferObj, textDataDeferObj).then(function () {
        vuethis.cur_i_change++
      })
      getJsonData(this.cur_news_i, 1, function (processed_json_data) {
        sysDatasetObj.updateJsonData(processed_json_data)
        jsonDataDeferObj.resolve()
      })
      getTextData(this.cur_news_i, function (processed_json_data) {
        sysDatasetObj.updateTextData(processed_json_data)
        textDataDeferObj.resolve()

      })
    }
  },
  methods: {
    iconClass(operation) {
      alert(operation)
      return 'icon-' + operation
    },
    menuItemClick(operation) {
      let vuethis = this;

      var index_News = vuethis.operationArray.indexOf(operation)
      // console.group(index_News)
      vuethis.cur_news_i = index_News + 1
      console.log("event", vuethis.cur_news_i)
    }
  }
}
</script>

<style lang="less">
html {
  font-size: 100%;
  overflow-y: hidden;
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

    --el-menu-horizontal-height:@menu-height+1;

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

    .nodeView {
      position: absolute;
      top: 0%;
      left: 0%;
      bottom: 0%;
      right: 95%;
    }

    .curveView {
      position: absolute;
      top: 0%;
      left: 5%;
      bottom: 0%;
      right: 85%;
    }

    .textView {
      position: absolute;
      top: 0%;
      left: 15%;
      bottom: 0%;
      right: 0%;
    }
  }
}
</style>
