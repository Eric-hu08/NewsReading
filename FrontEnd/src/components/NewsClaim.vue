<template>

  <g class="Claim" :transform="claim_tran()" :id="('C' + c_node_data.index)">
    <circle cx="0" cy="0" :r="cNodeR" fill="blue" @click="cNodeClick()" opacity="0.3">

    </circle>
    <text text-anchor="middle" class="nodeText" dy="3">{{ cNodeName }}</text>
  </g>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'NewsClaim',
  props: {
    msg: String,
    barHeight: Number,
    c_node_data: Object,
    cNodeR: Number,
  },
  data() {
    return {
      marge: { top: 60, bottom: 60, left: 60, right: 60 },
      temp: 10,
      barWidth: 850,
      textWidth: 800,
      c_index: 0,
      cNodeName: "C",

    }

  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },
    f_y_change: function () {
      // console.log("y change")
      // this.$forceUpdate()

    },
    b_value: function () {

    }
  },
  computed: {
    ...mapState([
      'displayMode'
    ])
  },
  beforeMount: function () {
    this.cNodeName = "C" + String(this.c_node_data.index)
    console.log("cnodename", this.cNodeName)

  },
  mounted: function () {
    let vuethis = this

    vuethis.c_index = vuethis.c_node_data.index
    // this.drawCNode()
  },
  methods: {
    cNodeClick() {
      let vuethis = this
      vuethis.$store.commit("editCNodeUnfoldArray", vuethis.c_index - 1)
      var unfold_state = vuethis.$store.state.cNodeUnfoldArray[vuethis.c_index - 1]
      if (unfold_state == 1) {// unfold the node
        console.log("change cny,", vuethis.c_node_data.children.length + 1)
        vuethis.$store.commit('editChangeCIndex', vuethis.c_index)
        vuethis.$store.commit('editFFold', 1)
        vuethis.$store.commit('editCNodeYArray', { index: vuethis.c_index - 1, value: vuethis.c_node_data.children.length + 1 })


        vuethis.drawCNode()
      }
      else {//fold the node
        var node_detail_id = "c" + vuethis.c_index
        vuethis.$store.commit('editChangeCIndex', vuethis.c_index)
        vuethis.$store.commit('editFFold', 2)
        vuethis.$store.commit('editCNodeYArray', { index: vuethis.c_index - 1, value: 1 })

        document.getElementById(node_detail_id).remove()

      }

    },
    claim_tran() {
      return "translate(" + this.marge.top + "," + this.marge.left + ")"
    },
    drawCNode() {
      let vuethis = this;


      var barHeight = vuethis.barHeight
      var barWidth = vuethis.barWidth
      var textWidth = vuethis.textWidth
      var nodeR = 3

      var svg = d3.select(vuethis.$el)
      var g1 = svg.append("g").attr("class", "nodeDetail").attr("id", "c" + vuethis.c_index)
      var diagonal = d3.line()
        .x(function (d) { return d.x; })
        .y(function (d) { return d.y; })
        .curve(d3.curveStepBefore);
      var node_root
      node_root = d3.hierarchy(vuethis.c_node_data);
      node_root.x0 = 0;
      node_root.y0 = 0;
      update(node_root);
      function update(source) {
        var nodes = node_root.descendants();

        var height = Math.max(2000, nodes.length * barHeight)    //height of g not less than 1000
        var duration = 400;
        d3.select("svg").transition()
          .duration(duration)
          .attr("height", height);

        d3.select(self.frameElement).transition()
          .duration(duration)
          .style("height", height + "px");
        var index = -1;
        node_root.eachBefore(function (n) {
          n.x = ++index * barHeight;
          n.y = (n.depth + 1) * 20;
        });
        var i = 0
        // Update the nodes…
        g1.selectAll(".node").remove()
        var node = g1.selectAll(".node")
          .data(nodes, function (d) { return d.id || (d.id = ++i); });

        var nodeEnter = node.enter().append("g")
          .attr("class", "node")
          .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
          .style("opacity", 0);
        // Enter any new nodes at the parent's previous position.
        nodeEnter.filter(function (d) {
          if (d.data.type != "nono") {
            return true
          }
        }).append("rect")
          .attr("y", -barHeight / 2)
          .attr("height", barHeight)
          .attr("width", barWidth)
          .style("fill", color)
          .on("click", click);

        //add node text
        nodeEnter.filter(function (d) {
          if (d.data.type != "nono") {
            return true
          }
        }).append("text")
          .attr("id", "sent")
          // .attr("dy", 3.5)
          .attr("dx", 50)
          .each(function (d) {
            d3.select(this).call(wrapText, d.data.name, textWidth)
            // let f_1 = false
            // if (vuethis.less_array.indexOf(d.id) != -1) {
            //     f_1 = true
            // }
            // if (vuethis.b_value ^ f_1) {
            //     // if(d.data.type!="nono")
            //     d3.select(this).call(wrapText, d.data.name_less, textWidth)
            // }
            // else {
            //     d3.select(this).call(wrapText, d.data.name, textWidth)
            // }
          })

        //add node type name
        nodeEnter.filter(function (d) {
          if (d.data.type != "nono") {
            return true
          }
        })
          .append("text")
          .attr("dy", -8)
          .attr("dx", 5.5)
          .text(function (d) {
            if (d.data.type == "nono") {
              return ""
            }
            if (d.data.type == "title") {
              return d.data.type
            }
            else if (d.data.type.indexOf('E') == -1) {
              return "C" + "_" + d.data.index;
            }
            else {
              var end_i = d.data.type.indexOf(')')
              return "E" + d.data.type.slice(end_i - 2, end_i);
            }

          });
        // Transition nodes to their new position.
        nodeEnter.transition()
          .duration(duration)
          .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; })
          .style("opacity", 1);

        node.transition()
          .duration(2000)
          .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; })
          .style("opacity", 1)
          .select("rect")
          .style("fill", color);
        // Transition exiting nodes to the parent's new position.
        node.exit().transition()
          .duration(2000)
          .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
          .style("opacity", 0)
          .remove();

        // Update the links…
        var link = g1.selectAll(".link")
          .data(node_root.links(), function (d) { return d.target.id; });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
          .attr("class", "link")
          .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return diagonal([{ x: o.y, y: o.x }, { x: o.y, y: o.x }]);
          })
          .transition()
          .duration(duration)
          .attr("d", function (d) {
            return diagonal([{ x: d.source.y, y: d.source.x }, { x: d.target.y, y: d.target.x }]);
          });

        // Transition links to their new position.
        link.transition()
          .duration(duration)
          .attr("d", function (d) {
            return diagonal([{ x: d.source.y, y: d.source.x }, { x: d.target.y, y: d.target.x }]);
          });

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
          .duration(duration)
          .attr("d", function (d) {
            var o = { x: source.x, y: source.y };
            return diagonal([{ x: o.y, y: o.x }, { x: o.y, y: o.x }]);
          })
          .remove();

        // Stash the old positions for transition.
        node_root.each(function (d) {
          d.x0 = d.x;
          d.y0 = d.y;
        });

      }
      // Toggle children on click.
      function click(d) {
        // console.log("click id", d.id)
        // alert(d.id)
        // let index_i = vuethis.less_array.indexOf(d.id)
        // if (index_i != -1) {
        //     vuethis.less_array.splice(index_i, 1)
        // }
        // else {
        //     vuethis.less_array.push(d.id)
        // }

        if (d.children) {
          d._children = d.children;
          d.children = null;
          vuethis.$store.commit('editChangeCIndex', vuethis.c_index)
          vuethis.$store.commit('editFFold', 2)
          vuethis.$store.commit('editCNodeYArray', { index: vuethis.c_index - 1, value: 1 })

        } else {
          d.children = d._children;
          d._children = null;
          vuethis.$store.commit('editChangeCIndex', vuethis.c_index)
          vuethis.$store.commit('editFFold', 1)
          vuethis.$store.commit('editCNodeYArray', { index: vuethis.c_index - 1, value: vuethis.c_node_data.children.length + 1 })


          // vuethis.drawCNode()
        }
        update(d);

      }
      function color(d) {
        if (d.data.type == "title") {
          return "#dfe4ea"
        }
        else if (d.data.type.indexOf('E') == -1) {
          return "#ffffff"
        }
        else {
          if (d.data.type.indexOf('S') != -1) {
            return "#8dd3c7"
          }
          else if (d.data.type.indexOf('P') != -1) {
            return "#ffffb3"
          }
          else if (d.data.type.indexOf('O') != -1) {
            return "#bebada"
          }
          else {
            return "#fb8072"
          }

        }

      }
      // 自定义函数，实现文本自动换行
      function wrapText(text, getcontent, width) {
        // console.log("getcontent: ", getcontent)
        var content = getcontent

        var words = content.split(/\s+/);
        var lineHeight = 1; // 行高
        var line = [];
        var lineNumber = 0;
        var tspan = text.append("tspan")
          .attr("x", 0)
          .attr("y", -5)
          .attr("dy", 0);

        words.forEach(function (word) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan")
              .attr("x", 5)
              .attr("y", -5)
              // .attr("dy", 3)
              .attr("dy", lineHeight * ++lineNumber + "em")
              .text(word)
            // .style("text-anchor", "middle")
          }
        });
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

text.nodeText {
  font: 10px sans-serif;
  font-weight: bold;
  pointer-events: none;
}
</style>
