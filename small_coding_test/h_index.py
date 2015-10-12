"""
Given an array of citations (each citation is a non-negative integer) of a
researcher, write a function to compute the researcher's h-index.

According to the definition of h-index on Wikipedia: "A scientist has index h
if h of his/her N papers have at least h citations each, and the other N - h
papers have no more than h citations each."

For example, given citations = [3, 0, 6, 1, 5], which means the researcher has
5 papers in total and each of them had received 3, 0, 6, 1, 5 citations
respectively. Since the researcher has 3 papers with at least 3 citations each
and the remaining two with no more than 3 citations each, his h-index is 3.

Note: If there are several possible values for h, the maximum one is taken as
the h-index.

[6, 5, 3, 1, 0]
"""

citations = [6, 5, 3, 4, 0]



import os, sys
import numpy as np


class Solution(object):
    def getHindex(self, citations):
        n_citation = len(citations)
        hit_ind = 0
        for h in map(lambda x: n_citation - x, range(n_citation+1)):
            n_papers_at_h = len(filter(lambda x: x >= h, citations))
            if n_papers_at_h >= h:
                hit_ind += 1
                break

        if hit_ind == 0:
            h_index = 0
        else:
            h_index = h
        return h_index

citations = [6, 5, 3, 1, 0]
Solution().getHindex(citations)
