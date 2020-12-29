import pandas as pd
import numpy as np

df=pd.read_csv("phe_denoised.csv")
df=df[["phecode","phecode_str","phecode_extend_cui"]]
df=df.drop_duplicates()

df["phecode_extend_cui"] = df["phecode_extend_cui"].str.split(",")
print("A")
df=df.set_index(['phecode',"phecode_str"]).apply(lambda x: x.apply(pd.Series).stack()).reset_index()

import json
with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/cui_str_dict_updated.json") as fp:
	d=json.load(fp)
def m(x):
	if x in d:
		return(d[x])
	return ""

df["cui"] = df["phecode_extend_cui"]
df["cui_terms"] = df["cui"].apply(lambda x: m(x))
df["code"] = df["phecode"]
df["code_terms"] = df['phecode_str']
df["hierarchy"] = np.array(0*len(df))

df=df[["cui",'cui_terms','code','code_terms',"hierarchy"]]
print(df)


df.to_csv("phecode.csv",index=False)