#5 screenshots every 2 seconds till 10 seconds into the video
import cv2 as cv
import numpy as np
import os

# The program will capture a frame every 2 seconds
CAPTURE_PERIOD = 1  # seconds

# The program will only capture images from the first 26 seconds
CAPTURE_MAX_TIME = 1 * 79  # in seconds

#function to the get timestamp
def seconds_to_hms(seconds):
    """
    converts seconds to H:M:S
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

destination_folder = "Screenshots-V2"

video_names = os.listdir('../01-Download/videos/')

for video_name in video_names:
    #Open the video file
    cap = cv.VideoCapture(f"../01-Download/videos/{video_name}")

    #Get the frames per second (FPS) of the video
    fps = int(cap.get(cv.CAP_PROP_FPS))

    # Get the total number of frames in the video
    total_images = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # get a list of frame numbers which will be captured
    frame_numbers_to_capture = np.arange(1, total_images, CAPTURE_PERIOD * fps)

    for number in frame_numbers_to_capture:
    
        #Set the frame position to the specified frame number (using the pointer which points to that position)
        cap.set(cv.CAP_PROP_POS_FRAMES, number)

        #Read the frame at the specified frame number
        ret, frame = cap.read()

        # get seconds elapsed (timestamp for the name of the images)
        time_elapsed = number // fps
        hours, mins, secs = seconds_to_hms(time_elapsed)

        if time_elapsed > CAPTURE_MAX_TIME:
            print("Reached max time, terminating program...")
            break

        # Check if the frame was read successfully
        if ret:
            # process/save image frame
            path_to_save = "/".join(
                [
                    destination_folder,
                    "%s_frame_at_%02d_%02d_%02d.jpg" % (video_name, hours, mins, secs),
                ]
            )
            cv.imwrite(path_to_save, frame)

        else:
            print(f"Error: Could not retrieve frame {number}")

    
    cap.release()
