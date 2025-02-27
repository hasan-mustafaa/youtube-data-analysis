import isodate
from dateutil import parser
import pandas as pd


class YoutubeVideo:
    """
        Fetches and organizes various statistics and details for a YouTube video.

        **Attributes:**

        - `_youtube` (required): Build object from googleapiclient.discovery used for making YouTube Data API requests.
        - `_video_id` (str, private): ID of the video. Modifying this ID can lead to errors.
        - `channelTitle` (str): Title of the channel that uploaded the video.
        - `title` (str): Title of the video.
        - `description` (str): Description of the video.
        - `tags` (list, optional): List of tags associated with the video.
        - `publishedAt` (str): Date and time the video was published.
        - `viewCount` (str): Number of views the video has.
        - `likeCount` (str): Number of likes the video has.
        - `favoriteCount` (str): Number of times the video has been favorited.
        - `commentCount` (str): Number of comments on the video.
        - `duration` (str, optional): Duration of the video in ISO 8601 format.
        - `definition` (str, optional): Video definition (e.g., "sd", "hd", "fullhd").
        - `caption` (str, optional): Whether captions are available for the video.

        **Methods:**

        - `get_video_details(self, video_ids)`: Retrieves detailed statistics and information for a given list of video IDs. Returns a Pandas DataFrame containing the data.
        - `get_comments_in_videos(self, video_ids)`: Retrieves top-level comments (up to 10) as text for a given list of video IDs. Returns a Pandas DataFrame containing the data.
        """

    def __init__(self, youtube=None, video_id=None, channelTitle=None, title=None, description=None, tags=None,
                 publishedAt=None, viewCount=None, likeCount=None, favoriteCount=None, commentCount=None, duration=None,
                 definition=None, caption=None):
        """
         Initializes the YoutubeVideo object.

         **Args:**

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
         """
        self.videoFeedback = None
        self.dayPublishedAt = None
        self.titleLength = None
        self.likeRatio = None
        self.tagCount = None
        self.durationSecs = None
        self.commentRatio = None
        self._youtube = youtube  # Required to make requests to the API, modification could cause the program to stop running.
        self._video_id = video_id  # Modifying Video ID's to incorrect ID's will stop the program from working
        self.channelTitle = channelTitle
        self.title = title
        self.description = description
        self.tags = tags
        self.publishedAt = publishedAt
        self.viewCount = viewCount
        self.likeCount = likeCount
        self.favoriteCount = favoriteCount
        self.commentCount = commentCount
        self.duration = duration
        self.definition = definition
        self.caption = caption

    def _validate_video_ids(self, video_ids):
        """
        Validates the formats and existence of Channel IDS.

        :param video_ids: List of Video IDs to be validated
        :raises: If any Channel ID in the array is invalid
        """
        if not video_ids:
            raise ValueError("List of Channel IDs cannot be empty")

        for video_ids in video_ids:
            if not video_ids:
                raise ValueError('Video ID cannot be empty!')
            elif not isinstance(video_ids, str):
                raise ValueError('Video ID is of invalid datatype!')

    def day_published(self):  # Not working
        self.dayPublishedAt = parser.parse(self.dayPublishedAt)
        self.dayPublishedAt = self.publishedAt.strftime('%A')

    def calculate_duration_seconds(self):
        '''
        Converts the video duration from the propietary format, into seconds
        '''
        self.durationSecs = isodate.parse_duration(self.duration).total_seconds()

    def calculate_tags_count(self):
        '''
        Converts the number of tags associated with the video
        '''
        self.tagCount = len(self.tags) if self.tags else 0

    def calculate_like_ratio(self):
        '''
        Converts the video duration from the propietary format, into seconds
        '''
        if self.viewCount == 0 or self.likeCount == 0:
            self.likeRatio = 0
        else:
            self.likeRatio = (self.likeCount / self.viewCount) * 1000

    def calculate_comment_ratio(self):
        '''
        Calculates the Comment to View Ratio, per thousand views
        '''
        self.commentRatio = (self.commentCount / self.viewCount) * 1000 if self.commentCount or self.viewCount else 0

    def calculate_title_length(self):
        '''
        Calculates Length of the Title, inclusive of spaces
        '''
        self.titleLength = len(self.title)

    def get_video_details(self, video_ids):
        """
        Get video statistics of all videos with given IDs

        :param video_ids: list of video IDs

        Returns:
        Dataframe with statistics of videos, i.e.:
            'channelTitle', 'title', 'description', 'tags', 'publishedAt'
            'viewCount', 'likeCount', 'favoriteCount', 'commentCount'
            'duration', 'definition', 'caption'
        """
        self._validate_video_ids(video_ids)

        all_video_info = []

        for i in range(0, len(video_ids), 50):
            request = self._youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(video_ids[i:i + 50])
            )
            response = request.execute()

            for video in response['items']:
                stats_to_keep = YoutubeVideo(channelTitle=video['snippet']['channelTitle'],
                                             title=video['snippet']['title'],
                                             description=video['snippet']['description'],
                                             tags=video['snippet'].get('tags', []),  # Handle any missing values
                                             publishedAt=video['snippet']['publishedAt'],
                                             viewCount=video['statistics']['viewCount'],
                                             likeCount=video['statistics'].get('likeCount', 0),
                                             # Handle any missing values
                                             favoriteCount=video['statistics']['favoriteCount'],
                                             commentCount=video['statistics'].get('commentCount', 0),
                                             # Handle any missing values
                                             duration=video['contentDetails']['duration'],
                                             definition=video['contentDetails']['definition'],
                                             caption=video['contentDetails']['caption'])

                stats_to_keep.viewCount = int(stats_to_keep.viewCount)
                stats_to_keep.likeCount = int(stats_to_keep.likeCount)
                stats_to_keep.favoriteCount = int(stats_to_keep.favoriteCount)
                stats_to_keep.commentCount = int(stats_to_keep.commentCount)

                all_video_info.append(stats_to_keep)

        return pd.DataFrame([vars(video) for video in all_video_info])

    def get_comments_in_videos(self, video_ids):
        """
        Get top level comments as text from all videos with given IDs
        (only the first 10 comments due to quote limit of Youtube API)

        :param video_ids: list of video IDs

        Returns:
        Dataframe with video IDs and associated top level comment in text.
        """
        all_comments = []

        for video_id in video_ids:
            try:
                request = self._ube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id
                )
                response = request.execute()

                comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in
                                     response['items'][0:10]]
                comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

                all_comments.append(comments_in_video_info)
            except:
                # When error occurs - most likely because comments are disabled on a video
                print('Could not get comments for video ' + video_id)

        return pd.DataFrame(all_comments)

    def popular_video(self):
        """
        Checks whether a certain video was popular or not, based of whether it meets a threshold of views
        """
        if self.viewCount is not None:
            self.viewCount = int(self.viewCount)
            if self.viewCount >= 150000:
                self.videoPopularity = 'popular'
            else:
                self.videoPopularity = 'unpopular'

    def video_feedback(self):
        """
        Calculates video feedback using the number of comments
        """
        if self.commentCount is not None:
            self.commentCount = int(self.commentCount)
            if self.commentCount >= 125:
                self.videoFeedback = 'High Engagement'
            elif self.commentCount >= 75:
                self.videoFeedback = 'Medium Engagement'
            elif self.commentCount >= 25:
                self.videoFeedback = 'Low Engagement'
            else:
                self.videoFeedback = 'Not Well Recieved'
