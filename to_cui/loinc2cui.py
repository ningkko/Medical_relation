# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import re
import string
import json

df = pd.read_csv("raw_data/codebook.csv")

with open("/n/data1/hsph/biostat/celehs/yih798/loinc/VA_PHS/mapping_data/path_dict.json", 'r') as fp: 	
	path_dict = json.load(fp)

dict_df = pd.read_csv("raw_data/umls_loinc.csv", sep="\t")
with open("cui_loinc_dict.json",'r') as fp:
	LOINC_CUI_dict = json.load(fp)

#print(LOINC_CUI_dict)
loinc = df["feature_id"].apply(lambda x: x.split(":")[1].strip())

def find_CUI(x):
	x = re.sub(r'[A-Z]+', '', x).strip()
	if x in path_dict:
		path = path_dict[x]
		nodes = path.split(".")
		nodes.append(x)
		cuis = []
		for n in nodes:
			if n in LOINC_CUI_dict:
				cuis.append(LOINC_CUI_dict[n])
		if cuis:
			return "|".join(cuis)
	return np.nan
		
df["CUI"] = loinc.apply(lambda x: find_CUI(x))
df = df.drop_duplicates("feature_id")

reg = re.compile( "[a-zA-Z]")

def find_ind(x):
	prefix = reg.findall(x)
	return "".join(prefix)

df["indicator"] = loinc.apply(lambda x: find_ind(x))
# def _translate(x):
# 	if type(x)!=float:
# 		return x.translate(str.maketrans('', '', string.punctuation)).replace(" ","").lower().replace(" ","")
# 	return ""

# with open("../VA_PHS/mapping_data/loinc2text_dict.json","r") as fp:
# 	dictionary = dict([(_translate(value).lower().replace(" ",""), key) for key, value in  json.load(fp).items()]) 

# with open("STR_LOINC.json","w") as fp:
# 	json.dump(dictionary, fp, sort_keys=True, indent=4)

# def find_LOINC(x):
# 	x = _translate(x)
# 	if x in dictionary:
# 		return dictionary[x]
# 	return np.nan

# # clean punctuations 
# loinc = df["STR"].apply(lambda x: find_LOINC(x))
# df["LOINC"] = loinc
df_new = df.dropna(subset=["CUI"])
print("%i lines CUIs mapped. %i lines missing"%(len(df_new),len(df)-len(df_new)))
df.to_csv("output/CUI_LOINC.csv", index=False)


