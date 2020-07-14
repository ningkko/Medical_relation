import pandas as pd
import numpy as np
import ast
import json

# -------------- Read source data ---------------
print("Reading source data...")

df = pd.read_csv("output/drug_disease.csv")
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
        # if name in missing_terms_dict:
        #      cur_cuis.append(missing_terms_dict[name])

        name = name.replace(" prophylaxis", "")
        name = name.replace(" human","").replace("human", "")

        if name in str_cui_dict_updated:
             cur_cuis.append(str_cui_dict_updated[name])

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

df_rx.to_csv("output/disease_pheCode.csv")
