from googleapiclient.discovery import build

api_key = 'AIzaSyA0h_nvX_m1-ZlqeCyq07sxVbAkzjpzIvc'

youtube = build('youtube', 'v3', developerKey=api_key)

# request = youtube.channels().list(
#     part='statistics',
#     forUsername='sentdex'
# )
video_id = 'th5_9woFJmk'
video_response = youtube.commentThreads().list(
            maxResults = 100,
            part = 'snippet',
            videoId = video_id
            ).execute()
# response = request.execute()

# response
comments = []
while video_response:
        
    # extract required info from each result object 
    for item in video_response['items']:
    
        # extract comment resources from comment threat resource
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

        # append a single comment
        comments.append(comment)
print(comments)