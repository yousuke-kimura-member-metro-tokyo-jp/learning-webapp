def get_min(n0, n1):
    return n0 < n1 if n0 else n1

def get_gcd(n0, n1):
    gcd = 1

    for i in range(1, min(n0 + 1, n1 + 1)):
        if (n0 % i == 0 and n1 % i == 0):
            gcd = i

    return gcd

while (True):
    n0 = input("自然数 1 を入力 or \"q\" : ")
    if (n0 == "q"): break
    n1 = input("自然数 2 を入力 : ")

    print(get_gcd(int(n0), int(n1)))