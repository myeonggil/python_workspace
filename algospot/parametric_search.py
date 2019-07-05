
# 높이가 height일 때의 가격
def cal(vec, height, P, Q, n):
    res = 0
    for i in range(n):
        for j in range(n):
            if vec[i][j] - height > 0:
                mul = Q
            else:
                mul = -P
            res += (vec[i][j] - height) * mul

    return res

def solution(land, P, Q):
    n = len(land)
    answer = 100000007

    # 최대 높이 찾기
    s = 0
    e = 300
    m = 0

    # 기울기로 이분 탐색
    while s <= e:
        res = []
        m = int((s + e) / 2)
        res = [cal(land, m, P, Q, n), cal(land, m+1, P, Q, n)]
        if res[0] == res[1]: break

        if res[0] < res[1]:
            e = m - 1
        else:
            s = m + 1

    # 오차가 있을 수 있음
    for i in range(m - 1, m + 2):
        temp = cal(land, i, P, Q, n)
        if answer > temp:
            answer = temp

    return answer

if __name__ == '__main__':
    result = solution([[4, 4, 3], [3, 2, 2], [ 2, 1, 0 ]], 5, 3)
    print(result)