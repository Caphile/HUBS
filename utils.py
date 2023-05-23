from tkinter import filedialog, Tk
import os, re

class Normalize:    # 정규화 함수
    def __init__(self):
        self.stopwords = readFile(os.getcwd(), 'Stopwords')
        for i in range(len(self.stopwords)):
            self.stopwords[i] = self.stopwords[i].replace('\n', '')

    def process(self, text):
        text = self.stripSCharacter(text)
        text = self.removeStopword(text)
        text = self.lowercase(text)
        return text

    def stripSCharacter(self, text):        # 특수문자 제거
        return re.sub('[^a-zA-Z0-9\s]', '', text)

    def removeStopword(self, text):         # 불용어 제거
        words = text.split()
        return ' '.join([word for word in words if word.lower() not in self.stopwords])

    def lowercase(self, text):              # 소문자화
        words = text.split()
        return ' '.join([word.lower() for word in words])

def filePaths(opt = 1):
    root = Tk()
    root.withdraw()

    if opt == 1:
        fullPaths = filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])
    elif opt == 2:
        fullPaths = filedialog.askopenfilenames(title = 'Select Excel File', initialdir = os.getcwd(), filetypes=[('Excel files',('*.csv', '*.xlsx')), ("All files", "*.*")])

    paths, names = [], []
    for p in fullPaths:
        temp = p.split('/')
        paths.append('/'.join(temp[ : -1]))
        names.append(temp[-1])
    
    return paths, names

def readFile(path, name):
    name = re.sub(r'.txt', '', name)
    with open(f'{path}/{name}.txt', 'r', encoding ='UTF8') as f:
        text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i].replace('\n', '')
    return text

def saveFile(path, name, text):
    with open(f'{path}/{name}.txt', 'w', encoding ='UTF8') as f:    # txt파일
        for line in text:
            f.write(line + '\n')