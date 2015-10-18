"""
Write a program to check whether a given number is an ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5.
For example, 6, 8 are ugly while 14 is not ugly since it includes another
prime factor 7.

Note that 1 is typically treated as an ugly number.
"""


def checkPrime(primes, num):
    res = -1
    for p in primes:
        if num % p == 0:
            res = p
            break
    return res

def checkUglyNum(num):
    if num <= 1:
        return True
    else:
        primes = [2,3,5]
        candprime = 2
        while candprime > 0:
            candprime = checkPrime(primes, num)
            if candprime >0:
                num = num / candprime
    if num == 1:
        return True
    else:
        return False

num = 14
checkUglyNum(8)

