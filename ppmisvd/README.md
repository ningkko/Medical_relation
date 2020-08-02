## Purpose
Given a input file in csv, encrypt it, and output it in parquet.
## make_dict.py
Creates an encoding based on indiced of the sorted unique elements appeared in the original input.
## encrypt.py
Encrypt the original input file using the dictionary created in last step
## csv_to_parquet.py
Convert csv files to parquet files.