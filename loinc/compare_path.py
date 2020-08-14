# Author: Ning Hua
# yhua@smith.edu

# import pandas as pd
# import numpy as np

# # va_path = pd.read_csv("output/va_path_text.csv")
# va_path = pd.read_csv("output/va_path_loinc.csv")
# va_path.columns = ["LOINC", "va_path"]
# phs_path = pd.read_csv("output/phs_path.csv")
# phs_path.columns = ["LOINC", "phs_path"]

# print("Number of va paths: %i"%len(va_path))
# print("Number of phs paths: %i"%len(phs_path))

# df = pd.merge(va_path, phs_path, on="LOINC", sort=True).dropna()
# print("Number of same LOINCs: %i"%(len(df)))

# df.to_csv("joined_path.csv", index=False)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json

print("Preprocessing... Dropping nan and duplicates.")
phs = pd.read_csv("mapping_data/phs_loinc.csv")
va = pd.read_csv("mapping_data/core_team.csv")

with open("mapping_data/path_dict.json","r") as fp:
	path_dict = json.load(fp)

def find_path(x):
	if x in path_dict:
		return path_dict[x]
	return ""

phs["loinc"] = phs["feature_id"].apply(lambda x: x.split(":")[1].strip())
phs["path"] = phs["loinc"].apply(lambda x: find_path(x))
phs = phs[["loinc", "path"]].dropna().drop_duplicates()
phs_loinc = phs["loinc"].to_list()
phs_path = phs["path"].to_list()

va["loinc"] = va["LOINC"]
va["path"] = va["loinc"].apply(lambda x: find_path(x))
va = va[["loinc", "path"]].dropna().drop_duplicates()
va_loinc = va["loinc"].to_list()
va_path = va["path"].to_list()
print("%i va_paths and %i phs_paths (%i pairs) waiting to be evaluated."%(len(va_path), len(phs_path), len(va_path)*len(phs_path)))


def find_common_roots(x,y):
	"""
	returns the common root.
	the function assumes that x has fewer nodes than y
	"""
	x = x.split(".")
	y = y.split(".")
	shared = []
	for i in range(min(len(x), len(y))):
		if x[i] == y[i]:
			shared.append(x[i])
	return ".".join(shared)


shared_paths = []
num_shared_nodes = []
# for keeping the flattened permutation structure
va_paths = []
phs_paths = []

v_l = []
p_l = []


l = len(va_path)
print("Mapping...")
i_prev = 0 
for i in range(len(va_path)):
	progress = i/l
	if progress - i_prev > 0.1:
		print(progress)
		i_prev = progress

	for j in range(len(phs_path)):
		v_l.append(va_loinc[i])
		p_l.append(phs_loinc[j])
		va_paths.append(va_path[i])
		phs_paths.append(phs_path[j])
		
		c_root = find_common_roots(va_path[i], phs_path[j])
		shared_paths.append(c_root)

		if c_root:
			num_shared_nodes.append(c_root.count(".")+1)
		else:
			num_shared_nodes.append(0)


print("%i pairs have shared roots. "%np.count_nonzero(num_shared_nodes))
print("Writing...")

# df["common root"] = shared_paths
# df["diff level"] = diff_level

data = {'va_loinc': v_l,
		'phs_loinc': p_l,
		'va_path': va_paths,
		'phs_path': phs_paths,
		'common_root': shared_paths,
		'#shared_nodes': num_shared_nodes}

df = pd.DataFrame(data)

shared_df = df[df["#shared_nodes"]>2]
noshared_df = df[df["#shared_nodes"]==0]
print("%i pairs have more than 1 shared roots. %i pairs DO NOT have shared roots."%(len(shared_df), len(noshared_df)))

shared_df.sort_values(["va_loinc", "phs_loinc"], ascending = (True, True)).to_csv("output/roll_up/shared_root_summary_g3.csv", index=False)
# noshared_df.sort_values(["va_loinc", "phs_loinc"], ascending = (True, True)).to_csv("output/roll_up/no_common_root_summary.csv", index=False)

print("Plotting distribution...")

plt.bar(*zip(*Counter(shared_df["#shared_nodes"].to_list()).items()))
  
plt.xlabel("Number of common nodes in one (VA_path, PHS_path)") 
plt.ylabel("Number of occurrences") 
plt.title("Common Node Distribution") 
plt.savefig("output/roll_up/common_node_dist_g3.png")


