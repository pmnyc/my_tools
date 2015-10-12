"""
Gas Station

There are N gas stations along a circular route, where the amount of gas at station i is gas[i]. 
You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from station i to its next station (i+1).
You begin the journey with an empty tank at one of the gas stations. 
Return the starting gas station's index if you can travel around the circuit once, otherwise return -1. 

Note:
The solution is guaranteed to be unique.
"""

import os, sys
import numpy as np 

def backindex(i,n):
    if i < 0:
        return i+n
    else:
        return i

class Solution(object):
    def canCompleteCircuit2(self, fuel, cost):
        stations = range(len(fuel))
        n_stations = len(stations)
        fuel_raw = fuel[:]
        res = -999
        if sum(fuel) < sum(cost) or len(stations) < 1:
            res = -1
        else:
            for i in range(n_stations)[3:5]:
                fuel = fuel_raw[:]
                if fuel[i] < cost[i]:
                    continue
                else:
                    index = map(lambda x: (x+i+1) % n_stations,range(n_stations))
                    for j in range(n_stations-1):
                        backindex_ = backindex(index[j]-1,n_stations)
                        fuel[index[j]] += fuel[backindex_] - cost[backindex_]
                        if fuel[index[j]] < cost[index[j]]:
                            res = -1
                        else:
                            continue
                    if res == -999:
                        break
        if res == -1:
            return -1
        if res == -999:
            return i


s = Solution()
fuel = [3, 1, 1, 5, 4 ]
cost = [4, 1, 2, 2, 3 ]
s.canCompleteCircuit2(fuel, cost)
