import pandas as pd
import numpy as np
import json
df=pd.read_csv("/n/data1/hsph/biostat/celehs/SHARE/EHR_DICTIONARY_MAPPING/mapping/ICD_PheCode_CUI_broad_Mapping_yucong_08252020.csv", encoding='Latin')
print(df)

# check null entries
dd=df[~df["phecode_extend_cui"].isnull()]
print(dd)

# keep [1] entries (exact mapping)
# for [0] entries:
# 	1. check frequency 
#	2. check corresponding strings
#	3. denoise


# print(len(unsure))
ddf=pd.DataFrame()
ddf["phecode"] = df["phecode"]
ddf["phecode_str"] = df["phecode_str"]
ddf["phecode_extend_cui"] = df["phecode_extend_cui"]
ddf["phecode_extend_cui_term"] = df["phecode_extend_cui_term"].replace(", ","&",regex=True)
ddf = ddf.drop_duplicates()


i=0

keys=[]
values=[]

unsure = []
for phe_cuis in ddf["phecode_extend_cui"]:
	phe_cuis = phe_cuis.split(",")
	# store [0] cuis for each phecode
	li=[]
	for cui in phe_cuis:
		keys.append(cui)
		if "[0]" in cui:
			li.append(cui.split(":")[0])
			i+=1
	unsure.append(li)

for strings in ddf["phecode_extend_cui_term"]:
	strings = strings.split(",")
	# store [0] cuis for each phecode
	for s in strings:
		values.append(s)
			

def stringfy(x):
	return ",".join(x)

print(len(keys))
print(len(values))
	
ddf["extended"] = list(map(stringfy,unsure))

# d = dict(zip(keys,values))

# match string
with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/cui_str_dict_updated.json", 'r') as fp:
	d = json.load(fp)
def m(x):
	xs = x.split(",")
	li = []
	for x in xs:
		if x in d:
			li.append(d[x])
		li.append("MISSING")
	return ",".join(li)

ddf["phecode_extend_str"] = ddf["extended"].apply(lambda x: m(x))
ddf.to_csv("PheCode_broad_Mapping.csv",index=False)
