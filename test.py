# -*- encoding= cp949 -*-

import spacy
from tkinter import filedialog, Tk
import os

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def loadModel():
    print('1. �� �� 2. ���� ��')
    opt = int(input())
    if opt == 1:
        model = spacy.blank('en')
    elif opt == 2:
        modelName = 'ner_model' # ���Ŀ� ���� �����ϰԲ� �ٲ� ���� ����
        try:
            print('Ŀ���� �� ���')
            model = spacy.load(modelName)
        except:
            print('���¼ҽ��� ������ �н��� �� ���')
            model = spacy.load('en_core_web_sm')
    return model

fp = filePaths()
nlp = loadModel()

# ��Ʃ�� ��ũ��Ʈ���� ������ �ؽ�Ʈ
for f in fp:
    with open(f, 'r', encoding ='UTF8') as f:
        fullText = f.read()
        lines = fullText.split('\n')

        prod = []
        desc = []
        for line in lines:
            if line != '':
                doc = nlp(line)

                for entity in doc.ents:
                    if entity.label_ == "PRODUCT":
                        prod.append(entity.text)

                # �ؽ�Ʈ �з��� ���� ȭ��ǰ ���� ����
                descriptions = []
                sentences = [sent.text for sent in doc.sents]
                for sentence in sentences:
                    sentence_doc = nlp(sentence)
                    if sentence_doc.cats.get('DESCRIPTION', 0) > 0.5:   # Ȯ���� n�̻���
                        descriptions.append(sentence)

        print("ȭ��ǰ ��:", ' '.join(prod))
        print("ȭ��ǰ ����:", ' '.join(desc))

'''
from spacy.util import minibatch, compounding
import random

# �н� ������
TRAIN_DATA = [
    ("�̹��� �Ұ��� ��ǰ�� ���ӹ̹��� ���̼����� �ȷ�Ʈ�Դϴ�.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]}),
]
# ���ο� �� ����
nlp = spacy.blank('en')
#cust om_ner.to_disk('custom_model')
#custom_ner = spacy.load('custom_model')

ner = nlp.add_pipe("ner")

ner.add_label("PRODUCT")
ner.add_label("ORG")

pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# ���������� ����
#optimizer = nlp.entity.create_optimizer()

# �������Ķ���͸� �����մϴ�.
#learn_rate = 0.001
epochs = 10

# ��Ƽ�������� �ʱ�ȭ�մϴ�.
#nlp.begin_training(learn_rate=learn_rate, batch_size=batch_size, epochs=epochs, dropout=dropout)

with nlp.disable_pipes(*unaffected_pipes):
  # Training for 30 iterations
  for iteration in range(epochs):

    # shuufling examples  before every iteration
    random.shuffle(TRAIN_DATA)
    losses = {}
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size = compounding(4.0, 32.0, 1.001)) #����ũ��, �ִ�ũ��, ������
    for batch in batches:   # �������� ����
        texts, annotations = zip(*batch)
        nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses
                )
        print("Losses", losses)

nlp.to_disk('custom_model')

'''