import pandas as pd
import json
df = pd.read_csv("PheCode_broad_Mapping.csv")
df["extended"] = df["extended"].str.split(",")
ddf=df.explode("extended")
ddf=ddf[~ddf["extended"].isnull()]
from collections import Counter
d = dict(Counter(ddf["extended"]))
df = pd.DataFrame.from_dict(d,orient='index').reset_index()
df.columns=["code","freq"]
df=df.sort_values("freq",ascending=False)

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/cui_str_dict_updated.json", 'r') as fp:
	d = json.load(fp)
def m(x):
	if x in d:
		return d[x]
	return "missing"

df["str"] = df["code"].apply(lambda x: m(x))

df.to_csv("PheCode_broad_Mapping_freq.csv")



# print("Mean: %i, median: %i, std: %f"%(sss.mean(lengths),sss.median(lengths),sss.stdev(lengths)))
