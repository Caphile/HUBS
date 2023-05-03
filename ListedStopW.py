fileName = 'Stopwords.txt' #Stopword.txt 파일의 단어들을 나열

with open(fileName, 'r+') as f:
    lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    while 1:
        stopW = input()
        if stopW == 'x':
            break

        if stopW in lines:
            lines.remove(stopW)
            print(f'{stopW}이 목록에서 삭제됨')
        else:
            lines.append(stopW)
            print(f'{stopW}이 목록에 추가됨')

        lines.sort()    
        
        f.seek(0)
        f.truncate(0)
        f.write('\n'.join(lines))