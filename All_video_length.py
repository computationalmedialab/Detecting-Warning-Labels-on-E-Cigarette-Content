import os
import csv
import tempfile
from boxsdk import Client, OAuth2
from moviepy import VideoFileClip

# Declare global SKIP variable
SKIP = 0

def get_processed_videos(csv_file):
    """
    Get the list of video filenames from the CSV file to avoid reprocessing them.

    Args:
        csv_file (str): Path to the CSV file containing processed video names.

    Returns:
        set: Set of video filenames already processed.
    """
    processed_videos = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                processed_videos.add(row[0])  # Assuming the video name is in the first column
    return processed_videos

def get_video_lengths_from_box(client, folder_id, processed_videos):
    """
    Get the length of each video in a Box folder via temporary files, excluding those already processed.

    Args:
        client (boxsdk.Client): Authenticated Box client.
        folder_id (str): ID of the Box folder.
        processed_videos (set): Set of processed video filenames to avoid reprocessing.

    Returns:
        list: A list of tuples with video filenames and their durations in 'mm:ss' format.
    """
    global SKIP  # Use the global SKIP variable
    video_lengths = []
    try:
        folder = client.folder(folder_id).get()
        items = folder.get_items()
        for item in items:
            if item.type == 'file' and item.name.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')):
                if item.name in processed_videos:
                    print(f"Skipping already processed video: {item.name}")
                    SKIP += 1  # Increment SKIP counter
                    print(SKIP)
                    continue
                print(f"Processing {item.name}...")
                try:
                    # Download video file content
                    file_content = client.file(item.id).content()

                    # Write to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(item.name)[-1]) as temp_file:
                        temp_file.write(file_content)
                        temp_file_path = temp_file.name
                    
                    # Process the video file
                    try:
                        with VideoFileClip(temp_file_path) as video:
                            duration = video.duration  # Duration in seconds
                            minutes, seconds = divmod(duration, 60)
                            formatted_duration = f"{int(minutes):02}:{int(seconds):02}"  # mm:ss format
                            video_lengths.append((item.name, formatted_duration))
                    finally:
                        # Clean up the temporary file
                        os.remove(temp_file_path)
                except Exception as e:
                    print(f"Could not process {item.name}: {e}")
    except Exception as e:
        print(f"Error accessing Box folder: {e}")
    return video_lengths

def save_to_csv(data, output_file):
    """
    Save video lengths to a CSV file.

    Args:
        data (list): List of tuples with video filenames and durations.
        output_file (str): Path to the output CSV file.
    """
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:  # Changed 'w' to 'a'
        writer = csv.writer(csvfile)
        # If the file is empty, write the header row
        if os.stat(output_file).st_size == 0:
            writer.writerow(["Video File Name", "Duration"])
        for row in data:
            # Enclose the video name in quotes to prevent Excel from interpreting it as a formula
            #row[0] file name and row[1] duration
            writer.writerow([f'{row[0]}', row[1]])
    print(f"CSV file saved as {output_file}")


if __name__ == "__main__":
    # Replace with your Box Developer Token
    developer_token = "cMeMyP9gHreOEh5cg1JQhMIqzGjBfC9t"
    
    # Authenticate with Box
    auth = OAuth2(client_id='vhe985igvvc07cb5bw7kuap0zvw2pil1', client_secret='yGpcGSNu25dhcXYxtfd5fitAbykbBul2', access_token=developer_token)
    client = Client(auth)

    # Replace with your Box folder ID (e.g., 0 for root folder)
    folder_id = input("Enter the Box folder ID (e.g., '0' for the root folder): ")
    
    # Path to the CSV file where previously processed videos are stored
    csv_file = "box_video_lengths.csv"

    try:
        # Get the list of already processed videos
        processed_videos = get_processed_videos(csv_file)

        # Get video lengths from Box, excluding already processed videos
        video_lengths = get_video_lengths_from_box(client, folder_id, processed_videos)
        
        if video_lengths:
            # Print video durations
            print("Video durations (in seconds):")
            for video_name, duration in video_lengths:
                print(f"{video_name}: {duration} seconds")
            
            # Save CSV to the current working directory
            output_csv = os.path.join(os.getcwd(), csv_file)
            save_to_csv(video_lengths, output_csv)
        else:
            print("No new valid video files found in the Box folder.")

    except Exception as e:
        print(f"Error: {e}")
