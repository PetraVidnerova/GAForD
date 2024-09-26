import numpy as np
from individual import Individual, order_crossover

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

while True:
    ...
