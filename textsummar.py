import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest

def summarize_text(text, n):
    # 텍스트 전처리: 문장 토큰화, 단어 토큰화, 불용어 제거
    sentences = sent_tokenize(text) #sent_tokenize() 함수는 주어진 텍스트를 문장으로 나누어 리스트 형태로 반환합니다. 각 문장은 텍스트에서 문장 구분 기호(온점, 느낌표, 물음표 등)를 기준으로 분리됩니다.
    words = word_tokenize(text) 
    stop_words = set(stopwords.words('english')) #NLTK에서 제공하는 영어 stopwords를 가져오는 함수입니다. 이렇게 가져온 stopwords를 stop_words 변수에 할당하여 사용할 수 있습니다. 이후에는 텍스트에서 stop_words에 포함된 단어들을 제거하고 분석을 진행할 수 있습니다
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]

    # 단어의 빈도 계산
    word_freq = defaultdict(int) #defaultdict(int)는 int라는 내장 함수를 기본값으로 사용하는 defaultdict입니다. int는 0으로 초기화되는 기본값을 가지는 함수입니다
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
with open("올영베스트.txt","r",encoding='UTF8')as f:
    point=f.readlines()
    text=' '.join(point)
summary = summarize_text(text,1) #(text,n) n 은 상위 n개의 문장이 출력되도록 조정이 가능함.
print(summary) 
