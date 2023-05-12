# -*- encoding= cp949 -*-

import spacy
from tkinter import filedialog, Tk
import os

#-------------------------------------------------------------------------------------
# 모델명(경로), 추후에 유동적으로 선택 가능하게끔 바꿀 여지 있음
modelName = 'ner_model'
# 하이퍼파라미터
HP = {
    'dropout'   :   0.5,
    'minBatch'  :   4.0,
    'maxBatch'  :   32.0,
    'learnRate' :   0.01,
    'epochs'    :   10
    }
# 라벨
labels = ['PRODUCT', 'DESCRIPTION']
# 확률(predict)
probability = 0.5
#-------------------------------------------------------------------------------------

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    global modelName
    print('1. 커스텀 모델 생성')
    print('2. 기존 모델 사용')
    print('====================================')
    print('선택 : ', end = '')
    opt = int(input())
    if opt == 1:
        setModel()
        model = spacy.load(modelName)
    elif opt == 2:
        try:
            print('커스텀 모델 사용')
            model = spacy.load(modelName)
        except:
            print('오픈소스로 제공된 모델 사용')
            model = spacy.load('en_core_web_sm')
    return model

def saveModel():
    pass

def setModel():
    from spacy.util import minibatch, compounding
    import random

    trainData = []
    print('학습용 데이터 읽기')
    fp = filePaths()
    for f in fp:
        with open(f, 'r', encoding ='UTF8') as f:
            fullText = f.read()
            lines = fullText.split('\n')

            trainData.append(lines)
            
    # trainData = [("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})]
    # 위와 같은 형태의 trainData 제작해야 함

    model = spacy.blank('en')
    model.add_pipe("ner")
    ner = model.get_pipe('ner')
    for label in labels:
        ner.add_label(label)

    model.begin_training()

    global HP
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

#-------------------------------------------------------------------------------------
    
os.system('cls')
model = loadModel()
print('스크립트 읽기')
fp = filePaths()

# 유튜브 스크립트에서 추출한 텍스트
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
                    if entity.label_ == 'PRODUCT':
                        prod.append(entity.text)

                # 텍스트 분류를 통한 화장품 설명 추출
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = model(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > probability:   # 확률 조정
                        descriptions.append(sentence)

        print('화장품 명:', ' '.join(prod))
        print('화장품 설명:', ' '.join(desc))