import openai
# openai migrate
# export OPEN_API_KEY=
import os# 从环境变量中读取openai api key
os.environ["OPENAI_API_KEY"]= "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"

#上面的GPT-3.5-turbo是使用的GPT3.5模型 可以替换为其他模型如：
# gpt-4
# gpt-4-0314
# gpt-4-32k
# gpt-4-32k-0314
# ai_response = response.choices[0].message['content']
# print(ai_response)

def genGPTMp(input_text,mp_level):
    # openai.api_key = "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"
    input_word_num=len(input_text.split(" "))
    spec_word_count=300
    exp_word_num=spec_word_count*int(mp_level)/100
    if exp_word_num<10:
        exp_word_num=10
    exp_word_num_p=2*exp_word_num
    sys_content=f'You are a news reading expert,  and you are good at reading news articles and summarizing them precisely. ' \
            f'I will give you the report text and a specific word number, you need to summarize the news content, and the summary you generate should be around the specified number of words. ' \
            f'In order to do this, you need to get the gist of your essay, summarize it to the maximum extent possible, and meet the word count requirement. ' \
            f'Your generated profile word count should not more than 10 less than the word requirement. ' \
            f'Only return your generated summarization without showing word count.'
    # f'You must reduce the number of main points to 2 or less and turn each main point to keywords when the demand scale degree is too small' \
    # f'You choose use these ways to scale to remain the key information of the report.  ' \
    user_content=f'Here is the report \"{input_text}\" and word limit: {exp_word_num_p}'
    print("begin GPTing")
    resp = openai.chat.completions.create(temperature=0.0,model='gpt-4-1106-preview', messages=[
        {'role': 'system', 'content': sys_content},
        {"role":'user',"content":user_content}
    ])
    gpt_mp_content=resp.choices[0].message.content
    print(gpt_mp_content)
    print(resp.usage)
    print('demand len: ', exp_word_num)
    print('content len: ',len(gpt_mp_content.split(" ")))
    return gpt_mp_content
    # print(chat_res.generations[0][0].message.content)

if __name__=="__main__":
    # print("hello world")
    input_text=input('input your report\n')
    genGPTMp(input_text,5)