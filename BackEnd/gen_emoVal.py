import openai
# openai migrate
# export OPEN_API_KEY=
import os# 从环境变量中读取openai api key
import time
import json
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
def genGpt(input_str):

    user_content = input_str
    # promp1_path="sys_prompt.txt"
    # promp1_path = "am_p_1.txt"
    sys_content = "You are a nlp master.You will get a sentence, Summarize the sentence"\
                  "Only the summary sentence is returned" \
                  "In order to do this, you need to get the gist of your essay, summarize it to the maximum extent possible"

    resp = openai.chat.completions.create(model='gpt-4-1106-preview',
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role': 'user', "content": user_content}]
                                          )
    gpt_mp_content = resp.choices[0].message.content
    print(gpt_mp_content)
    print(resp.usage)
    return gpt_mp_content
def add_key(node):
    if node is None:
        return

    name_less=genGpt(node["name"])
    node['name_less'] = name_less  # 添加新的键'name_less'
    if 'children' in node and node['children'] is not None:
        for child in node['children']:
            add_key(child)

def genReCE(claim_n,evi_list):
    prompt1_path = "am_p_5_3.txt"
    # prompt1_path= "sys_p_2.txt"
    sys_content = file_read(prompt1_path)
    user_content="here is the claim and its evidence,claim: |claim start| "+claim_n+"|claim end|"
    evi_content="Here is the evidences:"
    for index,element in enumerate(evi_list):
        evi_content=evi_content+"E_"+str(index)+"_"+str(element["type"])+": |evidence start|"+element["name"]+"|evidence end| "
    user_content=user_content+evi_content
    start_time2 = time.time()
    print(user_content)
    print("begin gpt")
    resp = openai.chat.completions.create(model='gpt-4-1106-preview',
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role':'user',"content":user_content}])

    end_time1 = time.time()
    gpt_mp_content = resp.choices[0].message.content
    print(gpt_mp_content)
    print(resp.usage)
    print("time cost: ",end_time1-start_time2)
    # f = open("re-shot" + ".txt", "a+")
    # user_content=user_content.replace("\u2019","'")
    # user_content = user_content.replace("”", "\"")
    # user_content = user_content.replace("“", "\"")
    # gpt_mp_content = gpt_mp_content.replace("\u2019", "'")
    # gpt_mp_content = gpt_mp_content.replace("”", "\"")
    # gpt_mp_content = gpt_mp_content.replace("“", "\"")
    # q_content="Question: "+user_content+"\n"
    # a_content="Answer: "+gpt_mp_content+"\n"
    # f.writelines(q_content)
    # f.writelines(a_content)
    # f.close()
    return gpt_mp_content

def genEmo(flat_list):
    prompt1_path = "em_p_1.txt"
    # prompt1_path= "sys_p_2.txt"
    sys_content = file_read(prompt1_path)
    user_content="Here is the article: |article start| "
    for sen in flat_list:
        user_content+="|sentence start|"+sen+"|sentence end|"
    user_content+="|article end|"


    start_time2 = time.time()
    # print(user_content)
    print("begin gpt")
    resp = openai.chat.completions.create(model='gpt-4o',
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role':'user',"content":user_content}])

    end_time1 = time.time()
    gpt_mp_content = resp.choices[0].message.content
    print(gpt_mp_content)
    print(resp.usage)
    print("time cost: ",end_time1-start_time2)
    # f = open("re-shot" + ".txt", "a+")
    # user_content=user_content.replace("\u2019","'")
    # user_content = user_content.replace("”", "\"")
    # user_content = user_content.replace("“", "\"")
    # gpt_mp_content = gpt_mp_content.replace("\u2019", "'")
    # gpt_mp_content = gpt_mp_content.replace("”", "\"")
    # gpt_mp_content = gpt_mp_content.replace("“", "\"")
    # q_content="Question: "+user_content+"\n"
    # a_content="Answer: "+gpt_mp_content+"\n"
    # f.writelines(q_content)
    # f.writelines(a_content)
    # f.close()
    return gpt_mp_content

if __name__=="__main__":


    file_path = "t10_correct.json"
    f=open(file_path,'r')
    jsonData=json.load(f)
    json1= json.loads(json.dumps(jsonData))
    ret_list=[]
    flat_list=[]
    for claim in json1["children"]:
        claim_n=claim["name"]
        evidence_list=[]
        flat_list.append(claim_n)

        for evi in claim["children"]:
            temp_dict = {}
            temp_dict["name"]=evi["name"]
            temp_dict["type"]=evi["type"].split("_")[-1]
            evidence_list.append(temp_dict.copy())
            flat_list.append(evi["name"])


    ans_list=genEmo(flat_list)
    # print(ans_list)


