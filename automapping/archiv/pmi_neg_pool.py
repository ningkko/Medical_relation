# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
# import subprocess
import re

pmi_pool="biobank/pmi_neg_pool.csv"
pos = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/sample/pos_sample.csv"
pmifile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi.txt"
outputfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi_neg_pool0.txt"

# sample = "sample.csv"

# df = pd.read_csv(pos).astype(str).drop_duplicates().dropna()
# anchor = set(df["cui"])
# mapset = set(df.itertuples(index=False, name=None))
# process = subprocess.Popen(b.split(), stdout=subprocess.PIPE)
# n = int(re.findall(r'\d+',str(process.communicate()[0]))[0])
n = 1458776088
with open(pmifile,'r') as fpmi:
    pbar = tqdm.tqdm(total=n)
    with open(outputfile,'a') as fout:
        line = fpmi.readline()
        while line:
            note1, note2, pmi = line.replace('\t',',').split(",")
            # if note1 or note2 in anchor:
            # if tuple((note1, note2)) in mapset or tuple((note2, note1)) in mapset:
            if float(pmi)<0:
                fout.write("%s\t%s\t%s\n" % (note1, note2, pmi))

            pbar.update(1)
            line = fpmi.readline()

    fout.close()
fpmi.close()