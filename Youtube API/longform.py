from youtube_video import YoutubeVideo

class YoutubeLongForm(YoutubeVideo):
    def __init__(self, youtube=None, video_ids=None, channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None, dayPublishedAt=None, titleLength=None, likeRatio=None, commentRatio=None, durationSecs=None, vid_type='Longform', maxDuration='Infinite'):
        super().__init__(youtube,video_ids, channelTitle, title, description, tags,
                         publishedAt, viewCount, likeCount, favoriteCount, commentCount, duration,
                         definition, caption)
        self.videoPopularity = None
        self.videoFeedback = None
        self.commentEngagement = None
        self.likeEngagement = None
        self.commentRatio = commentRatio
        self.titleLength = titleLength
        self.dayPublishedAt = dayPublishedAt
        self.likeRatio = likeRatio
        self.durationSecs = durationSecs
        self.vid_type = vid_type
        self.maxDuration = maxDuration

    def comment_engagement(self):  # Assign value to dataframe based on ratio
        if self.commentRatio >= 4:
            self.commentEngagement = 'High Comment Engagement'
        elif self.commentRatio >= 2:
            self.commentEngagement = 'Medium Comment Engagement'
        elif self.commentRatio >= 1:
            self.commentEngagement = 'Low Comment Engagement'
        else:
            self.commentEngagement = 'Not Well Recieved'

    def like_engagement(self):  # Assign value to dataframe based on ratio
        if self.likeRatio >= 35:
            self.likeEngagement = 'High Like Engagement'
        elif self.likeRatio >= 20:
            self.likeEngagement = 'Medium Like Engagement'
        elif self.likeRatio >= 10:
            self.likeEngagement = 'Low Like Engagement'
        else:
            self.likeEngagement = 'Not Well Received'
