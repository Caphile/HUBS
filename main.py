import preprocessing as ps
import ner
import utils

def process():

	train = False

	if train == True:
		ner.setModel()
	elif train == False:
		p, n = ps.crawling(True)
		text = utils.readFile(p, n)
		products = ner.extract(False, text)
		
		print('\n=======================================================')
		print('화장품 명:')
		print('\n'.join(products))

process()