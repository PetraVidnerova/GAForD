import multiprocessing
import time

import click
import numpy as np

from individual import Mutation
from fitness import Fitness
from population import Population

N = 90    # size of one population
k = 10    # number of populations

PCX = 0.10    # 0.95
PMUT = 0.15
steps = 100


def run(pop):
    return pop.run(PCX, PMUT, steps=steps), pop


@click.command()
@click.argument('sourcename')
@click.argument('sim')
def main(sourcename, sim):
    s = time.time()
    t = islands(sourcename, sim)
    e = time.time()
    print(f"Computation time: {e-s:.2f}s. Solution found in: {t-s:.2f}s.")


def islands(sourcename, sim):

    f = Fitness(sourcename, int(sim))
    print(f.matrix)
    n = len(f.matrix)

    mutation = Mutation(
        f.matrix.sum(axis=1),
        f.centralities2,
        f.centralities2
    )

    populations = []
    for i in range(k):
        pop = Population(n, N, f, mutation)
        populations.append(pop)

    fitnesses = [ind.fitness for ind in pop.population]
    print(max(fitnesses), np.mean(fitnesses))

    pool = multiprocessing.Pool(5)
    gen = 0
    last_best = None
    best_ind = None
    stay_same = 0
    stay_same_thau = 0
    time_to_sol = 0

    while True:
        ret = pool.map(run, populations)
        ret = list(ret)
        populations = [x[1] for x in ret]
        results = [x[0] for x in ret]
        print(gen, ":", results, flush=True)
        gen += steps

        if True:
            elittes = [pop.elitte for pop in populations]

            for i, e in enumerate(elittes):
                for j, pop in enumerate(populations):
                    if i != j:
                        pop.update_elitte(e)

            l = [i for e in elittes for i in e]
            if best_ind is not None:
                l.append(best_ind)
            inds = sorted(l, key=lambda x: (x.F2, x.fitness, x.F), reverse=True)
            print("RESULT:", inds[0].fitness, inds[0].F, inds[0].F2)
            for x in inds[0].ind:
                print(x, end=" ")
            print()
            best = (inds[0].fitness, inds[0].F, inds[0].F2)
            best_ind_candidate = inds[0]
            if inds[0].F2 == 0:
                print("Solution found.")
                return time.time()

            if best == last_best:
                stay_same += 1
                stay_same_thau += 1
                for pop in populations:
                    pop.thau = 0.1*stay_same_thau/10
                if stay_same == 50:
                    print(" No progress. Exiting. ")
                    return time_to_sol   # END OF THE WHOLE THING
                if stay_same % 10 == 0:
                    # restarting
                    print(" * *** * RESTARTING * ** * ")
                    stay_same_thau = 0
                    for pop in populations:
                        pop.restart()
                    all_elitte = []
                    for pop in populations:
                        elittes = pop.elitte
                        pop.elitte = []
                        for elitte in elittes:
                            same = False
                            for e in all_elitte:
                                if e.fitness != elitte.fitness or e.F != elitte.F or e.F2 != elitte.F2:
                                    continue
                                if np.all(e.ind == elitte.ind):
                                    same = True
                                    break
                            if not same:
                                all_elitte.append(elitte)

                    print("LEN", len(all_elitte))
                    i = 0
                    for pop in populations:
                        pop.elitte = [] 
                    for elitte in all_elitte:
                        populations[i].elitte.append(elitte)
                        i += 1
                        if i >= len(populations):
                            i = 0
                else:
                    print(" * *** * MIXING POPULATIONS * ** *")
                    # mix populations somehow
                    kk = N // 3
                    groups = []
                    for pop in populations: 
                        group = pop.extract(kk)
                        groups.append(group)
                    for i, pop in enumerate(populations):
                        pop.append(groups[ (i+1) % k])

            elif (last_best is None or
                  (best[2] > last_best[2] or (best[2] == last_best[2] and
                                              best[1] < last_best[1]) or
                    (best[2] == last_best[2] and best[1] == last_best[1] and 
                     best[0] > last_best[0]))):
                last_best = best
                stay_same = 0
                best_ind = best_ind_candidate
                time_to_sol = time.time()
    return time_to_sol


if __name__ == "__main__":

    main()
