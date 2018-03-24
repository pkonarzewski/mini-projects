"""
Binnary search algorithm.
"""
import math

def binary_search(arr, target):
    """Binary search algorithm."""

    low = 0
    high = len(arr)-1
    mid = 0

    while low <= high:
        mid = math.ceil((high + low)/2)

        if arr[mid] == target:
            return mid
        elif target < arr[mid]:
            high = mid - 1
        elif target > arr[mid]:
            low = mid + 1

    return None

# TEST
print(binary_search([1,2,3,4,5], 3))
print(binary_search([1,2,3,5,6], 4))
