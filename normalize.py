# -*- coding: cp949 -*-

import nltk
from nltk.corpus import stopwords
import re

def openFile(fileName):
    with open(fileName, 'r') as f:
        lines = f.readlines()
    return lines

def saveFile(fileName, text):
    with open(fileName, 'w') as f:
        for line in text:
            f.write(line + '\n')

def addStopwords(): # 불용어 커스텀
    words = openFile('./Stopwords.txt')

    ASW = []    # additional stopwords
    for word in words:
        ASW.append(word)
    return ASW

class Normalize:    # 정규화 함수
    def __init__(self, text, stopwords):
        self.text = self.stripSCharacter(text)
        self.text = self.removeStopword(self.text, stopwords)
        self.text = self.lowercase(self.text)

    def stripSCharacter(self, text):        # 특수문자 제거
        return re.sub('[^a-zA-Z0-9\s]', '', text)

    def removeStopword(self, text, SW):     # 불용어 제거
        words = text.split(' ')
        return ' '.join([word for word in words if word not in SW])

    def lowercase(self, text):              # 소문자화
        words = text.split(' ')
        return ' '.join([word.lower() for word in words])

nltk.download('stopwords')
stopword_list = stopwords.words('english')
stopword_list.append(addStopwords())

while 1:
    fName = 'script_en.txt'
    text = openFile(fName)

    newText = []
    for line in text:
        if len(line) > 2 and line[-1 : ] == '\n':   # 텍스트 마지막의 개행문자 제거
            line = line[ : -1]

        newLine = Normalize(line, stopword_list).text
        if newLine != []:
            newText.append(newLine)

    saveFile(f'1{fName}', newText)

    break