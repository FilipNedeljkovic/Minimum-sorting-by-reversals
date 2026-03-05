import random
from basic_algorithms import *

def calc_value(permutation, reversals):
    perm = permutation

    for i, j in reversals:
        perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

    return -100*count_breakpoints(perm) - len(reversals)

def shake(reversals, n:int, k:int):
    revs = reversals.copy()

    for _ in range(k):
        if random.random() < 0.2:
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            revs.append((i, j))
        elif len(revs) > 0:
            revs.pop(random.randrange(len(revs)))

    return revs

def vns(permutation, max_iter:int = 200, k_min:int = 1, k_max:int = 3, move_prob:float = 0.5):
    start_perm = tuple(permutation)
    n = len(permutation)
    best_revs = local_search(start_perm, [], 5)
    best_value = calc_value(start_perm, best_revs)

    for _ in range(max_iter):
        for k in range(k_min, k_max + 1):
            new_revs = shake(best_revs, n, k)
            new_revs = local_search(start_perm, new_revs, 5)
            new_value = calc_value(start_perm, new_revs)

            if new_value > best_value or (new_value == best_value and random.random() < move_prob):
                best_value = new_value
                best_revs = new_revs
                break
    
    return len(best_revs), best_revs

