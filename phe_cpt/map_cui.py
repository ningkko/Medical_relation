# Ning Hua
# yhua@smith.edu

import pandas as pd 
import numpy as np
import json
import re

# broad_df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/broad_new_full_dict2019.txt",sep='\t',encoding="Latin")
# broad_df.columns=["content"]
# broad_df[['STR','CUI','TYPE','GROUP']] = broad_df.content.str.split("|",expand=True,)
# broad_df = broad_df.drop('content',axis=1)
# broad_df.to_csv("broad.csv",index=False)

output_df = pd.read_csv("phe_cpt.csv", encoding="Latin").replace(np.nan,"",regex=True)
cui_cpt_df = pd.read_csv("CUI_CPT.tsv",sep="\t", encoding="Latin").replace(np.nan,"",regex=True)

def de_paren(x):
	p = re.compile(r'\([^)]*\)')
	return re.sub(p, '', x)
def _clean_name(x):
    x = de_paren(x.lower().replace(",","").replace(" / ", "/").replace("|and","/"))
    return x

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/str_cui_dict_updated.json") as fp:
	str_cui_dict = json.load(fp)

cui_cpt_dict = dict(zip(cui_cpt_df["CUI"],cui_cpt_df["CODE"]))

# map phe_cui to cpt_cui
phec2cptc_df = pd.read_csv("dicts/procedure_diagnoses.csv", encoding="Latin")
phec2cptc_dict = dict(zip(phec2cptc_df["CUI2"],phec2cptc_df["CUI1"]))

def _map(x , _dict):
	x = x.split("|")
	li = []
	for c in x:
		# c = _clean_name(c)
		if c in _dict:
			# print(c)
			li.append(_dict[c])
	return "|".join(li)

def _map_extended(x, _dict):
	x = x.split("|")
	li = []
	for c in x:
		if c.split(":")[0] in _dict:
			li.append(_dict[c.split(":")[0]]+":"+c.split(":")[1])
	return "|".join(li)

output_df["cpt_cui"] = output_df["icd_cui"].apply(lambda x: _map(x,phec2cptc_dict))
output_df["cpt_cui_extended"] = output_df["icd_cuis_extended"].apply(lambda x: _map_extended(x,phec2cptc_dict))


# str_cpt_dict = dict(zip(cui_cpt_df["STR"].apply(lambda x:_clean_name(x)),cui_cpt_df["CODE"]))


output_df["cpt(cui)"] = output_df["cpt_cui"].apply(lambda x:_map(x, cui_cpt_dict))
output_df["cpt_extended(cui)"] = output_df["cpt_cui_extended"].apply(lambda x:_map_extended(x, cui_cpt_dict))
output_df["cpt"] = output_df["cpt(cui)"]+"|"+output_df["cpt_extended(cui)"]
output_df["cpt"] = output_df["cpt"].apply(lambda x: x.strip("|"))
output_df = output_df.drop(["str_icd","str_phe","cpt(icd_cui)","cpt(extended)"],axis=1)

output_df.to_csv("phe_cui_cpt.csv",index=False)
full_output = output_df[(output_df["cpt"]!="")]

print("%f phecodes (%i out of %i) mapped."%(len(full_output)/len(output_df),len(full_output),len(output_df)))
missing_phe2cui = len(output_df)-len(output_df[(output_df["cpt_cui"]!="")|(output_df["cpt_cui_extended"]!="")])
missing_cui_cpt = len(output_df[(output_df["cpt_cui"]!="")|(output_df["cpt_cui_extended"]!="")]) - len(output_df[output_df["cpt"]!=""])
print("%i phecodes not mapped to cui(cpt), %i cui(cpt) not mapped to cpt"%(missing_phe2cui, missing_cui_cpt))
