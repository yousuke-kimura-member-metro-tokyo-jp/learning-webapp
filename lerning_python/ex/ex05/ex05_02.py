def check_prime(n):
    isPrime = True

    for i in range(2, int(n) - 1):
        if (int(n) % i == 0):
            isPrime = False

    return isPrime

while (True):
    n = input("自然数を入力 or \"quit\" : ")
    if (n == "quit"): break

    if check_prime(n):
        print("素数だ")
    else:
        print("素数ではない")
