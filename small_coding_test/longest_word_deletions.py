
def ispossibleDelete(c, w):
    #check if it is possible to delete a letter
    # c = 'bdca'
    res = False
    for i in range(len(c)):
        c_ = c[:i] + c[i+1:]
        if c_ in w:
            res = True
            break
    return res

def restWords(cand, w):
    if len(cand) == 0:
        res = w
    else:
        smallest_length = min(map(lambda x: len(x), cand))
        res = filter(lambda x: x not in cand and len(x) < smallest_length,w)
        counter=0
        for r in res:
            for c in cand:
                if isPartofword(r, c):
                    counter += 1
                    break
        if counter == 0:
            res = []
    return res

def isPartofword(c1, c2):
    res = False
    if len(c1) == len(c2)-1:
        for i in range(len(c2)):
            c2_new = c2[:i]+c2[i+1:]
            if c2_new == c1:
                res = True
                break
    return res

def isPartofwords(c1, cand):
    res = False
    for c in cand:
        if isPartofword(c1, c):
            res = True
            break
    return res

def nextWord(c, w):
    restwords = restWords([c], w)
    return filter(lambda x: isPartofword(x,c), restwords)

def chains(w, cand, res=[], longest_delete=0):
    # res = [["a","ab",.], []] of [[]]
    # cand = ["bdca","bda"]
    if restWords(cand, w) == []:
        return
    elif len(filter(lambda x: nextWord(x,w)==[],restWords(cand, w))) == len(restWords(cand, w)):
        for i, wd in enumerate(restWords(cand, w)):
            if isPartofwords(wd, cand):
                r = cand + [wd]            
                if r not in res and len(r) >= longest_delete:        
                    res.append(r)
                    longest_delete = len(r)
    else:
        restwords = restWords(cand, w)
        for i, wd in enumerate(restwords):
            if len(cand) == 0:
                cand_new = [wd]
                res_seq = chains(w, cand_new, res, longest_delete)
            elif isPartofwords(wd, cand):
                cand_new = cand + [wd]
                res_seq = chains(w, cand_new, res, longest_delete)
            else:
                continue
            #res_seq = chains(w, cand_new, res, longest_delete)
            if res_seq is not None:
                for r in res_seq:
                    if r not in res and len(r) >= longest_delete:
                        res.append(r)
    return res
                

def longest_chain(w):
    res_seq = chains(w,cand=[])
    max_length = 0
    max_seq=[]
    for r in res_seq:
        if len(r) > max_length:
            max_length = len(r)
            max_seq = r
    print "The longest word change sequence is %s" %str(max_seq)
    return max_length




w = ["a","b","ba","bca","bda","bdc",'bdac','eeeeee']
longest_chain(w)
