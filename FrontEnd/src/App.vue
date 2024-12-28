<template>
  <div id="app" v-if="!loadingData">
    <el-menu class="el-menu-demo" mode="horizontal" background-color="#676767" text-color="#fff"
      :default-active="activeIndex" active-text-color="#ffd04b">
      <el-menu-item class='labelIcon' id="title" @click="handleTitleClick">
        {{ appName }}
      </el-menu-item>
      <!-- <el-tooltip class='labelIcon' v-for="(operation, i) in operationArray" :key="operation" :content="operation"
        effect="light">
        <el-menu-item :index="operation" @click="menuItemClick(operation)">
          {{ operation }}
        </el-menu-item>
      </el-tooltip> -->
    </el-menu>
    <!-- 侧边悬浮菜单 -->
    <el-menu class="el-menu-vertical-demo" :style="sidebarStyle" v-show="titleExpand"
      @mouseenter="handleSidebarMouseEnter" @mouseleave="handleSidebarMouseLeave" background-color="#f4f4f4">
      <!-- 新闻菜单项 -->
      <el-menu-item v-for="(news, index) in newsList" :key="index" :index="'1-' + (index + 1)"
        @mouseenter="expandItem(index)" @mouseleave="collapseItem(index)" @click="sideItemClick(index + 1)">
        <!-- 使用 el-card 显示新闻内容 -->
        <el-card class="news-card">
          <div class="menu-content">
            <!-- 新闻标题 -->
            <div class="news-title">{{ news.title }}</div>
            <!-- 鼠标悬停时显示第一句话 -->
            <div v-if="expandedItems[index]" class="news-preview">{{ news.preview }}</div>
          </div>
        </el-card>
      </el-menu-item>
    </el-menu>
    <div class="content-container">
      <div class="nodeView">
        <NewsNodeTree :cur_i_change="cur_i_change"></NewsNodeTree>
      </div>
      <div class="curveView">
        <NewsCurve :cur_i_change="cur_i_change"></NewsCurve>
      </div>
      <div class="textView">
        <NewsTextContent :jsonData="jsonData" :cur_i_change="cur_i_change"></NewsTextContent>
      </div>

    </div>
  </div>
</template>

<script>


