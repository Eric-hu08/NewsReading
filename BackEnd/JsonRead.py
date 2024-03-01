import json

def readJson(mp_level,cur_i):
    file_name="j"+str(cur_i)+" copy.json"
    file_path="./"+file_name
    fp=open(file_path,"r")
    # print(fp)
    jsondata=json.load(fp)

    fp.close()
    # print(jsondata)
    return jsondata

def readText(cur_i):
    file_name="j"+str(cur_i)+".txt"
    file_path="./"+file_name
    fp=open(file_path,"r",encoding='utf-8')
    # print(fp)
    textData=fp.readlines()
    # text_content=" ".join(textData)
    fp.close()
    # print(jsondata)
    return textData

if __name__=="__main__":
    readJson(1,cur_i=2)