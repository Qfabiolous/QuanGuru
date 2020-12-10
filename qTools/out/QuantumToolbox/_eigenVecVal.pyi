from .customTypes import Matrix as Matrix, floatList as floatList, matrixList as matrixList
from .functions import fidelityPure as fidelityPure
from typing import List

def eigVecStatKet(basis: matrixList, ket: Matrix) -> floatList: ...
def eigVecStatKetList(basis: matrixList, kets: matrixList) -> List[floatList]: ...
def eigVecStatKetNB(ket: Matrix) -> float: ...
