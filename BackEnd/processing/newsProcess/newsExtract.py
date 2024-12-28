import openai
import time
import re
import spacy
from spacy.pipeline.sentencizer import Sentencizer
import json
from spacy.language import Language
from spacy.matcher import Matcher
# openai migrate
# export OPEN_API_KEY=
import os# 从环境变量中读取openai api key
import os# 从环境变量中读取openai api key
os.environ["OPENAI_API_KEY"]= "sk-Uk5VveC2gP1MfREI11C89527986f401aAf9492A1F0D89b42"

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
    #solve the chinese Punctuation problem
    # text_str = text_str.replace("\u2019", "'")
    # text_str = text_str.replace("”", "\"")
    # text_str = text_str.replace("“", "\"")
    f.close()
    return text_str
def file_read_title(file_path):
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
    title=text.pop(0)
    text_str = " ".join(text)
    f.close()
    return title,text_str
def annRestruct(ann_list,title):
    #turn ann_list from dict list to tree dataset
    tree_dict=dict()
    tree_dict["name"]=title
    tree_dict["type"]="title"
    tree_dict["index"]=0
    tree_dict["children"]=list()
    temp_dict=dict()
    cur_i_list=list()
    for ann in ann_list:    #first traverse get claim list
        temp_dict["name"]=ann["sen"].strip()
        #idf C or E
        # if 'C' in ann['ann']:
        if ann['ann'].count('$')==1:   #filter to claim
            if 'MC'in ann['ann']:  #claim is MC
                claim_i=0
                claim_str='MC'
            elif 'S' in ann['ann']: #claim is C_S
                claim_i_1=ann["ann"].split('_')[1]
                claim_i_2 = ann["ann"].split('_')[3].split(')')[0]  #去除）
                claim_i=claim_i_1+'-'+claim_i_2
            else: # claim is C
                claim_str = ann["ann"].split('_')[1]
                end_i = claim_str.find(')')
                claim_i = claim_str[:end_i]
            # claim_str=ann["ann"].split('_')[1]
            # end_i=claim_str.find(')')
            # claim_i=claim_str[:end_i]
            # claim_i=int(claim_i)
            # f_1=0
            # for i in range(len(cur_i_list)-2):
            #     cur_i=cur_i_list[i]
            #     cur_i_next=cur_i_list[i+1]
            #     list_i=i+1
            #     if claim_i>cur_i and claim_i<cur_i_next:
            #         cur_i_list.insert(i+1,claim_i)
            #         f_1=1
            #         break
            # if f_1==0:
            #     cur_i_list.append(claim_i)
            #     list_i=len(cur_i_list)
            cur_i_list.append(claim_i)
            temp_dict["type"]="C"
            temp_dict["index"]=claim_i
            temp_dict["children"]=list()
            # tree_dict["children"].insert(list_i+1,temp_dict.copy())
            tree_dict["children"].append(temp_dict.copy())
    #before load all C then next load all E
    temp_dict["children"]=None
    temp_C_index=0
    temp_E_index=0
    # print("c index list:",cur_i_list)
    for ann in ann_list:
        temp_dict["name"] = ann["sen"].strip()

        if '$E' in ann['ann']:
            evi_type_str = ann['ann'].split('$')[1]
            evi_type = evi_type_str.split('_')[1]
            c_index_str=ann['ann'].split('$')[2].split(')')[0]
            if 'MC' in ann['ann']:
                temp_C_index=0
            elif 'S' in c_index_str:
                # print(ann['ann'])
                temp_C_index1=c_index_str.split('_')[1]
                temp_C_index2 = c_index_str.split('_')[3]
                temp_C_index=temp_C_index1+'-'+temp_C_index2
            else: # regular claim C_i
                temp_C_index=c_index_str.split('_')[1]

            # evid_list=ann["ann"].split('_')
            # evid_type='E_'+evid_list[2][0]
            # evid_i=int(evid_list[1])
            # if evid_i!=temp_C_index:
            #     temp_C_index=evid_i
            #     temp_E_index=0
            # else:
            #     temp_E_index+=1

            temp_dict["type"]=str(evi_type)
            # temp_dict["index"]=str(temp_C_index)+"_"+ str(temp_E_index)
            temp_dict["index"] = str(temp_C_index)    #之后再加E的index
            # if temp_C_index not in cur_i_list:
            #     print("evid index error!!")
            #     print(temp_C_index)
            #     print(cur_i_list)
            #     exit(111)
            # list_i=cur_i_list.index(temp_C_index)
            try:

                list_i=cur_i_list.index(temp_C_index)
                # print(temp_C_index, "list_i",list_i)
            except ValueError:
                print("c index 不存在！")
            tree_dict["children"][list_i]["children"].append(temp_dict.copy())


    #Todo count all to check whether miss
    return tree_dict

