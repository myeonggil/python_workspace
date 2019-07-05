n = int(input())
match = {'%20': ' ^', '%21': '!^', '%24': '$^', '%25': '%^', '%28': '(^', '%29': ')^', '%2a': '*^'}

results = []
for i in range(n):
    sentence = input()
    for key, value in match.items():
        sentence = sentence.replace(key, value)

    sentence = sentence.replace('^', '')
    results.append(sentence)

for result in results:
    print(result)