# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import re

df = pd.read_csv("cooc_neg_pool.txt",sep='\n')
df.columns=["cooc"]
df=df["cooc"].str.split("\t",expand=True)
df.columns=["c1","c2","cooc"]
df["cooc"] = df["cooc"].astype(int)

df = df[df["cooc"]<30]
df.to_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/cooc_neg_pool30.csv",index=False)