'''Module which contains all Promethee preference curves'''

from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

class Curve(ABC):
    '''Abstract preference curve'''
    @abstractmethod
    def compute_preference_degree(self, preference_value):
        '''Compute preference degree'''

class CurvaUsual(Curve):
    '''Usual preference curve'''
    def compute_preference_degree(self, preference_value):
        if preference_value <= 0:
            degree = 0
        else:
            degree = 1
        return degree

class CurvaUShape(Curve):
    '''U-Shape preference curve'''
    q: float

    def __init__(self, q: float) -> None:
        self.q = q

    def compute_preference_degree(self, preference_value):
        if preference_value <= self.q:
            degree = 0
        else:
            degree = 1

        if degree < 0:
            degree = 0

        return degree

@dataclass
class CurvaVShape(Curve):
    '''V-Shape preference curve'''
    p: float

    def compute_preference_degree(self, preference_value):
        if preference_value <= self.p:
            degree = round((preference_value/self.p), 3)
        else:
            degree = 1

        if degree < 0:
            degree = 0

        return degree

@dataclass
class CurvaLevel(Curve):
    '''Level preference curve'''
    p: float
    q: float

    def compute_preference_degree(self, preference_value):
        if preference_value <= self.q:
            degree = 0
        elif preference_value > self.q and preference_value <= self.p:
            degree = 0.5
        else:
            degree = 1

        if degree < 0:
            degree = 0

        return degree

@dataclass
class CurvaVShapeI(Curve):
    '''V-Shape I preference curve'''
    p: float
    q: float

    def compute_preference_degree(self, preference_value):
        if preference_value <= self.q:
            degree = 0
        elif preference_value > self.q and preference_value <= self.p:
            degree = round(((preference_value-self.q)/(self.p-self.q)), 3)
        else:
            degree = 1

        if degree < 0:
            degree = 0

        return degree

@dataclass
class CurvaGaussian(Curve):
    '''Gaussian preference curve'''
    s: float

    def compute_preference_degree(self, preference_value):
        if preference_value <= 0:
            degree = 0
        else:
            degree = round(
                (1 - (math.e ** ((-((preference_value)**2))/(2*(self.s ** 2))))), 3)

        if degree < 0:
            degree = 0

        return degree
