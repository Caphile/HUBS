from colorama import Fore, Style
import os

filePath = ''
fileName = 'Stopwords.txt'

with open(fileName, 'r+') as f:
    lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    while 1:
        print('추가/삭제할 불용어 입력 : ', end = '')
        stopW = input()
        if stopW == '':    # enter 눌러 종료
            break

        os.system('cls')

        if stopW in lines:  # 이미 존재하면 삭제
            lines.remove(stopW)
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}이 목록에서 {Fore.RED}삭제{Style.RESET_ALL}됨')
        else:
            lines.append(stopW)
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}이 목록에 {Fore.BLUE}추가{Style.RESET_ALL}됨')

        lines.sort()    
        
        f.seek(0)
        f.truncate(0)
        f.write('\n'.join(lines))