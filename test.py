# -*- encoding= cp949 -*-

import spacy
from tkinter import filedialog, Tk
import os

modelName = 'ner_model' # ���Ŀ� ���� ���� �����ϰԲ� �ٲ� ���� ����

# hyperparam
HP = {
    'dropout'   :   0.5,
    'minBatch'  :   4.0,
    'maxBatch'  :   32.0,
    'learnRate' :   0.01,
    'epochs'    :   10
    }

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    print('1. Ŀ���� �� ����')
    print('2. ���� �� ���')
    opt = int(input())
    if opt == 1:
        setModel()

    elif opt == 2:
        global modelName
        try:
            print('Ŀ���� �� ���')  # ���� �״�� �������, Ʃ�� �� ������� ���� �ؾ���
            model = spacy.load(modelName)
        except:
            print('���¼ҽ��� ������ �н��� �� ���')
            model = spacy.load('en_core_web_sm')
    return model

def saveModel():
    pass

def setModel():
    from spacy.util import minibatch, compounding
    import random

    trainData = []
    print('�н��� ������ �б�')
    fp = filePaths()
    for f in fp:
        with open(f, 'r', encoding ='UTF8') as f:
            fullText = f.read()
            lines = fullText.split('\n')

            trainData.append(lines)
            
    # trainData = [("�̹��� �Ұ��� ��ǰ�� ���ӹ̹��� ���̼����� �ȷ�Ʈ�Դϴ�.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})]
    # ���� ���� ������ trainData �����ؾ� ��

    model = spacy.blank('en')
    model.add_pipe("ner")
    ner = model.get_pipe("ner")
    ner.add_label("PRODUCT")

    global HP
    model.begin_training()
    for itn in range(HP['epochs']):
        random.shuffle(trainData)
        losses = {}
        batches = minibatch(
            trainData,
            size = compounding(HP['minBatch'], HP['maxBatch'], HP['learnRate']),
        )
        for batch in batches:
            texts, annotations = zip(*batch)
            try:
                model.update(
                    texts, annotations, drop = HP['dropout'], losses = losses,
                )
            except:
                pass

        print(f"{itn} Losses", losses)

    global modelName
    model.to_disk(modelName)
    
os.system('cls')
model = loadModel()
print('��ũ��Ʈ �б�')
fp = filePaths()

# ��Ʃ�� ��ũ��Ʈ���� ������ �ؽ�Ʈ
for f in fp:
    with open(f, 'r', encoding ='UTF8') as f:
        fullText = f.read()
        lines = fullText.split('\n')

        prod = []
        desc = []
        for line in lines:
            if line != '':
                doc = model(line)

                for entity in doc.ents:
                    if entity.label_ == "PRODUCT":
                        prod.append(entity.text)

                # �ؽ�Ʈ �з��� ���� ȭ��ǰ ���� ����
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = model(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > 0.5:   # Ȯ���� n�̻���
                        descriptions.append(sentence)

        print("ȭ��ǰ ��:", ' '.join(prod))
        print("ȭ��ǰ ����:", ' '.join(desc))