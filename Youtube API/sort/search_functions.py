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


# Search
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