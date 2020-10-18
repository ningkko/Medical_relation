# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json
import glob

files = glob.glob('neg_sample/*.csv')

df = pd.DataFrame()
for file in files:
	df = pd.concat([df,pd.read_csv(file)])

df = df.sort_values(by='cui')
with open('dicts/cui.json','r') as fp:
	d = json.load(fp)

def _map(x):
	if x in d:
		return d[x]
	else:
		return ""

df["cui"] = df["cui"].apply(lambda x: _map(x))
df.to_csv("neg_sample/template.csv",index=False)