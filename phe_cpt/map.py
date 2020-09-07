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
str_cpt_dict = dict(zip(cui_cpt_df["STR"].apply(lambda x:_clean_name(x)),cui_cpt_df["CODE"]))


def _map(x):
	x = x.split("|")
	li = []
	for c in x:
		c = _clean_name(c)
		if c in str_cpt_dict:
			# print(c)
			li.append(str_cpt_dict[c])
	return "|".join(li)


output_df["CPT(phe_str)"] = output_df["str_phe"].apply(lambda x:_map(x))
output_df["CPT(icd_str)"] = output_df["str_icd"].apply(lambda x:_map(x))
output_df["CPT"] = output_df["cpt(icd_cui)"]+"|"+output_df["cpt(extended)"]+"|"+output_df["CPT(phe_str)"]+"|"+output_df["CPT(icd_str)"]
output_df["CPT"] = output_df["CPT"].apply(lambda x: x.strip("|"))

output_df.to_csv("phe_cpt_stringmapped.csv",index=False)
full_output = output_df[(output_df["CPT"]!="")]

print("%f phecodes (%i out of %i) mapped."%(len(full_output)/len(output_df),len(full_output),len(output_df)))
