import subprocess
import os
import sys
import glob
import json
import numpy as np
import pandas as pd
from datetime import datetime

with open("exact_cui_log.txt", "a") as log_file:
	log_file.write("------------------ %s ------------------\n"%datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

dir_ = '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/MedScape_texts/NER/titles/cui_phe/title_txts/'

# ------------ load dictionary --------------
with open('exact_cui_phe_dict.json', 'r') as fp:
	cui_phe_dict = json.load(fp)

# --------------- mapping -------------------
files = []
for file in os.listdir(dir_):
	if file.endswith(".txt"):
		files.append(os.path.join(dir_, file))

for file in files:

	# construct dataframe
	names = [] 
	CUIs = []
	f = open(file, 'r')
	for line in f.readlines():
		terms = line.split("|")
		if len(terms)>1:		
			# get the title 
			names.append(terms[0])
			# get cuis
			if terms[2] != "NA":
				CUIs.append(terms[2].split(", "))			
			else:
				CUIs.append("NA")
	f.close()

	df = pd.DataFrame(names)
	df.columns = ["title"]
	df["CUIs"] = CUIs
	df = df[1:]

	# mapping
	phecodes = []
	exact_cuis = []
	mapped_num = 0
	empty_terms = 0

	i = 0
	l = len(df)

	for line in df.iterrows():
		# if i>200:
		# 	break
		i += 1
		print(i/l)

		CUIs = line[1][1]
		if CUIs == "NA":
			empty_terms += 1
			exact_cuis.append("NA")
			phecodes.append("NA")
		else:
			line_cuis = []
			line_phecodes = []
			for cui in CUIs:
				# print(cui)
				# cur_exact_cui = [key for key, value in cui_phe_dict.items() if cui in key]
				cur_phecode = [value for key, value in cui_phe_dict.items() if cui in key]
				if cur_phecode:
					line_cuis.append(cui)
					line_phecodes.append(",".join(set(cur_phecode)))

			if not line_cuis:	
				exact_cuis.append("NA")
				phecodes.append("NA")
			else:
				exact_cuis.append("|".join(set(line_cuis)))
				phecodes.append("|".join(set(line_phecodes)))
				mapped_num += 1 

	df["exact_CUI"] = exact_cuis
	df["phecodes"] = phecodes
	with open("exact_cui_log.txt", "a") as log_file:
		log_file.write("%s/ has %i titles mapped to PheCode using exact mapping.\n "%(file.split("/")[-1].replace(".txt", ""), mapped_num))
		log_file.write("The source has %i drugs. Overall mapping rate: %f.\n"%(l, mapped_num/l))
		log_file.write("The source has %i drugs with >= 1 CUI mappings. Mapping rate: %f\n\n"%(l-empty_terms, mapped_num/(l-empty_terms)))
			
	df.to_csv("mapping results/"+file.split("/")[-1].replace(".txt", "")+"_phe_exact.csv", index=False)
	print("Done")
