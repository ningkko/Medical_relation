import pandas as pd
import numpy as np

df=pd.read_csv("ICD_PheCode_CUI_broad_Mapping.csv")
df["cui"] = df["icd_cui"]
df["cui_terms"] = df["icd10cm_str"]
df["code"] = df["icd10cm"]
df["code_terms"] = df['icd_cui_term']
df["hierarchy"] = np.array(0*len(df))

df=df[["cui",'cui_terms','code','code_terms',"hierarchy"]]
print(df)


df.to_csv("icd.csv",index=False)