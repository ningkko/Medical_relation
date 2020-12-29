import pandas as pd
import numpy as np
import json
df=pd.read_csv("/n/data1/hsph/biostat/celehs/SHARE/EHR_DICTIONARY_MAPPING/mapping/ICD_PheCode_CUI_broad_Mapping_yucong_08252020.csv", encoding='Latin')
print(df)

# check null entries
dd=df[~df["icd_cui"].isnull()]
print(dd)

# get rid of the second icd_cui if there's any
def m(x):
	if type(x)!=float:
		if ',' in x:
			return x.split(",")[0]
	return x

df["icd_cui"] =df["icd_cui"].apply(lambda x: m(x))

df.to_csv("ICD_PheCode_CUI_broad_Mapping.csv",index=False)
