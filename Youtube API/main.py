# Google API
from googleapiclient.discovery import build
# Importing Classes
from youtube_channel import YoutubeChannel
from youtube_video import YoutubeVideo
from shorts import YoutubeShorts
from longform import YoutubeLongForm
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
def bubble_sort(array):
    # Determine the number of elements in the array
    items = len(array)
    # Outer loops for each item or element in the array
    for count in range(items):
        # Inner loop compares adjacent items (items next to each other)
        for index in range(0, items - count - 1):
            # 1 is subtracted to ensure that no comparison is made out of bounds, and count increases efficiency as the sorted items are not resorted
            # Checks if the current item is bigger than the one next to it, if they are they swap positions.
            if array[index]['likeRatio'] > array[index + 1]['likeRatio']:
                array[index], array[index + 1] = array[index + 1], array[index]
    # Sorted array is returned
    return array


'''
- Takes the length of the array
'''
# Copies the dataframe to avoid making changes to the original
video_df_copy = video_df.copy()
rows_to_sort = video_df_copy.to_dict('records')

# Apply Bubble sort, and record time taken to sort
start_time = time.time()
sorted_dataframe = bubble_sort(rows_to_sort)
end_time = time.time()

print('Time taken for bubble sort: {}'.format(end_time - start_time))

'''
Best Case Scenario:
- Already Sorted, and hence only need to make a single pass or run through to ensure that it is sorted. 
  The time complexity would be O(n) where n is the number of elements. Therefore 5062 operations for 5062 rows.
Worst Case Scenario:
- The worst case would be that the data is in reverse order, and therefore would it would pass through all 5062 items, 
  only filtering one item towards the back, which give it a complexity of O(n^2), where n is the number of elements
  hence 25,65,562 operations (5062^2). As it iterate through 5062 items, 5062 times and sort 1 item in each iteration.
  The exact time complexity would be n(n-1), as with each iteration, one less step is required.
'''


