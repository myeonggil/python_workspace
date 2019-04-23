global cache
global triangle

triangle = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
cache = [[-1 for i in range(0, 100)] for j in range(0, 100)]

def func(x, y, n, triangle):
    if x == n - 1: return triangle[x][y]
    if cache[x][y] != -1: cache[x][y]
    cache[x][y] = max(func(x + 1, y, n, triangle), func(x + 1, y + 1, n, triangle)) + triangle[x][y]
    return cache[x][y]

n = len(triangle)
result = func(0, 0, n, triangle)
print(result)