import pandas as pd
import json

print("Reading...")
data_path = "/n/data1/hsph/biostat/celehs/ch263/RPDR/cooccur_20200212/data/RPDR_cooccur30_1.csv"
df = pd.read_csv(data_path, encoding = "latin", dtype="str")

print("Reading done.")

print("Loading dictionary...")
with open('dictionary.json', 'r') as fp:
    _dict = json.load(fp)

print("Encrypting i...")
df["i"] = df["i"].apply(lambda x: _dict[x])
print("Encrypting j...")
df["j"] = df["j"].apply(lambda x: _dict[x])

print("Writing to csv...")
df.to_csv("encrypted_input.csv", index=False)