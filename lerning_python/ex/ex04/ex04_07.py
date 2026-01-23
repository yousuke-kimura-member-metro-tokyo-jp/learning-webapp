for i in range(4):
  for j in range(3 - i):
    print(' ', end='')

  for j in range(i+1):
    print(i+1, end='')
  
  print('')


for i in range(4):
  for j in range(i):
    print(' ', end='')

  for j in range(4-i):
    print(i+1, end='')
  
  print('')