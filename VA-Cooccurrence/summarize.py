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

folder_path = '/n/data1/hsph/biostat/celehs/SHARE/COOCCURRENCE_PMI_EMBEDDING/va/from_everett_nlp/VARV4T-04/COOCCURRENCE_MATRIX_ASYMMETRIC_NLP_ZERO/'
sub_folders = glob(folder_path+"/*/")

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

# fields for structure3
s3 = pd.DataFrame(columns=["code","count"])
s3 = s3.astype('int')

for folder in sub_folders[:1]:

    s1_subf.append(folder.split("/")[-2])
    files = [i for i in os.listdir(folder) if i.endswith('.parquet')]

    l = len(files)
    s1_numbers.append(l)
    i = 0    
    for file in files:
        i += 1
        print(i/l)

        # -------- structure 2 --------------
        s2_filename.append(file.split("/")[-1])
        s2_filesize.append(0.000001*os.path.getsize(folder+file))
        # read parquet file
        p = pd.read_parquet(folder+file)
        s2_npairs.append(len(p))
        p["ij"] = p["i"].apply(lambda x:str(x))+","+p['j'].apply(lambda x:str(x))
        s2_unique_pairs.append(len(p['ij'].unique()))
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
    s2.to_csv("s2.csv", index=False)
    s2_sub_paths.append(folder+"s2.csv")

s3.to_csv("output/s3.csv", index=False)

s1 = pd.DataFrame(columns=["foldername","#files"])
s1["foldername"] = s1_subf
s1["#files"] = s1_numbers

s1.to_csv("output/s1.csv", index=False)


s2 = pd.DataFrame(columns=["file name","size","pairs","unique_pairs","folder"])
for subf in s2_sub_paths:
    p = pd.read_csv(s2_subf)
    p["folder"] = subf.split("/")[-2]
    s2 = pd.concat(s2,p)

s2.to_csv("output/s2.csv", index=False)
