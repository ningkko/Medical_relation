# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json
import glob
import random

files = glob.glob('final/*.csv')

with open('dicts/cui.json','r') as fp:
	d = json.load(fp)


def _neg(x,pool):

	return "|".join(map(str, random.choices(pool, k=30)))

for file in files:
	print(file)
	df = pd.read_csv(file)
	neg_pool = df['code']
	df_n = df
	df_n["code"] = df_n["cui"].apply(lambda x: _neg(x,neg_pool))
	
	df_n = (df_n.set_index(df.columns.drop('code',1).tolist())
	.code.str.split('|', expand=True)
	.stack()
	.reset_index()
	.rename(columns={0:'code'})
	.loc[:, df.columns])

	print(df_n)
	df_n.to_csv("neg_sample/"+file.split("/")[-1],index=False)