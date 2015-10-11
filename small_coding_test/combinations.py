"""
Given two integers n and k, return all possible combinations of k numbers out
of 1 ... n.
For example,
If n = 4 and k = 2, a solution is:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]

Lessons:
1) Add print function in the loop that uses the recursion. Recursion within the loop is a bit tricky, using print helps 
  know what is happening
2) The template works for not knowing how many loops to go.
"""


import os, sys
import numpy as np 

n =4
k =2 

class Solution(object):
  def __init__(self, n, k):
    self.interval = map(lambda x: x+1, range(n))
    self.k = k
    self.res = []

  def getList(self):
      self.findComb(self.interval, [], self.k)

  def findComb(self, interval_, cand, k):
      if k < 0:
          return
      elif k == 0 and cand[:] not in self.res:
          self.res.append(cand[:])
      for i, num in enumerate(interval_):
          cand += [num]
          print(str(cand), str(k)) #this print is very helpful when encoutering the issue with recursion
          self.findComb(interval_[i+1:], cand, self.k-len(cand))
          cand.pop()

### test!
n = 4
k = 2
self = Solution(n,k)
self.getList()
self.res