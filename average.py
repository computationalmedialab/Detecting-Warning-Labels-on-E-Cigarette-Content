import pandas as pd


# Create DataFrame
df = pd.read_csv("normalized_video_lengths.csv")


# Function to convert mm:ss to total seconds
def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds

# Convert durations to seconds
durations_in_seconds = [time_to_seconds(d) for d in df["Duration"]]

# Compute average duration in seconds
average_seconds = sum(durations_in_seconds) / len(durations_in_seconds)

# Convert back to mm:ss format
average_minutes = int(average_seconds // 60)
average_remaining_seconds = int(average_seconds % 60)
average_time = f"{average_minutes}:{average_remaining_seconds:02d}"

print("average_time: ", average_time, "average_time in seconds: ",average_seconds)
