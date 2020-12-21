import pandas as pd

df = pd.read_csv("cpt_char_test.csv")
df = df.drop(columns=['code']).dropna()
df = (df.set_index(df.columns.drop('cui',1).tolist())
	.cui.str.split('|', expand=True)
	.stack()
	.reset_index()
	.rename(columns={0:'cui'})
	.loc[:, df.columns]
)

df.to_csv('cpt_char.csv',index=False)
