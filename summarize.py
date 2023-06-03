import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from collections import defaultdict
from heapq import nlargest

class TextSummarizer:
    def __init__(self):
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))

    def summarize_text(self, text, n):
        # 텍스트 전처리: 문장 토큰화, 단어 토큰화, 불용어 제거
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word.lower() for word in words if word.isalnum()]
        words = [word for word in words if word not in self.stop_words]

        # 품사 태깅
        tagged_words = nltk.pos_tag(words)
        interjections = ["UH"]

        # 감탄사만 제거한 문장
        words = [word for word, tag in tagged_words if tag not in interjections]

        def remove_strings(text, strings_to_remove):
            for string in strings_to_remove:
                text = text.replace(string, "")
            return text

        strings_to_remove = ["oh", "music", "Music", "Hello", "Today", "Now", "Applause", "[", "]"]
        words = remove_strings(text, strings_to_remove)

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




# 텍스트 파일 열기
#file_path = "(res) 8.7.txt"  (res) 8.7 텍스트를 사용할 경우 예시
#with open(file_path, "r",encoding='UTF8') as file:
#    text = file.read() text 변수에 사용할 텍스트 넣기

text = "사용할 텍스트 넣는곳"
n = 1

summarizer = TextSummarizer()
summary = summarizer.summarize_text(text, n)
print(summary)