<template>
    <div class="hello">



        <!-- <div class="NewsText">
            <h3>{{ NewsTitle }}</h3>
            <span class="NewsOri" style="text-align: left;display: inline-block;">{{ NewsOri }}</span>


        </div> -->
        <div class="CEview" ref="CEview">
            <svg class="CEsvg">
                <NewsClaim v-for="(node_data, index_i) in node_data_array" :key=node_data.index
                    :transform="genNodeTran(index_i)" :barHeight="cNodeYInter - cNodeIndent" :c_node_data="node_data"
                    :b_value="b_value" :cNodeR="cNodeR" :re_ce_data="re_ce_data[index_i]" :CxArray="xArray"
                    :rcInter="rcInter" :barWidth="barWidth" :leftbarIndent="leftbarIndent" :rcLinkRW="rcLinkRW"
                    :rcLinkRInter="rcLinkRInter"></NewsClaim>
                <NewsEvi v-for="(e_dict, index_i) in re_e_data" :key="e_dict.c_index" :e_dict="e_dict"
                    :e_node_y_array="e_node_y_array" :e_render_index="index_i" :e_index_map_array="e_index_map_array"
                    :eNodeR="eNodeR">
                </NewsEvi>
                <g class="CEPath"></g>
            </svg>

        </div>

        <!-- <div class="MpShow" v-loading="LoadingMp" element-loading-text="Waiting GPT answering">
            <el-switch v-model="b_value" active-color="#13ce66" inactive-color="#ff4949" class="showButton"
                active-text="coarse-grained" inactive-text="origin">
            </el-switch>
            <svg class="CNodeList" width="1000" height="2000">
                <NewsClaim v-for="(node_data, index_i) in node_data_array" :key=node_data.index
                    :transform="genNodeTran(index_i)" :barHeight="cNodeYInter" :c_node_data="node_data"
                    :b_value="b_value" :cNodeR="cNodeR"></NewsClaim>
            </svg>

        </div> -->
        <!-- <div class="forceView">
            <NewsForce></NewsForce>
        </div> -->
    </div>
</template>

