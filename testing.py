import random
import json
import os
import time
import pandas as pd

from basic_algorithms import bfs, count_breakpoints
from basic_algorithms import upper_bound_estimate
from branch_and_bound import branch_and_bound
from vns import vns
from genetic_algorithm import GeneticAlgorithm

def generate_instance(perm_length, seed = None):
    if seed is not None:
        random.seed(seed)

    permutation = []
    numbers = {i for i in range(1, perm_length + 1)}

    while len(numbers) > 0:
        num = random.choice(tuple(numbers))
        numbers.remove(num)
        permutation.append(num)

    return permutation

def save_instance(filename, permutation):
    with open(filename, "w", ) as f:
        json.dump(permutation, f)

def load_instance(filename):
    with open(filename, "r") as f:
        return json.load(f)

def make_tests(directory, num_tests, min_size, max_size):
    for i in range(1, num_tests + 1):
        lenght = random.randint(min_size, max_size)
        instance = generate_instance(lenght)
        save_instance(os.path.join(directory, f"{i}.json"), instance)
        print(f"Test {i}: {instance}")


def test_small_data(test_directory):
    test_names = os.listdir(test_directory)
    tests = []

    for name in test_names:
        tests.append(load_instance(os.path.join(test_directory, name)))

    results = []
    for i, instance in enumerate(tests, 1):
        result = {}
        print(f"Test case {i}")

        start = time.perf_counter()
        num_reversals, reversals = bfs(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["bruteforce"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals = branch_and_bound(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["branch_and_bound"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals = upper_bound_estimate(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["greedy"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals, _ = vns(instance, max_iter=1000, k_max=5)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["vns"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        gp = GeneticAlgorithm(instance, population_size=200, num_generations=100, mutation_prob=0.1, elitism_size=0.1, selection_type="tournament", tournament_size=10, search_localy=True)
        solution, _ = gp.solve()
        num_reversals = len(solution.reversals)
        reversals = solution.reversals
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["genetic_algorithm"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        results.append(result)

    algorithms = ["bruteforce", "branch_and_bound", "greedy", "vns", "genetic_algorithm"]
    summary = []

    for algo in algorithms:
        times = []
        optimal_count = 0
        success_count = 0

        for test_result in results:
            bfs_value = test_result["bruteforce"]["num_reversals"]
            algo_value = test_result[algo]["num_reversals"]
            times.append(test_result[algo]["time"])

            if algo_value == bfs_value:
                optimal_count += 1

            if test_result[algo]["succesfully_sorted"]:
                success_count += 1

        n = len(results)
        summary.append({
            "algorithm": algo,
            "average_time": sum(times) / n,
            "percent_of_optimal": 100 * optimal_count / n,
            "percent_successfully_sorted": 100 * success_count / n
        })

    df = pd.DataFrame(summary).set_index("algorithm").rename_axis(None)
    return df 

def test_medium_data(test_directory):
    test_names = os.listdir(test_directory)
    tests = []

    for name in test_names:
        tests.append(load_instance(os.path.join(test_directory, name)))

    results = []
    for i, instance in enumerate(tests, 1):
        result = {}
        print(f"Test case {i}")

        start = time.perf_counter()
        num_reversals, reversals = branch_and_bound(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["branch_and_bound"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals = upper_bound_estimate(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["greedy"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals, _ = vns(instance, max_iter=2000, k_max=10)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["vns"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        gp = GeneticAlgorithm(instance, population_size=200, num_generations=200, mutation_prob=0.1, elitism_size=0.1, selection_type="tournament", tournament_size=10, search_localy=True)
        solution, _ = gp.solve()
        num_reversals = len(solution.reversals)
        reversals = solution.reversals
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["genetic_algorithm"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        results.append(result)

    algorithms = ["branch_and_bound", "greedy", "vns", "genetic_algorithm"]
    summary = []

    for algo in algorithms:
        times = []
        optimal_count = 0
        success_count = 0

        for test_result in results:
            bfs_value = test_result["branch_and_bound"]["num_reversals"]
            algo_value = test_result[algo]["num_reversals"]
            times.append(test_result[algo]["time"])

            if algo_value == bfs_value:
                optimal_count += 1

            if test_result[algo]["succesfully_sorted"]:
                success_count += 1

        n = len(results)
        summary.append({
            "algorithm": algo,
            "average_time": sum(times) / n,
            "percent_of_optimal": 100 * optimal_count / n,
            "percent_successfully_sorted": 100 * success_count / n
        })

    df = pd.DataFrame(summary).set_index("algorithm").rename_axis(None)
    return df


def test_large_data(test_directory):
    test_names = os.listdir(test_directory)
    tests = []

    for name in test_names:
        tests.append(load_instance(os.path.join(test_directory, name)))

    results = []
    for i, instance in enumerate(tests, 1):
        result = {}
        print(f"Test case {i}")

        start = time.perf_counter()
        num_reversals, reversals = upper_bound_estimate(instance)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["greedy"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        num_reversals, reversals, _ = vns(instance, max_iter=5000, k_max=10)
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["vns"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        start = time.perf_counter()
        gp = GeneticAlgorithm(instance, population_size=200, num_generations=400, mutation_prob=0.1, elitism_size=0.15, selection_type="tournament", tournament_size=10, search_localy=True)
        solution, _ = gp.solve()
        num_reversals = len(solution.reversals)
        reversals = solution.reversals
        end = time.perf_counter()

        perm = instance.copy()
        for i, j in reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        result["genetic_algorithm"] = {
            "num_reversals": num_reversals,
            "time": end - start,
            "succesfully_sorted": count_breakpoints(tuple(perm)) == 0
        }

        results.append(result)

    algorithms = ["greedy", "vns", "genetic_algorithm"]
    summary = []

    for algo in algorithms:
        times = []
        best_count = 0
        success_count = 0

        for test_result in results:
            times.append(test_result[algo]["time"])
            min_value = min(test_result[a]["num_reversals"] for a in algorithms)

            if test_result[algo]["succesfully_sorted"]:
                success_count += 1

                if test_result[algo]["num_reversals"] == min_value:
                    best_count += 1

        n = len(results)
        summary.append({
            "algorithm": algo,
            "average_time": sum(times) / n,
            "percent_best_result": 100 * best_count / n,
            "percent_successfully_sorted": 100 * success_count / n
        })

    df = pd.DataFrame(summary).set_index("algorithm").rename_axis(None)
    return df

