import json
import preprocessing as ps
import ner
import utils

def process():

	train = True

	if train == True:
		ner.setModel()
	elif train == False:
		p, n = ps.crawling(True)				# crawling에 영상분석 추가 해야함
		products = ner.extract(p, f'2_{n}')[0]	# normalize된 텍스트에 대해 수행, 1개의 텍스트(임시)

		print('\n=======================================================')
		print('화장품 명:')
		print('\n'.join(products))

process()