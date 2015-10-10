"""
Mix Sort

Question: Given a string "eacxzqa02b721", give the output that orders the letters and numbers separated
    at the positions of this string originally for letter or number.

Lessons:
1) String's certain position can not be replaced directly, needs to convert to list then "".join() to convert
    back
2) string.sort() replaces string directly, a=b.sort() IS INVALID !!!
3) list(string) is to separate the strings into list for better manipulation.
"""
class Solution:
    def orderXbytype(x):
        letters_idx = filter(lambda i: x[i].isalpha(), range(len(x)))
        num_idx = filter(lambda i: x[i].isdigit(), range(len(x)))
        space_idx = filter(lambda i: x[i].isspace(), range(len(x)))
        
        def sortbyidx(x, idx):
            x2=map(lambda i: x[i], idx)
            x2.sort()
            return x2
        
        letters_ = sortbyidx(x, letters_idx)
        numbers_ = sortbyidx(x, num_idx)
        
        x_new = [' '] * len(x)
        
        for i in range(len(letters_)):
            x_new[letters_idx[i]] = letters_[i]
        for i in range(len(numbers_)):
            x_new[num_idx[i]] = numbers_[i]
        return "".join(x_new)


if __name__ == '__main__':
    import sys
    stdinput = sys.argv[1]
    print "typed in "+stdinput
    print "Ouptut is "+Solution().orderXbytype(stdinput)
