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
