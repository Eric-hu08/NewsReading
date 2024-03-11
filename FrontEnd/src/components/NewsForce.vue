<template>
  <div id="force-container"></div>

</template>

<script>
import { mapState, mapMutations } from 'vuex';
import * as d3 from "d3";

export default {
  name: 'NewsForce',
  props: {
    msg: String,

  },
  data() {
    return {
      marge: { top: 60, bottom: 60, left: 60, right: 60 },


      temp: 10,
      barWidth: 850,
      textWidth: 800,
      c_index: 0,

    }

  },
  watch: {
    displayMode: function () {
      console.log('displayMode')
    },

  },
  computed: {
    ...mapState([
      'displayMode'
    ])
  },
  mounted: function () {
    let vuethis = this
    vuethis.drawBarChart()

  },
  methods: {

    drawBarChart() {
      const width = 700;
      const height = 1000;
      const margin = 100;

      const color = d3.scaleOrdinal(d3.schemeCategory10);
      var c_array = window.sysDatasetObj.jsonData.children
      var node_list = [{ node: "T", type: 'T' }]
      var link_list = []
      //gen node and link

      for (var i = 0; i < c_array.length; i++) {
        var temp_node_name = c_array[i].type + c_array[i].index
        node_list.push({ node: temp_node_name, type: "C" })
        link_list.push({ source: 0, target: node_list.length - 1, value: 1 })
        var c_index = node_list.length - 1
        var e_array = c_array[i].children
        for (var j = 0; j < e_array.length; j++) {
          var temp_str = e_array[j].type.split(")")[0].split("_")
          temp_node_name = String(j) + "_" + String(temp_str[temp_str.length - 1])
          node_list.push({ node: temp_node_name, type: e_array[j].type })
          // console.log("index", c_index, node_list.length - 1, temp_node_name)
          link_list.push({ source: c_index, target: node_list.length - 1, value: 1 })

        }

      }
      console.log("node and link", node_list, link_list)
      const nodes = [
        { node: 'A', },
        { node: 'B', },
        { node: 'C', },
        { node: 'D', },
        { node: 'E', }
      ]
      // const nodes = [
      //   { node: 'A', value: 79 },
      //   { node: 'B', value: 15 },
      //   { node: 'C', value: 24 },
      //   { node: 'D', value: 44 },
      //   { node: 'E', value: 125 },
      //   { node: 'F', value: 22 },
      //   { node: 'G', value: 20 },
      //   { node: 'H', value: 64 },
      //   { node: 'I', value: 69 },
      //   { node: 'J', value: 2 },
      //   { node: 'K', value: 8 },
      //   { node: 'L', value: 40 },
      //   { node: 'M', value: 26 },
      //   { node: 'N', value: 69 },
      //   { node: 'O', value: 77 },
      //   { node: 'P', value: 17 },
      //   { node: 'Q', value: 1 },
      //   { node: 'R', value: 58 },
      //   { node: 'S', value: 63 },
      //   { node: 'T', value: 91 },
      //   { node: 'U', value: 29 },
      //   { node: 'V', value: 10 },
      //   { node: 'W', value: 23 },
      //   { node: 'X', value: 2 },
      //   { node: 'Y', value: 20 },
      //   { node: 'Z', value: 1 },
      // ];

      const links = [
        { source: 0, target: 4, value: 3 },
        // { source: 4, target: 8, value: 3 },
        // { source: 8, target: 14, value: 3 },
        // { source: 14, target: 20, value: 3 },
        { source: 0, target: 1, value: 1 },
        { source: 1, target: 2, value: 1 },
        { source: 2, target: 3, value: 1 },
        // { source: 3, target: 4, value: 1 },
        // { source: 4, target: 5, value: 1 },
        // { source: 5, target: 6, value: 1 },
        // { source: 6, target: 7, value: 1 },
        // { source: 7, target: 8, value: 1 },
        // { source: 8, target: 9, value: 1 },
        // { source: 9, target: 10, value: 1 },
        // { source: 10, target: 11, value: 1 },
        // { source: 11, target: 12, value: 1 },
        // { source: 12, target: 13, value: 1 },
        // { source: 13, target: 14, value: 1 },
        // { source: 14, target: 15, value: 1 },
        // { source: 15, target: 16, value: 1 },
        // { source: 16, target: 17, value: 1 },
        // { source: 17, target: 18, value: 1 },
        // { source: 18, target: 19, value: 1 },
        // { source: 19, target: 20, value: 1 },
        // { source: 20, target: 21, value: 1 },
        // { source: 21, target: 22, value: 1 },
        // { source: 22, target: 23, value: 1 },
        // { source: 23, target: 24, value: 1 },
        // { source: 24, target: 25, value: 1 },
        // { source: 16, target: 15, value: 2 },
        // { source: 17, target: 16, value: 2 },
        // { source: 18, target: 17, value: 2 },
        // { source: 19, target: 18, value: 2 }
      ];
      // console.log("node link", nodes, links)
      color.domain([0, node_list.length]);

      const sim = d3.forceSimulation(node_list);

      sim.force("center", d3.forceCenter());

      // console.log(sim.nodes());

      const svg = d3.select("#force-container").append("svg").attr("width", width).attr("height", height);
      const chart = svg.append("g").attr("transform", `translate(${[margin / 2 + width / 2, margin / 2 + height / 2]})`);

      sim.force("link", d3.forceLink(link_list).iterations(15));
      sim.force("manybody", d3.forceManyBody().strength(1))
      sim.force("collide", d3.forceCollide(20));

      sim.on("tick", redraw);

      // Dragging behavior
      const nodeDragged = d3.drag()
        .on('drag', function (d) {
          d.x = d3.event.x;
          d.y = d3.event.y;
          console.log(sim.alpha())
        })
        .on('start', function () {
          if (sim.alpha() <= sim.alphaMin()) {
            sim.restart();
          }
          sim.alphaTarget(sim.alphaMin() + .1)
        })
        .on('end', () => sim.alphaTarget(0));

      draw();
      function colorf(d) {
        console.log("d color", d.type)
        console.log("d color true", d.type.indexOf('L'))

        if (d.type.indexOf('T') != -1) {
          return "#aaaaaa"
          // return "#dfe4ea"
        }
        else if (d.type.indexOf('E') == -1) {
          return "#ffffff"
        }
        else {
          if (d.type.indexOf('S') != -1) {
            return "#8dd3c7"
          }
          else if (d.type.indexOf('P') != -1) {
            return "#ffffb3"
          }
          else if (d.type.indexOf('O') != -1) {
            return "#bebada"
          }
          else {
            return "#fb8072"
          }

        }

      }
      function draw() {
        chart.selectAll('line')
          .data(link_list).enter()
          .append('line')
          .attr("x1", d => d.source.x)
          .attr("x2", d => d.target.x)
          .attr("y1", d => d.source.y)
          .attr("y2", d => d.target.y)
          .style("fill", 'none')
          .style("stroke", 'black')
          .style("stroke-width", d => d.value * d.value)

        chart.selectAll('g.fnode')
          .data(node_list).enter()
          .append("g").attr("class", 'fnode')
          .attr("transform", d => `translate(${[d.x, d.y]})`)
          .each(function (d, i) {
            d3.select(this).append("circle")
              .attr("r", 15)
              .style("fill", colorf(d))
              .style("stroke", 'black')
            d3.select(this).append("text")
              .text(d => d.node)
              .attr("text-anchor", "middle")
          })
          .call(nodeDragged);

      }

      function redraw() {
        chart.selectAll('g.fnode')
          .attr("transform", d => `translate(${[d.x, d.y]})`);

        chart.selectAll('line')
          .attr("x1", d => d.source.x)
          .attr("x2", d => d.target.x)
          .attr("y1", d => d.source.y)
          .attr("y2", d => d.target.y)
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

.fnode text {
  font: 10px sans-serif;
  font-weight: bold;
  pointer-events: none;
}
</style>
