from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dataset.tabular_data_collection import load_tabular_dataset, get_tabular_dataset
from gpt_processing.GptMp import genGPTMp
from JsonRead import readJson,readText,readRelation
from processing.emoVal import emoVal

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
@app.route('/GptExt', methods=['GET'])
@cross_origin()
def getGPTExt():
    
    input_text = request.args.get('input_text')
    mp_level=request.args.get('mp_level')
    # print('tabular_name_list[]', tabular_name_list)
    Mp_content=genGPTMp(input_text,mp_level)
    return {"data": Mp_content}

@app.route('/JsonData', methods=['GET'])
@cross_origin()
def getJsonData():
    
    
    mp_level=request.args.get('mp_level')
    cur_i = request.args.get('cur_i')
    # print('tabular_name_list[]', tabular_name_list)
    json_data=readJson(mp_level,cur_i)
    return {"data": json_data}

@app.route('/RelationData', methods=['GET'])
@cross_origin()
def getRelationData():
    
    
    mp_level=request.args.get('mp_level')
    cur_i = request.args.get('cur_i')
    # print('tabular_name_list[]', tabular_name_list)
    json_data=readRelation(cur_i)
    return {"data": json_data}

@app.route('/TextData', methods=['GET'])
@cross_origin()
def getTextData():
    
    
    
    cur_i = request.args.get('cur_i')
    # print('tabular_name_list[]', tabular_name_list)
    json_data=readText(cur_i)
    return {"data": json_data}

@app.route('/emoVal', methods=['GET'])
@cross_origin()
def getEmoVal():
    file_path="t10_correct.json"
    cur_i = request.args.get('cur_i')
    # print('tabular_name_list[]', tabular_name_list)
    emo_flat_list=emoVal(file_path)
    return {"data": emo_flat_list}
if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    load_tabular_dataset()
    app.run(host='0.0.0.0', port=14449)

