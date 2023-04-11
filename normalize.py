# -*- coding: cp949 -*-

import nltk
from nltk.corpus import stopwords
import re

def stripSCharacter(text):  # 특수문자 제거
    stripped_text = re.sub('[^a-zA-Z0-9\s]', '', text)
    return stripped_text

def addStopwords(): # 불용어 커스텀
    file = open('./Stopwords.txt', 'r')
    
    ASW = []    # additional stopwords
    while 1:
        word = file.readline().strip('\n')
        if word == '':
            break
        ASW.append(word)
    file.close()

    return ASW

def removeStopword(SW):
    pass



nltk.download('stopwords')

stopwords = stopwords.words('english')
stopwords.append(addStopwords())



text = "Hi! Welcome to my channel. I'm really excited because it's been a long time since I haven't discussed a brand and its products."

# 불용어 제거
words = [word for word in text.split() if word.lower() not in stop_words]

print(words)
# 출력 결과: ['Hi!', 'Welcome', 'channel.', "I'm", 'really', 'excited', 'long', 'time', 'since', "haven't", 'discussed', 'brand', 'products.']
