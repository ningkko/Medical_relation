import pandas as pd
import numpy as numpy

df=pd.read_csv("PheCode_broad_Mapping_freq.csv")
df=df[df["noise"].notnull()]
noise = df["code"].to_list()

ddf = pd.read_csv("/n/data1/hsph/biostat/celehs/SHARE/EHR_DICTIONARY_MAPPING/mapping/ICD_PheCode_CUI_broad_Mapping_yucong_08252020.csv",encoding='Latin')
def m(x):
	xs=x.split(",")
	li=[]
	for x in xs:
		if '[0]' in x and x.split(":")[0] in noise:
			pass
		else:
			li.append(x.split(":")[0])
	return ",".join(li)

ddf["phecode_extend_cui"] = ddf["phecode_extend_cui"].apply(lambda x: m(x))
ddf.to_csv("phe_denoised.csv", index=False)