import nltk
import json
from nltk.sentiment import SentimentIntensityAnalyzer

# 下载情感分析模型（首次运行时需要下载）
# nltk.download('vader_lexicon')

# 示例文本
text = "I love using NLTK for sentiment analysis, it's fantastic!"

# 初始化情感分析器
sia = SentimentIntensityAnalyzer()

# 获取情感分析结果
sentiment_scores = sia.polarity_scores(text)

# 输出情感分析结果
print("Sentiment Scores:", sentiment_scores)

# 判断情感倾向
if sentiment_scores['compound'] >= 0.05:
    print("Positive sentiment")
elif sentiment_scores['compound'] <= -0.05:
    print("Negative sentiment")
else:
    print("Neutral sentiment")

def emoVal(file_path):
    f = open(file_path, 'r')
    json1 = json.load(f)
    jsonData = json.loads(json.dumps(json1))
    # 初始化情感分析器
    sia = SentimentIntensityAnalyzer()
    claim_json_list=jsonData["children"]

    emo_flat_list=[]
    for claim_json in claim_json_list:
        claim_text=claim_json["name"]
        sentiment_scores = sia.polarity_scores(claim_text)["compound"]
        emo_flat_list.append(sentiment_scores)
        for evi_json in claim_json["children"]:
            evi_text=evi_json["name"]
            sentiment_scores = sia.polarity_scores(evi_text)["compound"]
            emo_flat_list.append(sentiment_scores)

    return emo_flat_list






if __name__=="__main__":
    file_path="../t10_correct.json"
    emo_flat_list=emoVal(file_path)
    print(emo_flat_list)

