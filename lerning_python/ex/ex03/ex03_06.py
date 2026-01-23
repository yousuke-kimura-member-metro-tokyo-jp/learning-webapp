n0 = int(input('整数1 :'))
n1 = int(input('整数2 :'))
n2 = int(input('整数3 :'))

if (n0 > n1 and n0 > n2):
  print(n0)
elif (n1 > n0 and n1 > n2):
  print(n1)
else:
  print(n2)
