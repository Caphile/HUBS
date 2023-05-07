# -*- encoding= cp949 -*-

import spacy
import torch
from transformers import BertTokenizer, BertForTokenClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification
from tkinter import filedialog, Tk
import os

def filePaths():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

'''
# spaCy ���� �� �ε�
fp = filePaths()
nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('custom_model')

# ��Ʃ�� ��ũ��Ʈ���� ������ �ؽ�Ʈ
for f in fp:
    with open(f, 'r', encoding ='UTF8') as f:
        fullText = f.read()
        lines = fullText.split('\n')

        item = []
        data = []
        for line in lines:
            if line != '':
                doc = nlp(line)

                a = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
                if a != []:
                    item.append([ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']])

                # ���

        print(item)

'''

from spacy.util import minibatch, compounding
import random

# �н� ������
TRAIN_DATA = [
    ("�̹��� �Ұ��� ��ǰ�� ���ӹ̹��� ���̼����� �ȷ�Ʈ�Դϴ�.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]}),
]
# ���ο� �� ����
nlp = spacy.blank("en")
#custom_ner.to_disk('custom_model')
#custom_ner = spacy.load('custom_model')

ner = nlp.create_pipe('ner')
nlp.add_pipe(ner)

nlp.add_label("PRODUCT")
nlp.add_label("ORG")

# ���������� ����
optimizer = nlp.entity.create_optimizer()

# �������Ķ���͸� �����մϴ�.
learn_rate = 0.001
batch_size = 32
epochs = 10
dropout = 0.5

# ��Ƽ�������� �ʱ�ȭ�մϴ�.
#nlp.begin_training(learn_rate=learn_rate, batch_size=batch_size, epochs=epochs, dropout=dropout)

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    for itn in range(epochs):
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, drop=0.35,
                        losses=losses)
        print('Losses', losses)

nlp.to_disk('custom_model')