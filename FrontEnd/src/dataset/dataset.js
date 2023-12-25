export function Dataset () {
    this.tabularDatasetList = []
    this.GPTMpList=[]
}

Dataset.prototype = {
    init: function() {
    },
    updateTabularDatasetList: function(processed_tabular_datalist) {
        this.tabularDatasetList = processed_tabular_datalist
    },
    updateGPTMpList:function(processed_MPList){
        this.GPTMpList=processed_MPList
    }
}