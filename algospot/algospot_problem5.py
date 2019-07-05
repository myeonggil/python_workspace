n = int(input())
problems = []
results = []

# 완전 탐색
def search(start, remain, pSum, value, before):
    if len(results) != before: return
    if pSum == value:
        results.append('not weird')
        return
    if start == len(remain): return
    if pSum < value: return
    for i in range(start, len(remain)):
        search(i + 1, remain, pSum - remain[i], value, before)

for i in range(n):
    value = int(input())
    remain = [1]
    for j in range(2, int(value / 2) + 1):
        if value % j == 0: remain.append(j)

    pSum = sum(remain)
    before = len(results)
    if pSum > value:
        for i in range(0, len(remain)):
            sentence = search(i, remain, pSum, value, before)
        after = len(results)
        if before == after:
            results.append('weird')
    else:
        results.append('not weird')

for result in results:
    print(result)