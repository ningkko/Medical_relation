import pandas as pd
import json
import numpy as np

df = pd.read_csv("ccs.csv")
df["code"]=df["ccs"]
df["code_terms"] = df["description"]
with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/cui_str_dict_updated.json",'r') as fp:
	d = json.load(fp)


# print(ddf["CUI"])
# print(d_cui_str)
def m2(x):
	'''map cui to rolled up string'''
	if x in d:
		return d[x].split("||")[0]
	return ""
df["cui_terms"] = df["cui"].apply(lambda x:m2(x))
df["hierarchy"] = np.array([0]*len(df))
df=df[["cui",'cui_terms','code','code_terms',"hierarchy"]]
df.to_csv("ccs.csv",index=False)