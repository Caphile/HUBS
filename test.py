# -*- encoding= cp949 -*-

import spacy
from tkinter import filedialog, Tk
import os

modelName = 'ner_model' # ���Ŀ� ���� �����ϰԲ� �ٲ� ���� ����

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    print('1. Ŀ���� �� ����')
    print('2. ���� �� ���')
    opt = int(input())
    if opt == 1:
        model = spacy.blank('en')
        setModel(model)

    elif opt == 2:
        global modelName
        try:
            print('Ŀ���� �� ���')
            model = spacy.load(modelName)
        except:
            print('���¼ҽ��� ������ �н��� �� ���')
            model = spacy.load('en_core_web_sm')
    return model

def saveModel():
    pass

def setModel(model):
    from spacy.util import minibatch, compounding
    import random

    trainData = []
    print('�н��� ������ �б�')
    fp = filePaths()
    for f in fp:
        with open(f, 'r', encoding ='UTF8') as f:
            fullText = f.read()
            lines = fullText.split('\n')

            trainData.append(lines)     # lines ���� : ("�̹��� �Ұ��� ��ǰ�� ���ӹ̹��� ���̼����� �ȷ�Ʈ�Դϴ�.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})
            
    # ������
    ner = model.add_pipe("ner")
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]

    # ��
    ner.add_label("PRODUCT")
    ner.add_label("ORG")

    # �������Ķ����
    epochs = 10

    with model.disable_pipes(*unaffected_pipes):
      # Training for 30 iterations
      for iteration in range(epochs):

        # shuufling examples  before every iteration
        random.shuffle(trainData)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(trainData, size = compounding(4.0, 32.0, 1.001)) #����ũ��, �ִ�ũ��, ������
        for batch in batches:   # �������� ����
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