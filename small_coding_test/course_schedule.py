"""
There are a total of n courses you have to take, labeled from 0 to n - 1.
Some courses may have prerequisites, for example to take course 0 you have to
first take course 1, which is expressed as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, is it
possible for you to finish all courses?

This is only to return the result whether it is possible or not to finish the 
    coureses

For example:
2, [[1,0]]
There are a total of 2 courses to take. To take course 1 you should have
finished course 0. So it is possible.

2, [[1,0],[0,1]]
There are a total of 2 courses to take. To take course 1 you should have
finished course 0, and to take course 0 you should also have finished course
1. So it is impossible.

Lessons:
1) To avoid forming a loop, [1,2],[2,3],[3,1]
2) When dealing with graphs, one needs to build queues for looping each node
"""

import os, sys
import numpy as np 


numCourses=3
prerequisites=  [[1, 0], [0, 1]]

class Solution(object):
    """
    #This is just for handling single case when a-b-c-a, no duplicate
    def canFinish(self, numCourses, prerequisites):
        visited = []
        res = True
        if len(prerequisites) > 0:
            for node in prerequisites:
                if node in visited:
                    continue
                else:
                    if [node[1],node[0]] in prerequisites:
                        res = False
                        visited.append(node)
                        break
        return res
    """

    def canFinish(self, numCourses, prerequisites):
        looped_queue = []
        res = True
        if len(prerequisites) > 0:
            startingpoint = map(lambda x: x[0], prerequisites)
            for nodeid in range(len(prerequisites)-1):
                singlequeue = prerequisites[nodeid]
                for j in range(nodeid+1,len(prerequisites)):
                    if prerequisites[j][0] in singlequeue:
                        singlequeue.append(prerequisites[j][1])
                        if len(singlequeue) > len(set(singlequeue)):
                            looped_queue.append(singlequeue)
                            if len(looped_queue) > 0:
                                break
                if len(looped_queue) > 0:
                    break 
        if len(looped_queue) > 0:
            res = False
            print("The looped queque is %s" %str(looped_queue))
        return res


s = Solution()
print(s.canFinish(1, []))
print(s.canFinish(3, [[1, 0], [0, 1]]))
print(s.canFinish(3, [[1, 0], [0, 2],[2,3]]))

with open('test.txt') as f:
    args = f.read().split()
    arg0 = int(args[0][:-1])
    arg1 = eval(args[1])
    print(s.canFinish(arg0, arg1))