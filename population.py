import random
import numpy as np
from individual import Individual, order_crossover, tournament_select, mutate, cyclic_crossover, partially_mapped_crossover


class Population():

    def __init__(self, n, N, fitness, mutation):

        self.n = n
        self.N = N
        self.fitness = fitness
        self.mutation= mutation

        self.population = []
        for i in range(N):
            self.population.append(Individual(n))

        for ind in self.population:
            ind.evaluate(fitness.evaluate)

        self.elitte_size = 30
        self.elitte = []
        self.pmut = None
        self.thau = 0

    def extract(self, k):
        group = []
        for i in range(k):
            ind = self.population.pop(random.randrange(len(self.population)))
            group.append(ind)
        return group

    def append(self, group):
        self.population.extend(group)
            
        

    def restart(self):
        #self.population = []
        for i in range(self.N):
#           if i % 2 == 0:
            self.population[i] = Individual(self.n)
            self.population[i].evaluate(self.fitness.evaluate)
        #self.elitte = self.elitte[:1]

    def update_elitte(self, elittes):
        
        #       print([x.fitness for x in self.elitte])
        #       print([x.fitness for x in elitte])
        # $#        self.population.extend(elitte)
        #        self.elitte = sortedself.elitte + elitte, key=lambda x: x.fitness, reverse=True)[:self.elitte_size]
        #        self.elitte = elitte
        # for e in self.elitte:
        #    if np.all(e.ind == elitte.ind):
        #        return
        # self.population.append(elitte)

        #        print([x.fitness for x in self.elitte])
        #        exit()
        for elitte in elittes:
            same = False
            for e in self.elitte:
                if np.all(e.ind == elitte.ind):
                    same = True
                    break
            if not same:
                self.elitte.append(elitte)
#       self.elitte = self.elitte[:self.elitte_size]


    def run(self, pcx, pmut, steps=1):
        if self.pmut is None:
            self.pmut =pmut 
        for _ in range(steps):
            ret = self.step(pcx)
        return ret
            
    def step(self, pcx):
        new_pop = []
        new_pop.extend(self.elitte)
    
        while len(new_pop) < self.N+len(self.elitte):
            p1 = tournament_select(self.population)
            p2 = tournament_select(self.population)

            # cx = np.random.choice([order_crossover, cyclic_crossover, partially_mapped_crossover],
            #                       p=[0.45, 0.54, 0.01])
            #cx = cyclic_crossover
            cx = np.random.choice([order_crossover, cyclic_crossover], p=(0.3, 0.7))
            if np.random.random() < pcx:
                ch1, ch2 = cx(p1, p2)
                ch1.evaluate(self.fitness.evaluate)
                ch2.evaluate(self.fitness.evaluate)
            else:
                ch1, ch2 = p1.copy(), p2.copy()

            for child in ch1, ch2:
                if np.random.random() < self.pmut:
                    if np.random.random() < 0.1 + 0.5*self.thau:
                        mutate(child)
                    else:
                        self.mutation.mutate(child) #mutation in place
                    child.evaluate(self.fitness.evaluate)
                    
            new_pop.append(ch1)
            new_pop.append(ch2)
        
        self.population = sorted(new_pop, key=lambda x: (x.F2,  -x.F, x.fitness), reverse=True)
        #self.elitte = self.population[:self.elitte_size]
        self.elitte = []
        for i in self.population:
            same = False
            for e in self.elitte:
                if np.all(e.ind == i.ind):
                    same = True
                    break
            if not same:
                self.elitte.append(i.copy())
            if len(self.elitte) >= self.elitte_size // 2:
                break
        
        self.population = sorted(new_pop, key=lambda x: (x.fitness,  x.F2, -x.F), reverse=True)
        #self.elitte = self.population[:self.elitte_size]
        for i in self.population:
            same = False
            for e in self.elitte:
                if np.all(e.ind == i.ind):
                    same = True
                    break
            if not same:
                self.elitte.append(i.copy())
            if len(self.elitte) >= self.elitte_size:
                break
            


        diverse_pop = []
        diverse_pop.append(self.population[0])
        for ind in self.population[1:]:
            last_ind = diverse_pop[-1] 
            if ind.fitness != last_ind.fitness:
                diverse_pop.append(ind)
                continue
            else:
                if np.all(ind.ind == last_ind.ind):
                    continue
                else:
                    diverse_pop.append(ind)
        diversity =  len(diverse_pop)/len(self.population) 
        # 1.: self.pmut = 0.15 + 2*max(0.3-diversity, 0) * (0.95 - 0.15)
        #2: self.pmut = 0.15 + 2*max(0.5-diversity, 0) * (0.95 - 0.15)

        # 3: self.pmut = 0.15 + max(0.5-diversity, 0) * (0.95 - 0.15)
        #        print(diversity, self.pmut)
        #4: self.pmut = 0.15 +  (1 - diversity) * (0.95 - 0.15)
        self.pmut = 0.2 + 0.4*(1 - diversity)
        return float(-self.population[0].fitness), float(-np.mean([i.fitness for i in self.population]))

