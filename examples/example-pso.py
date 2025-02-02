#!/usr/bin/env python3

from pyrimidine import FloatChromosome, BasePopulation
from pyrimidine.pso import Particle, ParticleSwarm

from pyrimidine.benchmarks.special import *


def evaluate(x):
    return -rosenbrock(x)


class _Particle(Particle):
    element_class = FloatChromosome.set(default_size=8)
    def _fitness(self):
        return evaluate(self.position)


class MyParticleSwarm(ParticleSwarm):
    element_class = _Particle
    default_size = 10


pop = MyParticleSwarm.random()

stat={'Mean Fitness': 'mean_fitness', 'Best Fitness': 'max_fitness'}

data = pop.evolve(stat=stat, n_iter=10, history=True, verbose=True)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
axt = ax.twinx()
data[['Best Fitness']].plot(ax=ax)
data[['Mean Fitness']].plot(ax=axt, color='orange', linestyle='--')
ax.set_xlabel('Generations')
ax.set_ylabel('Fitness')
ax.set_title('Demo of PSO')
plt.show()
