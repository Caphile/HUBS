from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import clipboard
import time
import os

def getScript(lang):
    data = transcript.translate(lang).fetch()
    texts = []
    for i in data:
        texts.append(i['text'])
    return texts

def getTxt(lang, text):
    path = f'scripts/{title}/(ori)script_{lang}.txt'
    with open(path, 'w', encoding = 'UTF-8') as f:
        for t in text:
            f.write(t+'\n')
    print(lang + '완료')

langs = ['ko', 'en', 'ms']
not_in_title = ['/', '\\', ':', ',', ';' ,'*', '?' ,'"', '<', '>', '=', '|']

url_b = clipboard.paste()

print("주소를 복사한 순간부터 시작\n")
while 1:
    #print('유튜브 주소 입력 : ', end = '')
    #url = input()
    url = clipboard.paste()
    time.sleep(0.5)

    if url_b != url:
        url_b = url
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find("title").text.split("-")[0].strip()
            for i in not_in_title:
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

            if not os.path.exists(os.path.join('scripts', title)):
                os.makedirs(os.path.join('scripts', title))
            #for l in langs:
            #    getTxt(l , getScript(l))
            getTxt(langs[1], getScript(langs[1]))   # 영어만

        except:
            print("자막이 없는 영상이거나 잘못된 주소\n")

        print('---------------------------------------------------------------')