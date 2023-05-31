import json
import preprocessing as ps
import ner
import utils

def process():

	print('학습용(y/n) : ', end = '')
	train = input()
	if train == 'Y' or train == 'y':
		ner.setModel()
	else:
		model = ner.loadModel()

		p, n = ps.crawling(True)						# crawling에 영상분석 추가 해야함
		with open(f'{p}/{n}.json', 'w') as jsonFile:
			product = ner.extract(model, p, f'2_{n}',)[0]	# normalize된 텍스트에 대해 수행, 1개의 텍스트(임시)
			product = list(set(product))

			loc = []
			text = utils.readFile(p, f'2_{n}')
			for p in product:
				for c, line in enumerate(text):
					if p in line:
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
				print(product[i])
				print(' '.join(subText[i]))

				# text summerize 추가


			
			data = {
				'INFLUENCER'	:	'안녕',
				'PRODUCT'		:	product,
				'SUMMARY'		:	subText,
			}

			json.dump(data, jsonFile)
			

process()