from youtube_video import YoutubeVideo

class YoutubeShorts(YoutubeVideo):
    '''
    Extends YoutubeVideo class to handle Youtube Short Videos
    Includes additional methods and attributes exclusive to this class
    '''
    def __init__(self, youtube=None, video_ids=None,channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None,dayPublishedAt=None, titleLength=None, likeRatio=None, commentRatio=None, durationSecs=None, vid_type='Shorts', maxDuration=60):

        """
        Parameters

        - `youtube` (required): Build object from googleapiclient.discovery used for making YouTube Data API requests.
        - `video_id` (str, optional): ID of the video.
        - `channelTitle` (str, optional): Title of the channel that uploaded the video.
        - `title` (str, optional): Title of the video.
        - `description` (str, optional): Description of the video.
        - `tags` (list, optional): List of tags associated with the video.
        - `publishedAt` (str, optional): Date and time the video was published.
        - `viewCount` (str, optional): Number of views the video has.
        - `likeCount` (str, optional): Number of likes the video has.
        - `favoriteCount` (str, optional): Number of times the video has been favorited.
        - `commentCount` (str, optional): Number of comments on the video.
        - `duration` (str, optional): Duration of the video in ISO 8601 format.
        - `definition` (str, optional): Video definition (e.g., "sd", "hd", "fullhd").
        - `caption` (str, optional): Whether captions are available for the video.
        - `dayPublishedAt` (str, optional):
        - 'publishedAt` (str, optional):
        - 'titleLength: Length of the video title (optional)
        - 'likeRatio: Ratio of likes to views (optional)
        - 'commentRatio: Ratio of comments to views (optional)
        -' durationSecs: Duration of the video in seconds (optional)
        - 'vid_type: Type of video, defaults to 'Shorts'
        - 'maxDuration: Maximum allowed duration for a YouTube Shorts video, defaults to 60 seconds

        """

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

    def popular_video(self):
        """
        Checks whether a certain video was popular or not, based of whether it meets a threshold of views
        """
        if self.viewCount is not None:
            self.viewCount = int(self.viewCount)
            if self.viewCount >= 300000:
                self.videoPopularity = 'Popular'
            else:
                self.videoPopularity = 'Unpopular'

    def video_feedback(self):
        """
        Calculates video feedback using the number of comments
        """
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

    def comment_engagement(self):
        """
        Calculates comment engagement based on Comment Ratio
        """
        if self.commentRatio >= 4:
            self.commentEngagement = 'High Comment Engagement'
        elif self.commentRatio >= 2:
            self.commentEngagement = 'Medium Comment Engagement'
        elif self.commentRatio >= 1:
            self.commentEngagement = 'Low Comment Engagement'
        else:
            self.commentEngagement = 'Not Well Recieved'

    def like_engagement(self):
        """
        Calculates like engagement based on like Ratio
        """
        if self.likeRatio >= 40:
            self.likeEngagement = 'High Like Engagement'
        elif self.likeRatio >= 25:
            self.likeEngagement = 'Medium Like Engagement'
        elif self.likeRatio >= 10:
            self.likeEngagement = 'Low Like Engagement'
        else:
            self.likeEngagement = 'Not Well Received'