import difflib
import re
import json

def preprocess_text(text):
    # 移除文本中的标点符号，并转换为小写，以减少比较时的干扰
    # print(text)
    # text = re.sub(r'[^\w\s]', '', text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    # print(text)
    return text

def compare_lines(a, b):
    return a.strip() == b.strip()


def get_refined_word_differences(text1, text2):

    list1=text1.split(" ")
    # print(list1)
    list2=text2.split(" ")
    words1=[]
    for word in list1:
        word_p=preprocess_text(word)
        if word_p and len(word_p.strip()) > 0:
            words1.append(word_p)

    words2 = []
    for word in list2:
        word_p = preprocess_text(word)
        if word_p and len(word_p.strip()) > 0:
            words2.append(word_p)
    # # 预处理文本
    # preprocessed_1 = preprocess_text(text1)
    # preprocessed_2 = preprocess_text(text2)
    #
    # # 分割文本为单词列表
    # words1 = preprocessed_1.split()
    # words2 = preprocessed_2.split()

    # print(words1)
    # print(words2)
    # 使用SequenceMatcher找到差异
    seq_matcher = difflib.SequenceMatcher(None,words1,words2,autojunk=True)
    diffs = seq_matcher.get_opcodes()

    # 初始化记录添加和删除的单词列表
    added_words = []
    removed_words = []
    for diff in diffs:
        print(diff)
    cur_list=[]
    nxt_list=[]
    res_list=[]

    for tag, i1, i2, j1, j2 in diffs:
        # for i in range(i1,i2):
        #     cur_list.append({"word": list1[i], "tag": tag})
        # for i in range(j1, j2):
        #     nxt_list.append({"word": list2[i], "tag": tag})
        res_list.append({"tag":tag,"i1":i1,"i2":i2,"j1":j1,"j2":j2})



    # return {'added': added_words, 'removed': removed_words}
    # res_dict={"cur":cur_list,"nxt":nxt_list}
    print(res_list)
    return res_list


def diffGen(file_in_name,file_o_name):
    f = open(file_in_name, 'r')
    json1 = json.load(f)
    f.close()
    jsonData = json.loads(json.dumps(json1))
    for claim_data in jsonData["children"]:
        for i in range(5):
            attr_name="diffT"+str(i)
            if i==0:
                diff_content=get_refined_word_differences(claim_data["name"],claim_data["sum0"])
            else:
                sum1="sum"+str(i-1)
                sum2 = "sum" + str(i)
                diff_content=get_refined_word_differences(claim_data[sum1],claim_data[sum2])
            claim_data[attr_name]=diff_content

        for evi_data in claim_data["children"]:
            for i in range(5):
                attr_name = "diffT" + str(i)
                if i == 0:
                    diff_content = get_refined_word_differences(evi_data["name"], evi_data["sum0"])
                else:
                    sum1 = "sum" + str(i - 1)
                    sum2 = "sum" + str(i)
                    diff_content = get_refined_word_differences(evi_data[sum1], evi_data[sum2])
                evi_data[attr_name] = diff_content
                

    f=open(file_o_name,'w',encoding='utf-8')
    json.dump(jsonData, f)
    f.close()




if __name__ == "__main__":

    file_index=1
    # file_in_name="t"+str(file_index)+"_sum.json"
    # file_o_name="t"+str(file_index)+"_diff.json"
    file_in_name = "f" + str(file_index) + "p_sum_test.json"
    file_o_name = "f" + str(file_index) + "p_diff.json"

    diffGen(file_in_name,file_o_name)




    # # text_original = "Apple is the symbol of Apple Inc. and also a delicious and tasty fruit."
    # # text_modified = "Apple symbolizes Apple Inc and is also a tasty, delicious fruit. ..."
    #
    # text_original="Fani T. Willis, the district attorney of Fulton County, Ga., filed a motion on Monday seeking to block an appeal of a ruling last month allowing her to continue leading the state election interference case against former President Donald J. Trump"
    # text_modified="Fulton County District Attorney Fani T. Willis filed a motion to prevent an appeal against her continuing the election case against Donald Trump"
    #
    # word_diff_result = get_refined_word_differences(text_original, text_modified)
    # # print(word_diff_result)
    # # print("增加的单词:\n", word_diff_result['added'])
    # # print("删除的单词:\n", word_diff_result['removed'])