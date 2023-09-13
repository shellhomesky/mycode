import math

for i in range(1, 101):
    a = i
    for j in range(i, 100):
        b = j
        c = math.sqrt(a ** 2 + b ** 2)
        for k in range(j, 100):
            if k == c:
                c = round(c)
                print('{},{},{}'.format(a, b, c))
                print(1)
