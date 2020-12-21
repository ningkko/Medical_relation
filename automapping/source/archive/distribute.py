import pandas as pd
import numpy as np
import json
import glob

files = glob.glob('../final/*.csv')

print(files)
df = pd.DataFrame()
s = pd.read_csv("cui_code_yuheng.csv")

def isnode(x):
	if x.upper()==x.lower():
		return x
	else:
		return np.nan

for file in files:
	print(file )
	des = pd.read_csv(file)		
	if "ccs" in file:
		ccs = s[s["code"].str.contains("CCS")]
		print(ccs)
		ccs["code"] = ccs["code"].str.replace("CCS:","")
		ccs["code"] = "CCS-PCS-ext:"+ccs["code"].astype(str)
		des = pd.concat([ccs,des]).sort_values("cui")
		des.to_csv("../final/cui_ccs2.csv",index=False)

	elif "phe" in file:
		phe = s[s["code"].str.contains("PheCode")]
		print(phe)

		des = pd.concat([phe,des]).sort_values("cui")
		des.to_csv("../final/PheCode2.csv",index=False)

	elif "loinc" in file:
		loinc = s[s["code"].str.contains("LOINC")]
		print(loinc)
		loinc["code"] = loinc["code"].str.replace("LOINC:","")
		loinc["code"] = loinc["code"].apply(lambda x: isnode(x))
		loinc = loinc.dropna()
		des = pd.concat([loinc,des]).sort_values("cui")
		des.to_csv("../final/cui_loinc2.csv",index=False)



