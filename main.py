import json
import preprocessing as ps
import ner

def process():

	print('학습용(y/n) : ', end = '')
	train = input()
	if train == 'Y' or train == 'y':
		ner.setModel()
	else:
		model = ner.loadModel()

		with open(f'{p}/{n}.json', 'w') as jsonFile:
			p, n = ps.crawling(True)						# crawling에 영상분석 추가 해야함
			product = ner.extract(model, p, f'2_{n}',)[0]	# normalize된 텍스트에 대해 수행, 1개의 텍스트(임시)

			print('\n=======================================================')
			print('화장품 명:')
			print('\n'.join(product))




			data = {
				'INFLUENCER'	:	1,
				'PRODUCT'		:	product,
				'SUMMARY'		:	1
			}

			json.dump(data, jsonFile)

process()