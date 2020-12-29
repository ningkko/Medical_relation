# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json

df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/automapping/source/archive/cui_rxnorm.tsv",sep='\t').drop_duplicates()
ddf = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/drug-rxnorm/RXNORM-ingredient-base.csv")
# print(len(ddf["base"].unique()))
# print(len(ddf["ingredient"].unique()))

ingredient = set(ddf["ingredient"])
base = set(ddf["base"])


# d = dict(zip(map(str,ddf["ingredient"]),map(str,map(int,ddf["base"]))))

# cui_term_d = dict(zip(df["CUI"].astype(str),df["STR"]))
# code_term_d = dict(zip(df["CODE"].astype(str),df["STR"]))
with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/cui_str_dict_updated.json",'r') as fp:
	d = json.load(fp)


# print(ddf["CUI"])
# print(d_cui_str)
def m2(x):
	'''map cui to rolled up string'''
	if x in d:
		return d[x].split("||")[0]
	return ""

def m(x):
	# if "RXNORM:" not in x:
		# return x 

	# else: 
	# x = str(x)

	if x in ingredient:
		return 0
	elif x in base:
		return 1
	else:
		return np.nan


# df = df.dropna().sort_values(by="code")
# def find_term(x,d):
# 	if x in d:
# 		return d[x]
# 	return np.nan

# print(df)
# df[["code","hierarchy"]] = df["code"].str.split(",",expand=True)
print(df.columns)
df["code"] = df["CODE"]
df["cui"] = df["CUI"].astype(str)
df["cui_terms"] = df["CUI"].apply(lambda x:m2(x))
df["code_terms"] = df["STR"]
df["hierarchy"] = np.array([0]*len(df))
df=df[["cui",'cui_terms','code','code_terms',"hierarchy"]]
df["code_level"] = df["code"].apply(lambda x: m(x))
base = df[df["code_level"]==0]
ingredient = df[df["code_level"]==1]
n = df[df["code_level"].isnull()]
# print(df)

n.drop("code_level",axis=1).to_csv("rxnorm_not_sure.csv",index=False)
base.drop("code_level",axis=1).to_csv("rxnorm_base.csv",index=False)
ingredient.drop("code_level",axis=1).to_csv("rxnorm_ingredient.csv",index=False)