<script>
import { mapState, mapMutations, mapGetters } from 'vuex';
import { getGPTMp, getGPTExt } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
import NewsClaim from './NewsClaim.vue';
import NewsForce from './NewsForce.vue'
import NewsEvi from './NewsEvi.vue';
// const lodash = require('lodash')
export default {
    name: 'NewsS',
    props: {
        msg: String,
        cur_i_change: Number,
        // MpContent: String,
    },
    components: {
        NewsClaim,
        NewsEvi,
        // NewsForce,

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
            node_data_array: [],
            re_ce_data: [],
            re_cc_data: [],
            xArray: [],
            e_node_y_array: [],
            e_index_map_array: [],


            //attribute set
            cNodeYInter: 80,
            cNodeXInter: 25,//25
            marge: { top: 60, bottom: 60, left: 20, right: 60 },
            cNodeR: 15,
            cNodeIndent: 20,
            ENodeYInter: 30,
            EnodeunfoldYInter: 70,
            ENodeIndent: 10,
            eNodeR: 10,
            eTopInter: 40,

            barWidth: 620,
            rcInter: 100,
            leftbarIndent: 7,
            rcLinkRInter: 5,
            rcLinkRW: 3,
        }
    },
    beforeMount: function () {
        this.genNodeDataArray()
        this.genENodeTran()


    },
    mounted: function () {
        // alert("before mounted")
        // this.genNodeDataArray()
        // this.draw_tree()

        const divW = this.$refs.CEview.clientWidth
        const divH = this.$refs.CEview.clientHeight + 500
        // console.log("div w h ", divW, divH)
        d3.select(".CEsvg").attr("width", divW)
        d3.select(".CEsvg").attr("height", divH)

        // this.loadNews()
        this.drawNodePath()
        this.drawCELink()
        // this.renderNodePath()

    },
    computed: {
        ...mapState([
            'displayMode',
            'cNodeYArray',
            'eNodeYControlArray',
        ]),

    },
    watch: {
        cur_i_change: function () {

        },
        eNodeYControlArray: function () {
            this.genENodeTran()
            this.$nextTick(() => {
                this.drawCELink()
            })
        },

        b_value: function () {
            // alert('b_value change!')
            let vuethis = this
            console.log("text select", vuethis.b_value)
            d3.select(".CNodeList").selectAll(".node").selectAll("text#sent").selectAll("tspan").remove()
            d3.select(".CNodeList").selectAll(".node").selectAll("text#sent").each(function (d) {
                if (vuethis.b_value) {
                    d3.select(this).call(wrapText, d.data.name_less, 800)
                }
                else {
                    d3.select(this).call(wrapText, d.data.name, 800)
                }

            })
            // this.less_array = []
            // this.draw_tree()
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
        cNodeYArray: function () {
            console.log("nodey change")
            let vuethis = this

            // vuethis.renderNodePath()
            vuethis.drawNodePath()
        },


    },


    methods: {
        genNodeDataArray() {
            let vuethis = this
            vuethis.node_data_array = []
            var flare = window.sysDatasetObj.jsonData
            vuethis.node_data_array = flare.children
            console.log("gennodedataarray,", vuethis.node_data_array)
            var node_num = vuethis.node_data_array.length

            var relation_data = window.sysDatasetObj.relationData
            var re_ce_data = relation_data["re_e"]
            var re_cc_data = relation_data["re_c"]
            vuethis.re_ce_data = re_ce_data
            vuethis.re_cc_data = re_cc_data

            var e_re_data = []
            for (var i = 0; i < re_ce_data.length; i++) {
                var e_re_list = re_ce_data[i].e_re_list
                // console.log("in re e:", e_re_list)
                for (var j = 0; j < e_re_list.length; j++) {
                    e_re_data.push(e_re_list[j])
                }

            }
            vuethis.re_e_data = e_re_data
            console.log("re_e_data!!", vuethis.re_e_data)

            var unfoldarray = []
            var yArray = []
            for (i = 0; i < node_num; i++) {
                unfoldarray.push(0)
                yArray.push(1)
            }
            var xArray = []
            xArray.push(0)
            var temp_x = 0
            for (i = 0; i < vuethis.re_cc_data.length; i++) {
                var relation_str = vuethis.re_cc_data[i]["relation"]
                temp_x += vuethis.genXinter(relation_str)
                xArray.push(temp_x * vuethis.cNodeXInter)
            }
            //do not let left get out
            var minx = 0
            for (i = 0; i < xArray.length; i++) {
                if (minx > xArray[i]) {
                    minx = xArray[i]
                }
            }
            // console.log("x_array", minx * vuethis.cNodeXInter - vuethis.cNodeR, minx, vuethis.marge.left + vuethis.cNodeXInter * xArray[index_i], xArray[index_i])
            if (minx - vuethis.cNodeR < 0) {
                // console.log("left out!")
                var pro_factor = (0 - minx + vuethis.cNodeR)
                for (i = 0; i < xArray.length; i++) {
                    xArray[i] += pro_factor
                }
            }
            vuethis.xArray = xArray

            vuethis.$store.commit('setCNodeUnfoldArray', unfoldarray)
            //gen Node Y array
            vuethis.$store.commit('setCNodeYArray', yArray)

            //init ENodeYControlArray
            var eNodeYControlArray = []

            var e_index_map_array = []
            for (i = 0; i < re_ce_data.length; i++) {
                var re_ce_list = re_ce_data[i].e_re_list
                var temp_list = []
                // var c_index=re_ce_data[i].c_index
                for (j = 0; j < re_ce_list.length; j++) {
                    temp_list.push(0)
                    e_index_map_array.push(j)

                }
                eNodeYControlArray.push(lodash.cloneDeep(temp_list))
            }
            vuethis.e_index_map_array = e_index_map_array
            vuethis.$store.commit('setENodeYControlArray', eNodeYControlArray)
            // console.log('EnodeYC init', e_index_map_array, vuethis.e_index_map_array)








        },
        genXinter(relation_str) {
            switch (relation_str) {
                case "Sequence":
                    return 0
                case "Elaboration":
                    return 1
                case "Cause-effect":
                    return 1
                case "Concession":
                    return - 1
                case "Contrast":
                    return -1
            }

        },
        genNodeTran(index_i) {
            //gen claim node tranformation string
            let vuethis = this
            var index_c = 0
            var y_array = vuethis.cNodeYArray
            for (var i = 0; i < index_i; i++) {
                index_c += y_array[i]
            }
            // console.log("cychange", y_array, index_c)
            //gen CNode x array
            // var xArray = []
            // xArray.push(0)
            // var temp_x = 0
            // for (i = 0; i < vuethis.re_cc_data.length; i++) {
            //     var relation_str = vuethis.re_cc_data[i]["relation"]
            //     temp_x += vuethis.genXinter(relation_str)
            //     xArray.push(temp_x)
            // }
            // //do not let left get out
            // var minx = 0
            // for (i = 0; i < xArray.length; i++) {
            //     if (minx > xArray[i]) {
            //         minx = xArray[i]
            //     }
            // }
            // // console.log("x_array", minx * vuethis.cNodeXInter - vuethis.cNodeR, minx, vuethis.marge.left + vuethis.cNodeXInter * xArray[index_i], xArray[index_i])
            // if (minx * vuethis.cNodeXInter - vuethis.cNodeR < 0) {
            //     console.log("left out!")
            //     var pro_factor = (0 - minx * vuethis.cNodeXInter + vuethis.cNodeR) / vuethis.cNodeXInter
            //     for (i = 0; i < xArray.length; i++) {
            //         xArray[i] += pro_factor
            //     }
            // }
            // vuethis.xArray = xArray

            return "translate(" + (vuethis.marge.left) + "," + (vuethis.marge.top + vuethis.cNodeYInter * (index_c)) + ")"


        },
        genENodeTran() {
            let vuethis = this
            let re_ce_data = vuethis.re_ce_data

            //cal claim y 
            var index_c = 0
            var y_array = vuethis.cNodeYArray
            var eNodeYControlArray = vuethis.eNodeYControlArray
            // console.log("Enodecontrol in EnTran", eNodeYControlArray)
            var claim_y_list = []

            var indent_e = vuethis.eTopInter
            var e_node_y_array = []
            for (var i = 0; i < re_ce_data.length; i++) {
                var e_dict_list = re_ce_data[i].e_re_list
                var e_y_c_list = []

                for (var j = 0; j < e_dict_list.length; j++) {

                    e_y_c_list.push(indent_e)
                    if (eNodeYControlArray[i][j] == 1) {
                        indent_e += vuethis.EnodeunfoldYInter
                    }
                    else {
                        indent_e += vuethis.ENodeYInter
                    }


                    // deepclone!!
                }
                e_node_y_array.push(lodash.cloneDeep(e_y_c_list))
            }
            // to gen a dict
            // [c_dict,dict] C_index
            // [e_dict] E_index
            vuethis.e_node_y_array = lodash.cloneDeep(e_node_y_array)
        },
        drawNodePath() {
            let vuethis = this
            d3.select(".CEsvg").selectAll(".nodeLink").remove()
            // var cNodes = d3.select(vuethis.$el).selectAll(".Claim")
            // var cNode_array = cNodes._groups[0]
            // // console.log("cnodes", cNodes._groups[0][0])
            // var node_y_list = []
            // //get current node y list

            // for (var i = 0; i < cNode_array.length; i++) {
            //     var split_str_list = getComputedStyle(cNode_array[i]).transform.split(',')
            //     var nodey = parseInt(split_str_list[split_str_list.length - 1].split(')')[0])
            //     var nodex = parseInt(split_str_list[split_str_list.length - 2])
            //     node_y_list.push(nodey)
            //     // console.log("cNode attr", nodey)
            // }
            var y_array = vuethis.cNodeYArray
            var x_array = vuethis.xArray




            for (var i = 0; i < y_array.length - 1; i++) {
                var index_c1 = 0
                var index_c2 = 0

                for (var j = 0; j < i; j++) {
                    index_c1 += y_array[j]
                }
                index_c2 = index_c1 + y_array[i]
                //begin draw path between the near c node
                d3.select(".CEsvg").append("path").attr("id", "p" + i).attr("class", "nodeLink")
                    .attr("d", "M " + (vuethis.marge.left + x_array[i] - vuethis.cNodeR) + " " + (vuethis.marge.top + vuethis.cNodeYInter * index_c1 + vuethis.cNodeR) + " L " + (vuethis.marge.left + x_array[i + 1] - vuethis.cNodeR) + " " + (vuethis.marge.top + vuethis.cNodeYInter * index_c2 - vuethis.cNodeR))
                    .attr("stroke", "black")

            }

            // console.log("cychange", y_array, index_c)


        },
        drawCELink() {
            let vuethis = this
            // get C x,y coor
            // get C's all E x,y coor
            d3.selectAll(".CELink").remove()
            // draw path
            var c_g_list = d3.select(vuethis.$el).selectAll(".Claim")
            var c_x_list = []
            var c_y_list = []
            c_g_list.each(function (d, i) {
                // console.log("d", d, i)
                // console.log("c_g", d3.select(this).attr("transform"))
                var c_tran_str = d3.select(this).attr("transform")

                var index1 = c_tran_str.indexOf("(")
                var index2 = c_tran_str.indexOf(",")
                var index3 = c_tran_str.indexOf(")")
                var c_x = parseFloat(c_tran_str.slice(index1 + 1, index2))
                var c_y = parseFloat(c_tran_str.slice(index2 + 1, index3))
                // console.log("c_x!!", c_x, c_y)
                c_x_list.push(c_x)
                c_y_list.push(c_y)

            })
            var e_x_list = []
            var e_y_list = []
            var e_g_list = d3.select(vuethis.$el).selectAll(".Evi")
            e_g_list.each(function (d, i) {
                var e_tran_str = d3.select(this).attr("transform")

                var index1 = e_tran_str.indexOf("(")
                var index2 = e_tran_str.indexOf(",")
                var index3 = e_tran_str.indexOf(")")
                var e_x = parseFloat(e_tran_str.slice(index1 + 1, index2))
                var e_y = parseFloat(e_tran_str.slice(index2 + 1, index3))
                e_x_list.push(e_x)
                e_y_list.push(e_y)

            })

            var e_index_map_array = vuethis.e_index_map_array
            var g_path = d3.select(vuethis.$el).select(".CEPath")
            // console.log("e_map_array", e_index_map_array)
            var Bézier_curve_generator = d3.linkHorizontal()
                .x(function (d) { return d.x; })
                .y(function (d) { return d.y; });
            // .curve(d3.curveStepBefore);
            var c_index = -1
            for (var i = 0; i < e_index_map_array.length; i++) {
                if (e_index_map_array[i] == 0) c_index++
                var c_x = c_x_list[c_index]
                var c_y = c_y_list[c_index]

                var e_x = e_x_list[i]
                var e_y = e_y_list[i]
                var start_x = c_x + vuethis.barWidth + vuethis.rcInter + vuethis.leftbarIndent + vuethis.rcLinkRW - vuethis.rcLinkRInter
                var start_y = c_y
                var end_x = e_x - 10
                var end_y = e_y
                var start = { x: end_x, y: end_y }
                var end = { x: start_x, y: start_y }

                g_path.append("path").attr("class", "CELink")
                    .attr("d", Bézier_curve_generator({ source: start, target: end }))
                    // .attr("d", "M " + (c_x + 620 + 150 + 7 + 3 - 5) + " " + (c_y) + " L " + (e_x - 10) + " " + (e_y))
                    .attr("stroke", "#c8ccc6")
                    .attr("fill", "none")




            }











        },
        renderNodePath() {
            let vuethis = this
            var change_c_index = vuethis.$store.state.change_c_index
            console.log("change_c_index", change_c_index)
            if (change_c_index != 0) {
                d3.select(".CNodeList").selectAll(".nodeLink").filter(function (d) {
                    console.log("path id", this.id)
                    if (this.id.indexOf(change_c_index)) {
                        return true
                    }
                }).remove()
                var cNodes = d3.select(vuethis.$el).selectAll(".Claim")
                var cNode_array = cNodes._groups[0]
                var node_y_list = []
                //get current node y list

                for (var i = 0; i < cNode_array.length; i++) {
                    var split_str_list = getComputedStyle(cNode_array[i]).transform.split(',')
                    var nodey = parseInt(split_str_list[split_str_list.length - 1].split(')')[0])
                    var nodex = parseInt(split_str_list[split_str_list.length - 2])
                    node_y_list.push(nodey)
                    // console.log("cNode attr", nodey)
                }
                //begin draw path between the near c node
                d3.select(".CNodeList").append("path").attr("id", "p" + change_c_index).attr("class", "nodeLink")
                    .attr("d", "M " + nodex + " " + (node_y_list[change_c_index] + vuethis.cNodeR) + " L " + nodex + " " + (node_y_list[change_c_index + 1] - vuethis.cNodeR))
                    .attr("stroke", "black")

            }

        },
        loadNews() {
            //load news ori text

            // let textData = window.sysDatasetObj.textData
            // this.NewsTitle = textData[0]
            // this.NewsOri = textData.slice(1, textData.length).join(' ')
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
            let vuethis = this;
            console.log("array in draw,", vuethis.less_array)
            var marge = { top: 60, bottom: 60, left: 60, right: 60 }
            var barHeight = 45
            var barWidth = 850
            var textWidth = 800
            var nodeR = 3
            var svg = d3.select("body").select(".MpShow").select(".CNode")


            var g1 = svg.append("g").attr("transform", "translate(" + marge.top + "," + marge.left + ")");

            //set g2 to draw rpNodes
            var g2 = svg.append("g").attr("transform", "translate(" + marge.top + "," + marge.left + ")");
            // var scale = svg.append("g")
            //1. 准备数据

            // var diagonal = d3.linkHorizontal()
            //     .x(function (d) { return d.y; })
            //     .y(function (d) { return d.x; });
            var diagonal = d3.line()
                .x(function (d) { return d.x; })
                .y(function (d) { return d.y; })
                .curve(d3.curveStepBefore);


            var flare = window.sysDatasetObj.jsonData
            var root;


            console.log("flare", flare)
            root = d3.hierarchy(flare);
            root.x0 = 0;
            root.y0 = 0;
            update(root);
            // })
            var rp_flag_list = Array(flare.children.length).fill(0)
            var rpFoldList = flare.children
            console.log("rpFoldList", rpFoldList)
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

                //set representNode
                //set reNodes for all node with depth1
                var rpNodes = []
                // var nodes1 = lodash.cloneDeep(root.eachBefore())
                var rp_dpindex = -1
                var rp_index = -1
                root.eachBefore(function (n) {
                    ++rp_dpindex
                    if (n.depth == 1) {
                        ++rp_index
                        rpNodes.push(lodash.cloneDeep(n))
                        rpNodes[rpNodes.length - 1].x = rp_dpindex * barHeight;
                        rpNodes[rpNodes.length - 1].y = rpNodes[rpNodes.length - 1].depth
                        rpNodes[rpNodes.length - 1].id = rp_index
                    }
                })
                // for (var i = 0; i < nodes1.length; i++) {
                //     if (nodes1[i].depth == 1) {
                //         rpNodes.push(nodes1[i])
                //         rpNodes[rpNodes.length - 1].x = i * barHeight;
                //         rpNodes[rpNodes.length - 1].y = rpNodes[rpNodes.length - 1].depth
                //     }
                // }
                // for (var i = 0; i < rpNodes.length; i++) {
                //     console.log("rpnodes x", rpNodes[i].x)
                //     console.log("rpnodes id", rpNodes[i].id)
                // }
                var i = 0
                var rpNode = g2.selectAll(".rpNode")
                    .data(rpNodes, function (d) { return d.id || (d.id = ++i); });

                var rpNodeEnter = rpNode.enter().append("g")
                    .attr("class", "rpNode")
                    .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                    .style("opacity", 0);

                rpNodeEnter.append("circle")
                    .attr("cy", 0)
                    .attr("r", 10)
                    // .attr("width", barWidth)
                    .style("fill", "green")
                    // .style("opacity", 1)
                    .on("click", rp_click);

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
                //try to add circle
                // nodeEnter.append("circle")
                //     // .attr("cy", -barHeight / 2)
                //     .attr("r", nodeR)
                //     .attr("fill", "blue")
                // nodeEnter.append("text")
                //     .attr("dy", 3.5)
                //     .attr("dx", 5.5)
                //     .text(function (d) { return d.data.name; });
                nodeEnter.filter(function (d) {
                    if (d.data.type != "nono") {
                        return true
                    }
                }).append("text")
                    // .attr("dy", 3.5)
                    .attr("dx", 50)
                    .each(function (d) {

                        let f_1 = false
                        if (vuethis.less_array.indexOf(d.id) != -1) {
                            f_1 = true
                        }
                        if (vuethis.b_value ^ f_1) {
                            // if(d.data.type!="nono")
                            d3.select(this).call(wrapText, d.data.name_less, textWidth)
                        }
                        else {
                            d3.select(this).call(wrapText, d.data.name, textWidth)
                        }
                    })


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
                    .duration(duration)
                    .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; })
                    .style("opacity", 1)
                    .select("rect")
                    .style("fill", color);

                rpNodeEnter.transition()
                    .duration(duration)
                    .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; })
                    .style("opacity", 1);

                rpNode.transition()
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
                node.filter(function (d) {
                    if (d.data.type == "nono") {
                        return true
                    }
                }).transition()
                    .duration(duration)
                    .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
                    .style("opacity", 0)
                    .remove();

                rpNode.exit().transition()
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
            function rp_click(d) {
                // alert('click')
                // console.log("click id", d.id)
                // alert(d.id)
                // let index_i = vuethis.less_array.indexOf(d.id)
                // if (index_i != -1) {
                //     vuethis.less_array.splice(index_i, 1)
                // }
                // else {
                //     vuethis.less_array.push(d.id)
                // }
                var click_index = d.data.index - 1
                // g1.selectAll(".node").each(function (d1) {
                //     if (d1.data.type == 'C') {
                //         if (d1.data.index == click_index) {
                //             d1._children = d1.children
                //             d1.children = null
                //             // alert(1)
                //             return true
                //         }
                //     }
                // }).style("display", "none")
                // .each(function (d1) {
                //     if (d1.data.type.indexOf('C') != 0) {
                //         if (d1.data.index == click_index) {
                //             d1._children = d1.children
                //             d1.children = null

                //         }
                //     }
                // })
                // alert(click_index)
                if (rp_flag_list[click_index] == 0) {//fold to node
                    // alert("in if")
                    rp_flag_list[click_index] = 1
                    g1.selectAll(".node").each(function (d1) {
                        if (d1.data.type == "title") {
                            var node_temp = lodash.cloneDeep(d1.children[click_index])
                            node_temp.children = null
                            // node_temp.data.children = null
                            node_temp.data.type = "nono"
                            node_temp.data.name = "111"
                            // d1.children.splice(click_index, 1)
                            d1.children.splice(click_index, 1, node_temp)
                            console.log("childe chang", d1.children)
                        }
                    })
                }
                else {
                    // alert("in else")
                    rp_flag_list[click_index] = 0
                    g1.selectAll(".node").each(function (d1) {
                        if (d1.data.type == "title") {

                            d1.children.splice(click_index, 1, rpFoldList[click_index])
                        }
                    })
                }
                root.eachBefore(function (n) {
                    // console.log("type", n.data.type)
                })
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

.Claim .textG rect {
    cursor: pointer;
    fill: #ffffff;
    fill-opacity: 0.6; // stroke: #000000;
    stroke-width: 1.5px;
}

.Claim .cText {
    font: 10px sans-serif;
    font-weight: bold;
    pointer-events: none;
}

.eText {
    font: 8px sans-serif;
    font-weight: bold;
    pointer-events: none;
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

    .CEview {
        position: absolute;
        top: 0%;
        left: 1%;
        bottom: 0%;
        right: 0%;
    }

    .NewsText {
        position: absolute;
        top: 0%;
        left: 1%;
        bottom: 0%;
        right: 40%;
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
            top: 2%;
            left: 21%;
            bottom: 20%;
            right: 45%;
        }
    }

    .forceView {
        position: absolute;
        top: 0%;
        left: 60%;
        bottom: 0%;
        right: 0%;
    }
}
</style>
