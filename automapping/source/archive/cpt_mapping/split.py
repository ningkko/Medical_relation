# Author: Ning
# makiasagawa@gmail.com

import pandas as pd
import numpy as np
import json


# df = pd.read_csv("2019_ccs_services_procedures.csv")
def _isdigit(x):
	if x.isdigit():
		return x
	else: 
		return ""

def _isndigit(x):
	if not x.isdigit():
		return x
	else: 
		return ""

df = pd.read_csv("cui_cpt.tsv",sep='\t')

df = df.groupby(['code'])['cui'].apply(lambda x: '|'.join(x)).reset_index()

df_d = pd.DataFrame()
df_d['code'] = df["code"].map(lambda x: _isdigit(x))

df_d['cui'] = df["cui"]

df_d = df_d.replace("",np.nan).dropna()
df_d.to_csv('cpt_digit.csv',index=False)

df_c = pd.DataFrame()
df_c['code'] = df["code"].map(lambda x: _isdigit(x))

df_c['cui'] = df["cui"]

df_c = df_c.replace("",np.nan).dropna()
df_c.to_csv('cpt_char.csv',index=False)