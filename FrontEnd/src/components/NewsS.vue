<template>
    <div class="hello">



        <div class="NewsText">
            <h3>{{ NewsTitle }}</h3>
            <span class="NewsOri" style="text-align: left;display: inline-block;">{{ NewsOri }}</span>
            <!-- <p>
                <span v-for="(sen, index) in sen_array" :key="index">{{ sen + ". " }}</span>
            </p> -->

        </div>
        <div class="block">

            <!-- <el-slider class="MpSlider" v-model="mp_level_input" :step="10" show-stops show-input>
            </el-slider>
            <el-button type="primary" round @click="beginMp" class="MpButton"
                style="transform: translate(-20,0);">Generate</el-button> -->
        </div>
        <div class="MpShow" v-loading="LoadingMp" element-loading-text="Waiting GPT answering">
            <el-switch v-model="b_value" active-color="#13ce66" inactive-color="#ff4949" class="showButton" @click="b_click"
                active-text="coarse-grained" inactive-text="origin">
            </el-switch>
            <!-- <span class="MpSpan" style="white-space:pre-wrap;">{{ MpContent }}</span> -->
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import { getGPTMp, getGPTExt } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
export default {
    name: 'HelloWorld',
    props: {
        msg: String,
        cur_i_change: Number,
        // MpContent: String,
    },
    data() {
        return {
            new_input: '',
            mp_level_input: 0,
            MpContent: 'hello',
            LoadingMp: false,
            sen_array: [],
            NewsOri: '',
            NewsTitle: '',
            b_value: false,
            less_array: [],
        }
    },
    mounted: function () {
        // alert("before mounted")
        this.draw_tree()
        this.loadNews()
    },
    watch: {
        cur_i_change: function () {
            d3.select(".MpShow").select("svg").remove()

            this.draw_tree()
            this.loadNews()
        },
        displayMode: function () {
            console.log('displayMode')
        },
        textarea2: function () {
            console.log('test changed!')
            console.log(this.textarea2)
        },
        b_value: function () {
            d3.select(".MpShow").select("svg").remove()
            this.less_array = []
            this.draw_tree()

        },
        less_array: function () {

            d3.select(".MpShow").select("svg").remove()
            this.draw_tree()
        }
    },
    computed: {
        ...mapState([
            'displayMode'
        ])
    },

    methods: {
        b_click() {
            alert("click!")
            this.b_click = !this.b_click
            d3.select(".MpShow").select("svg").remove()
            this.draw_tree()

        },
        loadNews() {
            // let jsonData = window.sysDatasetObj.jsonData
            // function getNames(obj) {
            //     var names = [];
            //     for (var key in obj) {
            //         if (typeof obj[key] === "object") {
            //             names = names.concat(getNames(obj[key]));
            //         }
            //         if (key === "name") {
            //             names.push(obj[key]);
            //         }
            //     }
            //     return names;
            // }
            // let sen_list = getNames(jsonData)
            // console.log("sen_list", sen_list)
            // // let new_content = sen_list.join(".")
            // this.sen_array = sen_list
            let textData = window.sysDatasetObj.textData
            this.NewsTitle = textData[0]
            this.NewsOri = textData.slice(1, textData.length).join(' ')
        },
        beginMp() {
            let vuethis = this;
            console.log("text_input", vuethis.new_input)
            console.log("mp_level", vuethis.mp_level_input)

            // alert("button click")
            // d3.select(vuethis.$el).select(".MpButton").attr("loading","true")
            // d3.select(vuethis.$el).select(".MpButton").attr("disabled",true)
            // console.log(d3.select(vuethis.$el).select(".MpButton").attr("loading"))
            vuethis.LoadingMp = true

            let GPTMpDeferObj = $.Deferred()
            $.when(GPTMpDeferObj).then(function () {
                vuethis.LoadingMp = false
            })

            // initialize the tabular dataset
            getGPTExt(vuethis.new_input, vuethis.mp_level_input, function (mp_content) {
                // let processed_tabular_datalist = JSON.parse(processed_tabular_datalist_str)
                // console.log('processed_tabular_datalist', processed_tabular_datalist)
                // vuethis.MpContent = mp_content
                vuethis.draw_tree(mp_content)
                GPTMpDeferObj.resolve()
            })
        },
        draw_tree() {
            // alert("in draw_tree")
            let vuethis = this;
            console.log("array in draw,", vuethis.less_array)
            var marge = { top: 60, bottom: 60, left: 60, right: 60 }
            var barHeight = 45
            var barWidth = 850
            var textWidth = 800

            var svg = d3.select("body").select(".MpShow").append("svg")
            svg.attr("width", 1000)
            svg.attr("height", 1000)
            var width = svg.attr("width")
            var height = svg.attr("height")
            console.log("select MP", svg)
            var g1 = svg.append("g").attr("transform", "translate(" + marge.top + "," + marge.left + ")");
            var scale = svg.append("g")
            //1. 准备数据
            var dataset_test = {
                name: "中国",
                children: [
                    {
                        name: "浙江",
                        children: [
                            { name: "杭州", value: 100 },
                            { name: "宁波", value: 100 },
                            { name: "温州", value: 100 },
                            { name: "绍兴", value: 100 }
                        ]
                    },
                    {
                        name: "广西",
                        children: [
                            {
                                name: "桂林",
                                children: [
                                    { name: "秀峰区", value: 100 },
                                    { name: "叠彩区", value: 100 },
                                    { name: "象山区", value: 100 },
                                    { name: "七星区", value: 100 }
                                ]
                            },
                            { name: "南宁", value: 100 },
                            { name: "柳州", value: 100 },
                            { name: "防城港", value: 100 }
                        ]
                    },
                    {
                        name: "黑龙江",
                        children: [
                            { name: "哈尔滨", value: 100 },
                            { name: "齐齐哈尔", value: 100 },
                            { name: "牡丹江", value: 100 },
                            { name: "大庆", value: 100 }
                        ]
                    },
                    {
                        name: "新疆",
                        children:
                            [
                                { name: "乌鲁木齐" },
                                { name: "克拉玛依" },
                                { name: "吐鲁番" },
                                { name: "哈密" }
                            ]
                    }
                ]
            };
            // var diagonal = d3.linkHorizontal()
            //     .x(function (d) { return d.y; })
            //     .y(function (d) { return d.x; });
            var diagonal = d3.line()
                .x(function (d) { return d.x; })
                .y(function (d) { return d.y; })
                .curve(d3.curveStepBefore);
            var root;
            // d3.json("j1.json").then(function (flare) {//testtreeD3url
            var flare = window.sysDatasetObj.jsonData
            root = d3.hierarchy(flare);
            root.x0 = 0;
            root.y0 = 0;
            update(root);
            // })
            var i = 0;
            function update(source) {

                // Compute the flattened node list.
                // var root = source
                var nodes = root.descendants();

                var height = Math.max(500, nodes.length * barHeight + marge.top + marge.bottom);
                var duration = 400;
                d3.select("svg").transition()
                    .duration(duration)
                    .attr("height", height);

                d3.select(self.frameElement).transition()
                    .duration(duration)
                    .style("height", height + "px");

                // Compute the "layout". TODO https://github.com/d3/d3-hierarchy/issues/67
                var index = -1;
                root.eachBefore(function (n) {
                    n.x = ++index * barHeight;
                    n.y = n.depth * 20;
                });

                // Update the nodes…
                var node = g1.selectAll(".node")
                    .data(nodes, function (d) { return d.id || (d.id = ++i); });

                var nodeEnter = node.enter().append("g")
                    .attr("class", "node")
                    .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                    .style("opacity", 0);

                // Enter any new nodes at the parent's previous position.
                nodeEnter.append("rect")
                    .attr("y", -barHeight / 2)
                    .attr("height", barHeight)
                    .attr("width", barWidth)
                    .style("fill", color)
                    .on("click", click);

                // nodeEnter.append("text")
                //     .attr("dy", 3.5)
                //     .attr("dx", 5.5)
                //     .text(function (d) { return d.data.name; });
                nodeEnter.append("text")
                    // .attr("dy", 3.5)
                    .attr("dx", 50)
                    .each(function (d) {
                        let f_1 = false
                        if (vuethis.less_array.indexOf(d.id) != -1) {
                            f_1 = true
                        }
                        if (vuethis.b_value ^ f_1) {
                            d3.select(this).call(wrapText, d.data.name_less, textWidth)
                        }
                        else {
                            d3.select(this).call(wrapText, d.data.name, textWidth)
                        }
                    })
                // .text(function (d) { return d.data.name; });
                // .call(wrapText, "This is a long text that needs to be wrapped within the rectangle.", 100)
                // .call(wrapText, function (d) { return d.data.name; }, 200)

                nodeEnter.append("text")
                    .attr("dy", -8)
                    .attr("dx", 5.5)
                    .text(function (d) {
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
                    .duration(duration)
                    .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; })
                    .style("opacity", 1)
                    .select("rect")
                    .style("fill", color);

                // Transition exiting nodes to the parent's new position.
                node.exit().transition()
                    .duration(duration)
                    .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
                    .style("opacity", 0)
                    .remove();

                // Update the links…
                var link = g1.selectAll(".link")
                    .data(root.links(), function (d) { return d.target.id; });

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
                root.each(function (d) {
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
                } else {
                    d.children = d._children;
                    d._children = null;
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
                // return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
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




        }
    }
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

.NewsText {
    font-family: "Open Sans", Arial, sans-serif;
}

.MpSpan {
    white-space: pre-wrap;
    text-align: left;
    float: left;
    font-size: 20px;
    font-family: auto;
    font-weight: bold;
}

li {
    display: inline-block;
    margin: 0 10px;
}

a {
    color: #42b983;
}

.node rect {
    cursor: pointer;
    fill: #fff;
    // fill-opacity: 0.5
    stroke: #000000;
    stroke-width: 1.5px;
}

.node text {
    font: 10px sans-serif;
    font-weight: bold;
    pointer-events: none;
}

.link {
    fill: none;
    // stroke: #9ecae1;
    stroke: #000;
    stroke-width: 1.5px;
    stroke-opacity: 1;
}

.NewsInput {
    .el-textarea__inner {
        font-size: 20px;
        // font-weight: bold;
        color: black;
        font-family: auto;

    }
}

@menu-height: 2.5rem;

.hello {
    position: absolute;
    top: 0%;
    left: 0%;
    bottom: 0%;
    right: 0%;



    .NewsText {
        position: absolute;
        top: 0%;
        left: 1%;
        bottom: 0%;
        right: 60%;
    }

    .block {
        position: absolute;
        top: 80%;
        left: 50%;
        bottom: 0%;
        right: 0%;

        .MpSlider {
            position: absolute;
            top: 0%;
            left: 30%;
            bottom: 95%;
            right: 20%;
        }

        .MpButton {
            position: absolute;
            top: 15%;
            left: 45%;
            bottom: 70%;
            right: 45%;
        }

    }

    .MpShow {
        position: absolute;
        top: 0%;
        left: 41%;
        bottom: 20%;
        right: 5%;

        .showButton {
            position: absolute;
            top: 1.5%;
            left: 41%;
            bottom: 20%;
            right: 5%;
        }
    }
}
</style>
