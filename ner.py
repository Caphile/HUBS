<<<<<<< HEAD
import spacy
from tkinter import filedialog, Tk
import os 

#-------------------------------------------------------------------------------------
# �𵨸�(���), ���Ŀ� ���������� ���� �����ϰԲ� �ٲ� ���� ����
modelName = 'ner_model'
# �������Ķ����
=======
from tkinter import N
import spacy
from spacy.training.example import Example
import os
import utils

#-------------------------------------------------------------------------------------
# 모델명(경로), 추후에 유동적으로 선택 가능하게끔 바꿀 여지 있음
modelName = 'ner_model'
# 하이퍼파라미터
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
HP = {
    'dropout'   :   0.25,
    'minBatch'  :   16,
    'maxBatch'  :   32,
    'learnRate' :   0.01,
<<<<<<< HEAD
    'epochs'    :   10
    }
# ��
labels = ['PRODUCT', 'DESCRIPTION']
# Ȯ��(predict)
=======
    'epochs'    :   75,
    'patience'  :   100
}
# 라벨
labels = ['PRODUCT']
# 확률(predict)
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
probability = 0.5
#-------------------------------------------------------------------------------------

def loadModel():
    global modelName
<<<<<<< HEAD
    print('1. Ŀ���� �� ����')
    print('2. ���� �� ���')
    print('====================================')
    print('���� : ', end = '')
=======
    print('1. 커스텀 모델 생성')
    print('2. 기존 모델 사용')
    print('====================================')
    print('선택 : ', end = '')
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
    opt = int(input())
    if opt == 1:
        setModel()
        model = spacy.load(modelName)
    elif opt == 2:
        try:
<<<<<<< HEAD
            print('Ŀ���� �� ���')
            model = spacy.load(modelName)
        except:
            print('���¼ҽ��� ������ �� ���')
=======
            print('커스텀 모델 사용')
            model = spacy.load(modelName)
        except:
            print('오픈소스로 제공된 모델 사용')
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
            model = spacy.load('en_core_web_sm')
    return model

def setModel():
    from spacy.util import minibatch, compounding
    import random

    trainData = []
    print('학습용 데이터 읽기')
<<<<<<< HEAD
    fp = filePaths()
    for f in fp:
        with open(f, 'r', encoding ='UTF8') as f:
            fullText = f.read()
            lines = fullText.split('\n')

            trainData.append(lines)
            
    # trainData = [("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다. ", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})]
    # 위와 같은 형태의 trainData 제작해야 함

    model = spacy.blank('en')
    model.add_pipe("ner")
    ner = model.get_pipe('ner')
=======
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)
        for line in text:
            trainData.append(eval(line))

    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    ner = nlp.create_pipe('ner')
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
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

    global modelName
    nlp.to_disk(modelName)

#-------------------------------------------------------------------------------------

os.system('cls')
model = loadModel()
<<<<<<< HEAD
print('��ũ��Ʈ �б�')
fp = filePaths()

# ��Ʃ�� ��ũ��Ʈ���� ������ �ؽ�Ʈ
for f in fp:
    with open(f, 'r', encoding ='UTF8') as f:
        fullText = f.read()
        lines = fullText.split('\n')
=======
print('스크립트 읽기')
fp, fn = utils.filePaths()

# 유튜브 스크립트에서 추출한 텍스트
for p, n in zip(fp, fn): 
    text = utils.readFile(p, n)
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647

    prod = []
    for line in text[1 : ]:
        if line != '':
            doc = model(line)

            for entity in doc.ents:
                if entity.label_ == 'PRODUCT':
                    prod.append(entity.text)

<<<<<<< HEAD
                # �ؽ�Ʈ �з��� ���� ȭ��ǰ ���� ����
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = model(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > probability:   # Ȯ�� ����
                        descriptions.append(sentence)

        print('ȭ��ǰ ��:', ' '.join(prod))
        print('ȭ��ǰ ����:', ' '.join(desc))
=======
    print('=======================================================')
    print('화장품 명:\n', '\n'.join(prod))
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647
