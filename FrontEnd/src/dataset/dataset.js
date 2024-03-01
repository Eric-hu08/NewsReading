export function Dataset () {
    this.tabularDatasetList = []
    this.GPTMpList=[]
    this.jsonData=[]
    this.textData=[]
}

Dataset.prototype = {
    init: function() {
    },
    updateTabularDatasetList: function(processed_tabular_datalist) {
        this.tabularDatasetList = processed_tabular_datalist
    },
    updateGPTMpList:function(processed_MPList){
        this.GPTMpList=processed_MPList
    },
    updateJsonData:function(processed_json_data){
        this.jsonData=processed_json_data
    },
    updateTextData:function(processed_json_data){
        this.textData=processed_json_data
    }
}