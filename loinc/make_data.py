# author: Ning Hua
# yhua@smith.edu

import pandas as pd

# 1. VA mapping: CoreTeam_bestLabMap_11182019.xlsx. You will need columns: ShortName, Source and LOINC; rows where ShortName!=NULL. 

va_df = pd.read_excel("raw_data/CoreTeam_bestLabMap_11182019.xlsx")

va_df = va_df.dropna(subset=["ShortName", "Source", "LOINC"])

output_df = va_df[["ShortName", "Source", "LOINC"]].drop_duplicates().dropna()
output_df = output_df[output_df["Source"].str.contains("yoinc")]
print("%i unique yoinc entries in VA were found."%len(output_df["ShortName"]))
# 88 unique short names found

output_df.to_csv("mapping_data/core_team.csv", index=False)

# 2. PHS mapping: feature_codebook.tsv. You will need columns: feature_id; rows where feature_id starting with "LOINC". 
phs_df = pd.read_csv("raw_data/feature_codebook.tsv",sep="\t")

# keep rows with the substring "LOINC" in the "feature_id" column
phs_df = phs_df[phs_df["feature_id"].str.contains("LOINC")].drop_duplicates()
print("%i rows in PHS contains loinc code"%len(phs_df))
# 41298 rows

phs_df.to_csv("mapping_data/phs_loinc.csv", index=False)



