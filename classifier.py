import pandas as pd
import csv

def classify(statement):
    # Convert statement to lowercase for case-insensitive matching
    text = statement.lower() if isinstance(statement, str) else ""
    
    # Check the conditions
    if (("warning" in text and 
         ("this product contains nicotine" in text or 
          "this product contains tobacco" in text or 
          "nicotine as an addictive substance" in text or  
          "for adult(21+)" in text or 
          "nicotine is an addictive chemical" in text)) or 
         ('nicotine' in text and 'addictive' in text)):
        return True
    else:
        return False

# Read only the first column from the CSV.
df = pd.read_csv(
    'filtered_english_youtube.csv',
    engine='python',
    quoting=csv.QUOTE_NONE,
    escapechar='\\',
    header=None,
    usecols=[0],          # Only load the first column
    names=['statement']   # Name the column appropriately
)

# Apply classification on the 'statement' column.
df['state'] = df['statement'].apply(lambda x: "TRUE" if classify(x) else "FALSE")

# Optionally, if you want to output only the 'state' and 'statement' columns.
output_df = df[['state', 'statement']]

# Save the new DataFrame to a CSV file.
output_df.to_csv('output_youtube.csv', index=False)

print("Processing complete.")
