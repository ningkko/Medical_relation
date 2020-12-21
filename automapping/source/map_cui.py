# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json
import glob

df=pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/automapping/source/sample/archive/pos_sample2.csv")
df=pd.DataFrame(columns=["cui","code"])
for name in glob.glob('final/*'):
    df=pd.concat([df,pd.read_csv(name)]) 
# with open('dicts/cui.json','r') as fp:
# 	d = json.load(fp)

# ddf = pd.DataFrame.from_dict({y:x for x,y in d.items()},orient='index')
# ddf.reset_index(level=0, inplace=True)
# print(len(ddf))
# ddf.columns=["code","cui"]
# ddf["code"]=ddf["code"].str.split("|")
# ddf=ddf.explode("code")
# print(len(ddf))
# d = dict(zip(ddf["code"],ddf["cui"]))

# def _map(x):
# 	x = str(int(float(x)))
# 	if x in d:
# 		return d[x]
# 	else:
# 		return ""

# df["cui"] = df["cui"].apply(lambda x: _map(x))

# df = df.dropna().sort_values(by='cui')
print(df)
df.to_csv("final/pos_sample_cui_not_mapped.csv",index=False)