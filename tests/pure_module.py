import functools
import math
import typing
from dataclasses import dataclass
from operator import add, sub
from typing import Tuple,List
VectorTuple=Tuple[float,float,float]
def dot(u:Tuple[float,float,float], v:Tuple[float,float,float])->float:
    """
    3D dot product
    @param u:
    @param v:
    @return: float
    """

    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]



def norm(v:Tuple[float,float,float])->float:
    """
    norm is a length of  vector
    @param v:
    @return:
    """
    return math.sqrt(dot(v, v))

def subvec(u:VectorTuple,v:VectorTuple)->VectorTuple:
    return u[0]-v[0],u[1]-v[1],u[2]-v[2]
def addvec(u:VectorTuple,v:VectorTuple)->VectorTuple:
    return u[0]+v[0],u[1]+v[1],u[2]+v[2]
def mulvec(u:VectorTuple,v:float)->VectorTuple:
    return u[0]*v,u[1]*v,u[2]*v
def dist(P:VectorTuple, Q:VectorTuple)->float:
    """
    distance is a norm of difference
    @param P: vector
    @param Q: vector
    @return: float
    True
    """
    return norm(subvec(P, Q))


def punit(vec: VectorTuple) -> VectorTuple:
    """pure unit implementation"""




    nv = norm(vec)
    return vec[0] / nv, vec[1] / nv, vec[2] / nv


def cross(a:VectorTuple, b: VectorTuple) -> VectorTuple:
    """pure cross product implementation"""


    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]


def pangle(a: VectorTuple, b: VectorTuple) -> float:
    """pure angle implementation"""
    return math.acos(dot(punit(a), punit(b)))





@dataclass
class Vector:
    x:float
    y:float
    z:float
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z



    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __copy__(self)->'Vector':
        return Vector(vec=self.tuple())

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __len__(self) -> int:
        return 3

    def tuple(self) -> VectorTuple:
        return (self.x, self.y, self.z)

    def __getitem__(self, item: int) -> float:
        return self.tuple()[item]

    def __setitem__(self, item: int, val: float) -> float:
        if item == 0:
            self.x = val
        elif item == 1:
            self.y = val
        else:
            self.z = val

    def dot(self, other:'Vector')->float:
        return dot(self.tuple(),other.tuple())
    def cross(self, other:'Vector')->'Vector':
        return Vector(cross(self.tuple(),other.tuple()))
    def dist(self, other:'Vector')->float:
        return dist(self.tuple(),other.tuple())
    def angle(self, other:'Vector')->float:
        return pangle(self.tuple(), other.tuple())
    def unit(self)->'Vector':

        return Vector(unit(self.tuple()))

    def norm(self) -> float:

        return norm(self.tuple())
class Line:
    start: VectorTuple
    end: VectorTuple

    def __init__(self, start: VectorTuple, end:VectorTuple):
        self.start = start
        self.end = end

    @property
    def direction(self) -> VectorTuple:

        res = subvec(self.end, self.start)
        return res
    @property
    def unit(self) -> VectorTuple:
        return unit(self.direction)

    @property
    def length(self) -> float:
        return norm(self.direction)

    def __call__(self, t: List[float]) -> List[VectorTuple]:

        return [addvec(self.start ,mulvec(self.direction,u)) for u in t]
    def __repr__(self):
        return f'Line({self.start}, {self.end})'
    @property
    def a(self):
        return self.direction[0]

    @property
    def b(self):
        return self.direction[1]

    @property
    def c(self):
        return self.direction[2]
