from basic_algorithms import *

def branch_and_bound(permutation):
    start_perm = tuple(permutation)
    sorted_perm = tuple(sorted(permutation))
    upper_bound = upper_bound_estimate(permutation)
    
    stack = deque([(start_perm, 0, [])])
    visited = {start_perm: 0}
    n = len(permutation)

    while len(stack) > 0:
        perm, count, reversals = stack.pop()
        num_bp = count_breakpoints(perm)
        lowerbound = math.ceil(num_bp / 2)

        if count + lowerbound >= upper_bound:
            continue

        if perm == sorted_perm:
            upper_bound = count
            print(reversals)
            continue

        candidates = []

        for i in range(n - 1):
            for j in range(i + 1, n):
                new_perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]
                new_num_bp = count_breakpoints(new_perm)
                candidates.append((new_perm, new_num_bp, (i+1, j+1)))

        candidates.sort(key=lambda x: x[1], reverse=True)

        for new_perm, _, reversal in candidates:
            if new_perm not in visited or visited[new_perm] > count + 1:
                visited[new_perm] = count + 1
                stack.append((new_perm, count + 1, reversals + [reversal]))

    return upper_bound


print(branch_and_bound([13,1,3,5,4,7,6,9,10,8,12,11,2,15,16,14,20,18,17,19]))