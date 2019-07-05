"""import sys

sys.setrecursionlimit(10000)

def DPS(coins, deep, target, result, start):
    if deep == target:
        result[0] += 1
        return
    if deep > target: return

    for i in range(start, len(coins)):
        DPS(coins, deep + coins[i], target, result, i)

    return

if __name__ == '__main__':
    t = int(input())
    may = 1000000007
    results = []
    for i in range(t):
        coins = []
        result = [0]
        target, n = map(int, input().split(' '))
        temp = input().split(' ')
        for j in temp:
            coins.append(int(j))

        DPS(coins, 0, target, result, 0)
        temp = result[0] % may
        results.append(temp)

    for i in results:
        print(i)
"""
# 동전으로 만들 수 있는 방법의 수 를 모두 메모이제이션 후 누적하여 가산
if __name__ == '__main__':
    t = int(input())
    may = 1000000007
    results = []
    for i in range(t):
        coins = []
        target, n = map(int, input().split(' '))
        temp = input().split(' ')
        for j in temp:
            coins.append(int(j))

        coins.sort()
        count = [0 for j in range(target + 1)]

        count[0] = 1
        for index in range(n):
            for value in range(coins[index], target + 1):
                count[value] += count[value - coins[index]]

                if count[value] > may:
                    count[value] -= may

        results.append(count[target])

    for result in results:
        print(result)