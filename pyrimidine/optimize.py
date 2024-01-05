#!/usr/bin/env python3

"""
Optimiazation Helpers for GA
"""

import numpy as np

from .chromosome import BinaryChromosome
from .individual import makeIndividual, makeBinaryIndividual
from .population import StandardPopulation
from .de import DifferentialEvolution


def _decode(c, a, b):
    """Decode a binary sequence to a real number in [a,b]
    
    Args:
        c (binary seqence): Description
        a (number): lower bound
        b (number): upper bound
    
    Returns:
        number: a number in [a, b], represented by binary sequence,
        that 00...0 corresponds a, and 11...1 corresponds b
    
    Raises:
        e: fail to import a 3rd-part lib
    """

    try:
        from digit_converter import IntervalConverter
    except ImportError as e:
        print('The default decoder requires the 3rd-part lib `digit_converter`')
        raise e
    return IntervalConverter(a, b)(c)


def _make_individual(*xlim, size=8):
    """Make an individual class
    
    Args:
        *xlim: intervals
        size (int, tuple of int): the length of the encoding of xi
    """

    ndim = len(xlim)

    if ndim == 1:
        class _Individual(BinaryChromosome // size):

            def _fitness(self):
                return - func(self.decode())

            def decode(self):
                return decode(self, *xlim)
    else:
        class _Individual(makeIndividual(n_chromosomes=ndim, size=size)):
            default_size = ndim

            def _fitness(self):
                return - func(self.decode())

            def decode(self):
                return np.asarray([decode(c, a, b) for c, (a, b) in zip(self, xlim)])

    return _Individual


def ga_minimize(func, *xlim, decode=_decode, population_size=20, size=8, *args, **kwargs):
    """
    GA(with hall of fame) for minimizing the function `func` defined on `xlim`

    Arguments:
        func: objective function defined on R^n
        xlim {tuple of number pairs}: the intervals of xi
        decode {mapping}: transform a binary sequence to a real number
            ('0-1' sequence, lower_bound, upper_bound) |-> xi
        population_size {int}: size of the population
        size {int or tuple of int}: the length of the encoding of xi

    Example:
        ga_minimize(lambda x:x[0]**2+x[1], (-1,1), (-1,1))
    """

    _Individual = _make_individual(*xlim, size)
    _Population = StandardPopulation[_Individual] // population_size

    pop = _Population.random()
    return pop.ezolve(*args, **kwargs).solution


def de_minimize(func, *xlim, decode=_decode, population_size=20, size=8, **kwargs):
    """
    DE for minimizing the function `func` defined on `xlim`

    Arguments:
        func: objective function defined on R^n
        xlim: the intervals of xi
        decode: transform a binary sequence to a real number
            ('0-1' sequence, lower_bound, upper_bound) |-> xi
        population_size: size of the population
        size: the length of the encoding of xi

    Example:
        ga_minimize(lambda x:x[0]**2+x[1], (-1,1), (-1,1))
    """

    _Individual = _make_individual(*xlim, size)
    _Population = DifferentialEvolution[_Individual] // population_size

    pop = _Population.random()
    return pop.ezolve(**kwargs).solution


def ga_minimize_1D(func, xlim, decode=_decode, population_size=20, size=8, *args, **kwargs):
    """
    GA(with hall of fame) for minimizing 1D function `func` defined on the interval `xlim`

    Arguments:
        func: objective function defined on R
        xlim {pair of numbers}: the interval of x
        decode: transform a binary sequence to a real number
            ('0-1' sequence, lower_bound, upper_bound) |-> xi
        population_size {int}: size of the population
        size {int}: the length of the encoding of x

    Example:
        ga_minimize_1D(lambda x:x**2, (-1,1))
    """

    _Chromosome = _make_individual(xlim, size)
    _Population = StandardPopulation[_Chromosome] // population_size

    pop = _Population.random()
    return pop.ezolve(**kwargs).solution


class Optimizer:

    """Optimizer class for optimization problem
    
    Attributes:
        min_max (str): 'min' or 'max'
        Population: GA population or other evolutionary algorithms
    """
    
    def __init__(self, Population=None, min_max='min'):
        self.Population = Population
        self.min_max = min_max

    @classmethod
    def make_standard(cls, *xlim, min_max='min'):
        _Individual = _make_individual(*xlim, size)
        _Population = StandardPopulation[_Individual] // population_size
        return cls(_Population, min_max)

    def __call__(self, func, **kwargs):
        if self.min_max == 'min':
            def _evaluate(obj):
                return - func(obj.decode())
        else:
            def _evaluate(obj):
                return func(obj.decode())
        self.Population.set_fitness(_evaluate)
        
        return self.Population.random().ezolve(**kwargs).solution

