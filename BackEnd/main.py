from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dataset.tabular_data_collection import load_tabular_dataset, get_tabular_dataset
from gpt_processing.GptMp import genGPTMp

import os, random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'

@app.route('/tabulardata', methods=['GET'])
@cross_origin()
def getTabularData():
    tabular_dataset = get_tabular_dataset()
    print('tabular_dataset', str(tabular_dataset))
    tabular_name_list = request.args.get('tabularData[]')
    print('tabular_name_list[]', tabular_name_list)
    return {"data": str(tabular_dataset)}

@app.route('/GptMp', methods=['GET'])
@cross_origin()
def getGPTMp():
    
    input_text = request.args.get('input_text')
    mp_level=request.args.get('mp_level')
    # print('tabular_name_list[]', tabular_name_list)
    Mp_content=genGPTMp(input_text,mp_level)
    return {"data": Mp_content}


if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    load_tabular_dataset()
    app.run(host='0.0.0.0', port=14449)

