import pandas as pd
import numpy as np
import json

# ================= dictionaries from umls ===============
with open('../mapping data/dictionary/umls_str_cui_dict.json', 'r') as fp:
    str_cui_dic = json.load(fp)

#================ Read source data ======================

df = pd.read_csv("output/drug_disease.csv").replace(np.nan, '', regex=True)
df_rx = df[df["RX/OTC"] != 'otc']

def _unique(lst):
    '''returns a list with unique values'''
    return list(np.unique(np.array(lst)))

def _clean_generic_name(x):
    x = x.replace(" )","")
    x = x.replace("|and ","/")
    return x

def _map(names, _dict, unique_names):
	mapped_num = 0
	# map our data
	mapped_list = []
	prev_name_set = []

	# keep track of what is not found
	missing_names = []
	i = 0
	for name in names:

	    cur_cuis = []
	    # if name in generic_missing_terms_dict:
	    #     cur_cuis.append(generic_missing_terms_dict[name])
 
	    name = name.replace(" prophylaxis", "")
	    name = name.replace(" human","").replace("human", "")
	    name = name.replace(" )","")


	    if name in _dict:
	         cur_cuis.append(_dict[name])

	    cur_cuis = _unique(cur_cuis)

	    if name not in prev_name_set:
	        if len(cur_cuis) > 0:
	            mapped_num += 1
	        else:
	            missing_names.append(name)
	        prev_name_set.append(name)

	    mapped_list.append("|".join(cur_cuis))
	    i += 1

	return mapped_list, mapped_num,missing_names


generic_names = df_rx["generic name"].apply(lambda x: _clean_generic_name(x))
generic_names_unique = _unique(generic_names)
generic_names_unique.remove("")

cui_codes_gen, mapped_generic_num, missing_generic_names = _map(generic_names, str_cui_dic, unique_names=generic_names_unique)

missing_terms_df = pd.DataFrame(missing_generic_names)
missing_terms_df.columns = ["CUIs"]
missing_terms_df.to_csv("missing/missing generic names.csv", index=False)


mapping_rate_generic = mapped_generic_num/len(generic_names_unique)
print("Mapping rate(generic names to CUI): %f.\nMissing %i generic names." % (mapping_rate_generic, len(missing_generic_names)))


# df_rx["cui_from_generic"] = cui_codes_list_gen
#df_rx.to_csv("output/PheCode_rxNorm.csv")

# missing_generic_names_df = pd.DataFrame(missing_generic_names)
# missing_generic_names_df.columns = ["generic names"]
# missing_generic_names_df["CUIs"] = ""*len(missing_generic_names)

# missing_generic_names_df.to_csv("missing mappings/missing CUIs from generic name.csv", index=False)


brand_names = df_rx["brand names"]
brand_names_unique = _unique(brand_names)
brand_names_unique.remove("")

cui_codes_brand, mapped_brand_num, missing_brand_names = _map(brand_names, str_cui_dic, unique_names=brand_names_unique)


missing_terms_df = pd.DataFrame(missing_brand_names)
missing_terms_df.columns = ["CUIs"]
missing_terms_df.to_csv("missing/missing brand names.csv", index=False)


mapping_rate_brand = mapped_brand_num/len(generic_names_unique)
print("Mapping rate(brand names to CUI): %f.\nMissing %i brand names." % (mapping_rate_brand, len(missing_brand_names)))

def combine_CUIs(li_1, li_2):
	combined_cui = []
	for i in range(len(li_1)):
	    cur_cui = ""
	    if li_1[i]:
	        cur_cui += li_1[i]
	        if li_2[i]:
	            cur_cui = cur_cui + "|" + li_2[i]
	    elif not li_1[i]:
	        if li_2[i]:
	            cur_cui = li_2[i]

	    combined_cui.append(cur_cui)
	    i += 1
	return combined_cui

combined_cui = combine_CUIs(cui_codes_gen, cui_codes_brand)
non_empty_cuis_df = pd.DataFrame(combined_cui).replace("", np.nan, regex=True).dropna()
mapping_rate_str_cui = len(non_empty_cuis_df) / len(combined_cui)
print("After combining CUIs derived from generic names and brand names, %f of the drug names have at least one CUI." % mapping_rate_str_cui)

# =================== string - CUI - RXNorms =======================

print("Reading string - RXNorm dictionary...\n...")
with open('output/cui_str_dict_updated.json', 'r') as cui_str_fp:
    cui_rxnorm_dic = json.load(cui_str_fp)

# map combined cui to rxnorms using the cui_rxnorm_dic we just created

cui_rxnorms = []
missing_cuis = []
mapped_num_cui_rxnorm = 0

for row in combined_cui:
    cur_rxnorm = []
    for c in row.split("|"):
        if c in cui_rxnorm_dic:
            cur_rxnorm.append(cui_rxnorm_dic[c])

        else:
            # only track which cui is missing from the dict we are using
            missing_cuis.append(c)

        cur_rxnorm = _unique(cur_rxnorm)

    if cur_rxnorm:
        mapped_num_cui_rxnorm += 1

    cui_rxnorms.append("|".join(cur_rxnorm))

    missing_cuis = _unique(missing_cuis)

cui_rxnorm_mapping_rate = mapped_num_cui_rxnorm / len(combined_cui)
print("%f of the drug names are mapped." % cui_rxnorm_mapping_rate)


