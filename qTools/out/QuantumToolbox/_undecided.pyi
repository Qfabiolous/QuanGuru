from .customTypes import Matrix as Matrix, floatList as floatList, matrixList as matrixList
from .functions import expectation as expectation
from .linearAlgebra import hc as hc
from numpy import ndarray as ndarray
from typing import Any

def expectationKetList(operator: Matrix, kets: matrixList) -> floatList: ...
def expectationMatList(operator: Matrix, denMats: matrixList) -> floatList: ...
def expectationColArr(operator: Matrix, states: ndarray) -> floatList: ...
def fidelityKetList(ket1: Matrix, ketList: matrixList) -> floatList: ...
def fidelityKetLists(zippedStatesList: Any) -> floatList: ...
