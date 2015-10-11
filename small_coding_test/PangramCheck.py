"""
Pangram Check

This is to check what are the missing letters for forming Pangram

For example:
x = "A quick brown foz jumps over the dog lazy"
"""

import numpy as np

class Solution(object):
    def checkmissing(self, x):
        allLetters = "abcdefghijklmnopqrstuvwxyz"
        missingletters = filter(lambda t: t not in x, allLetters)
        if len(missingletters) == 0:
            print("The sentence is a pangram")
        else:
            print "The missing letters are %s" %(" ".join(missingletters))

if __name__ == "__main__":
    import sys
    x = sys.argv[1]
    Solution().checkmissing(x)

