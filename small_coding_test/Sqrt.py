"""
Sqrt(x)

Implement int sqrt(int x).
Compute and return the square root of x.
"""


def sqrt(x, error_threshold = 1e-4):
    res=1.0
    error = error_threshold + 1
    while error > error_threshold:
        next_ = 0.5 * (res + (x+0.0)/(res+0.0))
        error = abs(next_ - res)
        res = next_
    return res

x = 10000000
sqrt(x)
