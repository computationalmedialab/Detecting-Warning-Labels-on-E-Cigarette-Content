# Detecting-Warning-Labels-on-E-Cigarette-Content
Detecting Warning Labels on E-Cigarette Content Across Social Media Platforms
# Introduction
This repository contains scripts for collecting data from TikTok and YouTube, processing them, and feeding them to a rule-based classifier. The pipeline consists of multiple steps, including video downloading, screenshot extraction, OCR processing, language detection, classification, and statistical analysis.
# Technical requirements
Before proceeding, ensure that you have the following installed:
Python 3.x
An Oracle cloud instance
A Box account with API access
Basic command-line knowledge
# Required Dependencies
Install the following Python libraries before running the scripts:
```bash
pip install opencv-python pandas numpy pytesseract langdetect requests boxsdk
```
# Box Download
1. First we need to sign up for a free version of box. 
2. We get to the developer console and then we access the APP console then we click create new app. 
3. Then we click on custom app, and then we create a custom app.
4. Then we choose the authnetication type which is auth 2 and create the app afterwards.
5. Now in the configuration tab of the App that we created we click on App access only.
6. And then we choose Make API calls using using the as-user header and generate user access tokens.
7. and then we get the client ID, client secret and developer token.
8. The developer token has to be generated every 60 minutes because it will expire in every 60 minutes.
9. We now get the folder ID from box.
10. On the Oracle Instance we write a script to download all the videos. (`get_videos.py`)
# Screenshots
1. The script takes screenshots every one second until the max time which is 79 seconds.
# Oracle Vision
1. Takes the screenshots in form of images and turns them into text. (`ocr.py`)
2. Now we write a script called (`remove_null.py`) that gets rid of the rows containing no text.
3. We then write a script that gets rid of the duplicate texts inside the output text file called (`remove_textdup.py`)
# Language Detection
1. We write a program that can take all the text extracted from the images in the csv file and detect their language and output a file called, extracted_lang_output.txt. (`lang_detector.py`)
2. In the next step, in the script called (`lang_score.py`), we parse the json formatted text file (`extracted_lang_output.txt`) and we set a threshold of 90% and say that if the language detected score is higher than 90% then consider it a valid prediction and write it to a csv file (`language_score.csv`) alongside its language name and the text.
3. We then remove the duplicates with a script called (`remove_duplicates.py`)
4. We then get the english text rows by performing the command
```bash
cat unique_lang_score.csv | grep English > warnings.txt
```
# Classifier
1. We write a classifier script to check if each text row satisfies the classifier conditions. (`classifier.py`)
# Conditions
1. We write a script that checks if the text row belongs to condition 1 or condition 2. (`parser.py`)
2. We write a script that counts how many is condition 1 and how many is condition 2. (`count.py`)
3. We write a script that checks how many of the conditions overlap. (`overlap.py`)
# Video Length
1. We write a script that calculates the length of all videos. (`All_video_length.py`)
2. We write a script that normalizes (format: minutes and seconds) the durations of the videos. (`handle.py`) 
3. We write a script that calculates the average of all video lengths. (`average.py`)
4. We write a script that claculates the standard deviation of the video lengths. (`std.py`) 


