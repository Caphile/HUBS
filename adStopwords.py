import sys

file_path='Stopwords.txt' #Stopword.txt 파일의 단어들을 나열

<<<<<<< HEAD:ListedStopW.py
with open(file_path) as f:
    lines = f.readlines()
=======
filePath = ''
fileName = 'Stopwords.txt'

with open(fileName, 'r+', encoding ='UTF8') as f:
    lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    print('\n')
    while 1:
        print('enter를 눌러 종료')
        print('추가/삭제할 불용어 입력 : ', end = '')
        stopW = input()
        if stopW == '':
            break
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647:adStopwords.py

lines=[line.rstrip('\n') for line in lines]
lines.sort()    

words='\n'.join(lines) #배열된 단어들을 Stopwords 메모장에 저장되게 함
file = open("Stopwords.txt","w")
file.write(words)
file.close()

<<<<<<< HEAD:ListedStopW.py

=======
        if stopW in lines:  # 이미 존재하면 삭제
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}을 목록에서 {Fore.RED}삭제{Style.RESET_ALL}(Y/N)', end = ' ')
            opt = input()
            os.system('cls')
            if opt == 'Y' or opt == 'y':
                lines.remove(stopW)
                print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}이 목록에서 {Fore.RED}삭제{Style.RESET_ALL}됨\n')
            else:
                continue
        else:
            lines.append(stopW)
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}이 목록에 {Fore.BLUE}추가{Style.RESET_ALL}됨\n')

        #lines = [word.lower() for word in lines]
        lines.sort()    
        
        f.seek(0)
        f.truncate(0)
        f.write('\n'.join(lines))
>>>>>>> c73604efe208589eb86d7137438d4d657d84e647:adStopwords.py
