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
from longform import YoutubeLongForm
from shorts import YoutubeShorts

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

# Understand how it works
for position, series in channel_data.iterrows():
    # Converts row to dictionary, and creates a Youtube Channel instance
    channel_instance = YoutubeChannel(
        youtube=youtube,
        channelName=series['channelName'],
        subscribers=series['subscribers'],
        view=series['view'],
        totalVideos=series['totalVideos'],
        playlistId=series['_playlistId']
    )
    # Now subscriberss per hundredk can be calculated
    channel_instance.calculate_subscribers_per_hundredk()
    channel_data.at[position, 'subscribers_per_hundredk'] = channel_instance.subscribers_per_hundredk

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

for channel in channel_data['channelName'].unique():
    print("Getting video information from channel: " + channel)
    playlist_id = channel_data.loc[channel_data['channelName'] == channel, '_playlistId'].iloc[0]
    video_ids = channel_metrics.get_video_ids(playlist_id)  # Get the video
    current_video_data = video_metrics.get_video_details(video_ids)
    # Concatenate the current video data with the cumulative DataFrame
    video_df = pd.concat([video_df, current_video_data], ignore_index=True)

for position, series in video_df.iterrows():
    video_instance = YoutubeVideo(
        youtube=youtube,
        channelTitle=series['channelTitle'],
        title=series['title'],
        description=series['description'],
        tags=series['tags'],  # Gracefully handles where there is no value
        publishedAt=series['publishedAt'],
        viewCount=series['viewCount'],
        likeCount=series['likeCount'],  # Gracefully handles where there is no value
        favoriteCount=series['favoriteCount'],
        commentCount=series['commentCount'],  # Gracefully handles where there is no value
        duration=series['duration'],
        definition=series['definition'],
        caption=series['caption']
    )
    video_instance.calculate_duration_seconds()
    video_df.at[position, 'durationSecs'] = video_instance.durationSecs
    video_instance.calculate_tags_count()
    video_df.at[position, 'tagsCount'] = video_instance.tagCount
    video_instance.calculate_like_ratio()
    video_df.at[position, 'likeRatio'] = video_instance.likeRatio
    video_instance.calculate_comment_ratio()
    video_df.at[position, 'commentRatio'] = video_instance.commentRatio
    video_instance.calculate_title_length()
    video_df.at[position, 'titleLength'] = video_instance.titleLength

# Output the DataFrame directly
print(video_df)
video_df.to_csv('video_data.csv', index=False)

shorts_info = []
longform_info = []
for position, series in video_df.iterrows():

    if series['durationSecs'] <= 60:
        shorts_instance = YoutubeShorts(series['channelTitle'], series['title'], series['description'], series['tags'],
                                        series['publishedAt'], series['viewCount'], series['likeCount'],
                                        series['favoriteCount'], series['commentCount'], series['duration'],
                                        series['definition'], series['caption'])
        series['videoPopularity'] = shorts_instance.popular_video()
        series['videoFeedback'] = shorts_instance.video_feedback()
        series['commentEngagement'] = shorts_instance.comment_engagement()
        series['likesEngagement'] = shorts_instance.like_engagement()
        shorts_info.append(shorts_instance)
    elif series['durationSecs'] > 60:
        longform_instance = YoutubeLongForm(series['channelTitle'], series['title'], series['description'],
                                            series['tags'],
                                            series['publishedAt'], series['viewCount'], series['likeCount'],
                                            series['favoriteCount'], series['commentCount'], series['duration'],
                                            series['definition'], series['caption'])
        series['videoPopularity'] = longform_instance.popular_video()
        series['videoFeedback'] = longform_instance.video_feedback()
        series['commentEngagement'] = longform_instance.comment_engagement()
        series['likesEngagement'] = longform_instance.like_engagement()
        longform_info.append(longform_instance)

shorts_df = pd.DataFrame([vars(short) for short in shorts_info])
print(shorts_df)
shorts_df.to_csv('shorts_data.csv', index=False)

longform_df = pd.DataFrame([vars(longform) for longform in longform_info])
print(longform_df)
longform_df.to_csv('longform_vido_data.csv', index=False)



