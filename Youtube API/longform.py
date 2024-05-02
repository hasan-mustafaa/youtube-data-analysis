from youtube_video import YoutubeVideo


class YoutubeLongForm(YoutubeVideo):
    def __init__(self, maxDuration, vid_type='LongForm', channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None):
        super().__init__(channelTitle, title, description, tags,
                         publishedAt, viewCount, likeCount, favoriteCount, commentCount, duration,
                         definition, caption)
        self.vid_type = vid_type
        self.maxDuration = maxDuration


    def comment_engagement(self):  # Assign value to dataframe based on ratio
        if self.commentRatio >= 4:
            return 'High Engagement'
        elif self.commentRatio >= 2:
            return 'Medium Engagement'
        elif self.commentRatio >= 1:
            return 'Low Engagement'
        else:
            return 'Not Well Recieved'

    def like_engagement(self):  # Assign value to dataframe based on ratio
        if self.likeRatio >= 35:
            return 'High Engagement'
        elif self.likeRatio >= 20:
            return 'Medium Engagement'
        elif self.likeRatio >= 13:
            return 'Low Engagement'
        else:
            return 'Not Well Received'


