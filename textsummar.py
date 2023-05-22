import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest

def summarize_text(text, n):
    # 텍스트 전처리: 문장 토큰화, 단어 토큰화, 불용어 제거
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]

    # 단어의 빈도 계산
    word_freq = defaultdict(int)
    for word in words:
        word_freq[word] += 1

    # 문장의 점수 계산
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] += word_freq[word]

    # 상위 n개의 문장 선택
    summary_sentences = nlargest(n, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

# 예시 사용법 
with open("화알못.txt","r",encoding='UTF8')as f:
    point=f.readlines()
    text=' '.join(point)
summary = summarize_text(text, 2)
print(summary)