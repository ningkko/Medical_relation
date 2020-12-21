# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json


## ========== adding prefix ==============
df = pd.read_csv("ccs_cui.csv",sep='\t')
df = df["code,cui"].str.split(",",expand=True)
df.columns=["code","cui"]
print(df)

df =df.drop_duplicates().dropna()
def add_prefix(p,x):
	return p+str(x)

df["code"] = df["code"].apply(lambda x: add_prefix("CCS-PCS-ext:",x))
print(df)
df.to_csv("ccs_cui2.csv",index=False)

### ============= loinc ==================

# df = pd.read_csv("loinc_cui.csv")
# print(df)

# df = df[~df["code"].str.contains("S")].sort_values(by=["code"])
# df = \
# (df.set_index(df.columns.drop('cui',1).tolist())
#    .cui.str.split(',', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'cui'})
#    .loc[:, df.columns]
# )

# df.to_csv("loinc_cui.csv",index=False)

### ============= phecode ==================
# df = pd.read_csv("phe_cui.csv",sep="\t").dropna()
# def delete(x):
# 	li=[]
# 	xs=x.split(",")
# 	for x in xs:
# 		if "[1]" in x:
# 			li.append(x.split(":")[0])
# 	return "|".join(li)

# df["cui"] = df['cui'].apply(lambda x:delete(x))

# print(df)
# df = \
# (df.set_index(df.columns.drop('cui',1).tolist())
#    .cui.str.split(',', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'cui'})
#    .loc[:, df.columns]
# )
# df = df.drop_duplicates().dropna()

# df.to_csv("phe_cui2.csv",index=False)

### ============= ccs ===================
# ccs = pd.read_csv("ccs_cui.csv")

# ccs = \
# (ccs.set_index(ccs.columns.drop('cui',1).tolist())
#    .cui.str.split('|', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'cui'})
#    .loc[:, ccs.columns]
# )
# ccs.to_csv("ccs_cui.csv",index=False)

### =========== rxnorm =====================

# df = pd.read_csv("rxnorm_cui.csv")


# # explode
# df = \
# (df.set_index(df.columns.drop('brand_cui',1).tolist())
#    .brand_cui.str.split('|', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'brand_cui'})
#    .loc[:, df.columns]
# )

# df = \
# (df.set_index(df.columns.drop('generic_cui',1).tolist())
#    .generic_cui.str.split('|', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'generic_cui'})
#    .loc[:, df.columns]
# )
# print(df)

# # ravel
# df = pd.DataFrame(pd.concat([df["cui"],df["generic_cui"],df["brand_cui"]]))
# df.columns =["cui"]

# print(df)

# with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/cui_str_dict_updated.json","r") as fp:
#   cui_str_dict = json.load(fp)
# with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/str_rxnorm_dict.json","r") as fp:
#   str_rxnorm_dict = json.load(fp)

# def _clean_name(x):
#     x = x.replace(" )","")
#     x = x.replace("|and ","/")
#     return x


# def _cui2string(x):
#   if x in cui_str_dict:
#     return cui_str_dict[x]
#   else:
#     return ""

# def _string_rxnorm(x):
#   if x in str_rxnorm_dict:
#     return int(str_rxnorm_dict[x])
#   else:
#     return ""

# df["cui_string"] = df["cui"].apply(lambda x: _cui2string(x))
# df["rxnorm"] = df["cui_string"].apply(lambda x: _string_rxnorm(x))

# df = df.replace("",np.nan).dropna().drop(columns=["cui_string"])
# print(df)

# df.to_csv("rxnorm_cui2.csv",index=False)