import utils
import pandas as pd

def txtLabels():    # 수동 라벨링 데이터
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = []
        for line in text:
            token = line.split('/')
            sentense = ' '.join(token[0].split())

            targets, labels = [], []
            for info in token[1 : ]:
                si = info.split()
                targets.append(' '.join(si[1 : ]))
                labels.append(si[0])
            
            newText.append(standard(sentense, targets, labels))

        utils.saveFile(p, 'norm_' + n.replace('.txt', ''), newText)

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
    newOrigin = N.process(origin)

    for t, l in zip(target, label):
        s = newOrigin.find(N.process(t))
        e = s + len(t)
        entities.append((s, e, f'{l}'))

    res = (newOrigin, {'entities' : entities})
    return str(res)

N = utils.Normalize()

print('1. txt\n2. xlsx')
print('읽을 파일 종류 : ', end = '')
opt = int(input())
if opt == 1:
    txtLabels()
elif opt == 2:
    xlsxLabels()