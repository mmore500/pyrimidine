#!/usr/bin/env python3


from pyrimidine import *
from pyrimidine.benchmarks.optimization import *

from pyrimidine.deco import add_memory, fitness_cache, regester_map

# generate a knapsack problem randomly

evaluate = Knapsack.example()
n_bags = evaluate.n_bags


class _IndMixin:
    def _fitness(self):
        return evaluate(self.decode())

    def backup(self, check=True):
        f = self._fitness()
        if not check or (self.memory['fitness'] is None or f > self.memory['fitness']):
            self._memory = {
            'solution': self.solution,
            'fitness': f
            }

@add_memory({'fitness':None, 'solution':None})
class YourIndividual(_IndMixin, BinaryChromosome // n_bags):
    pass


@add_memory({'fitness':None, 'solution':None})
class MyIndividual(_IndMixin, QuantumChromosome // n_bags):

    def mutate(self):
        pass

    def cross(self, other):
        return self.__class__((self + other) /2)


class _Mixin:
    def init(self):
        for i in self: i.backup()
        super().init()

    def update_hall_of_fame(self, *args, **kwargs):
        """
        Update the `hall_of_fame` after each step of evolution
        """
        for i in self: i.backup()
        super().update_hall_of_fame(*args, **kwargs)


class MyPopulation(_Mixin, HOFPopulation):

    element_class = MyIndividual
    default_size = 20


class YourPopulation(_Mixin, HOFPopulation):

    element_class = YourIndividual
    default_size = 20


stat={'Mean Fitness': 'mean_fitness', 'Best Fitness': 'best_fitness'}
mypop = MyPopulation.random()
for i in mypop: i.measure()
yourpop = MyPopulation([YourIndividual(i.measure_result) for i in mypop])
mydata = mypop.evolve(n_iter=50, stat=stat, history=True)
yourdata = yourpop.evolve(n_iter=50, stat=stat, history=True)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
yourdata[['Mean Fitness', 'Best Fitness']].plot(ax=ax)
mydata[['Mean Fitness', 'Best Fitness']].plot(ax=ax)
ax.legend(('Mean Fitness', 'Best Fitness', 'Mean Fitness(Quantum)', 'Best Fitness(Quantum)'))
ax.set_xlabel('Generations')
ax.set_ylabel('Fitness')
ax.set_title(f'Demo of (Quantum)GA: {n_bags}-Knapsack Problem')
plt.show()
