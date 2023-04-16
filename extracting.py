# -*- coding: cp949 -*-

import torch
from transformers import BertTokenizer, BertForTokenClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification
from tkinter import filedialog, Tk
import os

def openFile():
    root = Tk()
    root.withdraw()

    return filedialog.askopenfilenames(title = 'Select txt Files', initialdir = os.getcwd(), filetypes = [("Text files", "*.txt"), ("All files", "*.*")])

def model():
    pass

def label(text):
    inputs = tokenizer.encode_plus(text, add_special_tokens = True, return_tensors = "pt")
    outputs = model(inputs["input_ids"]).logits
    predictions = torch.argmax(outputs, dim = 2)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [tokenizer.decode([prediction]) for prediction in predictions[0].tolist()]

    entity_start = None
    entity_end = None
    entity_type = None
    entities = []

    for i, token in enumerate(tokens):
        label = labels[i]
        if label.startswith("B-"):
            if entity_start is not None:
                entities.append((entity_type, entity_start, entity_end))
            entity_start = i
            entity_end = i + 1
            entity_type = label[2:]
        elif label.startswith("I-"):
            if entity_type is not None:
                entity_end = i + 1
        elif label.startswith("O"):
            if entity_start is not None:
                entities.append((entity_type, entity_start, entity_end))
                entity_start = None
                entity_end = None
                entity_type = None

    if entity_start is not None:
        entities.append((entity_type, entity_start, entity_end))

    entity_types = set([entity[0] for entity in entities])
    for entity_type in entity_types:
        print(entity_type)
        for entity in entities:
            if entity[0] == entity_type:
                print(entity[1], entity[2], " ".join(tokens[entity[1]:entity[2]]))

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels = 3)

filePaths = openFile()

for f in filePaths:
    with open(f, 'r') as f:
        fullText = f.read()
        lines = fullText.split('\n')

        item = []
        data = []
        for line in lines:
            if line != '':

                label(line)

                #tokens = tokenizer.encode(line, add_special_tokens = True)  # add_special_token : [CLS], [SEP] 추가

                #input_ids = torch.tensor([tokens])  # 텐서로 변환
                #outputs = model(input_ids)  # outputs[0] : 각 입력 토큰의 예측값
                #predictions = torch.argmax(outputs[0], dim = 2) # 예측값중 가장 큰 수의 인덱스

                ## 예측 결과 출력
                #for i in range(len(predictions[0])):
                #    token = tokenizer.decode([tokens[i]])
                #    tag = predictions[0][i].item()
                #    if tag == 1:
                #        item.append(token)
                #    elif tag == 2:
                #        data.append(token)

        print(1)
