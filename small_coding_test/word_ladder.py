
"""
Given two words (beginWord and endWord), and a dictionary, find the length of
shortest transformation sequence from beginWord to endWord, such that:

Only one letter can be changed at a time
Each intermediate word must exist in the dictionary
For example,

Given:
start = "hit"
end = "cog"
dict = ["hot","dot","dog","lot","log"]
As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
return its length 5.

Note:
Return 0 if there is no such transformation sequence.
All words have the same length.
All words contain only lowercase alphabetic characters.
"""


def areTwoWordsClose(a,b):
    # a = 'hot', b='dot'
    if a == b or len(a) != len(b):
        return False
    else:
        a_ = list(a)
        b_ = list(b)
        counter = 0
        for i in range(len(a_)):
            if counter > 1:
                break
                return False
            else:
                if a_[i] != b_[i]:
                    counter += 1
        if counter == 1:
            return True
        else:
            return False

def diff(list1,list2):
    # this is list1 - list2
    queue = []
    for l1 in list1:
        if l1 not in list2:
            queue += [l1]
    return queue

def getpaths(dic, start, end, cand=[], res=[], minsteps=None):
    # cand = ['hot',''] of []
    # res = [['hot',...], ['big',..]] of [[]]
    if minsteps is None:
        minsteps = len(dic)+2
    if len(cand) == 0:
        cand = [start]
    if len(cand) >= len(dic):
        return
    else:
        left_words = diff(dic, cand)
        onemoreword = False
        for word in left_words:
            if areTwoWordsClose(word, end) and areTwoWordsClose(word, cand[-1]):
                onemoreword = True
                r = cand + [word]
                if len(r) < minsteps and r not in res:
                    res.append(r)
        if not(onemoreword):
            for i, w in enumerate(left_words):
                if areTwoWordsClose(cand[-1], w):
                    cand_new = cand+[w]
                    res_seq = getpaths(dic, start, end, cand_new, res, minsteps)
                    for r in res_seq:
                        if len(r) < minsteps and r not in res:
                            res.append(r)
    return res


def getminipaths(dic, start, end):
    paths = getpaths(dic, start, end)
    paths = map(lambda x: x[1:], paths)
    if len(paths) == 0:
        print "No Such Transformation"
    else:
        minilength = 10**9
        for p in paths:
            print start + " -> " + " -> ".join(p) + " -> " + end

start = "hit"
end = "cog"
dic = ["hot","dot","dog","lot","log"]

getminipaths(dic, start, end)
