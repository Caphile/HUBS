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

# spaCy ���� �� �ε�
fp = filePaths()
nlp = spacy.load('en_core_web_sm')

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

# ��Ƽ������, �� ��Ű��ó ����
'''
# ������ �Ķ���� ����
from spacy.util import minibatch, compounding

# ���� �ε��մϴ�.
nlp = spacy.load("en_core_web_sm")

# �н� ������
TRAIN_DATA = [
    ("�̹��� �Ұ��� ��ǰ�� ���ӹ̹��� ���̼����� �ȷ�Ʈ�Դϴ�.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]}),
]
# ���ο� �� ����
custom_ner = spacy.blank("en")

# ���ο� ��ƼƼ ���̺� "PRODUCT"�� "ORG" ���
custom_ner.add_label("newLabel")

# ���������� ����
custom_ner.add_pipe(custom_ner.create_pipe("ner"))

# �������Ķ���͸� �����մϴ�.
learn_rate = 0.001  # �н���
L2_penalty = 1e-6  # L2 �г�Ƽ
momentum = 0.9  # �����
dropout = 0.2  # ��Ӿƿ� ����
n_iter = 20  # �ݺ� Ƚ��

# ��Ƽ�������� �ʱ�ȭ�մϴ�.
optimizer = nlp.begin_training()

# �������Ķ���͸� �����մϴ�.
optimizer.learn_rate = learn_rate
optimizer.L2_penalty = L2_penalty
optimizer.momentum = momentum

# �ݺ� Ƚ����ŭ �н��մϴ�.
for i in range(n_iter):
    # �н� �����͸� �����ϴ�.
    random.shuffle(TRAIN_DATA)
    
    # �̴Ϲ�ġ�� ����� �н��մϴ�.
    losses = {}
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer, drop=dropout, losses=losses)
    
    # �н� ����� ����մϴ�.
    print("Iteration {} - Loss: {}".format(i + 1, losses["ner"]))
'''