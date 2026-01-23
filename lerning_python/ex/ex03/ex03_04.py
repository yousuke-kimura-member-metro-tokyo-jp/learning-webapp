n = int(input('整数を入力（負値可）：'))

if (n < 0 or n > 10):
    print('範囲外です')
elif (n >= 7):
    print('合格です')
else:
    print('不合格です')