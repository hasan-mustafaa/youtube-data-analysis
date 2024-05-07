import pandas as pd


class YoutubeChannel:
    """
    Initializes the YouTube Channels class which fetches and organizes various metrics and data from Youtube for each channel

    **Attributes:**

    - `_youtube` (required): Build object from googleapiclient.discovery used for making YouTube Data API requests.
    - `_channel_ids` (list, private): List of channel IDs. Modifying these IDs can lead to errors.
    - `channelName` (str): Name of the channel.
    - `subscribers` (str): Number of subscribers the channel has.
    - `views` (str): Total number of views the channel's videos have.
    - `totalVideos` (str): Total number of videos uploaded by the channel.
    - `_playlistId` (str, private): ID of the channel's upload playlist. Modifying this ID can lead to errors.

    **Methods:**

    - `_validate_channel_ids(self, channel_ids)` (private): Validates the format and existence of channel IDs. Raises `ValueError` if any ID is empty, not a string, or has incorrect length.
    - `get_channel_stats(self, channel_ids)`: Retrieves channel statistics (title, subscriber count, view count, video count, upload playlist ID) for a given list of channel IDs. Returns a Pandas DataFrame containing the data.
    - `get_video_ids(self, playlist_id)`: Retrieves a list of video IDs from a given playlist ID.
    """

    def __init__(self, youtube=None, channel_ids=None, channelName=None, subscribers=None, view=None, totalVideos=None,
                 playlistId=None):
        """
        Initializes the YoutubeChannel object.

        **Args:**

        - `youtube`: Build object from googleapiclient.discovery (required).
        - `channel_ids` (list, optional): List of channel IDs.
        - `channelName` (str, optional): Name of the channel.
        - `subscribers` (str, optional): Number of subscribers the channel has.
        - `view` (str, optional): Total number of views the channel's videos have.
        - `totalVideos` (str, optional): Total number of videos uploaded by the channel.
        - `playlistId` (str, optional): ID of the channel's upload playlist.
        """
        self.subscribers_per_hundredk = None
        self._youtube = youtube  # Required to make requests to the API, modification could cause the program to stop running
        self._channel_ids = channel_ids  # Modifying Channel ID's to incorrect Id's will stop the program from working
        self.channelName = channelName
        self.subscribers = subscribers
        self.view = view
        self.totalVideos = totalVideos
        self._playlistId = playlistId  # Modifying Playlist ID's to incorrect Id's will stop the program from working

    def _validate_channel_ids(self, channel_ids):
        """
        Validates the formats and existence of Channel IDS.

        :param channel_ids: List of Channel IDs to be validated
        :raises: If any Channel ID in the array is invalid
        """
        if not channel_ids:
            raise ValueError("List of Channel IDs cannot be empty")

        for channel_id in channel_ids:
            if not channel_id:
                raise ValueError('Channel ID cannot be empty!')
            elif len(channel_id) != 24:
                raise ValueError('Channel ID is of incorrect length!')
            elif not isinstance(channel_id, str):
                raise ValueError('Channel ID is of invalid datatype!')

    def calculate_subscribers_per_hundredk(self):
        '''
        Calculates the number of subscribers per hundred thousand, and adds it as an attribute to the instance
        '''
        self.subscribers_per_hundredk = self.subscribers // 100000

    def get_channel_stats(self, channel_ids):
        """
        Get channel statistics: title, subscriber count, view count, video count, upload playlist

        Params:
        channels_ids: list of channel IDs

        Returns:
        Dataframe containing the channel statistics for all channels in the provided list: title, subscriber count, view count, video count, upload playlist
        """
        self._validate_channel_ids(channel_ids)  # Calls the private method to validate channel ids.

        channel_info = []
        request = self._youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=','.join(channel_ids))
        response = request.execute()

        for i in range(len(response['items'])):
            data = YoutubeChannel(channelName=response['items'][i]['snippet']['title'],
                                  subscribers=response['items'][i]['statistics']['subscriberCount'],
                                  view=response['items'][i]['statistics']['viewCount'],
                                  totalVideos=response['items'][i]['statistics']['videoCount'],
                                  playlistId=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])

            data.view = int(data.view)
            data.subscribers = int(data.subscribers)
            data.totalVideos = int(data.totalVideos)

            channel_info.append(data)

        return pd.DataFrame([vars(channel) for channel in channel_info])

    def get_video_ids(self, playlist_id, page_token=None):
        """
        Get list of video IDs of all videos in the given playlist, using recusion
        Params:

        playlist_id: playlist ID of the channel
        page_token: Checks whether there is more pages

        Returns:
        List of video IDs of all videos in the playlist
        """

        if page_token is None:
            request = self._youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50)
        else:
            request = self._youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token)

        response = request.execute()
        video_ids = [item['contentDetails']['videoId'] for item in response['items']]

        check_next_page_token = response.get('nextPageToken')
        if check_next_page_token:
            video_ids.extend(self.get_video_ids(playlist_id, check_next_page_token))
        return video_ids





