# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import subprocess
import json

# codebook = "/n/data1/hsph/biostat/celehs/SHARE/COOCCURRENCE_PMI_EMBEDDING/rpdr/rpdr_code_codebook_victor_2019.tsv"
# df = pd.read_csv(codebook).astype(str).drop_duplicates().dropna()
# df = df[["feature_id","raw_ct"]]
# codebbok_mapset = set(df.itertuples(index=False, name=None))



pmifile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi.txt"
coocfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/cooc.txt"
outputfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/biobank.txt"
not_found_file =  "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/not_found.txt"
# loop through cooc and pmi, match them 
# if not matched, store in a not_found file, use cooc dictionary to loop through it.
not_dict = dict()

print("Matching...")
n = 977768073
i=0
with open(coocfile,'r') as fcooc:
    pbar = tqdm.tqdm(total=n)
    with open(pmifile,'r') as fpmi:
        with open(outputfile,'a') as fout:
            with open(not_found_file, "a") as f_not:
                pmi_line = fpmi.readline()
                cooc_line = fcooc.readline()
                while pmi_line:
                    pnote1, pnote2, PMI = pmi_line.replace("\n","").split("\t")
                    cnote1, cnote2, cooc = cooc_line.split(",")
                    if (pnote1 == cnote1 and pnote2==cnote2) or (pnote1==cnote2 and pnote2==cnote1):
                        fout.write("%s,%s,%s,%s\n" % (pnote1, pnote2, PMI, cooc))
                        i+=1
                    else:
                        f_not.write("%s,%s,%s\n" % (pnote1, pnote2, PMI))
                        key=pnote1+","+pnote2
                        not_dict[key] = PMI

                    pbar.update(1)
                    pmi_line = fpmi.readline()
                    cooc_line = fcooc.readline()
                
                # store the dict
                with open("not_found_pmi.json","w") as fp:
                    json.dump(not_dict,fp,indent=4)

            f_not.close()
        fout.close()
    fpmi.close()
fcooc.close()

print("%i out of %i (%f) found."%(i,n,i/n))
# loop through cooc, find mpi in pmi dict
print("Matching unfounded...")

