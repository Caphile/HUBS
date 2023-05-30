import preprocessing as ps
import ner
import utils

def process():
	p, n = ps.crawling(True)
	text = utils.readFile(p, n)
	ner.extract(False, text)

process()