def treeRestruct(tree_dict):
    c_list=tree_dict['children']
    for index,claim_dict in enumerate(c_list):


        for i in range(len(claim_dict['children'])):
            # set Evi index
            c_index=claim_dict['children'][i]['index']
            claim_dict['children'][i]['index']=c_index+'_'+str(i)

        # reset claim index
        claim_index = claim_dict['index']
        claim_dict['index']=index+1
        claim_dict['s_index']=claim_index


    return tree_dict

def responseRead(res_content,file_path,title):

    RedunSen_f=redunSenCheck(res_content)
    annotated_f,ann_list=annotationExtract(res_content)
    relation_f,relation_list=relationExtract(res_content)
    if RedunSen_f or annotated_f or relation_f:
        print("extract error! stop extracting")
        # mainGen(file_path)
    else:
        print("————————————————————————————")
        print(ann_list)
        print("————————————————————————————")
        print(relation_list)
        print("————————————————————————————")
        tree_dict=annRestruct(ann_list,title)
        print(tree_dict)
        print("————————————————————————————")
        tree_dict_pro = treeRestruct(tree_dict)
        print(tree_dict_pro)
        print("————————————————————————————")
        return tree_dict_pro




def redunSenCheck(res_content):
    nlp = spacy.load("en_core_web_sm")

    # 添加Sentencizer组件，用于分句
    sentencizer = Sentencizer()
    nlp.add_pipe("sentencizer")
    doc = nlp(res_content)
    res_sen_list=[sentence for sentence in doc.sents]
    # res_sen_list=res_content.split(".")
    seen = set()  # 创建一个空集合来存储已经看到的句子
    repeated = set()  # 创建一个空集合来存储重复的句子

    for sentence in res_sen_list:
        if sentence in seen:  # 如果这个句子已经在seen集合中，那么它就是重复的
            repeated.add(sentence)
        seen.add(sentence)  # 将这个句子添加到seen集合中
    if len(repeated)!=0:
        print("reduntent! reduntent content: :",repeated)
        return True
    return False




def annotationExtract(res_content):
    str_start="|passage start|"
    str_end="|passage end|"
    ann_f=False

    ann_dict_list = []
    if (str_start in res_content) and (str_end in res_content):
        ann_content=res_content[res_content.find(str_start)+len(str_start):res_content.find(str_end)]
        index_m1=ann_content.find("($C_1).")
        index_m2 = ann_content.find(".($C_1)")
        f_m1=(index_m1!=-1)
        f_m2 = (index_m2 != -1)
        if (f_m1 and not f_m2) or (not f_m1 and f_m2):
            nlp = spacy.load("en_core_web_sm")
            # 添加Sentencizer组件，用于分句
            sentencizer = Sentencizer()
            # nlp.add_pipe(sentencizer,name="sentencizer",before="parser")
            nlp.add_pipe("sentencizer")

            doc=nlp(ann_content)
            temp_str = ""
            ann_sen_list = []
            pattern = re.compile("[\"”“]")
            f_inQuote = False
            for i in range(len(doc)):
                temp_str += doc[i].text
                temp_str += doc[i].whitespace_
                # print(doc[i],doc[i].text)

                if bool(pattern.search(doc[i].text)):
                    f_inQuote = not f_inQuote
                    # print("quote count:",doc[i:i+4])
                if doc[i].is_sent_end:
                    # if f_inQuote and i + 1 < len(doc):
                    if not f_inQuote:
                        ann_sen_list.append(temp_str)
                        temp_str = ""

            if f_inQuote==True:
                print("quote error!!!")
                exit(222)

            ann_dict=dict()

            if f_m1:
                #mode1
                for ann_sen in ann_sen_list:
                    if len(ann_sen)==0:
                        continue
                    index_a=ann_sen.find("($")
                    ann_dict["sen"]=ann_sen[:index_a]
                    ann_dict["ann"]=ann_sen[index_a:]
                    ann_dict_list.append(ann_dict.copy())

            else:
                #mode2
                temp_sen=""
                for ann_sen in ann_sen_list:
                    if len(ann_sen)==0:
                        continue
                    index_a=ann_sen.find("($")
                    ann_dict["sen"] = temp_sen
                    temp_sen=ann_sen[:index_a]
                    if index_a==-1:
                        continue

                    ann_dict["ann"]=ann_sen[index_a:]
                    ann_dict_list.append(ann_dict.copy())
        else:
            print("annotation mode check false!")
            ann_f=True
    else:
        ann_f=True
        print(str_start in res_content)
        print(str_end in res_content)
        print("annotation check false!")
    return ann_f,ann_dict_list