# Merge Sort
def merge_sort(array):
    if len(array) > 1:
        left_array = array[:len(array) // 2]
        right_array = array[len(array) // 2:]

        # Recursion
        merge_sort(left_array)
        merge_sort(right_array)

        # Merge
        i = 0  # Left Array Index
        j = 0  # Right Array Index
        k = 0  # Merged Array Index

        while i < len(left_array) and j < len(right_array):  # Loops until all items are processed
            if left_array[i]['likeRatio'] < right_array[j]['likeRatio']:
                '''
                Checks whether the current element being compared is in right or left array which is appended to main array
                '''
                array[k] = left_array[i]
                i += 1
                '''
                Index is incremented so that now, for example the second element of left array will be checked against the first element of the right array
                '''
            else:
                array[k] = right_array[j]
                j += 1
            k += 1
        while i < len(left_array):  # Loop runs until all elements from this left array has been processed
            array[k] = left_array[
                i]  # Assigns current element in the left array to the current position of the array being merged
            i += 1
            k += 1

        while j < len(right_array):  # Loop runs until all elements from the right aray has been processed.
            array[k] = right_array[j]
            j += 1
            k += 1

    return array


'''
- Pass an array through the function to sort it, utilizes divide and conquer principle
- Splits array into 2, a left array and then right array containing the left and right half of the data
- This process repeats recursively until split the array in half until we are left with individual items whith a size of 1
- At the most fundamental level, each item represents either a left or right sub array. These left and right subarrays will be
  sorted and merged into a sub-array of size 2 which again is either a left or right subarray. This process repeats recursively until
  until we are left with the original array in which they came from and it's sorted.
  
In Practice, the array is spit in half,it then continunally splits then sorts left side of the array, until your are left with a sorted left array.
Solves one branch first, then sorts the other, in this case the right array is then sorted and merged after the left half is completely sorted

'''

# Copies the dataframe to avoid making changes to the original
video_df_copy = video_df.copy()
rows_to_sort = video_df_copy.to_dict('records')

# Apply Bubble sort, and record time taken to sort
start_time = time.time()
sorted_dataframe = merge_sort(rows_to_sort)
end_time = time.time()

print('Time taken for merge sort: {}'.format(end_time - start_time))

'''
Best Case Scenario = Worst Case Scenario
- In all cases merge maintains a time complexity of O(n log n) where n is the number of elements,
  because the algorithm still needs to the divide the array into halves, sort right and left half
  then merge them together. This would take O(5062 log 5062), which results to roughly 62,000 operations. (Base 2)
'''

'''
Verdict, Bubble Sort is considerably faster for shorter datasets because it can sort with a single check in a best case scenario
unlike Merge Sort which still maintains n log n steps, as oppose to O(n) but as the dataset increases in size or maybe be reversed,
Merge Sort maintains O(n log n), while Bubble Sort now takes O(n^2) which is considerable slower 62,000 >>> 25,65,562.
'''

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

# Linear Search
def linear_search(df, column_name, target_value):
    for location, value in df.iterrows():
        if value[column_name] == target_value:
            return location  # Returns the index of where the value was found
    return 'Could not find the target value {}'.format(target_value)


'''
Example Test Values: 
- LLM Bootcamp testimonial by an AI and ML expert 
- Time Management- How Do I Efficiently Manage My Time?  My Experience- Motivation
- Install your favorite Windows app on M1 Mac - ft. Parallels
'''

column_name = 'title'
target_value = 'LLM Bootcamp testimonial by an AI and ML expert'
start_time = time.time()
index = linear_search(video_df, column_name, target_value)
end_time = time.time()
if index != -1:
    print(f"Found: {target_value} at index {index}")
    print('Time taken for Linear Search: {}\n'.format(end_time - start_time))
else:
    print(f"{target_value} not found\n")

'''
Best Case Scenario:
- The first element of the array is the desired value, which means it would take a single step and therefore a time complexity
  of O(1), indicating a single step.
Worst Case Scenario:
- The desired element is at the end of the dataset, which means it would linearly check from first to last element meaning
  it would take 5062 steps, with a time complexity of O(n).
'''


# Binary Search

def binary_search(df, column_name, target_value):
    sorted_df = df.sort_values(by=column_name)  # Sorts the dataset, so that it can upper and lower half correctly

    # Reset the index, to ensure the data is in the correct order, and it's continous
    sorted_df.reset_index(drop=True, inplace=True)

    low = 0
    high = len(sorted_df) - 1

    while low <= high:
        middle = (low + high) // 2
        middle_value = sorted_df.at[middle, column_name]

        if middle_value == target_value:
            return middle
        elif middle_value < target_value:
            low = middle + 1
        else:
            high = middle - 1
    return -1


start_time = time.time()
index = binary_search(video_df, column_name, target_value)
end_time = time.time()

# Different index returned, because dataset is sorted first
if index != -1:
    print(f"Found: {target_value} at index {index}")
    print('Time taken for Binary Search: {}\n'.format(end_time - start_time))
else:
    print(f"{target_value} not found\n")

'''
Best Case Scenario:
- The desired element is right in the middle of the array or dataset, which means it would take a single step, with
  a time complexity of O(1) meaning it would take a single step.
Worst Case Scenario:
- The desired element is at the very beginning or end of the dataset, requiring it to iterate through the loop,
  the maximum amount of times, as it would need to continuously take halves, until it reaches the first or last 2 elements.
  This would take a time complexity of O(log n), which means it would approximate 12 steps (Base 2)
'''

'''
Verdict:
- Binary search is better search algorithm, because the best case scenario is equal to linear search,
  which is a single step, and the worst case is significantly better as well, because the worst case is
  O(log n) is faster than O(n), which is roughly 12 > 5062.
'''

# Visualisation: Add Variety

'''
sns.violinplot(data=video_df, x="viewCount", y="commentCount")
plt.show()
'''

# Recursion
# Fix TagCount and PublishedAt



