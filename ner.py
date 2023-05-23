from tkinter import N
import spacy
from spacy.training.example import Example
import os
import utils

#-------------------------------------------------------------------------------------
# 모델명(경로), 추후에 유동적으로 선택 가능하게끔 바꿀 여지 있음
modelName = 'ner_model'
# 하이퍼파라미터
HP = {
    'dropout'   :   0.3,
    'minBatch'  :   10,
    'maxBatch'  :   32,
    'learnRate' :   0.01,
    'epochs'    :   75,
    'patience'  :   100
}
# 라벨
labels = ['PRODUCT']
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

def setModel():
    from spacy.util import minibatch, compounding
    import random

    ds = []
    print('학습용 데이터 읽기')
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)
        for line in text:
            ds.append(eval(line))

    dataSize = len(ds)
    splitIdx = int(0.8 * dataSize)

    trainData = ds[ : splitIdx]
    validationData = ds[splitIdx : ]

    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    ner = nlp.create_pipe('ner')
    for label in labels:
        ner.add_label(label)
    nlp.add_pipe('ner')

    notImp = 0
    bestLoss = 10000

    nlp.begin_training()
    for itn in range(HP['epochs']):
        random.shuffle(trainData)
        losses = {}
        batches = minibatch(
            trainData,
            size = compounding(HP['minBatch'], HP['maxBatch'], HP['learnRate'])
        )
        for batch in batches:
            example = []
            texts, annotations = zip(*batch)
            for text, annotation in zip(texts, annotations):
                doc = nlp.make_doc(text)
                tags = spacy.training.offsets_to_biluo_tags(doc, annotation['entities'])
                example.append(Example.from_dict(doc, {'entities': tags}))
            nlp.update(example, drop = HP['dropout'], losses = losses)

        print(f"{itn} Losses: {losses['ner']:.3f}")

        if bestLoss > losses['ner']:
            bestLoss = losses['ner']
            notImp = 0
        else:
            notImp += 1
            if notImp >= HP['patience']:
                print(f"No improvement for {notImp} epochs. Early stopping.")
                break

        '''
        validation_results = nlp.evaluate(validationData)
        validation_loss = validation_results['ents_per_type']['']
        print(f"Validation Loss: {validation_loss:.3f}")
        '''

    global modelName
    nlp.to_disk(modelName)

#-------------------------------------------------------------------------------------

os.system('cls')
model = loadModel()
print('스크립트 읽기')
fp, fn = utils.filePaths()

# 유튜브 스크립트에서 추출한 텍스트
for p, n in zip(fp, fn): 
    text = utils.readFile(p, n)

    prod = []
    for line in text[1 : ]:
        if line != '':
            doc = model(line)

            for entity in doc.ents:
                if entity.label_ == 'PRODUCT':
                    prod.append(entity.text)

    print('=======================================================')
    print('화장품 명:')
    print('\n'.join(prod))
