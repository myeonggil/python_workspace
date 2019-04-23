def solution(scoville, K):
    answer = 0
    avg = 0
    flag = False
    sco_len = len(scoville)

    if scoville[0] * pow(2, sco_len) - 1 < K:
        answer = -1
    else:
        while avg != K:
            if min(scoville) < K:
                flag = False
            else:
                avg = K

            if flag == False:
                flag = True
                very_small = min(scoville)
                scoville.remove(very_small)
                small = min(scoville)
                scoville.remove(small)
                result = very_small + (small * 2)
                scoville.insert(0, result)
                answer += 1
                if len(scoville) == 1:
                    if scoville[0] < K:
                        answer = -1
                        break

    return answer