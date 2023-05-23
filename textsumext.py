import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extractive_summarization(document, num_sentences):
    # 문서를 문장 단위로 분리
    sentences = sent_tokenize(document)
    
    # 문장 벡터화
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    
    # 문장 간 유사도 계산
    similarity_matrix = cosine_similarity(X, X)
    
    # 중요한 문장 선택
    sentence_scores = [(sentence, score) for sentence, score in zip(sentences, similarity_matrix.sum(axis=1))]
    sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # 선택된 문장들을 요약 문서로 결합
    summary = ' '.join([sentence for sentence, _ in sentence_scores])
    
    return summary

# 예시 문서
with open("화알못.txt","r",encoding='UTF8')as f:
    point=f.readlines()
    text=' '.join(point)
document = text

# 추출적 요약 수행
# summary = extractive_summarization(document, num_sentences=2)
summary = extractive_summarization(document, num_sentences=2)
print(summary)
