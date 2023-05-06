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

# spaCy 영어 모델 로드
fp = filePaths()
nlp = spacy.load('en_core_web_sm')

# 유튜브 스크립트에서 추출한 텍스트
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

                # 출력

        print(item)

# 옵티마이저, 모델 아키텍처 선택
'''
# 하이퍼 파라미터 변경
from spacy.util import minibatch, compounding

# 모델을 로드합니다.
nlp = spacy.load("en_core_web_sm")

# 학습 데이터
TRAIN_DATA = [
    ("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]}),
]
# 새로운 모델 생성
custom_ner = spacy.blank("en")

# 새로운 엔티티 레이블 "PRODUCT"와 "ORG" 등록
custom_ner.add_label("newLabel")

# 파이프라인 구성
custom_ner.add_pipe(custom_ner.create_pipe("ner"))

# 하이퍼파라미터를 설정합니다.
learn_rate = 0.001  # 학습률
L2_penalty = 1e-6  # L2 패널티
momentum = 0.9  # 모멘텀
dropout = 0.2  # 드롭아웃 비율
n_iter = 20  # 반복 횟수

# 옵티마이저를 초기화합니다.
optimizer = nlp.begin_training()

# 하이퍼파라미터를 설정합니다.
optimizer.learn_rate = learn_rate
optimizer.L2_penalty = L2_penalty
optimizer.momentum = momentum

# 반복 횟수만큼 학습합니다.
for i in range(n_iter):
    # 학습 데이터를 섞습니다.
    random.shuffle(TRAIN_DATA)
    
    # 미니배치를 만들고 학습합니다.
    losses = {}
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer, drop=dropout, losses=losses)
    
    # 학습 결과를 출력합니다.
    print("Iteration {} - Loss: {}".format(i + 1, losses["ner"]))
'''