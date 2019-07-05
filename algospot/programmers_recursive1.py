
def recursive(cookie, l, m, r, results):
    if l > len(cookie) or m > len(cookie) or r > len(cookie): return 0
    sum1 = sum(cookie[l: m])
    sum2 = sum(cookie[m: r])
    if sum1 == sum2:
        results.append(sum1)
        return 0

    recursive(cookie, l, m, r + 1, results)
    recursive(cookie, l, m + 1, r, results)
    recursive(cookie, l + 1, m, r, results)


    return 0

def solution(cookie):
    answer = 0
    l = 0
    m = 1
    r = 2
    results = []
    recursive(cookie, l, m, r, results)

    if len(results) == 0:
        answer = 0
    else:
        answer = max(results)

    return answer

if __name__ == '__main__':
    datas = [[1, 1, 2, 3], [1, 2, 4, 5]]
    for data in datas:
        a = solution(data)
        print(a)