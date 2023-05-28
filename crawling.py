from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import requests
import clipboard
import pyperclip
import time
import os, re
import utils

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

                    path = f'{os.getcwd()}/scripts'
                if not os.path.exists(path):
                    os.makedirs(path)

                data = transcript.translate('en').fetch()
                text = [url]
                for i in data:
                    text.append(i['text'])

                utils.saveFile(path, f'0_{title}', text)
                print('crawling 완료')


            except:
                print("자막이 없는 영상이거나 잘못된 주소\n")
            
            
pyperclip.copy('')
crawling()              