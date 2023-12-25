<template>
    <div class="hello">
    
    
    
        <div class="NewsText">
            <el-input class="NewsInput"
                style="font-weight: bold;"
                type="textarea"
                :autosize="{ minRows: 50, maxRows: 60}"
                placeholder=" 请输入内容"
                v-model="new_input">
            </el-input>
        </div>
        <div class="block">
            
            <el-slider
                class="MpSlider"
                v-model="mp_level_input"
                :step="10"
                show-stops
                show-input>
            </el-slider>
            <el-button type="primary" round @click="beginMp" class="MpButton" style="transform: translate(-20,0);">Generate</el-button>
        </div>
        <div class="MpShow" v-loading="LoadingMp" element-loading-text="Waiting GPT answering">
            <span class="MpSpan">{{ MpContent }}</span>
        </div>
    </div>

</template>

<script>
import { mapState, mapMutations } from 'vuex';
import { getGPTMp } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
export default {
    name: 'HelloWorld',
    props: {
    msg: String,
    // MpContent: String,
    },
    data(){
        return{
            new_input: '',
            mp_level_input: 0,
            MpContent: '',
            LoadingMp: false,
        }
    },
    watch: {
        displayMode: function() {
            console.log('displayMode')
        },
        textarea2:function(){
            console.log('test changed!')
            console.log(this.textarea2)
        }
    },
    computed: {
        ...mapState([
            'displayMode'
        ])
    },
    methods:{
        beginMp(){
            let vuethis=this;
            console.log("text_input",vuethis.new_input)
            console.log("mp_level",vuethis.mp_level_input)

            // alert("button click")
            // d3.select(vuethis.$el).select(".MpButton").attr("loading","true")
            // d3.select(vuethis.$el).select(".MpButton").attr("disabled",true)
            // console.log(d3.select(vuethis.$el).select(".MpButton").attr("loading"))
            vuethis.LoadingMp=true
            
            let GPTMpDeferObj = $.Deferred()
            $.when(GPTMpDeferObj).then(function() {
                vuethis.LoadingMp=false
            })
            
            // initialize the tabular dataset
            getGPTMp(vuethis.new_input,vuethis.mp_level_input, function(mp_content) {
                // let processed_tabular_datalist = JSON.parse(processed_tabular_datalist_str)
                // console.log('processed_tabular_datalist', processed_tabular_datalist)
                vuethis.MpContent=mp_content
                GPTMpDeferObj.resolve()
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
.MpSpan{
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
.NewsInput{
    .el-textarea__inner{
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
    .block{
        position: absolute;
        top: 50%;
        left: 50%;
        bottom: 0%;
        right: 0%;
        .MpSlider{
        position: absolute;
            top: 0%;
            left: 30%;
            bottom: 95%;
            right: 20%;
        }        
        .MpButton{
            position: absolute;
            top: 10%;
            left: 45%;
            bottom: 85%;
            right: 45%;
        }

    }
    
    .MpShow{
        position: absolute;
        top: 10%;
        left: 51%;
        bottom: 50%;
        right: 5%;
    }
}

</style>
