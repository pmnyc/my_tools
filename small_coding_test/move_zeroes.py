"""
Given an array nums, write a function to move all 0's to the end of it while
maintaining the relative order of the non-zero elements.

For example, given nums = [0, 1, 0, 3, 12], after calling your function, nums
should be [1, 3, 12, 0, 0].

Note:
You must do this in-place without making a copy of the array.
Minimize the total number of operations.
"""

def moveZeros(nums):
    n = len(nums)
    j = 0
    i = 0
    counter = 0
    while i < n-j:
        if nums[i] ==0:
            nums = nums[:i] + nums[i+1:]
            j += 1  #remove a 0 from nums
        else:
            i += 1
        counter += 1
    return nums + [0] * (n-len(nums))

nums = [0, 1, 0, 3, 12]
moveZeros(nums)
