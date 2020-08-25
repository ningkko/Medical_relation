# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import re
import string
import json

df = pd.read_csv("/n/data1/hsph/biostat/celehs/EHR_mapping/temporary/dict_fake_VA_to_Tianxi.csv")

def translate(x):
	if type(x)!=float:
		return x.translate(str.maketrans('', '', string.punctuation)).replace(" ","")
	return ""

# clean punctuations 
test_name = df["LabChemTestName"].apply(lambda x: translate(x).lower().replace(" ",""))
print_name = df["LabChemPrintTestName"].apply(lambda x:translate(x).lower().replace(" ",""))
df["indicator"] = test_name

with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/loinc2text_dict.json") as fp:
	dictionary = dict([(translate(value).lower().replace(" ",""), key) for key, value in  json.load(fp).items()]) 

def find_loinc(x):
	if x in dictionary:
		return dictionary[x]

	return ""
test_loinc = test_name.apply(lambda x:find_loinc(x))
print_loinc = print_name.apply(lambda x:find_loinc(x))
loinc = []
different = 0
missing = 0
for tl,pl in zip(test_loinc, print_loinc):
	if tl or pl:
		if tl == "" or tl==pl:
			loinc.append(pl)
		elif pl == "":
			loinc.append(tl)
		else:
			different += 1
			loinc.append(tl)
	else: 
		missing += 1
		loinc.append(np.nan)

df["test_loinc"] = test_loinc
df["print_loinc"] = print_loinc
df["loinc"] = loinc
df = df.dropna().drop_duplicates(subset=['indicator']).drop(columns=["indicator"]).sort_values(by=["test_loinc"], ascending=False)
unique_test_loincs = len(df["test_loinc"].dropna().unique())
print("%i lines mapped, %i of which are mapped from lab_test_names.\n%i lines have different loinc code mapping. %i lines not mapped"%(len(loinc), unique_test_loincs,different,missing))
df.to_csv("output/fake/exact_mapping.csv", index=False)


