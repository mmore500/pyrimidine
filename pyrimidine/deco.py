#!/usr/bin/env python3

"""
Decorators
"""

from types import MethodType

import copy


def clear_cache(func):
    def mthd(obj, *args, **kwargs):
        result = func(obj, *args, **kwargs)
        obj.clear_cache()
        return result
    return mthd

def side_effect(func):
    """Decorator for methods with side effect

    Apply the decorator to methods with side effects.
    If all the methods called by a particular method have the decorator applied,
    it is not advisable to include the decorator in that method.
    
    Args:
        func (TYPE): a method
    
    Returns:
        Decorated method
    """

    def mthd(obj, *args, **kwargs):
        result = func(obj, *args, **kwargs)
        # clear the cache after calling the method
        if hasattr(obj, '_cache'):
            obj.clear_cache()
        return result
    return mthd


def clear_fitness(func):
    def mthd(obj, *args, **kwargs):
        result = func(obj, *args, **kwargs)
        obj.clear_cache('fitness')
        return result
    return mthd


usual_side_effect = ['mutate', 'extend', 'pop', 'remove', '__setitem__', '__setattr__', '__setstate__']

def method_cache(func, a):
    """cache for methods

    Pre-define `_cache` as an attribute of the obj.
    
    Args:
        func (TYPE): the original method
        a (TYPE): an attribute (or any value) computed by the method
    
    Returns:
        MethodType
    """
    def mthd(obj):
        # get the attribute from cache, otherwise compute it again
        if obj._cache[a] is None:
            f = obj.func()
            obj._cache[a] = f
            return f
        else:
            return obj._cache[a]
    return mthd


class add_cache:

    """Handle with cache for class
    
    Attributes:
        attrs (tuple[str]): a tuple of attributes
        methods (tuple[str]): a tuple of method names
    """

    def __init__(self, attrs, methods=(), scope=None):
        self.methods = methods
        self.attrs = attrs
        self.scope = scope

    def __call__(self, cls):

        # add `_cache` to the class
        if hasattr(cls, '_cache'):
            cls._cache.update({a: None for a in self.attrs})
        else:
            cls._cache = {a: None for a in self.attrs}

        @property
        def cache(obj):
            return obj._cache

        cls.cache = property(cache)

        def _clear_cache(obj, k=None):
            if k is None:
                obj._cache = {k: None for k in obj._cache.keys()}
            elif k in obj._cache:
                obj._cache[k] = None

        def _cleared(obj, k=None):
            if k is None:
                return all(v == None for v in obj._cache.values())
            elif k in obj._cache:
                return obj._cache[k] == None

        def _set_cache(obj, **d):
            obj._cache.update(d)

        cls_clone = cls.clone
        def _clone(obj, cache=True, *args, **kwargs):
            cpy = cls_clone(obj, *args, **kwargs)
            if cache:
                cpy.set_cache(**obj._cache)
            return cpy

        cls.cleared = _cleared
        cls.clear_cache = _clear_cache
        cls.set_cache = _set_cache
        cls.clone = _clone

        for a in self.attrs:
            def f(obj):
                """get the attribute from cache, 
                otherwise compute it again by the default method
                """
                if obj._cache[a] is None:      
                    if hasattr(cls, '_'+a):
                        v = getattr(obj, '_'+a)()
                    else:
                        v = getattr(super(cls, obj), a)
                    obj._cache[a] = v
                    return v
                else:
                    return obj._cache[a]
            setattr(cls, a, property(f))

        def _after_setter(obj):
            obj.clear_cache()

        cls.after_setter = _after_setter

        for name in self.methods:
            if hasattr(obj, name):
                setattr(cls, name, clear_cache(getattr(cls, name)))

        cls_new = cls.__new__
        def _new(cls, *args, **kwargs):
            obj = cls_new(cls, *args, **kwargs)
            obj._cache = copy.copy(cls._cache)
            return obj

        cls.__new__ = _new

        return cls


fitness_cache = add_cache(('fitness',))


class set_fitness:

    def __init__(self, f=None):
        self.f = f

    def __call__(self, cls):
        if self.f is None:
            if '_fitness' in globals():
                self.f = globals()['_fitness']
            else:
                raise Exception('Function `_fitness` is not defined before setting fitness. You may forget to create the class in the context of environment.')
        cls._fitness = self.f
        return cls


class add_memory:

    """
    add the `_memory` dict to the cls/obj

    The memory dict stores the best solution,
    unlike the `_cache` dict which only records the last computing result.
    """

    def __init__(self, memory={}):
        self._memory = memory

    def __call__(self, cls):

        cls._memory = self._memory

        def memory(obj):
            return obj._memory

        cls.memory = property(memory)

        def _set_memory(obj, **d):
            obj._cache.update(d)

        cls.set_memory = _set_memory

        def fitness(obj):
            # get fitness from memory by default
            if obj.memory['fitness'] is None:
                return obj._fitness()
            else:
                return obj.memory['fitness']

        cls.fitness = property(fitness)

        cls_clone = cls.clone
        def _clone(obj, *args, **kwargs):
            cpy = cls_clone(obj, *args, **kwargs)
            cpy._memory = copy.deepcopy(obj._memory)
            return cpy
        cls.clone = _clone

        cls_new = cls.__new__
        def _new(cls, *args, **kwargs):
            obj = cls_new(cls, *args, **kwargs)
            obj._memory = copy.deepcopy(cls._memory)
            return obj

        cls.__new__ = _new

        return cls


basic_memory = add_memory({'fitness':None, 'solution': None})


usual_side_effect = ['mutate', 'extend', 'pop', 'remove', '__setitem__', '__setattr__', '__setstate__']

def method_cache(func, a):
    """cache for methods

    Pre-define `_cache` as an attribute of the obj.
    
    Args:
        func (TYPE): the original method
        a (TYPE): an attribute (or any value) computed by the method
    
    Returns:
        MethodType
    """
    def mthd(obj):
        # get the attribute from cache, otherwise compute it again
        if obj._cache[a] is None:
            f = obj.func()
            obj._cache[a] = f
            return f
        else:
            return obj._cache[a]
    return mthd


class Regester:
    # regerster operators, used in the future version

    def __init__(name, key=None):
        self.name = name
        self.key = key

    def __call__(self, cls):

        def _regester_operator(self, name, key=None):
            if hasattr(self, name):
                raise AttributeError(f'"{name}" is an attribute of "{self.__name__}", and would not be regestered.')
            self._operators.append(key)
            setattr(self, name, MethodType(key, self))

        def _element_regester(self, name, e):
            if hasattr(self, e):
                raise AttributeError(f'"{e}" is an attribute of "{self.__name__}", would not be regestered.')
            self._elements.append(e)
            setattr(self, name, e)

        cls.regester_operator = _regester_operator
        cls.regester_element = _regester_element

        return cls
