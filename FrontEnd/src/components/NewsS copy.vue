<template>
    <div class="hello">



        <div class="NewsText">
            <el-input class="NewsInput" style="font-weight: bold;" type="textarea" :autosize="{ minRows: 50, maxRows: 60 }"
                placeholder=" 请输入内容" v-model="new_input">
            </el-input>
        </div>
        <div class="block">

            <el-slider class="MpSlider" v-model="mp_level_input" :step="10" show-stops show-input>
            </el-slider>
            <el-button type="primary" round @click="beginMp" class="MpButton"
                style="transform: translate(-20,0);">Generate</el-button>
        </div>
        <div class="MpShow" v-loading="LoadingMp" element-loading-text="Waiting GPT answering">
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
        // MpContent: String,
    },
    data() {
        return {
            new_input: '',
            mp_level_input: 0,
            MpContent: 'hello',
            LoadingMp: false,
        }
    },
    mounted: function () {
        // alert("before mounted")
        this.draw_tree()
    },
    watch: {
        displayMode: function () {
            console.log('displayMode')
        },
        textarea2: function () {
            console.log('test changed!')
            console.log(this.textarea2)
        }
    },
    computed: {
        ...mapState([
            'displayMode'
        ])
    },

    methods: {
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
            var marge = { top: 60, bottom: 60, left: 60, right: 60 }

            var svg = d3.select("body").select(".MpShow").append("svg")
            svg.attr("width", 1000)
            svg.attr("height", 1000)
            var width = svg.attr("width")
            var height = svg.attr("height")
            console.log("select MP", svg)
            var g = svg.append("g").attr("transform", "translate(" + marge.top + "," + marge.left + ")");
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
            //2. 创建层级布局
            var hierarchyData = d3.hierarchy(dataset_test)
                .sum(function (d) {
                    return d.value;
                });
            //3. 创建一个树状图
            var tree = d3.tree()
                .size([width - 400, height - 200])
                .separation(function (a, b) {
                    return (a.parent == b.parent ? 1 : 2) / a.depth;
                })
            //4. 初始化树状图，也就是传入数据,并得到绘制树基本数据
            var treeData = tree(hierarchyData);
            var nodes = treeData.descendants();
            var links = treeData.links();
            //5. 创建一个贝塞尔生成曲线生成器
            var Bézier_curve_generator = d3.linkVertical()
                .x(function (d) { return d.x; })
                .y(function (d) { return d.y; });
            //6. 绘制边
            g.append("g")
                .selectAll("path")
                .data(links)
                .enter()
                .append("path")
                .attr("d", function (d) {
                    var start = { x: d.source.x, y: d.source.y };
                    var end = { x: d.target.x, y: d.target.y };
                    return Bézier_curve_generator({ source: start, target: end });
                })
                .attr("fill", "none")
                .attr("stroke", "yellow")
                .attr("stroke-width", 1);
            //7. 常规：建立用来放在每个节点和对应文字的分组<g>
            var gs = g.append("g")
                .selectAll("g")
                .data(nodes)
                .enter()
                .append("g")
                .attr("transform", function (d) {
                    var cx = d.y;
                    var cy = d.x;
                    return "translate(" + cy + "," + cx + ")";
                });
            //8. 绘制节点和文字
            gs.append("rect")
                .attr("width", 40)
                .attr("height", 35)
                .attr("x", -10)
                .attr("y", -7)
                .attr("fill", "rgba(255, 0, 0, 0.5)")
                .attr("stroke", "blue")
                .attr("stroke-width", 1);

            //文字
            gs.append("text")
                .attr("x", function (d) {
                    return d.children ? -40 : 8;//如果某节点有子节点，则对应的文字前移
                })
                .attr("y", -5)
                .attr("dy", 10)
                .text(function (d) {
                    return d.data.name;
                })




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
        left: 0%;
        bottom: 0%;
        right: 50%;
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
        top: 10%;
        left: 51%;
        bottom: 20%;
        right: 5%;
    }
}
</style>
