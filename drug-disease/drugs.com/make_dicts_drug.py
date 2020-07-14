import pandas as pd
import numpy as np
import json
import csv

# # =================== Broad dictionary =======================
# print("Building str-Cui Dictionary... Notice that you might need 10G memory in interactive mode.")
# broad_dict_raw = pd.read_csv("../mapping data/broad_new_full_dict.txt", sep="|", header=None)
# # names columns for extracting
# broad_dict_raw.columns = ["name","1",'2',"cui",'4','5']

# broad_dict_raw2019 = pd.read_csv("../mapping data/broad_new_full_dict2019.txt", sep="|", header=None)
# # names columns for extracting
# broad_dict_raw2019.columns = ["name","cui",'2','3']

# def create_str_CUI_dictionary(broad_dict_raw):
#     # create string - CUI pairs
#     generic_name = broad_dict_raw["name"].apply(lambda x: x.lower().replace(",","").replace(" / ", "/") if type(x) == str else "")
    
#     cui = broad_dict_raw["cui"].apply(lambda x: x.replace(";", "|"))
#     str_cui_dic = dict(zip(generic_name,cui))
#     return str_cui_dic
    

# str_cui_dic2012 = create_str_CUI_dictionary(broad_dict_raw)
# str_cui_dic2019 = create_str_CUI_dictionary(broad_dict_raw2019)


# def merge(dict1, dict2): 
#     res = {**dict1, **dict2} 
#     return res

# str_cui_dic = merge(str_cui_dic2012, str_cui_dic2019) 

# with open('../mapping data/dictionary/str_cui_dict_updated.json', 'w') as fp:
#     json.dump(str_cui_dic, fp, indent=4)

# print("Building done.")
# =================== string - CUI - RXNorm strings =======================

print("Constructing string - CUI dictionary...\n...")
rx_norms_df = pd.read_csv("../mapping data/RXNORM-ingredient-base.csv")
rx_norm_strings = rx_norms_df["ingredient_str"].apply(lambda x: x.replace(" / ", "/")).to_list()

rx_norms_new_df = pd.read_csv("../mapping data/rxnorm_string.csv")
rx_norm_strings_new = rx_norms_new_df["STR"].apply(lambda x: x.lower().replace(" / ", "/")).to_list()
rx_norm_strings = list(set(rx_norm_strings + rx_norm_strings_new))
print("From the RXNORM-ingredient-base.csv file, %i RX Norms are found." % len(rx_norm_strings))


def _unique(lst):
    '''returns a list with unique values'''
    return list(np.unique(np.array(lst)))

def _clean_generic_name(x):

    x = x.replace(" )","")
    x = x.replace("|and ","/")

    return x

# # =================== Mapping =======================

# mapped_cuis = []
# missed_strings = []
# for string in rx_norm_strings:
#     if string in str_cui_dic:
#         mapped_cuis.append(str_cui_dic[string])
#     else:
#         missed_strings.append(string)

# # Mappinge rate:
# cui_rxnorm_mapping_rate = len(mapped_cuis)/len(rx_norm_strings)
# print("Mapping rate(CUI - RXNorms): %f.\nMissing %i strings." % (cui_rxnorm_mapping_rate, len(missed_strings)))

# cui_rxnorm_dic = dict(zip(mapped_cuis, rx_norm_strings))

# with open('../mapping data/dictionary/str_cui_dict_updated.json', 'w') as fp:
#     json.dump(cui_rxnorm_dic, fp, indent=4)

# # with open('output/missing_strings_in_broad.txt', 'w') as file:
# #     file.write("\n".join(missed_strings))


# =================== RXNorm strings - rxnorms =======================
rx_norms = rx_norms_df["ingredient"].to_list()
rx_norms_new = rx_norms_new_df["RXCUI"].to_list()
rx_norms += rx_norms_new
str_rxnorm_dic = dict(zip(rx_norm_strings, rx_norms))
with open('../mapping data/dictionary/str_rxnorm_dic.json', 'w') as fp:
    json.dump(str_rxnorm_dic, fp, indent=4)