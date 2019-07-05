x, y = map(int, input().split(' '))
data = [[0] * y for _ in range(x)]
for i in range(x):
    temp = input()
    for j in range(y):
        data[i][j] = int(temp[j])
# print(data)
visit = [[0] * y for _ in range(x)]

# right, left, down, up
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

# bfs
arr = []
arr.append((0, 0))
visit[0][0] = 1
while arr:
    a, b = arr.pop(0)
    if a == x - 1 and b == y - 1:
        print(visit[a][b])
        break
    for i in range(4):
        ax = a + dx[i]
        ay = b + dy[i]
        if ax >= 0 and ax < x and ay >= 0 and ay < y:
            if visit[ax][ay] == 0 and data[ax][ay] == 1:
                visit[ax][ay] = visit[a][b] + 1
                arr.append((ax, ay))