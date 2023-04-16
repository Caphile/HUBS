# -*- coding: cp949 -*-

import nltk
from nltk.tokenize import sent_tokenize
from tkinter import filedialog, Tk
import os

nltk.download('punkt')

def openFile():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def editFile(title, text, lang = 'en'):
    path = f'scripts/{title}/(res)script_{lang}.txt'
    with open(path, 'w', encoding = 'UTF-8') as f:
        for t in text:
            f.write(t+'\n')

filePaths = openFile()

for f in filePaths:
    with open(f, 'r', encoding='utf-8') as f:
        fullText = f.read()
        lines = fullText.split('\n')

    text = ''
    for line in lines:
        if line != '':
            text += line
    newText = sent_tokenize(text)

    editFile(f.name.split('/')[-2], newText)