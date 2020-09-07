# Ning Hua
# yhua@smith.edu

import pandas as pd 
import numpy as np

output_df = pd.read_csv("(checked)phe_cui.csv", encoding="Latin")
cui_cpt_df = pd.read_csv("CUI_CPT.tsv",sep="\t", encoding="Latin")

cui_cpt_dict = dict(zip(cui_cpt_df["CUI"],cui_cpt_df["CODE"]))

def _map_icd(x):
	x = x.split("|")
	li = []
	for c in x:
		if c in cui_cpt_dict:
			print(c)
			li.append(cui_cpt_dict[c])
	return "|".join(li)

def _map_extended(x):
	x = x.split("|")
	li = []
	for c in x:
		if c.split(":")[0] in cui_cpt_dict:
			print(c)
			li.append(cui_cpt_dict[c.split(":")[0]]+c.split(":")[1])
	return "|".join(li)

output_df["cpt(icd_cui)"] = output_df["icd_cui"].apply(lambda x:_map_icd(x))
output_df["cpt(extended)"] = output_df["icd_cuis_extended"].apply(lambda x:_map_extended(x))

output_df.to_csv("phe_cpt.csv",index=False)
full_output = output_df[((output_df["cpt(icd_cui)"]!="")|(output_df["cpt(extended)"]))]

print("%f phecodes (%i out of %i) mapped."%(len(full_output)/len(output_df),len(full_output),len(output_df)))
