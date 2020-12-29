import pandas as pd
import numpy as np
import json

## Check if icd_cui is assigend to specific string

addr = "/n/data1/hsph/biostat/celehs/yih798/code-cui/rxnorm/"
a = "rxnorm_not_sure.csv"
b = "rxnorm_base.csv"
c = "rxnorm_ingredient.csv"
not_sure=pd.read_csv(addr+a, encoding='Latin')
base=pd.read_csv(addr+b, encoding='Latin')
ing=pd.read_csv(addr+c, encoding='Latin')

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/mapping/dictionary/cui_str_dict_updated.json", 'r') as fp:
	cui_string_d = json.load(fp)

i=0
output=[]
for cui in ing["cui"]:
	if cui in cui_string_d:
		if "||" in cui_string_d[cui]:
			output.append("%s\t%s"%(cui,cui_string_d[cui]))
			i+=1


with open("multi_str.txt",'w') as fp:
	fp.write("\n".join(output))

print('loinc_cui with more than 1 strings: %i out of %i'%(i,len(ing)))

