df_d = pd.DataFrame()
df_d['l'] = df["l"].map(lambda x: _isdigit(x))
df_d['r'] = df["r"].map(lambda x: _isdigit(x))

df_d['CCS'] = df["CCS"]
df_d = df_d.replace("",np.nan).dropna()
df_d.to_csv('map_char.csv',index=False)
	
df["Code Range"] = df["Code Range"].str.replace("\'","")

def _splitl(x):
	xs=x.split("-")
	if xs:
		return xs[0]
	else:
		return x

def _splitr(x):
	xs=x.split("-")
	if xs:
		return xs[1]
	else:
		return x

df["l"] = df["Code Range"].apply(lambda x:_splitl(x))
df["r"] = df["Code Range"].apply(lambda x:_splitr(x))
df.to_csv("2019_ccs_services_procedures.csv",index=False)