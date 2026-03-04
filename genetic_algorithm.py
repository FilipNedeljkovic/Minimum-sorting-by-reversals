import random
from basic_algorithms import *

class Individual:
    def __init__(self, permutation, upper_bound:int, reversals = None):
        if reversals is not None:
            self.reversals = reversals
        else:
            length = random.randint(1, upper_bound)
            n = len(permutation)
            i = random.randint(0, n-2)
            j = random.randint(i + 1, n-1)
            self.reversals = [(i, j) for _ in range(length)]
        
        self.permutation = permutation
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        perm = self.permutation
        for i, j in self.reversals:
            perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

        return -100*count_breakpoints(perm) - len(self.reversals)

    def __lt__(self, other):
        return self.fitness < other.fitness


class GeneticAlgorithm:
    def __init__(self, permutation, population_size:int, num_generations:int, mutation_prob:float, elitism_size:float, 
                crossover_type:str, selection_type:str, tournament_size:int|None, search_localy:bool = False):
        self.permutation = tuple(permutation)
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        
        self.num_elite = int(population_size*elitism_size)
        if self.num_elite % 2 != self.population_size % 2:
            self.num_elite += 1

        self.tournament_size = tournament_size
        self.crossover_type = crossover_type
        self.selection_type = selection_type
        self.search_localy = search_localy

        if selection_type == 'tournament':
            assert tournament_size is not None
        
    def selection(self, population:list[Individual]):
        match self.selection_type:
            case 'tournament':
                participants = random.sample(population, self.tournament_size)
                return max(participants)
                
            case 'roulette':
                return random.choices(population, weights=[ind.fitness for ind in population], k=1)[0]

            case 'rang':
                sorted_population = sorted(population, key=lambda ind: ind.fitness)
                return random.choices(sorted_population, weights=[i for i in range(1, n+1)])

            case _:
                raise ValueError(f'unknown selection_type: {self.selection_type}')

    def crossover(self, parent1_code, parent2_code):
        i = random.randint(0, len(parent1_code))
        j = random.randint(0, len(parent2_code))
        child1_code = parent1_code[:i] + parent2_code[j:]
        child2_code = parent2_code[:j] + parent1_code[i:]

        return child1_code, child2_code
        
    def mutation(self, ind_code):
        code = list(ind_code)
        n = len(self.permutation)

        if random.random() < self.mutation_prob:
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            code.append((i, j))

        if code and random.random() < self.mutation_prob / 2:
            code.pop(random.randrange(len(code)))

        return code

    def solve(self) -> Individual:
        upper_bound = upper_bound_estimate(self.permutation)
        population = [Individual(self.permutation, upper_bound) for _ in range(self.population_size)]

        for h in range(self.num_generations):
            print(h)
            population.sort(reverse=True)
            new_population = population[:self.num_elite]

            for i in range(self.num_elite, self.population_size, 2):
                parent1 = self.selection(population)
                parent2 = self.selection(population)

                child1_code, child2_code = self.crossover(parent1.reversals, parent2.reversals)

                child1_code = self.mutation(child1_code)
                child2_code = self.mutation(child2_code)

                if self.search_localy:
                    child1_code = local_search(self.permutation, child1_code)
                    child2_code = local_search(self.permutation, child2_code)

                child1 = Individual(self.permutation, upper_bound, reversals=child1_code)
                child2 = Individual(self.permutation, upper_bound, reversals=child2_code)

                new_population.append(child1)
                new_population.append(child2)

            population = new_population.copy()

        return max(population)

gp = GeneticAlgorithm([23,1,2,11,24,22,19,6,10,7,25,20,5,8,18,12,13,14,15,16,17,21,3,4,9], population_size=200, num_generations=300, mutation_prob=0.1, elitism_size=0.1, selection_type="tournament", tournament_size=10, crossover_type='', search_localy=True)
solution = gp.solve()
print(len(solution.reversals))

perm = solution.permutation
for i, j in solution.reversals:
    perm = perm[:i] + perm[i:j+1][::-1] + perm[j+1:]

print(perm)
print(count_breakpoints(perm) == 0)