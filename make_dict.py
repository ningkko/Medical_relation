import pandas as pd
import numpy as np
import ast
import re
import json

icd_df = pd.read_excel("../../../../yl561/Phecode-cui_mapping/icd10cm2cui_umls2019.xlsx", encoding = "latin", dtype="str")
icd_df = icd_df.replace(np.nan, '', regex=True)

phecode = icd_df["phecode"]

def filter_main_CUI(x):
	ls = []
	xs = x.split(",")
	for cui in xs:
		if '[1]' in cui:
			ls.append(cui)
	return ls

phecode_cui = icd_df["phecode_extd_cui"].apply(lambda x: filter_main_CUI(x))
icd_extd_cui = icd_df["icd_extd_cui"].apply(lambda x: filter_main_CUI(x))
icd_cui = icd_df["icd_cui"].apply(lambda x: x.split(","))
phe_cui = icd_df["phecode_cui"].apply(lambda x: x.split(","))


cui = phecode_cui + icd_extd_cui + icd_cui + icd_cui

cui = cui.apply(lambda x :"|".join(set(x)))

#-------- build dict -----------

cui_phe_dict_extended = dict(zip(cui, phecode))

with open('exact_cui_phe_dict.json', 'w') as fp:
    json.dump(cui_phe_dict_extended, fp, indent=4)
