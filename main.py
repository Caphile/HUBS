import json
import preprocessing as ps
import ner

def process():

	train = False

	if train == True:
		ner.setModel()
	elif train == False:
		model = ner.loadModel()

		p, n = ps.crawling(True)						# crawling에 영상분석 추가 해야함
		products = ner.extract(model, p, f'2_{n}',)[0]	# normalize된 텍스트에 대해 수행, 1개의 텍스트(임시)

		print('\n=======================================================')
		print('화장품 명:')
		print('\n'.join(products))

process()