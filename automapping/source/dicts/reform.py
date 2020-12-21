import pandas as pd
import numpy as np
import json

with open("cui.json",'r') as fp:
	d = json.load(fp)

print(len(d))
df = pd.DataFrame({'col1': list(d.values()), 'col2': list(d.keys())})
print(df)

df = (df.set_index(df.columns.drop('col2',1).tolist())
		.col2.str.split(';', expand=True)
		.stack()
		.reset_index()
		.rename(columns={0:'col2'})
		.loc[:, df.columns])
print(df)

df = df.groupby(["col2"])['col1'].apply('|'.join).reset_index()
print(len(df))
df = df.sort_values(by="col1")

d = dict(zip(df["col2"],df["col1"]))
print(len(d))

with open("cui2.json",'w') as fp:
	json.dump(d,fp,indent=4)