import spacy
from tkinter import filedialog, Tk
import os 

#-------------------------------------------------------------------------------------
# �𵨸�(���), ���Ŀ� ���������� ���� �����ϰԲ� �ٲ� ���� ����
modelName = 'ner_model'
# �������Ķ����
HP = {
    'dropout'   :   0.5,
    'minBatch'  :   4.0,
    'maxBatch'  :   32.0,
    'learnRate' :   0.01,
    'epochs'    :   10
    }
# ��
labels = ['PRODUCT', 'DESCRIPTION']
# Ȯ��(predict)
probability = 0.5
#-------------------------------------------------------------------------------------

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    global modelName
    print('1. Ŀ���� �� ����')
    print('2. ���� �� ���')
    print('====================================')
    print('���� : ', end = '')
    opt = int(input())
    if opt == 1:
        setModel()
        model = spacy.load(modelName)
    elif opt == 2:
        try:
            print('Ŀ���� �� ���')
            model = spacy.load(modelName)
        except:
            print('���¼ҽ��� ������ �� ���')
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
            
    # trainData = [("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다. ", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})]
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
                    if entity.label_ == 'PRODUCT':
                        prod.append(entity.text)

                # �ؽ�Ʈ �з��� ���� ȭ��ǰ ���� ����
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = model(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > probability:   # Ȯ�� ����
                        descriptions.append(sentence)

        print('ȭ��ǰ ��:', ' '.join(prod))
        print('ȭ��ǰ ����:', ' '.join(desc))