def relationExtract(res_content):
    relation_f=False
    str_start="|passage end|"
    index_start=res_content.find(str_start)+len(str_start)
    relation_content=res_content[index_start:]
    pattern = r'\[(.*?)\]'  # 正则表达式，匹配[]内的内容
    relation_list = re.findall(pattern, res_content)
    relation_dict_list=[]
    relation_dict=dict()
    for relation in relation_list:
        index_r=relation.find("($")
        if index_r==-1:
            print("relation extract error!!!")
            relation_f=True
            return relation_f,relation_dict_list
        relation_dict["sen"]=relation[:index_r]
        relation_dict["ann"]=relation[index_r:]
        relation_dict_list.append(relation_dict.copy())
    return relation_f,relation_dict_list

def mainGen(file_path,file_index):
    start_time1 = time.time()
    # file_path = "news10 copy.txt"
    user_content = "This text is mainly about:"
    title,newsText=file_read_title(file_path)

    user_content = user_content + title + "\n"
    user_content = user_content + "Passage: |passage start|\n"
    user_content = user_content + newsText + "\n"
    user_content = user_content + "|passage end|\nResponse: Let's think step−by−step and read it line −by−line."
    # promp1_path="sys_prompt.txt"

    prompt1_path = "./prompts/am_p_7_1.txt"

    sys_content = file_read(prompt1_path)
    # add shot content
    # shot_am_dir = "shot_am2"
    # shot_am_file_list = os.listdir(shot_am_dir)
    # shot_am_content = ""
    # for shot_am_file_name in shot_am_file_list:
    #     shot_am_content = shot_am_content + "exmaple: \n" + file_read(
    #         os.sep.join([shot_am_dir, shot_am_file_name])) + "\n"

    # shot_content = file_read(shot1_path)
    # sys_content = sys_content + shot_am_content

    start_time2 = time.time()
    print("begin gpting")
    resp = openai.chat.completions.create(model='gpt-4o',
                                          temperature=0.00000001,
                                          messages=[{'role': 'system', 'content': sys_content},
                                                    {'role': 'user', "content": user_content}]
                                          )
    gpt_mp_content = resp.choices[0].message.content

    end_time1 = time.time()
    print(gpt_mp_content)
    # gpt_mp_content = gpt_mp_content.replace("\u2019", "'")
    # gpt_mp_content = gpt_mp_content.replace("”", "\"")
    # gpt_mp_content = gpt_mp_content.replace("“", "\"")
    print(resp.usage)
    # print(resp)
    # print(resp.usage)
    print("generate time cost: ", end_time1 - start_time2)
    print("total time cost: ", end_time1 - start_time1)

    f=open("f-ans"+str(file_index)+"p.txt","w",encoding="utf-8")
    # f = open("s-ans" + str(file_index) + "p.txt", "w", encoding="utf-8")

    f.writelines(gpt_mp_content)
    f.close()
    tree_dict=responseRead(gpt_mp_content,file_path,title)
    # with open("t"+str(file_index)+".json", "w", encoding="utf-8") as fp:
    with open("f" + str(file_index) + "p.json", "w", encoding="utf-8") as fp:
        json.dump(tree_dict, fp)
    fp.close()

# print(ai_response)
def testfunc(file_path):
    str=file_read(file_path)
    f=open("testtest.txt","w",encoding="utf-8")
    f.writelines(str)
    f.close()
def newsExtract():
    file_index = 4
    file_path = "f-news" + str(file_index) + ".txt"
    mainGen(file_path, file_index)

if __name__=="__main__":


    file_name = "f-news" + str(file_index) + ".txt"
    file_path = "../"
    # testfunc(file_path)
    mainGen(file_path,file_index)
