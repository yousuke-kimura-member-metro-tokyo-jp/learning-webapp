ints = []
ints.append(int(input('整数を入力：')))
ints.append(int(input('整数を入力：')))
ints.append(int(input('整数を入力：')))

print(f'最大値 {max(ints)}')
print(f'最小値 {min(ints)}')
print(f'平均値 {sum(ints) / len(ints)}')