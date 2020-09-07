# Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np

phe_CUI_df = pd.read_csv("/n/data1/hsph/biostat/celehs/SHARE/EHR_DICTIONARY_MAPPING/mapping/ICD_PheCode_CUI_broad_Mapping_yucong_08252020.csv",encoding="latin",dtype=str)
phe_CUI_df = phe_CUI_df.replace(np.nan,"",regex=True)
# phe_CUI_df = phe_CUI_df_raw.groupby(by=phe_CUI_df_raw["phecode"], as_index=False).count()
# print(phe_CUI_df.columns)
output_df = pd.DataFrame(phe_CUI_df["phecode"].unique())
output_df.columns = ["phecode"]


print("Matching Phe with CUI...")
icd_cuis = []
icd_cuis_extended = []
icd_strings = []
phe_strings = []

for i,item in enumerate(output_df["phecode"]):
	print((i+1)/len(output_df))
	item_icd_cuis = []
	item_icd_cuis_extended = []
	item_icd_strings = []
	item_phe_strings = []

	# find lines with the same phecode
	term_df = phe_CUI_df[phe_CUI_df["phecode"]==item]
	# add all id cuis and extends cuis 
	for cuis in term_df["icd_cui"].to_list():
		item_icd_cuis += cuis.split(",")
	for cuis in term_df["phecode_extend_cui"].to_list():
		item_icd_cuis_extended += cuis.split(",")

	icd_cuis.append("|".join(set(item_icd_cuis)))
	icd_cuis_extended.append("|".join(set(item_icd_cuis_extended)))
	icd_strings.append("|".join(set(term_df["icd10cm_str"].to_list())))
	phe_strings.append("|".join(set(term_df["phecode_str"].to_list())))


output_df["icd_cui"] = icd_cuis
output_df["icd_cuis_extended"] = icd_cuis_extended
output_df["str_icd"] = icd_strings
output_df["str_phe"] = phe_strings

output_df.replace(",","|",regex=True).replace(np.nan,"",regex=True).to_csv("phe_cpt.csv",index=False)
output_df.to_csv("(checked)phe_cui.csv",index=False)

# ========== BROAD DICT =================

# broad_df = pd.read_csv("dicts/broad.csv",encoding="Latin")
# print("Matching Phe with CUI...")
# CUIs=[]
# strings = []

# g = broad_df.groupby('CUI')
# l = len(g)
# i = 1
# for name, df in g:
# 	print(i/l)
# 	i+=1
# 	CUIs.append(name)
# 	strings.append("|".join(df["STR"].unique()))

# output_df = pd.DataFrame(broad_df["CUI"].unique())
# output_df["STR"] = strings
# output_df.to_csv("dicts/broad_df.csv",index=False)

