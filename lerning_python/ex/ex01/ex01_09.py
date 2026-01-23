num = input('4桁の正の整数を入力：')
num = int(num)
n0 = num % 10
n1 = int(num / 10) % 10
n2 = int(num / 100) % 10
n3 = int(num / 1000)

print(n3)
print(n2)
print(n1)
print(n0)