import random

import numpy as np

from individual import Individual, order_crossover, tournament_select, mutate

# x = Individual(10)
# y = Individual(10)

# print(x)
# print(y)

# order_crossover(x, y)

N = 30
n = 10
target = np.arange(n)

population = []


for i in range(N):
    population.append(Individual(n))

def fitness(x, t=target):
    return np.mean(x == t)

for ind in population:
    ind.eval(fitness)


fitnesses = [ ind.fitness for ind in population]
print(max(fitnesses), np.mean(fitnesses))

elitte = []
gen = 1
while True:
    new_pop = []
    new_pop.extend(elitte)
    
    while len(new_pop) < N:
        p1 = tournament_select(population)
        p2 = tournament_select(population)

        if np.random.rand() < 0.6:
            ch1, ch2 = order_crossover(p1, p2)
            ch1.eval(fitness)
            ch2.eval(fitness)
        else:
            ch1, ch2 = p1, p2

        for child in ch1, ch2:
            if np.random.rand() < 0.2:
                mutate(child) #mutation in place
                
        new_pop.append(ch1)
        new_pop.append(ch2)
        
    population = sorted(new_pop, key=lambda x: x.fitness, reverse=True)
    elitte = population[:3]
    
    fitnesses = [ ind.fitness for ind in population]
    print(gen, ":", max(fitnesses), np.mean(fitnesses))
    gen += 1

    if max(fitnesses) == 1:
        break
