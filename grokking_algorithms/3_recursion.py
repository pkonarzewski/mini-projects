"""
Recursion.
Rekurencja.
"""

def factorial(x):
    """Factorial of x."""
    if x == 1:
        return 1
    else:
        return x * factorial(x-1)


assert factorial(1) == 1
assert factorial(5) == 120
