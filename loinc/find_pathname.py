# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json

with open("mapping_data/loinc2text_dict.json","r") as fp:
	d = json.load(fp)

df2 = pd.read_csv("output/roll_up/shared_root_summary_g2_raw.csv")
df3 = pd.read_csv("output/roll_up/shared_root_summary_g3_raw.csv")

def find_path_description(x):
	tag = x.split(":")[0]
	# in case if there's more than one :
	nodes = (":".join(x.split(":")[1:])).split(".")
	output = []
	for node in nodes:
		node = node.strip()
		if node in d:
			output.append(d[node])
		else:
			print(node)
			print(node in d)
			output.append("______")
	if output.count("______") == len(output):
		return np.nan
	return tag+": "+" | ".join(output)

def find_path_descriptio_common(x):
	nodes = x.split(".")
	output = []
	for node in nodes:
		node = node.strip()
		if node in d:
			output.append(d[node])
		else:
			print(node)
			output.append("______")
	if output.count("______") == len(output):
		return np.nan
	return " | ".join(output)

def _map(df):
	df["common_root"] = df["common_root"].apply(lambda x: find_path_descriptio_common(x))
	df["roll_up_to"] = df["roll_up_to"].apply(lambda x: find_path_description(x))
	df["before"] = df["before"].apply(lambda x: find_path_description(x))
	df = df.dropna()
	df = df[["va_loinc","phs_loinc","va_path","phs_loinc","#shared_nodes","common_root","roll_up_to","before"]]
	return df

df2 = _map(df2)
print("%i pairs in g2 have descriptions"%len(df2))
df2.to_csv("output/roll_up/shared_root_summary_g2.csv", index=False)

df3 = _map(df3)
print("%i pairs in g3 have descriptions"%len(df3))
df3.to_csv("output/roll_up/shared_root_summary_g3.csv", index=False)
