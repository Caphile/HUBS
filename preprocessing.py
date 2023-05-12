from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import requests
import clipboard
import time
import os, re
import utils

class Normalize:    # 정규화 함수
    def __init__(self, text, stopwords):
        self.text = self.stripSCharacter(text)
        self.text = self.removeStopword(self.text, stopwords)
        #self.text = self.lowercase(self.text)

    def stripSCharacter(self, text):        # 특수문자 제거
        return re.sub('[^a-zA-Z0-9\s]', '', text)

    def removeStopword(self, text, stopwords):     # 불용어 제거
        words = text.split(' ')
        return ' '.join([word for word in words if word.lower() not in stopwords])

    def lowercase(self, text):              # 소문자화
        words = text.split(' ')
        return ' '.join([word.lower() for word in words])

def crawling():
    url_b = clipboard.paste()

    print("주소를 복사한 순간부터 시작\n")
    while 1:
        #print('유튜브 주소 입력 : ', end = '')
        #url = input()
        url = clipboard.paste()
        time.sleep(0.5)

        if url_b != url:
            os.system('cls')
            url_b = url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.find("title").text.split("-")[0].strip()
                for i in ['/', '\\', ':', ',', ';' ,'*', '?' ,'"', '<', '>', '=', '|']:
                    title = title.replace(i, '')

                print('타이틀 : ' + title)

                s = url.find('?v=')
                e = url.find('&')
                if not e:
                    key = url[s + 3 : e]
                else:
                    key = url[s + 3 : ]

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

                data = transcript.translate('en').fetch()
                text = []
                for i in data:
                    text.append(i['text'])

                utils.saveFile(path, f'0_{title}', text)
                print('crawling 완료')

                resentense(path, f'0_{title}')

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
        for line in text:
            if line != '':
                newText += ' ' + line
        newText = sent_tokenize(newText)

        newName = re.sub(r'\d+_', '', n)
        utils.saveFile(p, f'1_{newName}', newText)
        print('resentense 완료')

        normalize(p, f'1_{newName}')

def normalize(fp = None, fn = None):
    stopwords = utils.readFile(os.getcwd(), 'Stopwords.txt')
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].replace('\n', '')

    if fp == None or fn == None:
        fp, fn = utils.filePaths()
    else:
        fp = [fp]
        fn = [fn]
    for p, n in zip(fp, fn): 
        text = utils.readFile(p, n)

        newText = []
        for line in text:
            newLine = Normalize(line, stopwords).text
            if newLine != []:
                newText.append(newLine)

        newName = re.sub(r'\d+_', '', n)
        utils.saveFile(p, f'2_{newName}', newText)
        print('normalize 완료')

crawling()