from tkinter import filedialog, Tk
import os

def filePaths():
    root = Tk()
    root.withdraw()
    fullPaths = filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

    paths, names = [], []
    for p in fullPaths:
        temp = p.split('/')
        paths.append('/'.join(temp[ : -1]))
        names.append(temp[-1])
    
    return paths, names

def readFile(path, name):
    with open(f'{path}/{name}', 'r', encoding ='UTF8') as f:
        text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i].replace('\n', '')
    return text

def saveFile(path, name, text):

    with open(f'{path}/{name}', 'w', encoding ='UTF8') as f:
        for line in text:
            f.write(line + '\n')