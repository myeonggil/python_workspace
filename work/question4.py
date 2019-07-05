
def parenthesisPairs(n):
    ans = []
    recurse(ans, "", 0, 0, n);

    return ans

def recurse(ans, cur, op, close, n):
    if len(cur) == n * 2:
        ans.append(cur)
        return
    if op < n:
        recurse(ans, cur + "(", op + 1, close, n)
    if close < op:
        recurse(ans, cur + ")", op, close + 1, n)

print(parenthesisPairs(4))