<template>
  <text class="eText" :dx="e_text_dx">{{ "hello" }}
  </text>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'NewsEText',
  props: {
    e_content: String,

  },
  data() {
    return {
      marge: { top: 10, bottom: 60, left: 850, right: 60 },

      eCRInter: 20,
      eTextWidth: 590,
      ebarHeight: 50,
      ebarWidth: 600,
      e_text_dy: -10,  //不管用
      e_text_dx: 5,



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
    this.changeEText()
    // console.log("e_dict", this.e_dict)

  },
  methods: {




    changeEText() {
      let vuethis = this

      // console.log("e select ", d3.select(vuethis.$el))
      d3.select(vuethis.$el).text("")
      // console.log("d3 select changeetset", d3.select(vuethis.$el).select(".eText")._groups[0][0])
      // if (d3.select(vuethis.$el).select(".eText")._groups[0][0] == undefined) {
      //   d3.select(vuethis.$el).select(".EviT").append("text")
      //     .attr("class", "eText")
      //     .attr("dx", vuethis.e_text_dx)
      //   console.log("d3 select changeetset", d3.select(vuethis.$el).select(".EviT"))
      // }

      d3.select(vuethis.$el).call(wrapText, vuethis.e_content, vuethis.eTextWidth)




      function wrapText(text, getcontent, width) {
        // console.log("getcontent: ", getcontent)
        var content = getcontent

        var words = content.split(/\s+/);
        var lineHeight = 1; // 行高
        var line = [];
        var lineNumber = 0;
        var tspan = text.append("tspan")
          .attr("x", 0)
          .attr("y", vuethis.e_text_dy)
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
              .attr("y", vuethis.e_text_dy)
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

text.enodeText {
  font: 8px sans-serif;
  font-weight: bold;
  pointer-events: none;
}
</style>
