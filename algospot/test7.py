n = int(input())
results = []
for i in range(0, n):
    x, y = map(int, input().split(' '))
    results.append([x, y])

def quick_sort(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2][1]
        while low <= high:
            if arr[low][1] == pivot:
                pivot = arr[(low + high) // 2][0]
                while arr[low][0] < pivot:
                    low += 1
                while arr[high][0] > pivot:
                    high -= 1
            else:
                while arr[low][1] < pivot:
                    low += 1
                while arr[high][1] > pivot:
                    high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low

    return sort(0, len(arr) - 1)

quick_sort(results)
"""for i in range(0, n - 1):
    for j in range(i + 1, n):
        if results[i][1] > results[j][1]:
            temp = results[i]
            results[i] = results[j]
            results[j] = temp
        elif results[i][1] == results[j][1]:
            if results[i][0] > results[j][0]:
                temp = results[i]
                results[i] = results[j]
                results[j] = temp"""

"""for i in range(1, n):
    c = i
    while c != 0:
        root = int((c - 1) / 2)
        if results[root][1] < results[c][1]:
            temp = results[root]
            results[root] = results[c]
            results[c] = temp
        elif results[root][1] == results[c][1]:
            if results[root][0] < results[c][0]:
                temp = results[root]
                results[root] = results[c]
                results[c] = temp
        c = root

for i in range(n - 1, -1, -1):
    temp = results[0]
    results[0] = results[i]
    results[i] = temp
    root = 0
    c = 1
    while c < i:
        c = 2 * root + 1
        if c < i - 1 and results[c][1] < results[c + 1][1]:
            c += 1
        elif c < i - 1 and results[c][1] == results[c + 1][1]:
            if c < i - 1 and results[c][0] < results[c + 1][0]:
                c += 1
        if c < i and results[root][1] < results[c][1]:
            temp = results[root]
            results[root] = results[c]
            results[c] = temp
        elif c < i and results[root][1] == results[c][1]:
            if c < i and results[root][0] < results[c][0]:
                temp = results[root]
                results[root] = results[c]
                results[c] = temp
        root = c"""

for x, y in results:
    print(x, y)