"""
Divide and Conquer.
Dziel i rzadz.
"""


def summ(arr):
    """Sum array using recursion."""
    if len(arr) == 0:
        return 0
    else:
        return arr[0] + summ(arr[1:])


assert summ([1, 4, 3, 4, 1]) == 13


def countt(arr):
    """Count elements in a array."""
    if len(arr) == 1:
        return 1
    else:
        return 1 + countt(arr[1:])

assert countt([1, 5, 3, 2, 2]) == 5


def maxx(arr):
    """Biggest element in a array."""
    if len(arr) == 1:
        return arr[0]
    else:
        xn = maxx(arr[1:])
        if arr[0] > xn:
            return arr[0]
        else:
            return xn

assert maxx([10, 5, 2, 7, 1]) == 10
