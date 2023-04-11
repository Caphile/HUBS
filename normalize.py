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

def addStopwords(): # �ҿ�� Ŀ����
    words = openFile('./Stopwords.txt')

    ASW = []    # additional stopwords
    for word in words:
        ASW.append(word)
    return ASW

class Normalize:    # ����ȭ �Լ�
    def __init__(self, text, stopwords):
        self.text = self.stripSCharacter(text)
        self.text = self.removeStopword(self.text, stopwords)
        self.text = self.lowercase(self.text)

    def stripSCharacter(self, text):        # Ư������ ����
        return re.sub('[^a-zA-Z0-9\s]', '', text)

    def removeStopword(self, text, SW):     # �ҿ�� ����
        words = text.split(' ')
        return ' '.join([word for word in words if word not in SW])

    def lowercase(self, text):              # �ҹ���ȭ
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
        if len(line) > 2 and line[-1 : ] == '\n':   # �ؽ�Ʈ �������� ���๮�� ����
            line = line[ : -1]

        newLine = Normalize(line, stopword_list).text
        if newLine != []:
            newText.append(newLine)

    saveFile(f'1{fName}', newText)

    break