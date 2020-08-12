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

def _map(df):
	va_path = df["va_path"].to_list()
	phs_path = df["phs_path"].to_list()
	va_description = df["va_description"].to_list()
	phs_description = df["phs_description"].to_list()

	roll_up_to = []
	before = []
	for i in range(len(df)):
		if va_path[i].count(".")>phs_path[i].count("."):
			roll_up_to.append(phs_description[i]+" (phs)")
			before.append(va_description[i]+" (va)")
		else:
			before.append(phs_description[i]+" (phs)")
			roll_up_to.append(va_description[i]+" (va)")
	df = df.drop(["va_description", "phs_description"], axis=1)
	df["roll_up_to"] = roll_up_to
	df["before"] = before
	return df

df2 = _map(df2)
df3 = _map(df3)

print(len(df2))
print(len(df3))
df2.to_csv("output/roll_up/shared_root_summary_g2.csv", index=False)
df3.to_csv("output/roll_up/shared_root_summary_g3.csv", index=False)

