# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json


df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/2019_ccs_services_procedures.csv")



df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/map_digit.csv")
# print(df)
source = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/cpt_digit.csv")

print(source)
# source = source["code,cui"].str.split(",",expand=True)
# source.columns=["code","cui"]


import re
test=[]
i=0
l=len(source)
for x in source["code"].to_list():
	i+=1
	print(i/l)
	return_list=[]
	print(x)

	x = str(x)
	for index,line in df.iterrows():

		# non-digital x
		# if str(line['l'])==str(line['r']):
		# 	if str(line['l'])==x:
		# 		return_list.append(str(line['CCS']))

		# else:
		# 	lc = re.findall(rx,l)[0]
		# 	xc = re.findall(rx,x)[0]
		# 	if lc==xc:
		# 		l_int = int(l.replace(lc,''))
		# 		r_int = int(r.replace(re.findall(rx,r)[0],''))
		# 		x_int = int(x.replace(xc,''))
		# 		if x_int>=l_int and x_int<=r_int:
		# 			return_list.append(x)

		if int(x) > int(line['r']) :
			continue
		# print(x)
		# print(line['l'])
		# print(line['r'])
		# print("----------")
		if int(line['l'])<=int(x) and int(x)<=int(line['r']):
			return_list.append(str(line['CCS']))

	test.append("|".join(return_list))

source["test"] = test

source.to_csv('/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/cpt_mapping/cpt_digit_test.csv',index=False)



		# elif not x.isdigit() and not l.isdigit():
		# 	print("%s, %s"%(x,l))
		# 	lc = re.findall(rx,l)[0]
		# 	xc = re.findall(rx,x)[0]
 
