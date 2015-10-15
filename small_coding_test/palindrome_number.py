"""
Palindrome Number:
Determine whether an integer is a palindrome. Do this without extra space.
"""

def getLastdigit(x):
    # here , assume x >= 10
    return x % 10

def getFirstdigit(x):
    x_ = x + 0
    counter = 0
    while x_ >= 10:
        x_ = (x_ - (x_ % 10)) / 10
        counter += 1
    # here, the counter=3 means it is of the scale of 10^3
    return x_, counter

class Solution:
    # @return a boolean
    def isPalindrome(self, x):
        if x < 0:
            res = False
        elif x < 10:
            res = True
        else:
            x_ = x+0
            while x_ >= 10:
                first_digit = getFirstdigit(x_)[0]
                scale = getFirstdigit(x_)[1]
                last_digit = getLastdigit(x_)
                if first_digit == last_digit:
                    x_ = (x_ - (last_digit + first_digit * (10 ** scale))) / 10
                    res = True
                else:
                    res = False
                    break
        return res

Solution().isPalindrome(11221)
Solution().isPalindrome(1221)
