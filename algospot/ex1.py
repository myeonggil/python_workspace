import sys
global cache

def function(sums1, sums2, travel, limit, now):
    now += 1
    if now == len(travel): return
    for i in range(1, 4, 2):
        if sums2 + travel[now][i - 1] > limit:
            if sums1 > cache[0]:
                cache[0] = sums1
        if now == len(travel) - 1:
            if sums2 + travel[now][i - 1] <= limit:
                if sums1 + travel[now][i] > cache[0]:
                    cache[0] = sums1 + travel[now][i]
            else:
                if sums1 > cache[0]:
                    cache[0] = sums1
        function(sums1 + travel[now][i], sums2 + travel[now][i - 1], travel, limit, now)

N = int(input())
results = []
for i in range(0, N):
    lens, limit = map(int, sys.stdin.readline().split(' '))
    travel = []
    cache = [0]
    for j in range(0, lens):
        a, b, c, d = map(int, sys.stdin.readline().split(' '))
        travel.append([a, b, c, d])

    travel = sorted(travel, key=lambda x: x[1] + x[3], reverse=True)

    """for j in range(0, lens):
        a, b, c, d = map(int, sys.stdin.readline().split(' '))
        travel.append(a)
        travel.append(b)
        travel.append(c)
        travel.append(d)"""

    temp_time = 0
    temp_value = 0
    for j in range(0, lens):
        max_value = max(travel[j][1], travel[j][3])
        max_index = travel[j].index(max_value)
        if temp_time + travel[j][max_index - 1] <= limit:
            temp_time += travel[j][max_index - 1]
            temp_value += travel[j][max_index]
        else:
            temp_time += travel[j][4 - max_index - 1]
            temp_value += travel[j][4 - max_index]

    results.append(temp_value)
    # function(0, 0, travel, limit, -1)
    # results.append(cache[0])

for result in results:
    print(result)