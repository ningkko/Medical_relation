# Author: Ning Hua
# makiasagawa@gmail.com

import pandas as pd
import json
import numpy as np
import subprocess
import os
import sys
import shutil
from glob import glob

script_path = '/n/data1/hsph/biostat/celehs/SHARE/COOCCURRENCE_PMI_EMBEDDING/va/from_everett_nlp/VARV4T-04/'
folder_path = '/n/data1/hsph/biostat/celehs/SHARE/COOCCURRENCE_PMI_EMBEDDING/va/from_everett_nlp/VARV4T-04/COOCCURRENCE_MATRIX_ASYMMETRIC_NLP_ZERO/'
sub_folders = glob(folder_path+"/*/")
print(sub_folders)
# Csv Structure1: Subfolder, #files 
# Csv Structure2: Subfolder, filename, file_size, #pairs, #unique_pairs, code1, code2
# Csv Structure3 (overall): unique code, frequency 

# fields for structure1
s1_subf = []
s1_numbers = []

# fields for struture2
s2_filename = []
s2_filesize = []
s2_npairs = []
s2_unique_pairs = []

s2_sub_paths = []


s1 = pd.read_csv(script_path + "output/s1.csv")
s3 = pd.read_csv(script_path + "output/s3.csv")
s3 = s3.astype('int')


for folder in sub_folders:
    # print(folder)
    s1_subf.append(folder.split("/")[-2])
    files = [i for i in os.listdir(folder) if i.endswith('.parquet')]
    s1_numbers.append(len(files))

    for file in files:
        print(file)
        # -------- structure 2 --------------
        s2_filename.append(file.split("/")[-1])
        s2_filesize.append(format(0.000001*os.path.getsize(folder+file),'.2f'))
        # read parquet file
        try:
            p = pd.read_parquet(folder+file)
        except IOError:
            continue

        s2_npairs.append(len(p))
        # p["ij"] = p["i"].apply(lambda x:str(x))+","+p['j'].apply(lambda x:str(x))
        s2_unique_pairs.append(len(p[["i","j"]].drop_duplicates()))
        # print("s2 built...")
        # -------- structure 3 --------------

        pi = p[["i","count"]]
        pi.columns = ["code",'count']
        pj = p[["j","count"]]
        pj.columns = ["code",'count']

        pi_j = pd.concat([pi,pj])
        s3 = pd.concat([s3,pi_j]).groupby("code")["count"].sum().reset_index()
        
        # j=0
        # lp=len(p)
        # for line in p.iterrows():
        #     j+=1
        #     print(j/lp)
        #     if line[1]["i"] in d:
        #         d[line[1]["i"]] += line[1]["count"]
        #     else:
        #         d[line[1]["i"]] = line[1]["count"]

        #     if line[1]["j"] in d:
        #         d[line[1]["j"]] += line[1]["count"]
        #     else:
        #         d[line[1]["j"]] = line[1]["count"]
        # print("s3 built...")
    s2 = {
            "file name": s2_filename,
            "size": s2_filesize,
            "pairs": s2_npairs,
            "unique_pairs": s2_unique_pairs
            }

    s2 = pd.DataFrame(s2)
    s2["p==up"] = s2["pairs"]==s2["unique_pairs"]
    s2.to_csv(script_path+"s2/"+folder.split("/")[-2]+".csv", index=False)
    s2_sub_paths.append(script_path+"s2/"+folder.split("/")[-2]+".csv")


    s3.to_csv("output/s3.csv", index=False)

    s1_new = pd.DataFrame(columns=["foldername","#files"])
    s1_new["foldername"] = s1_subf
    s1_new["#files"] = s1_numbers
    s1 = pd.concat([s1,s1_new])
    s1.to_csv(script_path+"output/s1.csv", index=False)


s2 = pd.DataFrame(columns=["file name","size","pairs","unique_pairs","folder"])
for subf in s2_sub_paths:
    p = pd.read_csv(subf)
    p["folder"] = subf.split("/")[-2]
    s2 = pd.concat(s2,p)

s2.to_csv(script_path+"output/s2.csv", index=False)
