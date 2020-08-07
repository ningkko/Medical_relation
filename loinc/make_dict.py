# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import json
import math
hierarchy_df = pd.read_csv("/n/data1/hsph/biostat/celehs/yih798/loinc/Loinc_2/MultiAxialHierarchy.csv")

def h_count(x):
	'''returns the hierarchical number of a term
		e.g. a lonic code with the path 'LP29693-6.LP343406-7.LP7819-8.LP14559-6.LP98185-9.LP14082-9' 
		should have a hierarchical number 7 since it has 6 linear parents.
	'''
	if type(x)==float:
		return 1
	return x.count(".")+2

# h_counts = hierarchy_df["PATH_TO_ROOT"].apply(lambda x: h_count(x))
# hierarchy_dict =  dict(zip(hierarchy_df["CODE"].apply(lambda x: x.lower()), h_counts))

# with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/hierarchy_dict.json", "w") as fp:
#     json.dump(hierarchy_dict, fp, sort_keys=True, indent=4)

# loinc-path mapping
# path_dict =  dict(zip(hierarchy_df["CODE"].apply(lambda x: x.lower()), hierarchy_df["PATH_TO_ROOT"]))
# with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/path_dict.json", "w") as fp:
#     json.dump(path_dict, fp, sort_keys=True, indent=4)

def _clean(x):
	if " " in x:
		x = x.replace(" ", "")
	return x.lower()

text_dict =  dict(zip(hierarchy_df["CODE_TEXT"].apply(lambda x: _clean(x)), hierarchy_df["PATH_TO_ROOT"]))
with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/text_dict.json", "w") as fp:
    json.dump(text_dict, fp, sort_keys=True, indent=4)