## Author: Ning
## makiasagawa@gmail.com

import pandas as pd
import numpy as np

df = pd.read_csv("output/pos_train.csv")
std = np.std(df["pmi"])
mean = np.mean(df["pmi"])
low1 = mean-1*std
low2 = mean-2*std
p30 = np.percentile(df["pmi"],30)
p50 = np.percentile(df["pmi"],50)

print("pos_sample pmi std: %f"%(std))
print("pos_sample pmi mean: %f"%(mean))
print("pos_sample lower 2.1: %f"%(low2))
print("pos_sample lower 13.6: %f"%(low1))
print("pos_sample 30 percentile: %f"%(p30))
print("pos_sample 50 percentile: %f"%(p50))

