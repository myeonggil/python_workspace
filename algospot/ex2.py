import sys
N = int(input())
results = []
for i in range(0, N):
    number = int(input())
    jobs = []
    for j in range(0, number):
        a, b = map(int, sys.stdin.readline().split(' '))
        jobs.append([a, b])

    jobs = sorted(jobs, key=lambda x: x[1])
    count = 1
    end_time = jobs[0][1]
    for j in range(1, len(jobs)):
        if jobs[j][0] >= end_time:
            end_time = jobs[j][1]
            count += 1

    results.append(count)

for result in results:
    print(result)