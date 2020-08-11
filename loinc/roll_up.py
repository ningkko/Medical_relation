# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json

va_loinc = pd.read_csv("mapping_data/phs_loinc.csv")["feature_id"].apply(lambda x: x.split(":")[1]).unique()
phs_loinc = pd.read_csv("mapping_data/core_team.csv")["LOINC"].unique()

with open("mapping_data/roll_up_dict.json","r") as fp:
	roll_up_dict = json.load(fp)
with open("mapping_data/path_dict.json","r") as fp:
	path_dict = json.load(fp)

# ----------------------- VA --------------------------
print("Rolling VA...")
rolled_up_va = []
rolled_up_level = []
n = 0
for v in va_loinc:
	if v in roll_up_dict:
		rolled_up_va.append(roll_up_dict[v])
		roll_up_level.append(path_dict[v].count(".") - path_dict[rolled_up_va].count("."))
		n += 1
	else:
		rolled_up_va.append(v)
		roll_up_level.append(0)

print("VA: %i loincs rolled up. %i loincs remain unchanged."%(n, len(va_loinc)-n))

df = pd.DataFrame(va_loinc)
df.columns = ["LOINC"]
df["rolled_up"] = rolled_up_va
df["roll_up_level"] = roll_up_level
df.to_csv("output/roll_up/va.csv", index=False)


print("Plotting summary...")

plt.bar(*zip(*Counter(roll_up_level).items()))
  
plt.xlabel("Rolled_up level") 
plt.ylabel("Number of occurrences") 
plt.title("Roll-up Distribution") 

plt.savefig("output/roll_up/va_roll_up_distribution.png")

# ----------------------- PHS --------------------------
print("Rolling PHS...")

rolled_up_phs = []
rolled_up_level = []
n = 0
for v in phs_loinc:
	if v in roll_up_dict:
		rolled_up_va.append(roll_up_dict[v])
		roll_up_level.append(path_dict[v].count(".") - path_dict[rolled_up_va].count("."))
		n += 1
	else:
		rolled_up_phs.append(v)
		roll_up_level.append(0)

print("PHS: %i loincs rolled up. %i loincs remain unchanged."%(n, len(phs_loinc)-n))

df = pd.DataFrame(phs_loinc)
df.columns = ["LOINC"]
df["rolled_up"] = rolled_up_va
df["roll_up_level"] = roll_up_level
df.to_csv("output/roll_up/va.csv", index=False)


print("Plotting summary...")

plt.bar(*zip(*Counter(roll_up_level).items()))
  
plt.xlabel("Rolled_up level") 
plt.ylabel("Number of occurrences") 
plt.title("Roll-up Distribution") 

plt.savefig("output/roll_up/phs_roll_up_distribution.png")
