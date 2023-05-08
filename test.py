# -*- encoding= cp949 -*-

import spacy
from tkinter import filedialog, Tk
import os

modelName = 'ner_model' # 추후에 선택 가능하게끔 바꿀 여지 있음

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    print('1. 커스텀 모델 생성')
    print('2. 기존 모델 사용')
    opt = int(input())
    if opt == 1:
        model = spacy.blank('en')
        setModel(model)

    elif opt == 2:
        global modelName
        try:
            print('커스텀 모델 사용')
            model = spacy.load(modelName)
        except:
            print('오픈소스로 제공된 학습된 모델 사용')
            model = spacy.load('en_core_web_sm')
    return model

def saveModel():
    pass

def setModel(model):
    from spacy.util import minibatch, compounding
    import random

    trainData = []
    print('학습용 데이터 읽기')
    fp = filePaths()
    for f in fp:
        with open(f, 'r', encoding ='UTF8') as f:
            fullText = f.read()
            lines = fullText.split('\n')

            trainData.append(lines)     # lines 예시 : ("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})
            
    # 파이프
    ner = model.add_pipe("ner")
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]

    # 라벨
    ner.add_label("PRODUCT")
    ner.add_label("ORG")

    # 하이퍼파라미터
    epochs = 10

    with model.disable_pipes(*unaffected_pipes):
      # Training for 30 iterations
      for iteration in range(epochs):

        # shuufling examples  before every iteration
        random.shuffle(trainData)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(trainData, size = compounding(4.0, 32.0, 1.001)) #시작크기, 최대크기, 증가율
        for batch in batches:   # 데이터의 묶음
            texts, annotations = zip(*batch)
            model.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses
                    )
            print("Losses", losses)

    global modelName
    model.to_disk(modelName)

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
                    if entity.label_ == "PRODUCT":
                        prod.append(entity.text)

                # 텍스트 분류를 통한 화장품 설명 추출
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = model(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > 0.5:   # 확률이 n이상인
                        descriptions.append(sentence)

        print("화장품 명:", ' '.join(prod))
        print("화장품 설명:", ' '.join(desc))