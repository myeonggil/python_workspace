test_case = int(input())
results = []
answers = []

for t in range(0, test_case):
    results.append([])
    values = input().split(' ')
    # H, W, N = map(int, input().split(' '))
    results[t].append(int(values[0]))
    results[t].append(int(values[1]))
    results[t].append(int(values[2]))

for result in results:
    count = 0
    room = 0
    for i in range(1, result[1] + 1):
        for j in range(1, result[0] + 1):
            count += 1
            if i >= 10:
                room = int(str(j) + str(i))
            else:
                room = int(str(j) + '0' + str(i))
            # print(count)
            if count == result[2]:
                answers.append(room)
                break
        if count == result[2]: break

for answer in answers:
    print(answer)