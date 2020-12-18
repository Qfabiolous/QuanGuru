from .customTypes import Matrix as Matrix
from .operators import identity as identity, sigmax as sigmax, sigmay as sigmay, sigmaz as sigmaz

def xRotation(angle: float, sparse: bool=...) -> Matrix: ...
def yRotation(angle: float, sparse: bool=...) -> Matrix: ...
def zRotation(angle: float, sparse: bool=...) -> Matrix: ...
def qubRotation(xyz: str, angle: float, sparse: bool=...) -> Matrix: ...