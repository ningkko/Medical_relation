# Author: Ning Hua 
# yhua@smith.edu

import pandas as pd
import numpy as np
import ast
import json
from datetime import datetime

with open("output/cui2phe_log.txt","a") as log:
    now = datetime.now()
    log.write(now.strftime("%Y-%m-%d %H:%M:%S\n"))
    log.write("\n")
    # -------------- Read source data ---------------
    print("Reading source data...")

    df = pd.read_csv("output/disease_pheCode.csv")
    df = df.replace(np.nan, '', regex=True)
    # drop rows with only OTC
    df_rx = df[df["RX/OTC"] != 'otc']

    all_cuis = df_rx["cui_from_disease"].to_list()

    #--------------- Mapping from CUI to Phe ------------------
    with open('../../mapping data/dictionary/cui_phe_dict.json', 'r') as fp:
        cui_phe_dict = json.load(fp)
    with open('../../mapping data/dictionary/cui_phe_dict_extended.json', 'r') as fp:
        cui_phe_dict_extended = json.load(fp)

    # ------------ mapping function --------------


    def _unique(lst):
        """returns a list with unique values"""
        return list(np.unique(np.array(lst)))

    def mapping_cui_to_phe(dictionary_name, all_cuis):

        if dictionary_name == "cui_phe_dict":
            dictionary = cui_phe_dict
        else:
            dictionary = cui_phe_dict_extended

        mapped_num = 0
        # map our data
        phecodes = []
        error = {}
        error_num = 0
        prev_cui = ""

        # keep track of what is not found
        missing_cuis = []
        missing_cui = 0
        missing_term = 0
        i = 0
        l = len(all_cuis)
        # 
        for term_cuis in all_cuis:
            cur_phecodes = []
            print(i/l)
            if term_cuis == prev_cui and prev_cui!="":
                cur_phecodes = phecodes[-1]

            else:
                if term_cuis:
                    # loop through all cuis of the term
                    term_missing_cuis = []

                    for cui in term_cuis.split("|"):
                        # print("cui: %s"%cui)
                        cur_phecode = [value for key, value in dictionary.items() if cui in key]
                        # print("phecode: %s"%str(cur_phecode))
                        if not cur_phecode:
                            term_missing_cuis.append(cui)
                            # print("missing_cui: %s"%cui)
                            missing_cui += 1

                        else: # check if for 1 cui we found multiple-class phecodes
                            # e.g. 670.1 and 670 are both class 600. But 630 and 600 are not.
                            phe_class = []
                            for phe in cur_phecode:
                                phe_class.append(int(phe))
                            # if the current cui is mapped to phecodes of more than 1 class, track it.
                            if len(set(phe_class))>1:
                                error_num += 1
                                if cui not in error:
                                    error[cui] = list(set(cur_phecode))
                                else:
                                    for phe in cur_phecode:
                                        if cui not in error[cui]:
                                            error[cui].append(phe) 

                            # else we found some right mapping to phecode. Add it to the phecode list of the current term
                            else:
                                cur_phecodes.append("|".join(list(set(map(str,cur_phecode)))))

                    if term_missing_cuis:
                        missing_cuis.append("|".join(term_missing_cuis))

            phecodes.append("|".join(_unique(cur_phecodes)))
           
            if term_cuis != prev_cui:
                if len(cur_phecodes) > 0:
                    mapped_num += 1
                else:
                    missing_term += 1

            prev_cui = term_cuis
            i += 1

        mapping_rate_cui2phe = mapped_num/len(_unique(all_cuis))

        
        log.write("\n\nUsing map %s...\nMapping rate from CUI strings to PheCode: %f.\n%i unique cuis are missing. %i unique disease terms are missing. \n%i errors detected."%(dictionary_name, mapping_rate_cui2phe, missing_cui, missing_term, error_num))

        return phecodes, missing_cuis,error


    # #--------------- Map from CUI to Phe using cui_phe_dict ------------------

    print("Mapping using cui_phe_dict built from icd_cui+phecode_extended_cui : phecode...")
    phecodes, missing_cuis, error = mapping_cui_to_phe("cui_phe_dict", all_cuis)

    with open("missing/missing_cuis_inCUI2Phe.txt", 'w') as file:
        file.write("\n".join(set(missing_cuis)))

    with open("output/error_cui2phe.json", 'w') as fp:
        json.dump(error, fp, indent=4)

    df_rx["phecode"] = phecodes

    #--------------- Map from CUI to Phe using cui_phe_dict_extended ------------------

    print("Mapping using cui_phe_dict_extended built from icd_extended_cui+phecode_extended_cui : phecode...")
    phecodes_extended, missing_cuis_extended,error_extended = mapping_cui_to_phe("cui_phe_dict_extended", all_cuis)

    with open("missing/missing_cuis_inCUI2Phe_extended.txt", 'w') as file:
        file.write("\n".join(missing_cuis_extended))

    with open("output/error_cui2phe_extended.json", 'w') as fp:
        json.dump(error_extended, fp, indent=4)

    df_rx["phecode_extended"] = phecodes_extended

    df_rx.to_csv("output/disease_pheCode.csv", index=False)

    log.write("\n---------------------- End ----------------------\n")
