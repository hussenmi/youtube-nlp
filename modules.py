# pip install --upgrade google-api-python-client
# pip install --upgradpe google-auth-oauthlib google-auth-httplib2

from googleapiclient.discovery import build

class ApiCrawler():

    def __init__(self):
        self.api_key = 'AIzaSyDsD5jELu-4jyFRYpeUfOiueSuuBMXz7aA' # Chris' API key
    
    def get_comments(self, video_id):

        replies = []
  
        # create youtube resource object
        youtube = build('youtube', 'v3', developerKey = self.api_key)
  
        # retrieve youtube video results
        video_response = youtube.commentThreads().list(
        maxResults = 100,
        part = 'snippet, replies',
        videoId = video_id
        ).execute()
  
        # iterate video responses
        while video_response:
        
            # extract required info from each result object 
            for item in video_response['items']:
            
                # extract comments
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
              
                # count number of replies of comment
                replycount = item['snippet']['totalReplyCount']
  
                # if reply is there
                if replycount > 0:
                
                    # iterate through all reply
                    for reply in item['replies']['comments']:
                    
                        # extract reply
                        reply = reply['snippet']['textDisplay']
                      
                        # store reply as list
                        replies.append(reply)
  
                # print comment with list of reply
                print(comment, replies, end = '\n\n')
  
                # empty reply list
                replies = []
  
            # repeat if next page of comments exist
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                        part = 'snippet, replies',
                        videoId = self.video_id,
                        pageToken = video_response['nextPageToken']
                    ).execute()
            else:
                break