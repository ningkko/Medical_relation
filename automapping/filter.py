import pandas as pd
import numpy as np

AMPLIFIER = 200
NEG_THRESHOLD = AMPLIFIER/2	
PMI =  2.015600


print("1 anchor has %i max neg_sample"%AMPLIFIER)
print("PMI upper bound: %f"%PMI)

COOC = 30

df = pd.read_csv("output/full/neg_train.txt",sep='\n')
df = df["code1,code2,pmi,cooc"].str.split(",",expand=True)
df.columns = ["code1","code2","pmi","cooc"]
df["pmi"] = df["pmi"].astype(float)
df["cooc"] = df["cooc"].astype(int)
df = df[(df["pmi"]<PMI)]
# print(df)
# get pos_sample anchors
# pos = pd.read_csv("output/full/pos_train.txt",sep="\n")
# pos = pos["code1,code2,pmi,cooc"].str.split(",",expand=True)
# pos.columns = ["code1","code2","pmi","cooc"]
# pos.to_csv("output/pos_train.csv", index=False)
pos=pd.read_csv("output/pos_train.csv")
anchors = pos["code1"].to_list()
print("# unique anchors: %i"%len(anchors))
output=pd.DataFrame({"code1" : [],
					"code2" : [],
					"pmi" : [],
					"cooc" : []})
# print(anchors[:10])
not_enough = []

for a in anchors:
	d = df[df["code1"]==str(a)]
	# print(d)
	if len(d) == 0:
		not_enough.append("%s, %i"%(a,0))
		continue 
	if len(d) >= AMPLIFIER:
		d = d.sample(AMPLIFIER)
	elif len(d) < NEG_THRESHOLD:
		not_enough.append("%s, %i"%(a,len(d)))
	output = output.append(d)

output.to_csv("output/neg_train.csv",index=False)
with open("missing.txt","w") as fp:
	fp.write("\n".join(not_enough))
fp.close()

print("# neg_sample < %i: %i"%(NEG_THRESHOLD,len(not_enough)))
print("# neg_sample: %i"%len(output))

# def m(x):
# 	if x in not_enough:
# 		return np.nan
# 	else:
# 		return x

# pos["code1"]=pos["code1"].apply(lambda x: m(x))
# pos=pos.dropna()
# pos.to_csv("pos_sample2.csv",index=False)
# print(len(pos))

