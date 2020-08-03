# 3. Task: 1) For each LOINC code in VA and PHS mapping, find their hierarchy level in the LOINC dictionary that downloaded from LOINC.org. 
# 2) For each source in VA mapping (except for "NULL"), summarize how many LOINC codes can be mapped to PHS mapping. 

import pandas as pd
import json

print("Reading data...")
phs_df = pd.read_csv("mapping_data/phs_loinc.csv")
# ------ load the hierarchy dictionary -----
with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/hierarchy_dict.json", "r") as fp:
	h_dict = json.load(fp)

l = len(phs_df)
i = 0
mapped_loinc = 0
missing_loincs = []
h_num = []
loincs = []
print("Mapping...")
for loinc_raw in phs_df["feature_id"]:
	i += 1
	print(i/l)

	loinc = loinc_raw.split(":")[1].lower()
	loincs.append(loinc)

	if loinc in h_dict:
		h_num.append(h_dict[loinc])
		mapped_loinc += 1
	else:
		missing_loincs.append(loinc)
		h_num.append("")
		
missing_loincs = list(set(missing_loincs))

print("%f LOINCs in the PHS file were mapping. %i unique LOINCs were missing. Missing terms stored in missing/loincs.txt."%(mapped_loinc/l,len(missing_loincs)))
with open("missing/loincs.txt","w") as f:
	f.write("\n".join(missing_loincs))

phs_mapping_df = pd.DataFrame(loincs)
phs_mapping_df.columns = ["LOINC"]
phs_mapping_df["h_num"] = h_num
phs_mapping_df.to_csv("output/phs.csv", index=False)
