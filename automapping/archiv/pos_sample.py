# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
# import subprocess
import re

pos = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/source/sample/pos_sample.csv"
biobank = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pos_biobank.csv"
outputfile = "/n/data1/hsph/biostat/celehs/yih798/yucong_project/output/pos_sample.txt"
sample = "sample.csv"

df = pd.read_csv(pos).astype(str).drop_duplicates().dropna()
df_r = df.copy()

df["pair"] = df["cui"]+"|"+df["code"]
df_r["pair"] = df["code"]+"|"+df["cui"]

biobank = pd.read_csv(biobank).astype(str)
pos_full = pd.merge(df, biobank, left_on = ["pair"], right_on = ['pair'])
pos_r_full = pd.merge(df_r, biobank, left_on = ["pair"], right_on = ['pair'])

full = pd.merge(pos_full, pos_r_full, left_on = pos_full.index)
