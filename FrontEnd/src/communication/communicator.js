// 
import axios from 'axios'
let server_address = 'http://127.0.0.1:14449'

export function getTabularDataset(tabularDataList, getTabularDataCallback) {
    let formData = {"tabularData": tabularDataList}
    axios({
        methods: 'get',
        url: server_address + '/tabulardata',
        params: formData,
        timeout: 5000
    })
    .then((res) => {
        let tabularDatasetList = res['data']['data']
        // console.log('tabularDatasetList', tabularDatasetList)
        getTabularDataCallback(tabularDatasetList)
    })
}
export function getGPTMp(input_text, mp_level,getGPTMpCallback) {
    let formData = {"input_text": input_text,"mp_level":mp_level}
    axios({
        methods: 'get',
        url: server_address + '/GptMp',
        params: formData,
        timeout: 50000
    })
    .then((res) => {
        let GptMpList = res['data']['data']
        console.log('GPTMp in commu', GptMpList)
        getGPTMpCallback(GptMpList)
    })
}
export function getGPTExt(input_text, mp_level,getGPTExtCallback) {
    let formData = {"input_text": input_text,"mp_level":mp_level}
    axios({
        methods: 'get',
        url: server_address + '/GptExt',
        params: formData,
        timeout: 50000
    })
    .then((res) => {
        let GptExtList = res['data']['data']
        console.log('GPTExt in commu', GptExtList)
        getGPTExtCallback(GptExtList)
    })
}
export function getJsonData(cur_i, mp_level,getJsonDataCallback) {
    let formData = {"mp_level":mp_level,"cur_i":cur_i}
    axios({
        methods: 'get',
        url: server_address + '/JsonData',
        params: formData,
        timeout: 50000
    })
    .then((res) => {
        let jsonData = res['data']['data']
        console.log('Jsondata in commu', jsonData)
        getJsonDataCallback(jsonData)
    })
}
export function getRelationData(cur_i,getRelationDataCallback) {
    let formData = {"cur_i":cur_i}
    axios({
        methods: 'get',
        url: server_address + '/RelationData',
        params: formData,
        timeout: 50000
    })
    .then((res) => {
        let jsonData = res['data']['data']
        // console.log('Jsondata in commu', jsonData)
        getRelationDataCallback(jsonData)
    })
}
export function getTextData(cur_i,getTextDataCallback) {
    let formData = {"cur_i":cur_i}
    axios({
        methods: 'get',
        url: server_address + '/TextData',
        params: formData,
        timeout: 50000
    })
    .then((res) => {
        let jsonData = res['data']['data']
        console.log('Textdata in commu', jsonData)
        getTextDataCallback(jsonData)
    })
}