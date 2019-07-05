func = []
for i in range(1, 10001):
    temp = str(i)
    sums = i
    for j in temp:
        sums += int(j)

    func.append(sums)
    if i not in func:
        print(i)

print(func)