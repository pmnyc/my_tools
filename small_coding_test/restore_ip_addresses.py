"""
Given a string containing only digits, restore it by returning all possible
valid IP address combinations.

For example:
Given "25525511135",

return ["255.255.11.135", "255.255.111.35"]. (Order does not matter)
"""

def isvaliddigits(x, ip_digit_range):
    # x = '000'
    # x = '0'
    # x = '01'
    # x = '101'
    int_x = int(x)
    if int_x > ip_digit_range[1]:
        return False
    else:
        if str(int_x) == x:
            return True
        else:
            return False

def restoreIpAddresses(a, ip_digit_range = [0, 256]):
    n = len(a)
    queue = []
    each_select_length = range(1,len(str(ip_digit_range[1]))+1)
    for len_1 in each_select_length:
        digit1 = a[:len_1]
        if isvaliddigits(digit1,ip_digit_range):
            for len_2 in each_select_length:
                if len_1 +len_2 <= n-2:
                    digit2 = a[len_1:len_1+len_2]
                    if isvaliddigits(digit2,ip_digit_range):
                        for len_3 in each_select_length:
                            if len_1 +len_2 +len_3<= n-1:
                                digit3 = a[len_1+len_2:len_1+len_2+len_3]
                                if isvaliddigits(digit3,ip_digit_range):
                                    len_4 = n -(len_1+len_2+len_3)
                                    if len_4 in each_select_length:
                                        digit4 = a[len_1+len_2+len_3:len_1+len_2+len_3+len_4]
                                        if isvaliddigits(digit4,ip_digit_range):
                                            single_ip = ".".join([digit1,digit2,digit3,digit4])
                                            queue += [single_ip]
    return queue
    

a = "25525511135"
b = "010010"
print(restoreIpAddresses(a))
print(restoreIpAddresses(b))


####### Solution #2

def isvaliddigits(x, ip_digit_range=[0, 256]):
    # x = '000'
    # x = '0'
    # x = '01'
    # x = '101'
    try:
        int_x = int(x)
    except:
        return False
    if int_x > ip_digit_range[1]:
        return False
    else:
        if str(int_x) == x:
            return True
        else:
            return False

def restoreIpAddresses(candidates, cand=[], res=[]):
    # cand = ['12','34'] of []
    # candidates = '5678'
    # res =['0.0.0.0'] of []
    if len(cand) == 4:
        res = res
    elif len(cand)==3:
        if isvaliddigits(candidates):
            ip_array = cand + [candidates]
            ip = ".".join(ip_array)
            if ip not in res:
                res.append(ip)
    else:
        for len_ in range(1,min(4,len(candidates)+1)):
            cand_new = cand + [candidates[:len_]]
            candidates_new = candidates[len_:]
            if isvaliddigits(candidates[:len_]):
                res_seq = restoreIpAddresses(candidates_new, cand_new, res)
                for r in res_seq:
                    if r not in res:
                        res.append(r)
    return res

a = "25525511135"
b = "010010"
print(restoreIpAddresses(a,[],[]))
print(restoreIpAddresses(b,[],[]))
