from math import gcd

while (True):
    n0 = input("自然数 1 を入力 or \"q\" : ")
    if (n0 == "q"): break
    n1 = input("自然数 2 を入力 : ")

    print(gcd(int(n0), int(n1)))