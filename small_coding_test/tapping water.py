"""
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
    compute how much water it is able to trap after raining.

For example, 
Given [0,1,0,2,1,0,1,3,2,1,2,1], return 6.

https://leetcode.com/problems/trapping-rain-water/
"""




def reversearray(a):
    n = len(a)
    index = range(n)
    index_reverse = map(lambda i: n-1-i, index)
    return map(lambda i: a[i], index_reverse)

def getWaterArea(a):
    queue = []
    area_queue = []
    
    
    for ii in range(len(a)):
        if len(queue) == 0:
            start =0
        else:
            start = queue[-1][1]
        area = 0
        for j in range(start+1, len(a)):
            if a[j] < a[start]:
                area += a[start] - a[j]
                end = j
                continue
            else:
                end = j
                break
        queue += [[start, end]]
        if end == len(a)-1:
            area = 0
            endarray = a[start:end+1]
            endarray = reversearray(endarray)
            for id in range(len(endarray)-1):
                start = id
                if endarray[id] > endarray[id+1]:
                    start = id
                    break
            endarray = endarray[start:]
            if endarray[0] < endarray[-1]:
                endarray[-1] = endarray[0]
            else:
                endarray[0] = endarray[-1]
            for id in range(1,len(endarray)):
                area += max(0, endarray[id-1] - endarray[id])
        area_queue += [area]
        if end == len(a)-1:
            break
    
    return sum(area_queue)

a = [0,1,0,2,1,0,1,3,2,1,2,1]
getWaterArea(a)