import pandas as pd
import numpy as np
import ast
import json

# -------------- Read source data ---------------
print("Reading source data...")

df = pd.read_csv("output/PheCode_rxNorm.csv")
df = df.replace(np.nan, '', regex=True)
# drop rows with only OTC
df_rx = df[df["RX/OTC"] != 'otc']


# ------------- Flatten disease names -----------------
other_names = df_rx["other names"].to_list()
all_names = []

name = df_rx["disease name"].to_list()
for i in range((len(name))):
    new_line = []
    # add the disease name
    new_line.append(name[i])
    
    # see of the disease have other names
    if other_names[i]:
        other_names_list = other_names[i].split("|")

        new_line += other_names_list

    all_names.append(new_line)

def _unique(lst):
"""returns a list with unique values"""
return list(np.unique(np.array(lst)))

unique_all_names = _unique(all_names)

print("Number of all diseases: %i" %len(all_names))

print("Mapping from strings to CUI using broad_dictionary...")
#--------------- Mapping from CUI to Phe ------------------
with open('../mapping data/dictionary/str_cui_dict_updated.json', 'r') as fp:
    str_cui_dict_updated = json.load(fp)

# ------------ mapping --------------
mapped_num = 0
# map our data
cui_codes = []
multiple_cui_instances = []

prev_disease = []

# keep track of what is not found
missing_disease = []
i = 0
for disease in all_names:

    cur_cuis = []
    for name in disease:
        if name in missing_terms_dict:
             cur_cuis.append(missing_terms_dict[name])

        name = name.replace(" prophylaxis", "")
        name = name.replace(" human","").replace("human", "")

        if name in str_cui_dic:
             cur_cuis.append(str_cui_dic[name])

    cur_cuis = _unique(cur_cuis)

    if disease != prev_disease:
        if len(cur_cuis) > 0:
            mapped_num += 1
        else:
            missing_disease.append("|".join(disease))

    cui_codes.append("|".join(cur_cuis))
    i += 1
    prev_disease = disease

mapping_rate_str2cui = mapped_num/len(_unique(all_names))
print("Mapping rate from disease strings to CUI: %f. %i unique strings are missing."%(mapping_rate_str2cui, len(set(missing_disease))))
with open("missing_disease_str.txt", 'w') as file:
    file.write("\n".join(missing_disease))
df_rx["cui_from_disease"] = cui_codes


#--------------- Map from CUI to Phe usicd ICD CUIS------------------
1. check if matches multiple columns
2. chekc if icd & phecui not matching

print("Mapping from CUI to PheCodes using icdcui_phecode_dict...")
with open('../mapping data/dictionary/phecui_phecode_dict.json', 'r') as fp:
    phecui_phecode_dict = json.load(fp)

# unstack the dataframe
def _unstack(frame):
    data = []

    for i in frame.itertuples():
        lst = i[0]
        for col2 in lst:
            data.append([i[1], col2])

    frame_unstacked = pd.DataFrame(data=data, columns=frame.columns)
    return frame_unstacked


phe_cui_df_unstacked = pd.DataFrame(data=data, columns=phe_cui_df.columns)



# Map
mapped_num_cui2phe = 0
# map our data
phe_codes = []

missing_cui_phe = []
prev_cui = ""
i = 0
for cui_codes in cui_codes:
    cur_phes = []
    codes = _unique(cui_codes.split("|"))

    for cui in codes:
        if cui in cui_phe_dict:
            cur_phes.append(cui_phe_dict[cui])
    cur_phes = _unique(cur_phes)

    if cui_codes!= prev_cui:
        if len(cur_phes) > 0:
            mapped_num_cui2phe += 1
        else:
            missing_cui_phe.append(cui_codes)

    phe_codes.append("|".join(cur_phes))
    i += 1
    prev_cui = cui_codes

df_rx["phe_from_CUI"] = phe_codes
df_rx.to_csv("output/PheCode_rxNorm.csv")



with open('../mapping data/dictionary/phecui_phecode_dict.json', 'r') as fp:
    icdcui_phecode_dict.json

# ================= summary ===============
mapping_percentage_cui2phe = mapped_num_cui2phe/len(_unique(cui_codes_list))
print("Mapping rate from CUI to PheCodes: %f. %i unique CUIs are missing."%(mapping_percentage_cui2phe, len(set(missed_cui_phe))))
with open("missing_disease_cuis.txt", 'w') as file:
    file.write("\n".join(missing_cui_phe))

