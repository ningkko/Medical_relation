# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json

with open("mapping_data/loinc2text_dict.json","r") as fp:
	d = json.load(fp)

df2 = pd.read_csv("output/roll_up/shared_root_summary_g2.csv")
df3 = pd.read_csv("output/roll_up/shared_root_summary_g3.csv")

def find_description(x):
	if x in d:
		return d[x]
	return np.nan

df2["va_description"] = df2["va_loinc"].apply(lambda x: find_description(x))
df2["phs_description"] = df2["phs_loinc"].apply(lambda x: find_description(x))
df2 = df2.dropna()
print("%i pairs in g2 have descriptions"%len(df2))
df2.to_csv("output/roll_up/shared_root_summary_g2.csv", index=False)

df3["va_description"] = df3["va_loinc"].apply(lambda x: find_description(x))
df3["phs_description"] = df3["phs_loinc"].apply(lambda x: find_description(x))
df3 = df3.dropna()
print("%i pairs in g3 have descriptions"%len(df3))
df3.to_csv("output/roll_up/shared_root_summary_g3.csv", index=False)
