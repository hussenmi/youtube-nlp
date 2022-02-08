# pip install --upgrade google-api-python-client
# pip install --upgradpe google-auth-oauthlib google-auth-httplib2

from googleapiclient.discovery import build

class ApiCrawler():

    def __init__(self):
        """ 
        Initializes ApiCrawler instance with 10,000 units quote per day or 
        250,000 comments per day. E.g. a Joe Rogan podcast episode with Jordan
        Peterson has 89,925 comments + replies at 25,000,000 views
        """
        self.api_key = 'AIzaSyDsD5jELu-4jyFRYpeUfOiueSuuBMXz7aA' # Chris' API key

    def get_comments(self, video_id):
        """ Gets the top-level comments of a single video and returns an 
        array of strings
        e.g. [ "first comment", "second comment", ...]
        """

        # intialize empty array to return comments
        comments = []
  
        # create youtube resource object
        youtube = build('youtube', 'v3', developerKey = self.api_key)
  
        # retrieve youtube video results
        video_response = youtube.commentThreads().list(
            maxResults = 100,
            part = 'snippet',
            videoId = video_id
            ).execute()
  
        # iterate video responses
        while video_response:
        
            # extract required info from each result object 
            for item in video_response['items']:
            
                # extract comment resources from comment threat resource
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
  
                # append a single comment
                comments.append(comment)
  
                # # repeat if next page of comments exist
                # if 'nextPageToken' in video_response:
                #     video_response = youtube.commentThreads().list(
                #             part = 'snippet, replies',
                #             videoId = video_id,
                #             pageToken = video_response['nextPageToken']
                #         ).execute()
                # else:
                #     break

        return comments
    
    def get_comments_and_replies(self, video_id):
        """
        Gets the top-level comments and replies of a single video and returns a 
        nested array of strings.
        E.g. [["first comment", ["first reply", "second reply"]], ["second
        comment", ["first reply", "second reply"], [third...]]]
        """

        # intialize empty array to return comments
        comments_replies = []
  
        # create youtube resource object
        youtube = build('youtube', 'v3', developerKey = self.api_key)
  
        # retrieve youtube video results
        video_response = youtube.commentThreads().list(
        maxResults = 10,
        part = 'snippet, replies',
        videoId = video_id
        ).execute()
  
        # iterate video responses
        while video_response:
        
            # extract required info from each result object 
            for item in video_response['items']:
            
                # extract comment resources from comment threat resource
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
              
                # count number of replies of comment
                replycount = item['snippet']['totalReplyCount']
  
                replies = []

                # if reply is there
                if replycount > 0:
                
                    # iterate through all reply
                    for reply in item['replies']['comments']:
                    
                        # extract reply
                        reply = reply['snippet']['textDisplay']
                      
                        # store reply as list
                        replies.append(reply)
  
                # append a single comment and its replies
                comments_replies.append([comment, replies])
  
            # # repeat if next page of comments exist
            # if 'nextPageToken' in video_response:
            #     video_response = youtube.commentThreads().list(
            #             part = 'snippet, replies',
            #             videoId = video_id,
            #             pageToken = video_response['nextPageToken']
            #         ).execute()
            # else:
            #     break

        return comments_replies

crawler = ApiCrawler()
# comments = crawler.get_comments("RcYjXbSJBN8") # Joe Rofan podcase with 89,925 comments + replies
# comments = crawler.get_comments("___NoMi5pp0") # randome Korean video with 141 comments + replies
print(comments)


'''
Sample commentThreads.list() JSON response
{
  "kind": "youtube#commentThreadListResponse",
  "etag": etag,
  "nextPageToken": string,
  "pageInfo": {
    "totalResults": integer,
    "resultsPerPage": integer
  },
  "items": [
    commentThread Resource
  ]
}

Sample commentThread Resource object:
{
  "kind": "youtube#commentThread",
  "etag": etag,
  "id": string,
  "snippet": {
    "channelId": string,
    "videoId": string,
    "topLevelComment": comments Resource,
    "canReply": boolean,
    "totalReplyCount": unsigned integer,
    "isPublic": boolean
  },
  "replies": {
    "comments": [
      comments Resource
    ]
  }
}

Sample comments Resource object:
{
  "kind": "youtube#comment",
  "etag": etag,
  "id": string,
  "snippet": {
    "authorDisplayName": string,
    "authorProfileImageUrl": string,
    "authorChannelUrl": string,
    "authorChannelId": {
      "value": string
    },
    "channelId": string,
    "videoId": string,
    "textDisplay": string,
    "textOriginal": string,
    "parentId": string,
    "canRate": boolean,
    "viewerRating": string,
    "likeCount": unsigned integer,
    "moderationStatus": string,
    "publishedAt": datetime,
    "updatedAt": datetime
  }
}
'''