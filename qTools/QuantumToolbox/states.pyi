"""
    Stub of functions to create and/or normalise quantum states
"""

from typing import Union, Dict, List
from numpy import ndarray
from scipy.sparse import spmatrix

def basis(dimension:int, state:int, sparse:bool=True) -> Union[spmatrix, ndarray]: ...

def basisBra(dimension:int, state:int, sparse:bool=True) -> Union[spmatrix, ndarray]: ...

def zeros(dimension:int, sparse:bool=True) -> Union[spmatrix, ndarray]: ...

def superPos(dimension:int, excitations:Union[Dict[int, float], List[int], int], sparse:bool=True) -> Union[spmatrix, ndarray]: ...

def densityMatrix(ket:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def normalise(state:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def normaliseKet(ket:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def normaliseMat(denMat:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def compositeState(dimensions:List[int], excitations:List[Union[Dict[int, float], List[int], int]], sparse:bool=True) -> Union[spmatrix, ndarray]: ...

def partialTrace(keep:Union[ndarray, List[int]], dims:Union[ndarray, List[int]], state:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def mat2Vec(densityMatrix:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...

def vec2mat(vec:Union[spmatrix, ndarray]) -> Union[spmatrix, ndarray]: ...