import pandas as pd

def convert_to_seconds(time_str):
    """Convert mm:ss format to seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def convert_to_mmss(seconds):
    """Convert seconds to mm:ss format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def calculate_std_duration_for_csv(file_path):
    """Calculate and print the standard deviation of duration in mm:ss and seconds for a single CSV file."""
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return
    
    # Check if the 'duration' column exists
    if 'duration' not in df.columns:
        print(f"Error: 'duration' column not found in {file_path}")
        return

    # Convert durations to seconds
    df['duration_seconds'] = df['duration'].apply(convert_to_seconds)
    
    # Calculate the standard deviation of durations in seconds
    std_seconds = df['duration_seconds'].std()
    
    # Convert the standard deviation to mm:ss format
    std_mmss = convert_to_mmss(std_seconds)
    
    # Print the results
    print(f"Standard deviation of duration in mm:ss: {std_mmss}")
    print(f"Standard deviation of duration in seconds: {std_seconds:.2f}")

if __name__ == "__main__":
    # Replace with the path to your single CSV file
    file_path_youtube = "youtube_video_lengths.csv"  
    print("youtube:")
    calculate_std_duration_for_csv(file_path_youtube)
    file_path_tiktok = "tiktok_video_lengths.csv"  
    print("tiktok:")
    calculate_std_duration_for_csv(file_path_tiktok)
    
