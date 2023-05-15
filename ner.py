import spacy
from spacy.training.example import Example
import os
import json
import utils

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
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)
        for line in text:
            trainData.append(eval(line))
            
    model = spacy.blank('en')
    model.add_pipe("ner")
    ner = model.get_pipe('ner')
    model.add_pipe('parser')
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
            examples = []
            for text, annotation in batch:
                doc = model.make_doc(text)
                example = Example.from_dict(doc, annotation)
                examples.append(example)
            try:
                model.update(
                    examples, drop = HP['dropout'], losses = losses,
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
fp, fn = utils.filePaths()

# 유튜브 스크립트에서 추출한 텍스트
for p, n in zip(fp, fn): 
    text = utils.readFile(p, n)

    prod = []
    desc = []
    for line in text:
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