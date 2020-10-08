#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import BaseSpecies
from .utils import  *

class DualSpecies(BaseSpecies):

    @property  
    def male_population(self):
        return self.populations[0]

    @property  
    def female_population(self):
        return self.populations[1]

    @property  
    def males(self):
        return self.populations[0].individuals

    @property  
    def females(self):
        return self.populations[1].individuals

    @property
    def male_fitness(self):
        return self.populations[0].fitness

    @property
    def female_fitness(self):
        return self.populations[1].fitness
    

    def mate(self):
        # offspring = [male.cross(female) for male, female in zip(self.males, self.females) if self.match(male, female)]
        # self.populations[0].individuals += offspring
        # offspring = [male.cross(female) for male, female in zip(self.males, self.females) if self.match(male, female)]
        # self.populations[1].individuals += offspring
        for male in self.males:
            females = choice_with_fitness(self.females, [f.fitness for f in self.females], 5)
            for female in females:
                if self.match(male, female):
                    self.populations[0].individuals.append(male.cross(female))
                    self.populations[1].individuals.append(male.cross(female))
        for female in self.females:
            males = choice_with_fitness(self.males, [f.fitness for f in self.males], 5)
            for male in males:
                if self.match(male, female):
                    self.populations[0].individuals.append(male.cross(female))
                    self.populations[1].individuals.append(male.cross(female))
    

    def match(self, male, female):
        return True


    def transit(self, *args, **kwargs):
        self.populations[0].select()
        self.populations[1].select()
        self.mate()
        self.populations[0].mutate()
        self.populations[1].mutate()
        self.populations[0].rank()
        self.populations[1].rank()
        self.populations[0].fitness = self.populations[1].fitness = None
