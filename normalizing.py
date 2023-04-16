# -*- coding: cp949 -*-

import nltk
from nltk.corpus import stopwords
import os
import re

def searchPath(fileName):   # 현재 py와 같은 경로상에 스크립트 놓아야함
    rootDir = f'{os.getcwd()}/scripts'
    folders = [folder.path for folder in os.scandir(rootDir) if folder.is_dir()]    # HUBS 폴더의 하위 모든 폴더
    
    folderDirs = []
    fileName = '(res)script_en.txt'
    for folderDir in folders:
        if os.path.exists(f'{folderDir}/{fileName}'):
            folderDirs.append(folderDir)
    
    return folderDirs

def openFile(fileName):
    with open(fileName, 'r', encoding ='UTF8') as f:
        lines = f.readlines()
    return lines

def saveFile(fileName, text):
    with open(fileName, 'w') as f:
        for line in text:
            f.write(line + '\n')

def addStopwords(): # 불용어 커스텀
    words = openFile('./Stopwords.txt') # 소문자만 입력!

    ASW = []    # additional stopwords
    for word in words:
        if len(word) > 2 and word[-1 : ] == '\n':
            word = word[ : -1]
        ASW.append(word)
    return ASW

class Normalize:    # 정규화 함수
    def __init__(self, text, stopwords):
        self.text = self.stripSCharacter(text)
        self.text = self.removeStopword(self.text, stopwords)
        #self.text = self.lowercase(self.text)

    def stripSCharacter(self, text):        # 특수문자 제거
        return re.sub('[^a-zA-Z0-9\s]', '', text)

    def removeStopword(self, text, stopwords):     # 불용어 제거
        words = text.split(' ')
        return ' '.join([word for word in words if word.lower() not in stopwords])

    def lowercase(self, text):              # 소문자화
        words = text.split(' ')
        return ' '.join([word.lower() for word in words])

nltk.download('stopwords')
stopword_list = stopwords.words('english')
for stopword in addStopwords():
    stopword_list.append(stopword)

fileName = 'script_en.txt'
folderDirs = searchPath(fileName)

for folderDir in folderDirs:
    text = openFile(f'{folderDir}/(res){fileName}')

    newText = []
    for line in text:
        if len(line) > 2 and line[-1 : ] == '\n':   # 텍스트 마지막의 개행문자 제거
            line = line[ : -1]

        newLine = Normalize(line, stopword_list).text
        if newLine != []:
            newText.append(newLine)

    saveFile(f'{folderDir}/(norm){fileName}', newText)

    if not os.path.exists('norms'):
        os.mkdir('norms')
    fName = folderDir.split('\\')[-1]
    saveFile(f'norms/{fName}.txt', newText)