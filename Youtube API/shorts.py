from youtube_video import YoutubeVideo
import pandas as pd


class YoutubeShorts(YoutubeVideo):
    def __init__(self, youtube=None, video_ids=None,channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None,dayPublishedAt=None, titleLength=None, likeRatio=None, commentRatio=None, durationSecs=None, vid_type='Shorts', maxDuration=60):
        super().__init__(youtube, video_ids, channelTitle, title, description, tags,
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
        self.maxDuration = maxDuration
        self.type = vid_type

    def popular_video(self):  # Above a certain View Count
        if self.viewCount is not None:
            self.viewCount = int(self.viewCount)
            if self.viewCount >= 300000:
                self.videoPopularity = 'Popular'
            else:
                self.videoPopularity = 'Unpopular'

    def video_feedback(self):  # Above a certain comment count
        if self.commentCount is not None:
            self.commentCount = int(self.commentCount)
            if self.commentCount >= 60:
                self.videoFeedback = 'High Feedback'
            elif self.commentCount >= 30:
                self.videoFeedback = 'Medium Feedback'
            elif self.commentCount >= 10:
                self.videoFeedback = 'Low Feedback'
            else:
                self.videoFeedback = 'Insufficient Feedback'

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
        if self.likeRatio >= 40:
            self.likeEngagement = 'High Like Engagement'
        elif self.likeRatio >= 25:
            self.likeEngagement = 'Medium Like Engagement'
        elif self.likeRatio >= 10:
            self.likeEngagement = 'Low Like Engagement'
        else:
            self.likeEngagement = 'Not Well Received'

#Comment on Classes
