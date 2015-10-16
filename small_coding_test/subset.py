"""
Subsets:

Given a set of distinct integers, S, return all possible subsets.

Note:
Elements in a subset must be in non-descending order.
The solution set must not contain duplicate subsets.

For example,
If S = [1,2,3], a solution is:
"""


def subset(candidates, res=[[]]):
    if len(candidates) == 0:
        res = res
    elif len(candidates) <= 2:
        if candidates not in res:
            res.append(candidates)
        for r in candidates:
            if [r] not in res:
                res.append([r])
    else:
        if candidates not in res:
            res.append(candidates)
        for i, num in enumerate(candidates):
            if [num] not in res:
                res.append([num])
            candidates_new = candidates[:i] + candidates[i+1:]
            res_seq = subset(candidates_new, res)
            for r in res_seq:
                if r not in res:
                    res.append(r)
    return res


S = [1,2,3]
subset(S)
