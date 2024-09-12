import os
from googleapiclient.discovery import build

youtube_api_key = os.getenv("YOUTUBE_API")

if youtube_api_key is None:
    print("Error: YouTube API key not found.")
else:
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    print("YouTube client initialized successfully.")
    print(youtube_api_key)
