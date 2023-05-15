import utils
import pandas as pd

def txtLabels():
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = []
        for line in text:
            sentense, info = line.split('/')
            label = info.split()[0]
            entities = ' '.join(info.split()[1 : ])
        
            # newLine = f'{sentense}, {}'

            print(sentense)
            print(label)
            print(entities)

def xlsxLabels():   # 세포라 크롤링 데이터
    fp, fn = utils.filePaths(2)
    for p, n in zip(fp, fn): 
        df = pd.read_excel(f'{p}/{n}')
        product = df.iloc[ : , 0].values   # 상품명

        newData = []
        for i in product:
            newData.append(standard(i, i, 'PRODUCT'))

        utils.saveFile(p, n.replace('.xlsx', ''), newData)

def standard(origin, target, label):
    s = origin.find(target)
    e = s + len(target)

    res = (origin, {'entities' : [(s, e, f'{label}')]})
    #res = (origin, (s, e, f'{label}'))
    return str(res)

    #trainData = [("이번에 소개할 제품은 아임미미의 아이섀도우 팔레트입니다.", {"entities": [(12, 18, "ORG"), (21, 30, "PRODUCT")]})]
    # 라벨링 된 txt 파일 받아 표준화

xlsxLabels()