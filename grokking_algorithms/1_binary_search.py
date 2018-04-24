"""
Binnary search algorithm.
Wyszukiwanie binarne.
"""
import math

def binary_search(array, target):
    """Binary search algorithm."""

    low = 0
    high = len(array)-1
    mid = 0

    while low <= high:
        mid = math.ceil((high + low)/2)

        if array[mid] == target:
            return mid
        elif target < array[mid]:
            high = mid - 1
        elif target > array[mid]:
            low = mid + 1

    return None

# TEST
assert binary_search([1,2,3,4,5], 3) == 2
assert binary_search([1,2,3,5,6], 4) is None
