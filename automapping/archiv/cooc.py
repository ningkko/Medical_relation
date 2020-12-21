# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
# import subprocess
import re

pos = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/sample/pos_sample.csv"
neg = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/sample/neg_sample.csv"
pmifile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/cooc.txt"
outputfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/output/pos_pmi.txt"

df = pd.read_csv(pos).astype(str).drop_duplicates().dropna()
mapset = set(df.itertuples(index=False, name=None))

n = 977768073
with open(pmifile,'r') as fpmi:
    pbar = tqdm.tqdm(total=n)
    with open(outputfile,'a') as fout:
        line = fpmi.readline()
        while line:
            note1, note2, cooc = line.split(",")
            if tuple((note1, note2)) in mapset or tuple((note2, note1)) in mapset:
                # if int(cooc)<50:
                fout.write("%s\t%s\t%s\n" % (note1, note2, cooc))

            pbar.update(1)
            line = fpmi.readline()
    fout.close()
fpmi.close()
