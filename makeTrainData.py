import utils
import pandas as pd

def txtLabels():    # 수동 라벨링 데이터
    fp, fn = utils.filePaths()
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = []
        for line in text:
            if line == '':
                continue

            token = line.split('/')
            sentense = ' '.join(token[0].split())

            targets, labels = [], []
            for info in token[1 : ]:
                if info == '':
                    continue
                #si = info.split()
                targets.append(info)
                #targets.append(' '.join(si[1 : ]))
                #labels.append(si[0])

                opt = 2
                if opt == 1:
                    labels.append('PRODUCT')
                elif opt == 2:
                    labels.append('BRAND')

            newText.append(standard(sentense, targets, labels))
            if newText[-1] == 'x':
                newText.pop()

        utils.saveFile(p, 'norm_' + n.replace('.txt', ''), newText)

def xlsxLabels():   # 세포라 크롤링 데이터
    fp, fn = utils.filePaths(2)
    for p, n in zip(fp, fn): 
        df = pd.read_excel(f'{p}/{n}')

        print('=======================================')
        for i, c in enumerate(df.columns):
            print(f'{i + 1}번째 컬럼 : {c}')
        print('=======================================')
        print('컬럼 선택 : ', end = '')
        opt = int(input())

        product = df.iloc[ : , opt - 1].values   # 상품명

        newData = []
        for i in product:
            newData.append(standard(i, i, 'PRODUCT'))
            if newData[-1] == 'x':
                newData.pop()

        utils.saveFile(p, n.replace('.xlsx', ''), newData)

def standard(origin, target, label):
    if type(target) == str:
        target = [target]
    if type(label) == str:
        label = [label]

    entities = []
    newOrigin = N.process(origin)

    for t, l in zip(target, label):
        nt = N.process(t)
        s = newOrigin.find(nt)
        if s == -1:
            return 'x'
        e = s + len(nt)
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