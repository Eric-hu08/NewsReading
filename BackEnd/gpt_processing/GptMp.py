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
    sys_content=f'You are a news reading expert,  and you are good at reading news articles and summarizing them precisely' \
            f'I will give you the report text and a scale degree. '\
            f'You need to summarize the given report depend on a scale degree.' \
            f'The scale number I give you is a number from 0-100. If it is 100, it means you just return the original text. ' \
            f'If it is not 100, it means you need to reduce the number of words by summarizing the report while keeping the key information of the original report as much as possible. ' \
            f'The smaller the scale degree, the fewer words you will end up returning' \
            f'If the scale degree is near to 0, you may need to summarize the report in few sentences with few words.' \
            f'Only return the scaled summarization.'
    # f'You must reduce the number of main points to 2 or less and turn each main point to keywords when the demand scale degree is too small' \
    # f'You choose use these ways to scale to remain the key information of the report.  ' \
    user_content=f'Here is the report \"{input_text}\" and scale degree: {mp_level}'
    print("begin GPTing")
    resp = openai.chat.completions.create(temperature=0.0,model='gpt-4-1106-preview', messages=[
        {'role': 'system', 'content': sys_content},
        {"role":'user',"content":user_content}
    ])
    gpt_mp_content=resp.choices[0].message.content
    print(gpt_mp_content)
    print(resp.usage)
    return gpt_mp_content
    # print(chat_res.generations[0][0].message.content)

if __name__=="__main__":
    # print("hello world")
    input_text=input('input your report\n')
    genGPTMp(input_text,5)