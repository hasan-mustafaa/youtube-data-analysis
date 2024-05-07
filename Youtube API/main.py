# Google API
from googleapiclient.discovery import build
# Importing Classes
from youtube_channel import YoutubeChannel
from youtube_video import YoutubeVideo
from shorts import YoutubeShorts
from longform import YoutubeLongForm
from sort_search_functions import bubble_sort, merge_sort, linear_search, binary_search
# Import Data Analysis Libraries
import pandas as pd
import time
# Data visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="darkgrid", color_codes=True)

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

# Creates an instance of the 'YoutubeMetrics' Class passing the YouTube object
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

channel_data = channel_data.drop(['_youtube', '_channel_ids'], axis=1)
# Converts the data from channel_data to a csv
channel_data.to_csv('channel_data.csv', index=False)
print(channel_data)

# Create a dataframe with video statistics and comments from all channels
video_df = pd.DataFrame()  # Create an empty DataFrame for cumulative results

'''
Loops through each unique channel name in the channel name column. It outputs the name of the channel being processed.
Retrieves the playlist_id of each channel  then passed it through a method which retrieves the list of video_ids.
It then uses the video_ids to find details of each video, e.g. Description, Views etc
Last line concatenates the Video data from all channels
'''

for channel in channel_data['channelName'].unique():
    print("Getting video information from channel: " + channel)
    playlist_id = channel_data.loc[channel_data['channelName'] == channel, '_playlistId'].iloc[0]
    video_ids = channel_metrics.get_video_ids(playlist_id)
    # Get video data for the current channel efficiently
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
shorts_df = pd.DataFrame()
longform_df = pd.DataFrame()

for position, series in video_df.iterrows():
    if series['durationSecs'] <= 60:
        shorts_instance = YoutubeShorts(youtube=youtube, video_ids=video_ids, channelTitle=series['channelTitle'],
                                        title=series['title'],
                                        description=series['description'],
                                        tags=series['tags'], publishedAt=series['publishedAt'],
                                        viewCount=series['viewCount'], likeCount=series['likeCount'],
                                        favoriteCount=series['favoriteCount'], commentCount=series['commentCount'],
                                        duration=series['duration'],
                                        definition=series['definition'], caption=series['caption'],
                                        dayPublishedAt=series['dayPublishedAt'], titleLength=series['titleLength'],
                                        likeRatio=series['likeRatio'], commentRatio=series['commentRatio'],
                                        durationSecs=series['durationSecs'])
        shorts_instance.popular_video()
        shorts_df.at[position, 'videoPopularity'] = shorts_instance.videoPopularity
        shorts_instance.video_feedback()
        shorts_df.at[position, 'videoFeedback'] = shorts_instance.videoFeedback
        shorts_instance.comment_engagement()
        shorts_df.at[position, 'commentEngagement'] = shorts_instance.commentEngagement
        shorts_instance.like_engagement()
        shorts_df.at[position, 'likeEngagement'] = shorts_instance.likeEngagement
        shorts_info.append(shorts_instance)
    elif series['durationSecs'] > 60:
        longform_instance = YoutubeLongForm(channelTitle=series['channelTitle'], title=series['title'],
                                            description=series['description'],
                                            tags=series['tags'], publishedAt=series['publishedAt'],
                                            viewCount=series['viewCount'], likeCount=series['likeCount'],
                                            favoriteCount=series['favoriteCount'], commentCount=series['commentCount'],
                                            duration=series['duration'],
                                            definition=series['definition'], caption=series['caption'],
                                            dayPublishedAt=series['dayPublishedAt'], titleLength=series['titleLength'],
                                            likeRatio=series['likeRatio'], commentRatio=series['commentRatio'],
                                            durationSecs=series['durationSecs'])
        longform_instance.popular_video()
        longform_df.at[position, 'videoPopularity'] = longform_instance.videoPopularity
        longform_instance.video_feedback()
        longform_df.at[position, 'videoFeedback'] = longform_instance.videoFeedback
        longform_instance.comment_engagement()
        longform_df.at[position, 'commentEngagement'] = longform_instance.commentEngagement
        longform_instance.like_engagement()
        longform_df.at[position, 'likeEngagement'] = longform_instance.likeEngagement
        longform_info.append(longform_instance)

shorts_df = pd.DataFrame([vars(short) for short in shorts_info])
print(shorts_df)
shorts_df.to_csv('shorts_data.csv', index=False)

longform_df = pd.DataFrame([vars(longform) for longform in longform_info])
print(longform_df)
longform_df.to_csv('longform_vido_data.csv', index=False)


# Bubble Sort
# Copies the dataframe to avoid making changes to the original
video_df_copy = video_df.copy()
rows_to_sort = video_df_copy.to_dict('records')
# Apply Bubble sort, and record time taken to sort
start_time = time.time()
sorted_dataframe = bubble_sort(rows_to_sort)
end_time = time.time()
print('Time taken for bubble sort: {}'.format(end_time - start_time))


# Merge Sort
# Copies the dataframe to avoid making changes to the original
video_df_copy = video_df.copy()
rows_to_sort = video_df_copy.to_dict('records')
# Apply Bubble sort, and record time taken to sort
start_time = time.time()
sorted_dataframe = merge_sort(rows_to_sort)
end_time = time.time()
print('Time taken for merge sort: {}'.format(end_time - start_time))

# Default Sorting Algorithm

# Copies the dataframe to avoid making changes to the original
video_df_copy = video_df.copy()
rows_to_sort = video_df_copy.to_dict('records')

# Apply Bubble sort, and record time taken to sort
start_time = time.time()
sorted_dataframe = sorted(rows_to_sort, key=lambda x: x['likeRatio'])
end_time = time.time()

print('Time taken for Python Sorting Algorithm: {}\n'.format(end_time - start_time))


# Searching
column_name = 'title'
target_value = 'LLM Bootcamp testimonial by an AI and ML expert'

# Linear Search
start_time = time.time()
index = linear_search(video_df, column_name, target_value)
end_time = time.time()
if index != -1:
    print(f"Found: {target_value} at index {index}")
    print('Time taken for Linear Search: {}\n'.format(end_time - start_time))
else:
    print(f"{target_value} not found\n")

# Binary Search
start_time = time.time()
index = binary_search(video_df, column_name, target_value)
end_time = time.time()

# Different index returned, because dataset is sorted first
if index != -1:
    print(f"Found: {target_value} at index {index}")
    print('Time taken for Binary Search: {}\n'.format(end_time - start_time))
else:
    print(f"{target_value} not found\n")


# Visualisation: Add Variety

# Bubble Chart, shows optimal length to gain maximum views (Shows Audience Preferences, Engagement Levels)
sns.scatterplot(data=video_df, x="durationSecs", y="viewCount", size="viewCount", sizes=(20, 2000))
plt.title('Bubble Chart of Video Duration vs. Views')
plt.show()

# Drop Columns
# PublishAt