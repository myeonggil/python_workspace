

INF = 987654321;
# A[]: 양자화해야 할 수열, 정렬한상태
# pSum[]: A[]의부분합을저장, pSum[i]는A[0]..A[i]의합
# pSqSum[]: A[]제곱의부분합을저장.pSqSum[i]는A[0] ^ 2..A[i] ^ 2의합

pSum = [0 for i in range(0, 101)]
pSqSum = [0 for i in range(0, 101)]
# A를정렬하고각부분합을계산

def precalc(n):
    A = []
    values = input().split(' ')

    for value in values:
        A.append(int(value))

    A = sorted(A)

    pSum[0] = A[0]
    pSqSum[0] = A[0] * A[0]

    for i in range(1, n):
        pSum[i] = pSum[i - 1] + A[i]
        pSqSum[i] = pSqSum[i - 1] + A[i] * A[i]

    print(pSum)
    print(pSqSum)

# A[lo]..A[hi]구간을 하나의 숫자로 표현 할 때 최소오차합을 계산

def minError(lo, hi):
    # 부분합을 이용해 A[lo] ~ A[hi]까지의 합을 구함
    sums = 0
    spSum = 0
    if lo == 0:
        sums = pSum[hi]
        sqSum = pSqSum[hi]
    else:
        sums = pSum[hi] - pSum[lo - 1]
        sqSum = pSqSum[hi] - pSqSum[lo - 1]

    # 평균을반올림한값으로이수들을표현
    m = int(0.5 + (float)(sums / (hi - lo + 1)))
    # sums(A[i] - m) ^ 2를전개한결과를부분합으로표현

    ret = sqSum - 2 * m * sums + m * m * (hi - lo + 1)
    print(ret)


    return ret;

global cache

def quantize(froms, parts, n):
    # 기저사례: 모든 숫자를 다 양자화했을 때
    if (froms == n): return 0
    # 기저사례: 숫자는 아직 남았는데 더 묶을 수 없을 때 아주 큰 값을 반환
    if (parts == 0): return INF
    if cache[froms][parts] != -1:
        return cache[froms][parts]

    cache[froms][parts] = INF
    # 조각의 길이를 변화시켜가며 최소치를 찾음

    for partSize in range(1, n - froms + 1):
        cache[froms][parts] = min(cache[froms][parts], minError(froms, froms + partSize - 1) + quantize(froms + partSize, parts - 1, n))

    return cache[froms][parts]

if __name__ == '__main__':
    t = int(input())
    for i in range(0, t):
        cache = [[-1 for i in range(0, 11)] for j in range(0, 101)]
        n, parts = map(int, input().split(' '))
        precalc(n)
        print(quantize(0, parts, n))