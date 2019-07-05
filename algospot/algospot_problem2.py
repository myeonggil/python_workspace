n = int(input())
results = []
for i in range(n):
    dic_x = {}
    dic_y = {}
    for j in range(3):
        x, y = map(int, input().split(' '))
        if x not in dic_x:
            dic_x[x] = 1
        else:
            dic_x[x] += 1
        if y not in dic_y:
            dic_y[y] = 1
        else:
            dic_y[y] += 1

    dic_x = sorted(dic_x.items(), key=lambda x: x[1])
    dic_y = sorted(dic_y.items(), key=lambda x: x[1])
    results.append([dic_x[0][0], dic_y[0][0]])

for result in results:
    print(result[0], result[1])


