import pandas as pd
import numpy as np
import ast
import json

icd_df = pd.read_csv("../mapping data/disease_phe_broad.csv", encoding = "latin", dtype="str")
icd_df = icd_df.replace(np.nan, '', regex=True)

phecode = icd_df["phecode"].to_list()

phecode_cui = icd_df["phecode_extd_cui"].apply(lambda x: x.split(", ")).to_list()
icd_cui = icd_df["icd_extd_cui"].apply(lambda x: x.split(", ")).to_list()


# create a dictionary
phecui_phecode_dict = dict(zip(str(phecode_cui), phecode))
icdcui_phecode_dict = dict(zip(str(icd_cui), phecode))

# phecui_phecode dict 
with open('../mapping data/dictionary/phecui_phecode_dict.json', 'w') as fp:
    json.dump(phecui_phecode_dict, fp, indent=4)


# icdcui_phecode dict
with open('../mapping data/dictionary/icdcui_phecode_dict.json', 'w') as fp:
    json.dump(icdcui_phecode_dict, fp, indent=4)