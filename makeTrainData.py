import utils
import pandas as pd

def txtLabels():    # 수동 라벨링 데이터
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = []
        for line in text:
            token = line.split('/')
            sentense = token[0]

            targets, labels = [], []
            for info in token[1 : ]:
                si = info.split()
                targets.append(' '.join(si[1 : ]))
                labels.append(si[0])
            
            newText.append(standard(sentense, targets, labels))

        utils.saveFile(p, n.replace('.txt', ''), newText)

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
    if type(target) == str:
        target = [target]
    if type(label) == str:
        label = [label]

    entities = []
    for t, l in zip(target, label):
        s = origin.find(t)
        e = s + len(t)
        entities.append((s, e, f'{l}'))

    res = (origin, {'entities' : entities})
    return str(res)

print('1. txt 2. xlsx')
opt = int(input())
if opt == 1:
    txtLabels()
elif opt == 2:
    xlsxLabels()