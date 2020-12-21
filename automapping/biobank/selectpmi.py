# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import re

df = pd.read_csv("pmi_neg_pool.txt",sep='\n')
df.columns=["pmi"]
df=df["pmi"].str.split("\t",expand=True)
df.columns=["c1","c2","pmi"]
df["pmi"] = df["pmi"].astype(float)

df = df[df["pmi"]<0]
df.to_csv("/n/data1/hsph/biostat/celehs/yih798/yucong_project/biobank/pmi_neg_pool0.csv",index=False)