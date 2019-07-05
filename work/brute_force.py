def func(x, y, cache, matrix_sizes):
    if x == y: return 0
    if cache[x][y] != -1: return cache[x][y]
    cache[x][y] = 100000007
    for i in range(x, y):
        cache[x][y] = min(cache[x][y], func(x, i, cache, matrix_sizes) +
                          func(i + 1, y, cache, matrix_sizes) +
                          matrix_sizes[x][0] * matrix_sizes[i][1] * matrix_sizes[y][1])

    return cache[x][y]


def solution(matrix_sizes):
    answer = 0

    n = len(matrix_sizes)

    cache = [[-1 for i in range(501)] for j in range(501)]
    answer = func(0, n - 1, cache, matrix_sizes)

    return answer

if __name__ == '__main__':
    print(solution([[5, 3], [3, 10], [10, 6]]))