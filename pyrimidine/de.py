#!/usr/bin/env python

"""
Differential Evolution Algorithm
"""

import copy

import numpy as np
from .mixin import PopulationMixin
from .individual import MonoIndividual

from .utils import *


class DifferentialEvolution(PopulationMixin):

    params ={
    "factor" : 0.1,
    "cross_prob": 0.75,
    }

    def init(self):
        self.ndims = tuple(map(len, self[0]))


    def transition(self, *args, **kwargs):
        self.move()
        for k, (test_individual, individual) in enumerate(zip(self.test, self)):
            if test_individual.fitness > individual.fitness:
                self[k] = test_individual.clone()


    def move(self):
        self.test = self.clone()
        for t in self.test:
            x0, x1, x2 = choice(self, size=3, replace=False)
            jrand = map(np.random.randint, self.ndims)
            xx = x0 + self.factor * (x1 - x2)
            for chromosome, xc, n, r in zip(t, xx, self.ndims, jrand):
                ind = np.random.random(n) < self.cross_prob
                chromosome[ind] = xc[ind]
                chromosome[r] = xc[r]



class DifferentialEvolutionC(PopulationMixin):
    # For the population of chromosomes

    params ={
    "factor": 0.5,
    "cross_prob": 0.75,
    }

    def init(self):
        self.ndim = len(self[0])
        self.test = self.clone()


    def move(self):
        for t in self.test:
            x0, x1, x2 = choice(self, size=3, replace=False)
            xx = x0 + self.factor * (x1 - x2)
            jrand = np.random.randint(self.ndim)
            ind = np.random.random(n) < self.cross_prob
            t[ind] = xx[ind]
            t[jrand] = xx[jrand]

