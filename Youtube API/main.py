from dateutil import parser
import pandas as pd
import isodate

# Data visualization libraries
import seaborn as sns

sns.set(style="darkgrid", color_codes=True)

# Google API
from googleapiclient.discovery import build

# Importing Classes
from youtube_channel import YoutubeChannel
from youtube_video import YoutubeVideo


api_key = 'AIzaSyAUQfbrbRO2VDhHLuQcfVBTk6QQKmyHiPs'

# Channel Ids to be analysed
channel_ids = ['UCtYLUTtgS3k1Fg4y5tAhLbw',  # Statquest
               'UCCezIgC97PvUuR4_gbFUs5g',  # Corey Schafer
               'UCfzlCWGWYyIQ0aLC5w48gBQ',  # Sentdex
               'UCNU_lfiiWBdtULKOw6X0Dig',  # Krish Naik
               'UCzL_0nIe8B4-7ShhVPfJkgw',  # DatascienceDoJo
               'UCLLw7jmFsvfIVaUFsLs8mlQ',  # Luke Barousse
               'UCiT9RITQ9PW6BhXK0y2jaeg',  # Ken Jee
               'UC7cs8q-gJRlGwj4A8OmCmXg',  # Alex the analyst
               'UC2UXDak6o7rBm23k3Vv5dww',  # Tina Huang
               ]

youtube = build('youtube', 'v3', developerKey=api_key)

# Creates an instance of the 'YoutubeMetrics' Class passing the youtube object
channel_metrics = YoutubeChannel(youtube)
video_metrics = YoutubeVideo(youtube)
# Uses a method from the class, to retrieve statistics using the channel id's in the array
channel_data = channel_metrics.get_channel_stats(channel_ids)

# Convert count columns which were originally contain string values to numeric columns which is required for analysis
numeric_cols = ['subscribers', 'views', 'totalVideos']
channel_data[numeric_cols] = channel_data[numeric_cols].apply(pd.to_numeric, errors='coerce') #String to Numeric(Either Int or Float)

# Tells us which playbutton they might have using comparisons
subscribers_per_hundredk = channel_data['subscribers'] // 100000
channel_data['subscribers_per_hundredk'] = subscribers_per_hundredk

# Converts the data from channel_data to a csv
channel_data.to_csv('channel_data.csv', index=False)
print(channel_data)


# Create a dataframe with video statistics and comments from all channels
video_df = pd.DataFrame()  # Create an empty DataFrame for cumulative results


'''
Loops through each unique channel name in the channel name column. It outputs the name of the channel being processed.
Retrives the playlist_id of each channel  then passed it through a method which retrieves the list of video_ids.
It then uses the video_ids to find details of each video, e.g. Description, Views etc
Last line concatenates the Video data from all channels
'''
for c in channel_data['channelName'].unique():
    print("Getting video information from channel: " + c)
    playlist_id = channel_data.loc[channel_data['channelName'] == c, 'playlistId'].iloc[0]
    video_ids = channel_metrics.get_video_ids(playlist_id)
    # Get video data for the current channel efficiently
    current_video_data = video_metrics.get_video_details(video_ids)
    # Concatenate the current video data with the cumulative DataFrame
    video_df = pd.concat([video_df, current_video_data], ignore_index=True)

# Converts column with string representation to numeric for analysis
cols = ['viewCount', 'likeCount', 'favoriteCount', 'commentCount']
video_df[cols] = video_df[cols].apply(pd.to_numeric, errors='coerce', axis=1) #String to Numeric

# Create publish day (in the week) column
'''
First line parses timestamps into datetime objects representing date and time of video publications
Second line, creates a new column and extracts the day of the week that it was published
'''
video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x)) #String to Datetime
video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))

# Convert duration to seconds
'''
First line parses the string of duration e.g. 'PT6M49S' into Pandas TimeDelta Datetime. 
Second line parsed durations to specific units of seconds
'''
video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]') #String to Pandas TimeDelta Datetime

# Add number of tags
video_df['tagsCount'] = video_df['tags'].apply(lambda x: 0 if x is None else len(x))

# Comments and likes per 1000 view ratio
video_df['likeRatio'] = video_df['likeCount'] / video_df['viewCount'] * 1000
video_df['commentRatio'] = video_df['commentCount'] / video_df['viewCount'] * 1000

# Title character length
video_df['titleLength'] = video_df['title'].apply(lambda x: len(x)) #Converting String to Integer

# Output the DataFrame directly
print(video_df)
video_df.to_csv('video_data.csv', index=False)
