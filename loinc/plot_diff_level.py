import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

df = pd.read_csv("shared_root_summary.csv")["diff level"].to_list()

print(Counter(df))
plt.bar(*zip(*Counter(df).items()))
  
plt.xlabel("Number of shared nodes in paths") 
plt.ylabel("Number of occurrences of #nodes") 
plt.title("Roll-up Distribution") 

plt.savefig("roll_up_distribution.png")