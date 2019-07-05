n = int(input())
numberic = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
            'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}

results = []
operations = []
for i in range(n):
    way = input().split(' ')
    operations.append(str(numberic[way[0]]) + way[1] + str(numberic[way[2]]) + ' ' + way[4])

for operation in operations:
    temp = operation.split(' ')
    result = int(eval(temp[0]))

    if result >= 0 and result <= 10:
        for key, value in numberic.items():
            if value == result:
                result = key
                break

        flag = 'Yes'
        for j in result:
            if result.count(j) != temp[1].count(j):
                flag = 'No'
                break
    else:
        flag = 'No'

    results.append(flag)

for k in results:
    print(k)