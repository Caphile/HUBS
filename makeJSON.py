import json
from msilib import PID_APPNAME
import utils

import random

ranNM = ['A', 'B', 'C', 'D', 'E']

fp, fn =  utils.filePaths(3)

# YOUTUBE.json
YTdata = {}
for idx, (p, n) in enumerate(zip(fp, fn)):
	with open(f'{p}/{n}') as f:
		SCdata = json.load(f)
		INFL, URL = SCdata['INFL'], SCdata['URL']
		for P_NM, SUMM in zip(SCdata['P_NM'], SCdata['SUMM']):
			data = {
				'P_NM'	:	P_NM,			# 제품명
				'INFL'	:	ranNM[random.randrange(0,4)],			# 채널명
				'SUMM'	:	'SUMM',			# 요약
				'URL'	:	URL				# url
			}
			YTdata[len(YTdata) + 1] = data

# PRODUCT.json
PDdata = {}
for i in YTdata.values():
	P_NM = i['P_NM']
	if P_NM not in PDdata:
		data = {
			'PID'	:	len(PDdata) + 1,	# 제품명
			'INGR'	:	'Ingredient',		# 성분
			'USE'	:	'How to use',		# 사용법
		}
		PDdata[P_NM] = data

# INFLUENCER.json
IFdata = {}
for i in YTdata.values():
	INFL = i['INFL']
	if P_NM not in IFdata:
		data = {
			'IID'	:	len(IFdata) + 1,	# 채널명
			'INFO'	:	'Infomation'		# 채널정보
		}
		IFdata[INFL] = data

with open('YOUTUBE.json', 'w') as f:
	json.dump(YTdata, f)
with open('PRODUCT.json', 'w') as f:
	json.dump(PDdata, f)
with open('INFLUENCER.json', 'w') as f:
	json.dump(IFdata, f)