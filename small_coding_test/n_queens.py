"""
N-Queens

The n-queens puzzle is the problem of placing n queens on an nXn chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle.
"""

class Solution(object):
    def __init__(self,n):
        self.n = n
        grid = [[1] * n] * n
        self.grid = grid
        grid_index=[]
        for i in range(n):
            for j in range(n):
                grid_index.append([i,j])
        self.grid_index = grid_index
        self.conflict_storage = []

    def queenConflict(self, a,b):
        # a =[0,1]
        # b = [1,2]
        if [a,b] in self.conflict_storage:
            return True
        elif (a[0]-a[1]) == (b[0]-b[1]) or sum(a)==sum(b): #diagonal
            self.conflict_storage.append([a,b])
            self.conflict_storage.append([b,a])
            return True
        elif a[0] == b[0] or a[1] == b[1]:
            self.conflict_storage.append([a,b])
            self.conflict_storage.append([b,a])
            return True # being on the same line
        else:
            return False

    def isConflict(self, a, cand):
        # a = [0,1]
        # cand = [[0,1],[2,3]]
        if a in cand:
            return True
        elif [a,sorted(cand)] in self.conflict_storage:
            return True
        elif len(filter(lambda x: self.queenConflict(x,a),cand)) >= 1:
            self.conflict_storage.append([a,sorted(cand)])
            return True
        else:
            return False

    def queensLoc(self, candidates, cand, n, grid_index, res=[]):
        # cand is like [[0,1],[2,3]], of format [[]]
        # candidates is like [[0,1],[2,3]], also [[]]
        # res is of [[[]]]
        # n is the total number of queens we put on board
        n = self.n
        grid_index = self.grid_index
        
        candidates = filter(lambda x: x not in cand and not(self.isConflict(x,cand)), candidates)
       
        if len(candidates) == 0:
            res = res
        elif len(candidates) == 1:
            candidates.sort()
            cand.sort()
            if len(cand) == n-1:
                if len(filter(lambda x: self.queenConflict(candidates[0], x),cand)) == 0:
                    res_ = cand + candidates
                    res_.sort()
                    if res_ not in res:
                        res.append(res_)
            elif len(cand) == n:
                if cand not in res:
                    res.append(cand)
            else:
                res = res
        else:
            candidates.sort()
            cand.sort()
            if len(cand) == n:
                if cand not in res:
                    res.append(cand)
            else:
                for i, c in enumerate(candidates):
                    if not(self.isConflict(c, cand)):
                        cand_new = cand + [c]
                        candidates_new = candidates[:i] + candidates[i+1:]
                        res_seq = self.queensLoc(candidates_new, cand_new, n, grid_index, [])
                        for r in res_seq:
                            r.sort()
                            if r not in res:
                                res.append(r)
        return res
    
    def solve(self):
        res = self.queensLoc(candidates=self.grid_index, cand=[], n=self.n, grid_index=self.grid_index, res=[])
        return res

        
s = Solution(6)
result = s.solve()
