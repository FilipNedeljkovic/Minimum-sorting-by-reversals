# Minimum-sorting-by-reversals

Implementation of several algorithms for solving the **Minimum Sorting by Reversals** problem. \
Project developed for the *Computational Intelligence* course at the **Faculty of Mathematics, University of Belgrade**.

## Authors

- Matija Đorđević (59/2022)  
- Filip Nedeljković (43/2022)

## Problem

Given a permutation of numbers `1..n`, the goal is to transform it into the sorted permutation using the **minimum number of reversals**. \
A **reversal** operation reverses the order of elements inside a chosen segment of the permutation.

Example:
```
3412 → 1432 → 1234
```

The minimum number of such operations needed to sort the permutation is called the **reversal distance**. \
The problem is known to be **NP-hard for unsigned permutations**.

## Implemented Algorithms

This repository includes implementations of several approaches:

- **Brute Force (BFS)** – explores the full permutation space and guarantees an optimal solution (practical only for very small inputs)
- **Branch and Bound** – optimal algorithm that prunes the search space using upper and lower bounds
- **Greedy Heuristic** – fast heuristic based on reducing the number of breakpoints
- **Variable Neighborhood Search (VNS)** – metaheuristic that explores multiple neighborhoods with local search
- **Genetic Algorithm** – evolutionary approach using selection, crossover, mutation, and local search

## Application

The problem has applications in **bioinformatics**, particularly in **comparative genomics**, where genomes can be modeled as permutations of genes and reversals represent evolutionary mutations.