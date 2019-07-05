count = 0
minCount = 9
results = []

def BFS(N, number):
    global count
    global minCount
    global results
    if count >= minCount: return
    if len(results) >= minCount: return
    if len(results) == 0:
        lastNumber = 0
    else:
        lastNumber = results[-1]
    print(results)
    if lastNumber == number:
        minCount = min(count, minCount)
        return minCount

    n = 0
    addCount = 0

    c = 1
    while c <= 10000000:
        addCount += 1
        if count + addCount >= minCount:
            c *= 10
            continue

        n += (N * c)

        count += addCount

        results.append(lastNumber + n)
        BFS(N, number)
        results.pop(-1)

        if lastNumber - n != 0:
            results.append(lastNumber - n)
            BFS(N, number)
            results.pop(-1)

        results.append(lastNumber * n)
        BFS(N, number)
        results.pop(-1)

        if int(lastNumber / n) != 0:
            results.append(int(lastNumber / n))
            BFS(N, number)
            results.pop(-1)

        count -= addCount

        c *= 10

    return


def solution(N, number):
    answer = -1

    BFS(N, number)
    if minCount <= 8:
        answer = minCount

    return answer

solution(5, 12)