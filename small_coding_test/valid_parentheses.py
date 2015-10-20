"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid
but "(]" and "([)]" are not.
"""


def aretwopair(a,b):
    if a=="(" and b==")":
        return True
    elif a =="[" and b=="]":
        return True
    elif a=="{" and b=="}":
        return True
    else:
        return False

def isValieparen(s):
    left_group = ["[","(","{"]
    right_group = ["]",")","}"]
    s_left_seq = [s+""]
    s_left = s_left_seq[-1]
    continueInd = True
    while continueInd:
        if len(s_left)>=2:
            for i in range(len(s_left)-1):
                if s_left[i] in left_group and s_left[i+1] in right_group:
                    if aretwopair(s_left[i],s_left[i+1]):
                        s_left = s_left[:i]+s_left[i+2:]
                        break
        if s_left_seq[-1] == s_left:
            continueInd = False
        else:
            s_left_seq += [s_left]
            
    if len(s_left) >0:
        return False
    else:
        return True

s = "()(]"
isValieparen(s)
s = "{()[]}"
isValieparen(s)
