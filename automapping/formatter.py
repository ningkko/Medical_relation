# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import subprocess

# anchor | 
#[pos1, pos2, pos3, ....] | [pos-PMI1, pos-PMI2, pos-PMI3, ...] | [pos-co-occur1, pos-co-occur2, pos-co-occur3, ...] | 
#[neg1, neg2, neg3, ...] | [neg-PMI1, neg-PMI2, neg-PMI3, ...] | [neg-co-occur1, neg-co-occur2, neg-co-occur3, ...]

pos = "/n/data1/hsph/biostat/celehs/yih798/automapping/output/pos_train.csv"
neg = "/n/data1/hsph/biostat/celehs/yih798/automapping/output/neg_train.csv"
pos = pd.read_csv(pos).astype(str)
neg = pd.read_csv(neg).astype(str)
 
anchors = list(pos["code1"].unique())
output = []
for a in anchors:
    dp = pos[pos["code1"]==str(a)]
    dn = neg[neg["code1"]==str(a)]
    sample = "%s|[%s]|[%s]|[%s]|[%s]|[%s]|[%s]"%(a,",".join(pos["code2"]),",".join(pos["pmi"]),",".join(pos["cooc"]),
        ",".join(neg["code2"]),",".join(neg["pmi"]),",".join(neg["cooc"]))

    output.append(sample)

with open("output/train.txt","w") as fp:
    fp.write("\n\n".join(output))