import os
import pandas as pd
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

API_KEY = os.getenv("YOUTUBE_API")

# this function is used to get the video comments
def get_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1000
    )
    
    response = request.execute()
    
    while request is not None:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            author = comment['authorDisplayName']
            text = comment['textDisplay']
            comments.append([author, text])
        
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100
            )
            response = request.execute()
        else:
            break
    
    return comments

# saving data to csv file format
def save_to_csv(comments, filename):
    df = pd.DataFrame(comments, columns=['Name', 'Comment'])
    df.to_csv(filename, index=False)

# extract video id from the video url
def get_video_id(url):
    parsed_url = urlparse(url)
    
    # the ID is usually in the 'v' parameter
    if parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v")
        if video_id:
            return video_id[0]
    
    if parsed_url.netloc == "youtu.be":
        return parsed_url.path[1:]

    return None

if __name__ == '__main__':
    video_url = input("Enter video url: ")
    video_id = get_video_id(video_url)
    comments = get_comments(video_id)
    save_to_csv(comments, 'data.csv')

    print(f"Extracted {len(comments)} comments and saved to data.csv")
