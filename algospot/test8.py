order = [1, 2, 4]
t = int(input())

results = []
for i in range(0, t):
    n = int(input())
    results.append(n)

index = 4
while index < 12:
    next_value = sum(order[index - 4: ])
    order.append(next_value)
    index += 1

for i in range(0, t):
    print(order[results[i] - 1])