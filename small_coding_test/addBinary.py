"""
Given two binary strings, return their sum (also a binary string).
For example,
a = "11"
b = "1"
Return "100".

Lessons:
1) convert binary to decmial int(x,2), where x HAS TO BE string
"""

import os, sys
import numpy as np 


sum_ = int(a,2) + int(b,2)
binary = bin(sum_)[2:]
print binary