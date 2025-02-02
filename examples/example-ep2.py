#!/usr/bin/env python3

from pyrimidine import *
import numpy as np
from pyrimidine.benchmarks.special import *


# generate a knapsack problem randomly

n=10
_evaluate = schaffer

class _Individual(BaseEPIndividual):
    element_class = FloatChromosome // n, FloatChromosome // n

    def decode(self):
        return self.chromosomes[0]


    def _fitness(self):
        return - _evaluate(self.decode())


class _Population(EvolutionProgramming, BasePopulation):
    element_class = _Individual
    default_size = 20


pop = _Population.random()

stat={'Mean Fitness':'mean_fitness', 'Max Fitness': 'max_fitness', 'Size': len}
data = pop.evolve(stat=stat, n_iter=100, period=5, history=True, verbose=True)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)

data[['Mean Fitness', 'Max Fitness']].plot(ax=ax)
ax.set_xlabel('Generations * 5')
ax.set_ylabel('Fitness')
plt.show()
