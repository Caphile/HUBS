from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import requests
import clipboard
import pyperclip
import time
import os, re
import utils
import json

def crawling(oneTime = False):
    url_b = clipboard.paste()

    print("주소를 복사한 순간부터 시작\n")
    while 1:
        #print('유튜브 주소 입력 : ', end = '')
        #url = input()
        url = clipboard.paste()
        time.sleep(0.1)

        if url_b != url:
            os.system('cls')
            url_b = url
            try:
                command = ['yt-dlp', '--dump-json', url]
                output = subprocess.check_output(command).decode('utf-8')

                video_info = json.loads(output)

                key = video_info['id']
                title = N.stripSCharacter(video_info['title'])
                uploader = N.stripSCharacter(video_info['uploader'])
                upload_date = video_info['upload_date']

                transcript_list = YouTubeTranscriptApi.list_transcripts(key)
 
                for transcript in transcript_list:
                    '''
                    print(
                        transcript.video_id,
                        transcript.language,
                        transcript.language_code,
       
                        transcript.is_generated,
         
                        transcript.is_translatable,
         
                        transcript.translation_languages,
                    )
                        '''
                path = f'{os.getcwd()}/scripts'
                if not os.path.exists(path):
                    os.makedirs(path)

                text = [url, title, uploader, upload_date]
                data = transcript.translate('en').fetch()
                for i in data:
                    timeSTP = f"|{int(i['start'])}|"
                    line = timeSTP + N.stripSCharacter(i['text'], True)
                    text.append(line)

                utils.saveFile(path, f'0_{title}', text)
                print('crawling 완료')

                resentense(path, f'0_{title}')

                if oneTime == True:
                    return (path, title)

            except:
                print("자막이 없는 영상이거나 잘못된 주소\n")

def resentense(fp = None, fn = None):
    if fp == None or fn == None:
        fp, fn = utils.filePaths()
    else:
        fp = [fp]
        fn = [fn]
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = ''
        for line in text[4 : ]:
            if line != '':
                newText += ' ' + line

        pattern_res = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
        newText = re.split(pattern_res, newText)

        pattern_TS = r'\|\d+\|'
        matches = []
        for idx, line in enumerate(newText):
            matches.append(re.findall(pattern_TS, line))
            newLine = re.sub(pattern_TS, '', line)
            if line[0] != '|':
                newText[idx] = matches[idx - 1][-1] + newLine
            else:
                newText[idx] = matches[idx][0] + newLine

        newText = text[ : 4] + newText
        newName = re.sub(r'\d+_', '', n)

        utils.saveFile(p, f'1_{newName}', newText)
        print('resentense 완료')

        normalize(p, f'1_{newName}')

def normalize(fp = None, fn = None):
    if fp == None or fn == None:
        fp, fn = utils.filePaths()
    else:
        fp = [fp]
        fn = [fn]
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        pattern_TS = r'\|\d+\|'
        newText = []
        timeSTP = []
        for idx, line in enumerate(text[4 : ]):
            timeSTP.append(re.findall(pattern_TS, line)[0])
            newLine = re.sub(pattern_TS, '', line)

            newLine = N.process(newLine)
            if newLine != []:
                newText.append(timeSTP[idx] + newLine)

        newText = text[ : 4] + newText
        newName = re.sub(r'\d+_', '', n)

        utils.saveFile(p, f'2_{newName}', newText)
        print('normalize 완료')

N = utils.Normalize()
pyperclip.copy('')  # 클립보드 초기화
#crawling()