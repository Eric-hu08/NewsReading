<template>
  <el-slider class="evi-slider" :max="5" :min="0" v-model="evi_sum" :step="1" show-stops v-if="elShow(el_show)" />
  <span :id="'E' + e_index" class="evi-span">
    <transition-group name="slide">
      <mark v-for="(item, index) in evi_sum_list" :key="item.id">
        {{ item.text }}<span>&nbsp</span>
      </mark>
    </transition-group>
  </span>
  <span>&nbsp</span>

</template>

<script>
import { at, sum } from 'lodash';
import { mapState, mapMutations } from 'vuex';
import { nextTick } from 'vue';


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
      // evi_sum_list: [
      //   { id: this.generateUniqueId(), text: 'data1' },
      //   { id: this.generateUniqueId(), text: 'data2' },
      //   { id: this.generateUniqueId(), text: 'data3' },
      // ],
      evi_sum_list: [],



    }

  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },
    evi_sum_exter: function () {
      this.evi_sum = this.evi_sum_exter
    },
    evi_sum: {
      handler(newSum, oldSum) {
        // 使用Vue.set来触发表达式更新，这里我们添加一个不会影响展示的临时属性
        // this.evi_sum_list = [...this.evi_sum_list]
        // nextTick(() => {
        // 这里可以放一些在DOM更新后需要执行的逻辑
        var evi_sum;
        var sum_str;


        if (newSum > oldSum) {
          evi_sum = newSum
          var attr_str = "diffT" + (evi_sum - 1)
        }
        else {
          evi_sum = newSum
          var attr_str = "diffT" + (evi_sum)
        }
        if (evi_sum == 0) {
          sum_str = "name"
        }
        else {
          sum_str = "sum" + (evi_sum - 1)
        }

        var diff_list = this.evi[attr_str]
        console.log("num sum str", evi_sum, sum_str)


        var list_i_del = 0
        if (newSum > oldSum) {
          var nxt_str = this.evi[sum_str]
          var nxt_str_list = nxt_str.split(" ")
          for (var i = 0; i < diff_list.length; i++) {
            var tag = diff_list[i].tag
            if (tag == "insert") {
              var start_i = diff_list[i].i1 + list_i_del
              for (var j = diff_list[i].j1; j < diff_list[i].j2; j++) {
                this.evi_sum_list.splice(start_i, 0, { id: this.generateUniqueId(), text: nxt_str_list[j] })
                start_i++;
                list_i_del++;
              }
            }
            else if (tag == "equal") {
              var start_i = diff_list[i].i1 + list_i_del
              for (var j = diff_list[i].j1; j < diff_list[i].j2; j++) {
                // console.log("cur_id", this.evi_sum_list, start_i, this.evi_sum_list[start_i])
                var cur_id = this.evi_sum_list[start_i].id
                this.evi_sum_list.splice(start_i, 1, { id: cur_id, text: nxt_str_list[j] })
                start_i++;
              }

            }
            else if (tag == "delete") {
              var start_i = diff_list[i].i1 + list_i_del
              for (var j = diff_list[i].i1; j < diff_list[i].i2; j++) {
                this.evi_sum_list.splice(start_i, 1)
                list_i_del--;
              }

            }
            else if (tag == "replace") {
              var start_i = diff_list[i].i1 + list_i_del
              for (var j = diff_list[i].i1; j < diff_list[i].i2; j++) {
                this.evi_sum_list.splice(start_i, 1)
                list_i_del--;
              }
              for (var j = diff_list[i].j1; j < diff_list[i].j2; j++) {
                this.evi_sum_list.splice(start_i, 0, { id: this.generateUniqueId(), text: nxt_str_list[j] })
                start_i++;
                list_i_del++;
              }
            }
          }
          var len = this.evi_sum_list.length
          this.evi_sum_list.splice(len - 1, 1, { id: this.evi_sum_list[len - 1].id, text: this.evi_sum_list[len - 1].text + "." })
        }
        else {
          var cur_str = this.evi[sum_str]
          var cur_str_list = cur_str.split(" ")
          for (var i = 0; i < diff_list.length; i++) {
            var tag = diff_list[i].tag
            if (tag == "insert") {
              var start_i = diff_list[i].j1 + list_i_del
              for (var j = diff_list[i].j1; j < diff_list[i].j2; j++) {
                this.evi_sum_list.splice(start_i, 1)
                list_i_del--;
              }
            }
            else if (tag == "equal") {
              start_i = diff_list[i].j1 + list_i_del
              for (var j = diff_list[i].i1; j < diff_list[i].i2; j++) {
                var start_id = this.evi_sum_list[start_i].id
                this.evi_sum_list.splice(start_i, 1, { id: start_id, text: cur_str_list[j] })
                start_i++;
              }


            }
            else if (tag == "delete") {
              var start_i = diff_list[i].j1 + list_i_del
              for (var j = diff_list[i].i1; j < diff_list[i].i2; j++) {
                this.evi_sum_list.splice(start_i, 0, { id: this.generateUniqueId(), text: cur_str_list[j] })
                start_i++;
                list_i_del++;
              }

            }
            else if (tag == "replace") {
              var start_i = diff_list[i].j1 + list_i_del
              for (var j = diff_list[i].j1; j < diff_list[i].j2; j++) {
                this.evi_sum_list.splice(start_i, 1)
                list_i_del--;
              }
              for (var j = diff_list[i].i1; j < diff_list[i].i2; j++) {
                this.evi_sum_list.splice(start_i, 0, { id: this.generateUniqueId(), text: cur_str_list[j] })
                start_i++;
                list_i_del++;
              }
            }
          }
          var len = this.evi_sum_list.length
          this.evi_sum_list.splice(len - 1, 1, { id: this.evi_sum_list[len - 1].id, text: this.evi_sum_list[len - 1].text + "." })
        }

        // console.log("diff_dict", index, attr_str)
        // if (newSum > oldSum) {
        //   var id = this.generateUniqueId()
        //   this.evi_sum_list.push({ text: "test", id: id })
        // }
        // else {
        //   this.evi_sum_list.splice(0, 1, { text: "replace", id: this.evi_sum_list[0].id })
        // }


        // });
        setTimeout(() => {
          this.$emit('updateEviMark')
        }, 2010)

      },
      // immediate: true,

    }

  },
  computed: {
    ...mapState([
      'displayMode',
      'eNodeYControlArray'
    ]),
    // evi_sum_list: function () {
    //   var evi_sum_content = this.sumContent(this.evi, this.evi_sum, this.evi_sum_exter)
    //   var evi_sum_list = evi_sum_content.split(" ")
    //   console.log("evi_sum_list", evi_sum_list)
    //   return evi_sum_list.map((word, index) => ({ word, added: this.ifAdd(index, this.evi_sum), deleted: this.ifDelete(index, this.evi_sum) }));
    // }
  },
  beforeMount: function () {

    // console.log("cnodename", this.cNodeName)

  },
  updated() {
    this.$emit('updateEviMark')
  },
  mounted: function () {
    var evi_sum_content = this.sumContent(this.evi, this.evi_sum, this.evi_sum_exter)
    console.log("evi_sum_content: ", evi_sum_content)
    var evi_sum_list = evi_sum_content.split(" ")
    for (var i = 0; i < evi_sum_list.length; i++) {
      var id = this.generateUniqueId()
      if (i == evi_sum_list.length - 1) {
        this.evi_sum_list.push({ id: id, text: evi_sum_list[i] + "." });
      }
      else {
        this.evi_sum_list.push({ id: id, text: evi_sum_list[i] });
      }

    }

    console.log("mount evi sum list", this.evi_sum_list)
    setTimeout(() => {
      this.$emit('updateEviMark')
    }, 10)


  },
  methods: {
    generateUniqueId() {
      return `${Date.now()}${Math.floor(Math.random() * 1000000)}`;
    },
    elShow() {
      if (this.el_show == 1) {
        return true
      }
      else {
        return false
      }
    },
    sumContent(evi, evi_sum, evi_sum_exter) {
      console.log("sumContext: evi: ", evi, evi_sum, evi_sum_exter, this.el_show)
      //根据概括层级获取内容
      if (this.el_show == 0) {
        evi_sum = evi_sum_exter
      }
      if (evi_sum == 0) {
        return (evi.name)
      }
      else {
        var sum_str = "sum" + (evi_sum - 1)
        return (evi[sum_str])
      }
    },






  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style lang="less">
.evi-span {
  // display: inline-block;
  white-space: normal;
  word-wrap: break-word;

  mark {
    background: white;
  }

  mark:hover {
    background: grey;
  }





}

.slide-enter-active {
  transition: all 1.5s ease;
  background-color: green !important;
}


.slide-leave-active {
  transition: all 1.5s ease;
  background-color: red !important;
}

.slide-enter-from {
  // transform: translateX(20px);
  opacity: 0;
  // background-color: green;
}

.slide-enter-to {
  // transform: translateX(0);
  opacity: 1;
  // background-color: red;
}



.slide-leave-from {
  opacity: 1;
  // background-color: red;
  // transform: translateX(20px);
}


.slide-leave-to {
  // transform: translateX(20px);
  opacity: 0;
  // background-color: red;
}




// @keyframes fadeIn {
//   from {
//     opacity: 0;
//     background-color: #42b983;
//   }

//   to {
//     opacity: 1;
//     background-color: white;
//   }
// }

// @keyframes fadeOut {
//   from {
//     opacity: 1;
//     background-color: red;
//   }

//   to {
//     opacity: 0;
//     background-color: white;
//   }
// }

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
</style>
