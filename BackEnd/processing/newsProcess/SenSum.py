import openai
# openai migrate
# export OPEN_API_KEY=
import os# 从环境变量中读取openai api key
import time
import json
import re
os.environ["OPENAI_API_KEY"]= "sk-bVh05aHctexyrC2qC6F6E687B9344fD99b3e7eE60f4b9dEf"

# print(resp)
#上面的GPT-3.5-turbo是使用的GPT3.5模型 可以替换为其他模型如：
# gpt-4
# gpt-4-0314
# gpt-4-32k
# gpt-4-32k-0314
# ai_response = response.choices[0].message['content']
def file_read(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    text = []
    # 读取全部内容 ，并以列表方式返回
    lines = f.readlines()
    for line in lines:
        # 如果读到空行，就跳过
        if line.isspace():
            continue
        else:
            # 去除文本中的换行等等，可以追加其他操作
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            # 处理完成后的行，追加到列表中
            text.append(line)
    text_str = " ".join(text)
    f.close()
    return text_str
def genProDict(data):
    if isinstance(data, dict):
        # 添加额外的键 "name_sum"
        if "name" in data:
            data["name_sum"] = len(data["name"])
        # 递归处理字典中的每个值
        for key, value in data.items():
            data[key] = genProDict(value)
        # 如果数据是列表，递归处理列表中的每个元素
    elif isinstance(data, list):
        data = [genProDict(item) for item in data]
    return data
# print(ai_response)

def addSummary(file_path):
    f = open(file_path, 'r')
    json1 = json.load(f)
    f.close()
    jsonData = json.loads(json.dumps(json1))
    # temp_sen=jsonData['children'][0]['name']
    # ans=genGpt(temp_sen)
    # f=open("temptext.txt",'w')
    # f.write(ans)
    # f.close()
    for claim_json in jsonData["children"]:
        sen=claim_json["name"]
        sen_list=genGpt(sen)
        print("sen list: ",sen_list)
        for i in range(5):
            attr_name="sum"+str(i)
            claim_json[attr_name]=sen_list[i]
        for evi_json in claim_json['children']:
            sen=evi_json["name"]
            sen_list=genGpt(sen)
            print("sen list: ", sen_list)
            for i in range(5):
                attr_name = "sum" + str(i)
                evi_json[attr_name] = sen_list[i]

    return jsonData




def genGpt_test(input_str):
    start_time=time.time()
    test_str="Since 2020, scientists have seen signs of increased volcanic activity on the Reykjanes Peninsula, which had been dormant for 800 years, and they have detected tens of thousands of earthquakes in recent months"
    user_content = "|sentence start|"+test_str+"|sentence end|"
    # promp1_path="sys_prompt.txt"
    promp1_path = "sen_gen_p_1.txt"
    sys_content=file_read(promp1_path)
    # sys_content = "You are a nlp master.You will get a sentence, Summarize the sentence"\
    #               "Only the summary sentence is returned" \
    #               "In order to do this, you need to get the gist of your essay, summarize it to the maximum extent possible"
    shot_sum_dir = "shot_sum1"
    shot_sum_file_list = os.listdir(shot_sum_dir)
    shot_sum_content = ""
    # for shot_sum_file_name in shot_sum_file_list:
    #     shot_sum_content = shot_sum_content + "exmaple: \n" + file_read(os.sep.join([shot_sum_dir, shot_sum_file_name])) + "\n"
    #
    # # shot_content = file_read(shot1_path)
    # sys_content = sys_content + shot_sum_content



    resp = openai.chat.completions.create(model='gpt-4-turbo',
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role': 'user', "content": user_content}]
                                          )
    gpt_mp_content = resp.choices[0].message.content
    end_time=time.time()

    print(gpt_mp_content)
    print(resp.usage)
    print("total time cost: ",end_time-start_time)
    # return parseSum(gpt_mp_content)
    return gpt_mp_content
def parseSum(content):
    sum_list=[]
    for i in range(5):
        sen_start=content.find("|sentence start|")
        sen_end=content.find("|sentence end|")
        sen=content[sen_start+len("|sentence start|"):sen_end]
        content=content[sen_end+len("|sentence end|"):]
        sum_list.append(sen)

    # process the sum_list
    for i in range(len(sum_list)):
        sum_list[i]=sum_list[i].replace("[","")
        sum_list[i] = sum_list[i].replace("]", "")

    sorted_sum_list=sorted(sum_list,key=len,reverse=True)


    return sorted_sum_list


def genGpt(input_str):
    start_time=time.time()
    # test_str="Since 2020, scientists have seen signs of increased volcanic activity on the Reykjanes Peninsula, which had been dormant for 800 years, and they have detected tens of thousands of earthquakes in recent months"
    user_content = "|sentence start|"+input_str+"|sentence end|"
    # promp1_path="sys_prompt.txt"
    promp1_path = "sen_gen_p_2.txt"
    sys_content=file_read(promp1_path)
    # sys_content = "You are a nlp master.You will get a sentence, Summarize the sentence"\
    #               "Only the summary sentence is returned" \
    #               "In order to do this, you need to get the gist of your essay, summarize it to the maximum extent possible"
    shot_sum_dir = "shot_sum1"
    shot_sum_file_list = os.listdir(shot_sum_dir)
    shot_sum_content = ""
    # for shot_sum_file_name in shot_sum_file_list:
    #     shot_sum_content = shot_sum_content + "exmaple: \n" + file_read(os.sep.join([shot_sum_dir, shot_sum_file_name])) + "\n"
    #
    # # shot_content = file_read(shot1_path)
    # sys_content = sys_content + shot_sum_content



    resp = openai.chat.completions.create(model='gpt-4o',
                                          temperature=0.00000001,
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role': 'user', "content": user_content}]
                                          )
    gpt_mp_content = resp.choices[0].message.content
    end_time=time.time()

    print(gpt_mp_content)
    print(resp.usage)
    print("total time cost: ",end_time-start_time)
    sum_list=parseSum(gpt_mp_content)
    return sum_list
    # return gpt_mp_content
def add_key(node):
    if node is None:
        return

    name_less=genGpt(node["name"])
    node['name_less'] = name_less  # 添加新的键'name_less'
    if 'children' in node and node['children'] is not None:
        for child in node['children']:
            add_key(child)

def fixUCharater(str):

    re.sub(r'\\u201.', '', str)
    # user_content = user_content.replace("\u2019", "'")











if __name__=="__main__":

    file_index=13
    file_index = 1
    # file_path = "t"+str(file_index)+".json"
    file_path = "f" + str(file_index) + "p.json"


    re_json=addSummary(file_path)
    # f=open("t"+str(file_index)+"_sum_test.json","w",encoding='utf-8')
    f = open("f" + str(file_index) + "p_sum_test.json", "w", encoding='utf-8')
    json.dump(re_json,f)
    f.close()



