"""
Distributed Back-Up of Data Centers

DataCopier syncrhonizes data sets between different data centers using minimum copy operations.

3 data centers, each row is the data in the data center, now sync all three data centers

3
5 1 3 4 5 7
2 1 3
1 2

output is:  data --> data_center_id_from --> data-center_id_to

output:
2 3 2
2 3 1
1 1 3
4 1 2
5 1 3
5 3 2
4 2 3
3 1 3
7 1 2
7 1 3

Lessons:
1) Even in class, the staticmethod defined still needs self.method to call it.

"""

import os
import sys
import numpy as np 

class Solution(object):

    @staticmethod
    def getdatafromrow(row):
        #row = "5 1 3 4 5 7"
        return (row.split(" ")[0], row.split(" ")[1:])
    
    @staticmethod
    def checkValueinRow(x,row):
        row_value = self.getdatafromrow(row)[1]
        bl = (x in row_value)
        return bl

    def getAllRawData(self, data):
        x = []
        for row in data:
            x += (self.getdatafromrow(row)[1])
        distinct_values = list(set(x))
        centers = range(numOfCenters)
        for i in centers:
            othercenters = range(numOfCenters)
            missingValues = list(np.setdiff1d(distinct_values, self.getdatafromrow(data[i])[1]))
            othercenters.remove(i)
            if len(missingValues) == 0:
                continue
            else:
                for missvlue in missingValues:
                    for j in othercenters:
                        if missvlue in self.getdatafromrow(data[j])[1]:
                            print (str(missvlue)+" "+str(j+1)+" "+str(i+1))

if __name__ == '__main__':
    numOfCenters = 3
    data = ["5 1 3 4 5 7",
            "2 1 3",
            "1 2"]
    Solution().getAllRawData(data)
    print("done")
