import pandas as pd

data_path = "/n/data1/hsph/biostat/celehs/ch263/RPDR/cooccur_20200212/data/RPDR_cooccur30_1.csv"
df = pd.read_csv(data_path, encoding = "latin", dtype="str")
elements = list(set(df["i"].to_list()+df["j"].to_list()))
elements.sort()

_dict = {k: v for v, k in enumerate(elements)}

import json
with open('dictionary.json', 'w') as fp:
    json.dump(_dict, fp, sort_keys=True, indent=4)