# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json

path="/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/broad_new_full_dict.txt"
df=pd.read_csv(path,sep='\t')

df = df["Dipalmitoyl Phosphatidylcholine|2|2|C0000039|Pharmacologic Substance|CHEM"].str.split("|",expand=True)
df.columns = ["n1",'e1','e2','c','n2','sub']
d = dict(zip(df['c'],df['e1']))

with open('cui.json','w') as fp:
	json.dump(d,fp,indent=4)