import { getTabularDataset, getJsonData, getTextData, getRelationData, getEmoVal } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'

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
      appName: "LivingNews",
      // operationArray: ['News1', 'News2', 'News3'],
      operationArray: ['', '', ''],
      titleExpand: false,
      expandedItems: [], // 存储每个新闻项的展开状态
      sidebarfoldWidth: 400,
      sidebarExpandWidth: 600,
      sidebarWidth: 400,
      newsList: [
        { title: 'Global Warming Made Helene More Menacing, Researchers Say', preview: 'In cooler times, a similarly rare storm over the Southeast would have delivered less rain and weaker winds, a team of scientists concluded in an analysis.' },
        { title: 'Our Planet’s Twin Crises', preview: 'In her last newsletter for the Times, a Climate Forward reporter reflects on the intertwined problems of climate change and biodiversity loss.' },
        { title: 'When a Television Meteorologist Breaks Down on Air and Admits Fear', preview: 'John Morales, who has forecast weather for decades, went viral after choking up on air while discussing Hurricane Milton.' },
        { title: 'A ‘Miracle’: Plane Erupts in Flames Landing in Tokyo, but All Aboard Survive', preview: 'Japan Airlines said all 367 passengers and 12 crew members had safely evacuated the jet. But five crew members on a Japanese Coast Guard plane that collided with it were killed.' },
        // { title: '娱乐新闻：明星婚礼曝光', preview: '近日，某明星的婚礼照片曝光，引发了广泛的关注。' },
      ],
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
    // let textDataDeferObj = $.Deferred()
    let relationDataDeferObj = $.Deferred()
    let emoValDataDeferObj = $.Deferred()
    $.when(tabularDataDeferObj, jsonDataDeferObj, emoValDataDeferObj).then(function () {
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
    // getTextData(self.cur_news_i, function (processed_json_data) {
    //   sysDatasetObj.updateTextData(processed_json_data)
    //   textDataDeferObj.resolve()

    // })
    // getRelationData(self.cur_news_i, function (processed_json_data) {
    //   sysDatasetObj.updateRelationData(processed_json_data)
    //   relationDataDeferObj.resolve()

    // })
    getEmoVal(self.cur_news_i, function (processed_json_data) {
      //录制系统case的定制情感波动曲线
      // if (self.cur_news_i == 1) {
      //   var temp_emo_list = [-0.5, -0.6, -0.7, -0.8, -0.8, -0.4, -0.5, -0.4, -0.5, -0.2, -0.8, 0, -0.2, -0.3, -0.5, -0.4, -0.6, -0.2, -0.4, -0.3, -0.2, -0.3, -0.5, -0.1, 0, 0, -0.4, -0.2]
      //   processed_json_data = temp_emo_list
      // }
      sysDatasetObj.updateEmoFlatList(processed_json_data)
      emoValDataDeferObj.resolve()

    })






  },
  watch: {
    cur_news_i: function () {
      let vuethis = this;
      console.log("in change", this.cur_news_i)
      let jsonDataDeferObj = $.Deferred()
      // let textDataDeferObj = $.Deferred()
      let emoValDataDeferObj = $.Deferred()
      $.when(jsonDataDeferObj, emoValDataDeferObj).then(function () {
        vuethis.cur_i_change++
        console.log("cur_i_change!!", vuethis.cur_i_change)
      })
      getJsonData(this.cur_news_i, 1, function (processed_json_data) {
        sysDatasetObj.updateJsonData(processed_json_data)
        jsonDataDeferObj.resolve()
        vuethis.jsonData = processed_json_data
      })
      getEmoVal(this.cur_news_i, (processed_json_data) => {
        // console.log("cur_news_i in getEmoVal", this.cur_news_i)
        // if (this.cur_news_i == 1) {
        //   var temp_emo_list = [-0.5, -0.6, -0.7, -0.8, -0.8, -0.4, -0.5, -0.4, -0.5, -0.2, -0.8, 0, -0.2, -0.3, -0.5, -0.4, -0.6, -0.2, -0.4, -0.3, -0.2, -0.3, -0.5, -0.1, 0, 0, -0.4, -0.2]
        //   processed_json_data = temp_emo_list
        // }
        sysDatasetObj.updateEmoFlatList(processed_json_data)
        emoValDataDeferObj.resolve()

      })

      // getTextData(this.cur_news_i, function (processed_json_data) {
      //   sysDatasetObj.updateTextData(processed_json_data)
      //   textDataDeferObj.resolve()

      // })
    }
  },
  computed: {
    sidebarStyle() {
      return {
        width: this.sidebarWidth + 'px',
        position: 'fixed',
        top: '40px',  // 留出顶部空间，假设标题高度为 60px
        left: this.titleExpand ? '0' : '-350px',  // 侧边栏默认隐藏，通过左侧位置调整
        height: 'calc(100vh - 20px)',  // 侧边栏的高度留出顶部 60px（标题的高度）
        overflowY: 'auto',
        transition: 'left 0.3s ease, width 0.3s ease', // 平滑过渡
        zIndex: '9999', // 确保悬浮在最上层
      };
    },
  },
  methods: {
    handleTitleClick(event) {
      this.titleExpand = !this.titleExpand
    },
    handleSidebarMouseEnter() {
      // 鼠标进入侧边栏时展开所有新闻项并调整宽度
      this.sidebarWidth = this.sidebarExpandWidth; // 增加侧边栏宽度
      this.expandedItems = this.newsList.map(() => true); // 展开所有项
    },
    handleSidebarMouseLeave() {
      // 鼠标离开侧边栏时收起所有新闻项并恢复原始宽度
      this.sidebarWidth = this.sidebarfoldWidth; // 恢复侧边栏宽度
      this.expandedItems = this.newsList.map(() => false); // 收起所有项
    },
    expandItem(index) {
      // 鼠标进入单个新闻项时展开
      this.expandedItems = this.expandedItems.map((item, idx) => (idx === index ? true : item));
    },
    collapseItem(index) {
      // 鼠标离开单个新闻项时收起
      this.expandedItems = this.expandedItems.map((item, idx) => (idx === index ? false : item));
    },
    iconClass(operation) {
      alert(operation)
      return 'icon-' + operation
    },
    updateNewsList() {
      let vuethis = this;

    },
    sideItemClick(index) {
      let vuethis = this;

      vuethis.cur_news_i = index


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

  .el-menu-vertical-demo {
    width: 200px;
    position: fixed;
    top: 60px;
    /* 留出顶部空间，假设标题高度为 60px */
    left: -350px;
    /* 初始时隐藏侧边栏，位于左侧外面 */
    height: calc(100vh - 60px);
    /* 侧边栏的高度根据剩余的空间调整 */
    overflow-y: auto;
    z-index: 9999;
    /* 确保侧边栏浮动在最前面 */
    background-color: #f4f4f4;
    transition: left 0.3s ease, width 0.3s ease;
    /* 平滑过渡效果 */
  }

  .el-menu-vertical-demo .el-menu-item {
    padding: 0;
    /* 每个菜单项的上下内边距，控制高度 */
    display: block;
    /* 使每个菜单项显示为块级元素，避免重叠 */
    height: auto;
    /* 菜单项的高度根据内容自适应 */
  }

  .el-menu-vertical-demo .news-card {
    height: auto;
    /* 使卡片高度适应内容 */
    padding: 0px;
    /* 为卡片设置内边距 */
    overflow: hidden;
    /* 防止内容溢出 */
  }

  .el-menu-vertical-demo .news-title {
    font-weight: bold;
    font-size: 14px;
    text-align: left;
    word-wrap: break-word;
    /* 允许长单词换行 */
    white-space: normal;
    /* 允许文本换行 */
    overflow-wrap: break-word;
    line-height: 1.2;
    /* 设置较小的行间距，避免换行后的间距过大 */
    margin: 0;
    /* 去除默认的 margin，确保标题紧凑 */
    /* 允许文本在必要时换行 */
  }

  .el-menu-vertical-demo .news-preview {
    font-size: 10px;
    /* 设置新闻第一句话的字体大小为较小 */
    color: #888;
    margin-top: 5px;
    text-align: left;
    /* 预览内容靠左对齐 */
    /* 减少与标题之间的间距 */
    white-space: normal;
    /* 允许文本换行 */
    line-height: 1.4;
    /* 设置行间距，让文本更加易读 */
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
