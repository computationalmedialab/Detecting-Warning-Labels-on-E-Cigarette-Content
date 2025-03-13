import pandas as pd

# Load the CSV files
con1 = pd.read_csv("condition1.csv")
con2 = pd.read_csv("condition2.csv")

# Extract the 'text' columns
col1 = con1['text']
col2 = con2['text']

# Find the common records
common_records = set(col1).intersection(set(col2))

# Print the count and common values
print(f"Number of common records: {len(common_records)}")
