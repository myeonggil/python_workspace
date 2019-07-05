def match(w, s):
    pos = 0
    while (pos < len(w) and pos < len(s)) and \
        ((w[pos] == '?') or (w[pos] == s[pos])):
        pos += 1

    if pos == len(w):
        return pos == len(s)

    if w[pos] == '*':
        for skip in range(0, len(s) - pos + 1):
            if match(w[pos + 1: ], s[pos + skip: ]):
                return True

    return False

test_case = int(input())
for t in range(0, test_case):
    str1 = input()
    n = int(input())
    for i in range(0, n):
        str2 = input()
        print(match(str1, str2))