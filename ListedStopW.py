file_path='Stopwords.txt' #Stopword.txt 파일의 단어들을 나열

with open(file_path) as f:
    lines = f.readlines()

lines=[line.rstrip('\n') for line in lines]
lines.sort()      


words='\n'.join(lines) #배열된 단어들을 ListedStopw란 메모장에 저장되게함
file = open("ListedStopw.txt","w")
file.write(words)
file.close()


