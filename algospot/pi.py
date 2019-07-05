cache = [-1 for i in range(0, 10002)]
INF = 987654321
N = ''
# N[a..b] 구간의 난이도를 반환
def classify(a, b):
    # 숫자 조각을 가져온다
    M = N[a: b + 1]
    # 첫 글자만으로 이루어진 문자열과 같으면 난이도는 1
    if M == (M[0] * len(M)): return 1
    # 등차수열인지 검사
    progressive = True
    for i in range(0, len(M) - 1):
        if int(M[i + 1]) - int(M[i]) != int(M[1]) - int(M[0]):
            progressive = False
    # 등차수열이고 공차가 1 혹은 -1이면 난이도는 2
    if progressive and abs(int(M[1]) - int(M[0])) == 1: return 2
    # 두 수가 번갈아 등장하는지 확인
    alternating = True
    for i in range(0, len(M)):
        if M[i] != M[i % 2]:
            alternating = False
    if alternating: return 4    # 두 수가 번갈아 등장하면 난이도 4
    if progressive: return 5    # 공차가 1 아닌 등차수열의 난이도는 5

    return 10   # 이 외는 모두 난이도 10

def memorize(begin):
    # 기저 사례: 수열의 끝에 도달했을 경우
    if begin == len(N): return 0
    # 메모이제이션
    if cache[begin] != -1: return cache[begin]
    cache[begin] = INF
    for i in range(3, 6):
        if begin + i <= len(N):
            cache[begin] = min(cache[begin], memorize(begin + i) + classify(begin, begin + i - 1))

    return cache[begin]

if __name__ == '__main__':
    test_case = int(input())
    for i in range(0, test_case):
        N = input()
        print(memorize(0))
        cache = [-1 for i in range(0, 10002)]