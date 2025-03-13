import pandas as pd

# Define file path
file_path = "output_youtube.csv"

# Load CSV file and preview first few rows
df = pd.read_csv(file_path)
df.head()

# Ensure "status" is treated as a string for filtering
df["status"] = df["status"].astype(str)

# Convert "text" column to string to avoid errors
df["text"] = df["text"].astype(str)

# Filter rows where status is TRUE
df_true = df[df["status"].str.upper() == "TRUE"]

# Define keywords for filtering df1
df1_keywords = [
    "This product contains nicotine",
    "This product contains tobacco",
    "Nicotine is an addictive substance",
    "For adult (21+)",
    "Nicotine is an addictive chemical"
]

# Create df1: Text contains "WARNING" and at least one keyword
df1 = df_true[
    df_true["text"].str.contains("WARNING", case=False, na=False) &
    df_true["text"].str.contains("|".join(df1_keywords), case=False, na=False)
]

# Create df2: Text contains both "Nicotine" and "Addictive"
df2 = df_true[
    df_true["text"].str.contains("Nicotine", case=False, na=False) &
    df_true["text"].str.contains("Addictive", case=False, na=False)
]

# Show filtered results
df1_preview = df1.head()
df2_preview = df2.head()

df1.to_csv("condition1.csv", index=False)
df2.to_csv("condition2.csv", index=False)
print(df1_preview)
print(df2_preview)
