# pyrimidine

OO implement of genetic algorithm by python

![LOGO](logo.jpeg)


## Why

Why is the package named as pyrimidine? Because it begins with `py`.

## Download

It is not uploaded to pypi at present, so just download it from github.

## Idea

We regard the population as a container of individuals, an individual as a container of chromosomes
and a chromosome as a container(array) of genes.

The container could be a list or an array.
Container class has an attribute `element_class`, telling itself the class of the elements in it.

Following is the part of the source code of `BaseIndividual` and `BasePopulation`.
```python
class BaseIndividual(BaseIterativeModel):
    element_class = BaseChromosome
    default_size = 1
    
class BasePopulation(BaseIterativeModel):
    element_class = BaseIndividual
    default_size = 20
```

## Use

### Main classes

- BaseGene: the gene of chromosome
- BaseChromosome: sequence of genes, represents part of a solution
- BaseIndividual: sequence of chromosomes, represents a solution of a problem
- BasePopulation: set of individuals, represents a set of a problem
                also the state of a stachostic process
- BaseSpecies: set of population for more complicated optimalization


### import
Just use the command `from beagle import *` import all of the objects.

### subclass

#### Chromosome

Generally, it is an array of genes.

As an array of 0-1s, `BinaryChromosome` is used most frequently.

#### Individual
just subclass `SimpleIndividual` in most cases.

```python
class MyIndividual(SimpleIndividual):
    """individual with only one chromosome
    we set the gene is 0 or 1 in the chromosome
    """
    element_class = BinaryChromosome

    def _fitness(self):
        ...
```

equivalent to

```python
class MyIndividual(SimpleBinaryIndividual):

    def _fitness(self):
        ...
```



If an individual contains several chromosomes, then subclass `BaseIndividual`. It could be applied in multi-real-variable optimization problems.

```python
class _Chromosome(BinaryChromosome):
    def decode(self):
        """if the sequence of 0-1 represents a real number, then overide the method
        to transform it to a nubmer"""

class ExampleIndividual(BaseIndividual):
    element_class = _Chromosome

    def _fitness(self):
        # define the method to calculate the fitness
        x = self.decode()  # will call decode method of _Chromosome
        return evaluate(x)
```

If the chromosomes in an individual are different with each other, then subclass `MixIndividual`, meanwhile, the property `element_class` should be assigned with a tuple of classes for each chromosome.

```python
class MyIndividual(ExampleIndividual, MixIndividual):
    """
    Inherit the fitness from ExampleIndividual directly.
    It has 6 chromosomes, 5 are instances of _Chromosome, 1 is instance of FloatChromosome
    """
    element_class = (_Chromosome,)*5 + (FloatChromosome,)
```



#### Population

```python
class MyPopulation(SGAPopulation):
    element_class = MyIndividual
```

`element_class` is the most important attribute of the class that defines the class of the individual of the population.



### Initialize randomly

#### Initialize a population

Generate a population, with 50 individuals and each individual has 100 genes

`pop = MyPopulation.random(n_individuals=50, size=100)`

When each individual contains 5 chromosomes.

`pop = MyPopulation.random(n_individuals=10, n_chromosomes=5, size=10)`

For `MixIndividual`, we recommand to use, for example

`pop = MyPopulation.random(n_individuals=10, sizes=(10,8,8,3))`

#### Initialize an individual

In fact, `random` method of `Population` will call random method of `Individual`. If you want to generate an individual, then just execute `MyIndividual.random(n_chromosomes=5, size=10)`, for simple individuals, just execute `SimpleIndividual.random(size=10)` since its `n_chromosomes` equals to 1.

### Evolution

#### `evolve` method
Initialize a population with `random` method, then call `evolve` method.

```python
pop = MyPopulation.random(n_individuals=50, size=100)
pop.evolve()
print(pop.best_individual)
```

set `verbose=True` to display the data for each generation.

#### History

Get the history of the evolution.

```python
stat={'Fitness':'fitness', 'Best Fitness': lambda pop: pop.best_individual.fitness}
data = pop.history(stat=stat)
```
`stat` is a dict mapping keys to function, where string 'fitness' means function `lambda pop:pop.fitness` which gets the mean fitness of pop.



## Example

### Example 1

Description

    select ti, ni from t, n
    sum of ni ~ 10, while ti dose not repeat

The opt. problem is

    min abs(sum_i{ni}-10) + maximum of frequences in {ti}
    where i is selected.

```python
t = np.random.randint(1, 5, 100)
n = np.random.randint(1, 4, 100)

import collections
def max_repeat(x):
    # maximum of numbers of repeats
    c = collections.Counter(x)
    bm=np.argmax([b for a, b in c.items()])
    return list(c.keys())[bm]

class MyIndividual(SimpleIndividual):
    # or subclass SimpleBinaryIndividual

    element_class = BinaryChromosome

    def _fitness(self):
        x = self.evaluate()
        return - x[0] - x[1]

    def evaluate(self):
        return abs(np.dot(n, self.chromosome)-10), max_repeat(ti for ti, c in zip(t, self) if c==1)

class MyPopulation(SGAPopulation):
    element_class = MyIndividual

pop = MyPopulation.random(n_individuals=50, size=100)
pop.evolve()
print(pop.best_individual)
```



Notate that there is only one chromosome in SimpleIndividual, which could be represented as `self.chromosome` .

### Example2: Knapsack Problem

One of the famous problem is the knapsack problem. It is a good example for GA.

We apply `history` method in the example, that will record the main data of the whole evolution. The return value is an object of `pandas.DataFrame`. The argument `stat`  is a dict from a key to function/str(corresponding to a method) that map a population to a number. the numbers in one generation will be stored in a row of the dataframe.

see `# examples/example0`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from beagle import SimpleBinaryIndividual, SGAPopulation

from beagle.benchmarks.optimization import *

# generate a knapsack problem randomly
evaluate = Knapsack.random()

class MyIndividual(SimpleBinaryIndividual):
    def _fitness(self):
        return evaluate(self)


class MyPopulation(SGAPopulation):
    element_class = MyIndividual

pop = MyPopulation.random(size=20)

stat={'Fitness':'fitness', 'Best Fitness':'best_fitness'}
data = pop.history(stat=stat)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(data.index, data['Fitness'], data.index, data['Best Fitness'])
ax.legend(('Fitness', 'Best Fitness'))
ax.set_xlabel('Generations')
ax.set_ylabel('Fitness')
plt.show()

```

