import preprocessing as ps
import ner

def process():
	text = ps.crawling(True)
	ner.extract(False, text)


process()