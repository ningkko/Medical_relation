import pandas as pd
import numpy as np
import json


# ddf = pd.read_csv("mrconso_chi.txt",sep='\n')
# ddf=ddf["C0008138|ENG|S|L0008138|PF|S0024528|N|A8311744||||HL7V2.5|PT|CHI|Chiropractic|0|N|256|"].str.split("|",expand=True)
# ddf.columns=['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 'SAUI',
#        'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 'SUPPRESS', 'CVF',""]
# base=ddf[~ddf["STR"].str.contains(":")]
# d_str_cui = dict(zip(base["STR"],base["CUI"]))

# print(d_str_cui)
df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/automapping/source/rollup/ARCHIVE/loinc.tsv",sep='\t',encoding='Latin')
ddf = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/automapping/source/rollup/loinc_rolled.csv",encoding='Latin')
df['STR'] = df["STR"].astype(str)
df['STR'] = df[['CODE','STR']].groupby(['CODE'])['STR'].transform(lambda x: '||'.join(x))
df[["CODE","STR"]].drop_duplicates()

# print(df)
def m(x):
	if x.upper().lower()==x:
		return x
	else:
		return np.nan

df["code"]=df["CODE"].apply(lambda x: m(x))
df=df[df["code"].notnull()]

print(df)

d_cui_cui = dict(zip(ddf["CUI"],ddf["ROLLED_CUI"]))

def m(x):
	if x in d_cui_cui:
		return d_cui_cui[x]+",-1"
	return x+",0"

df["cui"] = df["CUI"].apply(lambda x: m(x))
df[["cui","hierarchy"]] = df["cui"].str.split(",",expand=True)

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/cui_str_dict_updated.json",'r') as fp:
	d = json.load(fp)


# print(ddf["CUI"])
# print(d_cui_str)
def m2(x):
	'''map cui to rolled up string'''
	if x in d:
		# return d[x].split("||")[0]
		return d[x]
	return x
# print(df["cui"])

df["cui_terms"] = df["cui"].apply(lambda x: m2(x))
# print(df["mapped_terms_cui"].dropna())
# pd.DataFrame(df[["mapped_terms_cui"]].dropna()).to_csv("test.csv")
# pd.DataFrame(df[["STR","mapped_terms_cui"]]).to_csv("test.csv")
# d_str_str = dict(zip(df["STR"],df["mapped_terms_cui"]))
# with open("dict.json",'w') as fp:
# 	json.dump(d_str_str,fp,indent=4)
# print(d_str_str)
# def m3(x):
# 	if type(d_str_str[x])!=float:
# 		return d_str_str[x]
# 	return x 
	
# df["cui_terms"] = df["STR"].apply(lambda x: m3(x))
df["code_terms"]= df["STR"]
df["code"] = df["CODE"]

# print(d_cui_cui)
# broad="/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/str_cui_dict_updated.json"
# with open(broad,"r") as fp:
# 	str_d = json.load(fp)

df=df[["cui","cui_terms","code","code_terms","hierarchy"]]
df["cui"]=df["cui"].str.split("|")
df=df.explode("cui")
df=df.sort_values("cui")
# print(df)



# ###--------chinese---------
# df2 = pd.read_csv("loinc_rolled.csv")
# d=dict(zip(df2["LOINC"],df2["ROLLED_CUI"]))
# def m(x):
# 	if x in d:
# 		return d[x]
# 	else:
# 		return ""
# df["ROLLED_CUI"]=df["CODE"].apply(lambda x: m(x))
df.to_csv("/n/data1/hsph/biostat/celehs/yih798/code-cui/loinc.csv",index=False)
df.to_csv("loinc.csv",index=False)





