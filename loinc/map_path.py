# Author: Ning Hua
# yhua@smith.edu

import pandas as pd
import json

print("Reading data...")
phs_df = pd.read_csv("mapping_data/phs_loinc.csv")
va_df = pd.read_csv("mapping_data/core_team.csv")

# ------ load the hierarchy dictionary -----
with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/path_dict.json", "r") as fp:
	h_dict = json.load(fp)
with open("/n/data1/hsph/biostat/celehs/yih798/loinc/mapping_data/text_dict.json", "r") as fp:
	text_dict = json.load(fp)
# -------------------- phs --------------------

l = len(phs_df)
i = 0
mapped_loinc = 0
missing_loincs = []
paths = []
loincs = []
print("Mapping...")
for loinc_raw in phs_df["feature_id"]:
	i += 1
	# print(i/l)

	loinc = loinc_raw.split(":")[1].lower()
	loincs.append(loinc)

	if loinc in h_dict:
		paths.append(h_dict[loinc])
		mapped_loinc += 1
	else:
		missing_loincs.append(loinc)
		paths.append("")
		
missing_loincs = list(set(missing_loincs))

print("%f LOINCs in the PHS file were mapped. %i unique LOINCs were missing. Missing terms stored in missing/phs.txt."%(mapped_loinc/l,len(missing_loincs)))
with open("missing/loincs.txt","w") as f:
	f.write("\n".join(missing_loincs))

phs_mapping_df = pd.DataFrame(loincs)
phs_mapping_df.columns = ["LOINC"]
phs_mapping_df["path"] = paths
phs_mapping_df = phs_mapping_df.drop_duplicates().sort_values(by=['LOINC']).dropna()
phs_mapping_df.to_csv("output/phs_path.csv", index=False)


# -------------------- va --------------------
def _clean(x):
	if " " in x:
		x = x.replace(" ", "")

	return x.lower()

l = len(va_df)
i = 0
mapped_loinc = 0
missing_loincs = []
paths = []
print("Mapping...")
for ShortName in va_df["ShortName"]:
	i += 1
	# print(i/l)

	ShortName = _clean(ShortName)

	if ShortName in text_dict:
		paths.append(text_dict[ShortName])
		mapped_loinc += 1
	else:
		missing_loincs.append(ShortName)
		paths.append("")
		
missing_loincs = list(set(missing_loincs))

print("%f ShortNames in the VA file were mapped. %i unique ShortNames were missing. Missing terms stored in missing/VA.txt."%(mapped_loinc/l,len(missing_loincs)))
with open("missing/shortname.txt","w") as f:
	f.write("\n".join(missing_loincs))

va_mapping_df = pd.DataFrame(va_df["LOINC"])
va_mapping_df.columns = ["LOINC"]
va_mapping_df["path"] = paths
va_mapping_df = va_mapping_df.drop_duplicates().sort_values(by=['LOINC']).dropna()
va_mapping_df.to_csv("output/va_path.csv", index=False)
