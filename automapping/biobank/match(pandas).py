# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
# import subprocess
import re
import numpy as np

pos = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/sample/pos_sample.csv"
pmifile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi.txt"
coocfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/cooc.txt"
sample = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/sample.csv"
pmi1000 = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi1000.txt"
cooc1000 = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/cooc1000.txt"

print("reading pos file...")
pos  = pd.read_csv(pos).astype(str)
anchor = set(pos["cui"])
# print(anchor)
## ------------ for the full biobank data ----------------

def is_in_pos(x):
	if x in anchor:
		return x
	else:
		return ""

def drop_null_name(x):
	if x=="|":
		return np.nan
	else:
		return x

print("reading pmi")
df = pd.read_csv(pmifile,sep='\n')
df.columns=["t"]
df = df["t"].str.split("\t",expand=True)
df.columns=["c1","c2","pmi"]
# print("=======")
# print(df)

## ------------ for anchors appeared in pos samples ----------
print("creating pos-pmi")

df_pos = df.copy()
# print(df_pos["c1"].unique())
df_pos["c1"] = df_pos["c1"].apply(lambda x: is_in_pos(x))
df_pos["c2"] = df_pos["c2"].apply(lambda x: is_in_pos(x))
df_pos["name"] = df_pos["c1"]+"|"+df_pos["c2"]
df_pos["name"] = df_pos["name"].apply(lambda x: drop_null_name(x))
df_pos = df_pos.replace("",np.nan).dropna()
# df_pos["name2"] = df_pos["c2"]+"|"+df_pos["c1"]
# pos1 = pd.DataFrame(df_pos[["name",'pmi']])
# pos2 = pd.DataFrame(df_pos[["name2",'pmi']])
# pos1.columns= ["pair",'pmi']
# pos2.columns=["pair",'pmi']
print("concating pos pmi")
# pos_pmi_df_full = pd.concat([pos1,pos2])
# pos_pmi_df_full = pos_pmi_df_full.drop_duplicates().dropna()
df_pos = df_pos[["name","pmi"]]
df_pos.columns=["pair",'pmi']
pos_pmi_df_full=df_pos.drop_duplicates().dropna()
## this is a bi-directional dataframe

## ------------ for anchors appeared in pos samples ----------

print("concating pmi")
# print("=======")
# print(df["c2"])

df["name"] = df["c1"]+"|"+df["c2"]
# df["name2"] = df["c2"]+"|"+df["c1"]
# s1 = pd.DataFrame(df[["name",'pmi']])
# s2 = pd.DataFrame(df[["name2",'pmi']])
# s1.columns=["pair",'pmi']
# s2.columns=["pair",'pmi']
# pmi_df_full = pd.concat([s1,s2])
# pmi_df_full = pmi_df_full.drop_duplicates().dropna()
df = df[["name","pmi"]]
df.columns=["pair",'pmi']
pmi_df_full=df.drop_duplicates().dropna()

#### ============= cooc =============


print("reading cooc")

c = pd.read_csv(coocfile,sep='\n')
c.columns=["t"]
c = c["t"].str.split(",",expand=True)
c.columns=["c1","c2","cooc"]
print("=======")
print(c)

## ------------ for anchors appeared in pos samples ----------

print("creating pos cooc")

c_pos = c.copy()
# print(c_pos["c1"].unique())
c_pos["c1"] = c_pos["c1"].apply(lambda x: is_in_pos(x))
c_pos["c2"] = c_pos["c2"].apply(lambda x: is_in_pos(x))
c_pos["name"] = c_pos["c1"]+"|"+c_pos["c2"]
c_pos["name"] = c_pos["name"].apply(lambda x: drop_null_name(x))
c_pos = c_pos.replace("",np.nan).dropna()
c_pos = c_pos[["name","cooc"]]
c_pos.columns=["pair",'cooc']
# c_pos["name2"] = c_pos["c2"]+"|"+c_pos["c1"]
# print("=======")
# print(c_pos)
# cpos1 = pd.DataFrame(c_pos[["name",'cooc']])
# cpos2 = pd.DataFrame(c_pos[["name2",'cooc']])
# cpos1.columns= ["pair",'cooc']
# cpos2.columns=["pair",'cooc']
# print("concating pos cooc")
# pos_cooc_df_full = pd.concat([cpos1,cpos2])
pos_cooc_df_full = c_pos.drop_duplicates().dropna()
# print("=======")
# print(pos_cooc_df_full)
## this is a bi-directional dataframe
## ------------ for anchors appeared in pos samples ----------
print("concating cooc")


c["name"] = c["c1"]+'|'+c["c2"]
# c["name2"] = c["c2"]+'|'+c["c1"]
# s1 = pd.DataFrame(c[["name",'cooc']])
# s2 = pd.DataFrame(c[["name2",'cooc']])
# s1.columns=["pair",'cooc']
# s2.columns=["pair",'cooc']
# cooc_df_full = pd.concat([s1,s2])
c = c[["name","cooc"]]

c.columns=["pair",'cooc']
cooc_df_full = c.drop_duplicates().dropna()
# print(cooc_df_full)


print("creating dictionary")

# create a dict of name-cooc 
d = dict(zip(cooc_df_full["pair"],cooc_df_full["cooc"]))
print("creating pos dictionary")

pos_d = dict(zip(pos_cooc_df_full["pair"],pos_cooc_df_full["cooc"]))

def m(x):
    if x in d:
        return d[x]
    else:
        return np.nan

print("mapping")

pmi_df_full["cooc"] = pmi_df_full["pair"].apply(lambda x: m(x))
pmi_df_full = pmi_df_full.drop_duplicates().dropna()
pmi_df_full = pmi_df_full.sort_values(by="pair")

pmi_df_full.to_csv("biobank.csv",index=False)

print("mapping pos")

pos_pmi_df_full["cooc"] = pos_pmi_df_full["pair"].apply(lambda x: m(x))
pos_pmi_df_full = pos_pmi_df_full.drop_duplicates().dropna()
pos_pmi_df_full = pos_pmi_df_full.sort_values(by="pair")

pos_pmi_df_full.to_csv("pos_biobank.csv",index=False)


print("deleting duplicates")

print("done")

