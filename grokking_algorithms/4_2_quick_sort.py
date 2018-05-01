"""
Quick Sort.
Sortowanie szybkie.
"""

def qsort(arr):
    """Quick sort algorithm."""
    if len(arr) < 2:
        return arr
    else:
        greater = []
        lesser = []
        pivot = arr[0]

        for x in arr[1:]:
            if x >= pivot:
                greater += [x]
            else:
                lesser += [x]

        return qsort(lesser) + [pivot] + qsort(greater)


assert qsort([9, 5, 2, 3, 6, 1, 2]) == [1, 2, 2, 3, 5, 6, 9]
