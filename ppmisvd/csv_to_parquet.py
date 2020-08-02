import pandas as pd
df = pd.read_csv('encrypted_input.csv')
df.to_parquet('encrypted_input.parquet')