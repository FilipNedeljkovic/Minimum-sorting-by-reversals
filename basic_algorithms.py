from collections import deque
import math
import random

def bfs(permutation) -> int:
    start_perm = tuple(permutation)
    sorted_perm = tuple(sorted(start_perm))
    visited = {start_perm}
    queue = deque([(start_perm, 0)])
    n = len(permutation)

    while len(queue) > 0:
        perm, count = queue.popleft()

        for i in range(n - 1):
            for j in range(i + 1, n):
                new_perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

                if new_perm == sorted_perm:
                    return count + 1

                if new_perm not in visited:
                    visited.add(new_perm)
                    queue.append((new_perm, count + 1))

    return -1


def count_breakpoints(permutation) -> int:
    n = len(permutation)
    extended_perm = (0,) + permutation + (n + 1,)
    num_bp = 0

    for i in range(len(extended_perm) - 1):
        if abs(extended_perm[i] - extended_perm[i + 1]) != 1:
            num_bp += 1

    return num_bp

def upper_bound_estimate(permutation):
    perm = tuple(permutation)
    sorted_perm = tuple(sorted(permutation))
    n = len(permutation)
    count = 0

    while perm != sorted_perm:
        best_num_bp = float('inf')
        best_perm = None

        for i in range(n - 1):
            for j in range(i + 1, n):
                new_perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]
                num_bp = count_breakpoints(new_perm)
                
                if num_bp < best_num_bp:
                    best_num_bp = num_bp
                    best_perm = new_perm
        
        perm = best_perm
        count += 1

    return count

def improving_reversals(permutation):
    n = len(permutation)
    extended = (0,) + permutation + (n + 1,)
    current_bp = count_breakpoints(permutation)
    candidates = []

    for i in range(n - 1):
        if abs(extended[i] - extended[i + 1]) != 1:
            for j in range(i + 1, n):
                new_perm = permutation[:i] + permutation[i:j+1][::-1] + permutation[j+1:]
                if count_breakpoints(new_perm) < current_bp:
                    candidates.append((i, j))

    return candidates

def local_search(permutation, reversals, max_steps=3):
        perm = permutation

        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        for _ in range(max_steps):
            candidates = improving_reversals(perm)
            if not candidates:
                break

            move = random.choice(candidates)

            i, j = move
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]
            reversals.append(move)

        return reversals


