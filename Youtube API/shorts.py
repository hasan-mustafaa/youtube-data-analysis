from youtube_video import YoutubeVideo


class YoutubeShorts(YoutubeVideo):
    def __init__(self, vid_type='shorts', maxDuration=60, channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None):
        super().__init__(channelTitle, title, description, tags,
                 publishedAt, viewCount, likeCount, favoriteCount, commentCount, duration,
                 definition, caption)
        #Do I need Like,Comment Ratio
        self.maxDuration = maxDuration
        self.type = vid_type

    def popular_video(self):  # Above a certain View Count
        if self.viewCount is not None:
            self.viewCount = int(self.viewCount)
            if self.viewCount >= 500000:
                return 'Popular'
            else:
                return 'Unpopular'


    def video_feedback(self):  # Above a certain comment count
        if self.commentCount is not None:
            self.commentCount = int(self.commentCount)
            if self.commentCount >= 100:
                return 'High Feedback'
            elif self.commentCount >= 50:
                return 'Medium Feedback'
            elif self.commentCount >= 10:
                return 'Low Feedback'
            else:
                return 'Insufficient Feedback'

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
        if self.likeRatio >= 40:
            return 'High Engagement'
        elif self.likeRatio >= 25:
            return 'Medium Engagement'
        elif self.likeRatio >= 10:
            return 'Low Engagement'
        else:
            return 'Not Well Received'

# Take avg of comment and video count and provide ratings based on how much higher or lower it is
# May need to import methods to calculate ratio
# don't forget UML
# Create different dataframes for shorts and longform
