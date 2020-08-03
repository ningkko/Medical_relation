# LOINC - hierarchy level mapping
hierarchy levels are counted by counting previous "generations" of a LOINC code.\
e.g. a lonic code with the path 'LP29693-6.LP343406-7.LP7819-8.LP14559-6.LP98185-9.LP14082-9' 
should have a hierarchical number 7 since it has 6 linear parents.

## make_dict.py
makes the {LOINC_code : hierarchy_level} dictionary from Loinc_2/MultiAxialHierarchy.csv

## make_data.py
cleans raw data.

## map_phs_hnum.py
maps LOINC codes in feature_book (PHS) with LOINC hierarchy levels.

## raw_data/ 
has all data from Skyler's folder except for the hierarchy dictionary.

## Loinc_2/
has information about the hierarchy csv and the csv file itself.

## mapping_data/
has all cleaned data from raw_data/ and the dictionary built from the hierarchy csv.

## missing/
contains missing LOINCs during matching processes.

## output/
stores output files of the LOINC-hierarchy level mapping.

