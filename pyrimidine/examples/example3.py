#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from beagle import *
from digit_converter import *
from beagle.benchmarks.neural_network import MLP

import numpy as np


N, input_dim = 1000, 2

evaluate = MLP.random(N=1000, p=2)

h = 10

c = IntervalConverter(-5,5)


class _Chromosome(BinaryChromosome):
    def decode(self):
        return c(self)

class ExampleIndividual(MixIndividual):
    """base class of individual

    You should implement the methods, cross, mute
    """
    element_class = FloatChromosome, FloatChromosome, FloatChromosome, _Chromosome

    def decode(self):
        return self[0].reshape(input_dim, h), self[1], self[2], self[3].decode()

    def _fitness(self):
        return evaluate(self.decode())

class ExampleIndividual2(ExampleIndividual, TraitThresholdIndividual):
    """base class of individual

    You should implement the methods, cross, mute
    """
    element_class = FloatChromosome, FloatChromosome, FloatChromosome, _Chromosome, FloatChromosome

if __name__ == '__main__':
    SGAPopulation.element_class = ExampleIndividual

    pop = SGAPopulation.random(n_individuals=50, sizes=[h*input_dim, h, h, 8])
    pop.mate_prob = 0.8
    pop.mutate_prob = 0.4
    stat={'Fitness':'fitness', 'Best Fitness':'best_fitness'}

    data = pop.history(ngen=350, stat=stat)

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data.index, data['Fitness'], data.index, data['Best Fitness'])

   
    SGAPopulation.element_class = ExampleIndividual2
    pop = SGAPopulation.random(n_individuals=50, sizes=[h*input_dim, h, h, 8, 3])

    pop.mate_prob = 1
    pop.mutate_prob= 1
    d = pop.history(ngen=350, stat={'Fitness':'fitness', 'Best Fitness':'best_fitness', 
        'mean threshold': lambda pop: np.mean([ind.threshold for ind in pop.individuals]),
        'mean mate_prob': lambda pop: np.mean([ind.mate_prob for ind in pop.individuals]),
        'mean mutate_prob': lambda pop: np.mean([ind.mutate_prob for ind in pop.individuals]),
        })
    d.to_csv('h.csv')
    ax.plot(d.index, d['Fitness'], d.index, d['Best Fitness'], '.-')
    ax.legend(('Traditional','Traditional best', 'New', 'New best'))
    ax.set_xlabel('Generation')
    plt.show()

