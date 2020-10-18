# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json



df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/map_char.csv")
df_d = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/map_digit.csv")
source = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/cpt_char.csv")

print(source)
# source = source["code,cui"].str.split(",",expand=True)
# source.columns=["code","cui"]


import re
rx = re.compile("[a-zA-Z]+")
test=[]
i=0
l=len(source)
for x in source["code"].to_list():
	i+=1
	print(i/l)
	return_list=[]
	if str(x).isdigit():
		for index,line in df_d.iterrows():
			if x > int(line['r']) :
				continue
			# print(x)
			# print(line['l'])
			# print(line['r'])
			# print("----------")
			if int(line['l'])<=x and x<=int(line['r']):
				return_list.append(str(line['CCS']))

	else:
		for index,line in df.iterrows():
			l = str(line['l'])
			r = str(line['r'])
			print(x)
			# non-digital x
			if str(line['l'])==str(line['r']):
				if str(line['l'])==x:
					return_list.append(str(line['CCS']))

			else:
				lc = rx.findall(l)[0]
				xc = rx.findall(x)[0]
				if lc==xc:
					l_int = int(l.replace(lc,''))
					r_int = int(r.replace(rx.findall(r)[0],''))
					x_int = int(x.replace(xc,''))
					if x_int>=l_int and x_int<=r_int:
						return_list.append(x)



	test.append("|".join(return_list))

source["test"] = test

source.to_csv('/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/cpt_char_test.csv',index=False)



		# elif not x.isdigit() and not l.isdigit():
		# 	print("%s, %s"%(x,l))
		# 	lc = re.findall(rx,l)[0]
		# 	xc = re.findall(rx,x)[0]
 
