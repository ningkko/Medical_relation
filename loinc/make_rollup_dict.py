# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import json

va_loinc = pd.read_csv("mapping_data/core_team.csv")["LOINC"].apply(lambda x : x.strip()).unique()
phs_loinc = pd.read_csv("mapping_data/phs_loinc.csv")["feature_id"].apply(lambda x: x.split(":")[1].strip()).unique()
print("Number of pairs: %i"%(len(va_loinc)*len(phs_loinc)))
with open("mapping_data/path_dict.json","r") as fp:
	path_dict = json.load(fp)

def find(x):
	if x in path_dict:
		return path_dict[x]
	return ""

def roll_up(x,y):
	"""
	returns the common root.
	the function assumes that x has fewer nodes than y
	"""
	x_path = find(x)
	y_path = find(y)

	if x_path and y_path:

		if x_path in y_path: 
			return x, abs(y_path.count(".") - x_path.count("."))
		if y_path in x_path: 
			return y, abs(y_path.count(".") - x_path.count("."))

	return "", 0


def find_highest_h(a, b):
	""" if the loinc is rolled up to b_new, 
		f hierarchy level of b_new is higher than that of the previously documented rolled_up a (b_old)
			if yes
				update b_old to b_new
				return b_new
			else:
				return b_old

		else add {a: b_new} to the dict
			return b_new
	"""
	if a in roll_up_dict:
		if path_dict[roll_up_dict[a]].count(".") > b.count("."):
			roll_up_dict[a] = b
		else: 
			return roll_up_dict[a]
	else:
		roll_up_dict[a] = b
	return b 


rolled_up = []
roll_up_levels = []
# original loincs expanded
roll_up_dict = {}
same_parent = []
print("Mapping...")
i = 0
l = len(va_loinc)
for va in va_loinc:
	i+=1
	# print(i/l)
	for phs in phs_loinc:
		loinc_rolled_up = ""
		roll_up_level = 0
		va_path = find(va)
		phs_path = find(phs)
		if va!= phs and va_path and phs_path:

			if va_path!=phs_path:
				if va_path in phs_path:
					loinc_rolled_up = find_highest_h(phs, va)
				elif phs_path in va_path:
					loinc_rolled_up = find_highest_h(va, phs)

			else:
				same_parent.append([va, phs])

		if loinc_rolled_up:
			roll_up_level = max(va.count("."), phs.count(".")) - loinc_rolled_up.count(".")

		rolled_up.append(loinc_rolled_up)
		roll_up_levels.append(roll_up_level)

same_parent = set(tuple(sorted(x)) for x in same_parent)
print("%i pairs have same parents."%(len(same_parent))) 


with open("mapping_data/roll_up_dict.json","w") as fp:
	json.dump(roll_up_dict, fp, sort_keys=True, indent=4)
