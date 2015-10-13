"""
Write a function to find the longest common prefix string amongst an array of
strings.
"""


class Solution(object):
    def longestCommonPrefix(self, strs):
        if len(strs) == 0:
            res = ""
        elif len(strs) == 1:
            res = strs[0]
        else:
            scan_length = len(strs[0])
            res = ""
            for i in range(scan_length):
                letter = strs[0][i]
                try:
                    if len(strs) == sum(map(lambda x: x[i] == letter, strs)):
                        res += letter
                except IndexError:
                    break
        return res


strs = ["abccccce","abc","abcea"]
Solution().longestCommonPrefix(strs)
