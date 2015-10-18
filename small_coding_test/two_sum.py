
"""
Two Sum

Given an array of integers, find two numbers such that they add up to a specific target number.
The function twoSum should return indices of the two numbers such that they add up to the target, 
where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution.

Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
"""

numbers = [2,7,11,15]
target = 9


for i in range(len(numbers)-1):
    for j in range(1,len(numbers)):
        if sum([numbers[i],numbers[j]]) == target:
            index1 = i+1
            index2 = j+1
            break

print("Output: index1=%s, index2=%s" %(str(index1), str(index2)))
