import pandas as pd

def normalize_duration(duration):
    parts = list(map(int, duration.split(':')))
    
    if len(parts) == 3:  # hh:mm:ss format
        minutes = parts[0]
        seconds = parts[1]
    else:
        return duration  # Return as is if format is unexpected
    
    return f"{minutes}:{seconds:02d}"



df = pd.read_csv('box_video_length_latest.csv')

# Normalize durations
df["Duration"] = df["Duration"].apply(normalize_duration)

df.to_csv("normalized_video_lengths.csv", index=False)