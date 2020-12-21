# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import subprocess

pos = "/n/data1/hsph/biostat/celehs/yih798/automapping/source/sample/neg_train.csv"
biobank = "/n/data1/hsph/biostat/celehs/yih798/automapping/biobank/biobank.txt"
# new_biobank = "/n/data1/hsph/biostat/celehs/yih798/automapping/biobank/biobank2.txt"
poolfile = "/n/data1/hsph/biostat/celehs/yih798/automapping/output/neg_train.txt"
# cdr2loinc = "/n/data1/hsph/biostat/celehs/yih798/automapping/source/sample/archive/cdr2loinc.csv"

# df_cdr=pd.read_csv(cdr2loinc).astype(str)
# d = dict(zip(df_cdr["CDR"],df_cdr["LOINC"]))

df = pd.read_csv(pos).astype(str).drop_duplicates().dropna()
mapset = set(df.itertuples(index=False, name=None))

n = 977768073
i = 0
print("Start...")
with open(biobank,'r') as biobankfp:
    pbar = tqdm.tqdm(total=n)
    with open(poolfile,'w') as fpos:
        line = biobankfp.readline()
        while line:
            if line!="\n":
                note1, note2, PMI, cooc = line.replace("\n","").split(",")
                # if note1 in d:
                #     note1 = d[note1]
                # if note2 in d:
                #     note2 = d[note2]

                # new_biobankfp.write("%s,%s,%s,%s\n" % (note1, note2, PMI, cooc))

                if tuple((note1, note2)) in mapset or tuple((note2, note1)) in mapset:
                    fpos.write("%s,%s,%s,%s\n" % (note1, note2, PMI, cooc))
                    i += 1


            pbar.update(1)
            line = biobankfp.readline()
    fpos.close()
biobankfp.close()

print("%i negative sample found, %i negative not found"%(i,len(mapset)-i))