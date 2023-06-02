import json
import preprocessing as ps
import ner
import utils
import os

def process():
	while 1:	# 추후 조건 작성 예정

		print('학습용(y/n) : ', end = '')
		train = input()

		os.system('cls')

		if train == 'Y' or train == 'y':
			ner.setModel()
		else:
			model = ner.loadModel()

			while 1:
				p, n = ps.crawling(True)						# crawling에 영상분석 추가 해야함
				
				product = ner.extract(model, p, f'2_{n}',)[0]	# normalize된 텍스트에 대해 수행, 1개의 텍스트(임시)
				product = list(set(product))

				loc = []
				text = utils.readFile(p, f'2_{n}')
				for pd in product:
					for c, line in enumerate(text):
						if pd in line:
							loc.append(c)
							break

				sortList = list(zip(product, loc))
				sortList.sort(key = lambda x : x[1])


				product, loc = zip(*sortList)

				subText = []
				for i in range(len(product)):
					s = loc[i]
					try:
						e = loc[i + 1]
						if s == e:
							e += 1
					except:
						e = len(text)

					subText.append(text[s : e])

					print('================================================================')
					print(product[i].replace(',', ''))
					print(' '.join(subText[i]))

					# text summerize 추가
					# summary.append() 

				#print('인플루언서 입력 : ', end = '')
				#influencer = input()
				influencer = 'RISABAE'		# 어떻게 입력 받을지에 대한 고민 필요

				product = [pd.replace(',', '') for pd in product]

				with open(f'{p}/{n}.json', 'w') as jsonFile:

					data = {
						'INFL'		:	influencer,
						'P_NM'		:	product,
						'SUMM'		:	subText,	# summary
						'URL'		:	text[0],
					}

					json.dump(data, jsonFile)			

process()