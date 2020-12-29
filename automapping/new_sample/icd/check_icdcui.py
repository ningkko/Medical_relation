import pandas as pd
import numpy as np
import json

## Check if icd_cui is assigend to specific string

df=pd.read_csv("ICD_PheCode_CUI_broad_Mapping.csv", encoding='Latin')


with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/str_cui_dict_updated.json", 'r') as fp:
	d = json.load(fp)

cui_string_d = {}

for k,v in d.items():
	# print(v)
	if v in cui_string_d:
		# print(cui_string_d[v])
		# print(type(cui_string_d[v]))
		cui_string_d[v] = cui_string_d[v]+"||"+k
	else:
		cui_string_d[v] = k

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping data/dictionary/cui_str_dict_updated.json",'w') as file:
	json.dump(cui_string_d,file,indent=4)

i=0
output=[]
for icd in df["icd_cui"]:
	if icd in cui_string_d:
		if "||" in cui_string_d[icd]:
			output.append("%s\t%s"%(icd,cui_string_d[icd]))
			i+=1

with open("multi_str.txt",'w') as fp:
	fp.write("\n".join(output))

print('icd_cui with more than 1 strings: '+str(i))


