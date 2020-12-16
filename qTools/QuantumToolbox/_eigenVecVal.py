import numpy as np # type: ignore
import scipy.linalg as lina # type: ignore
from scipy.sparse import spmatrix # type: ignore

from .functions import fidelityPure

from .customTypes import Matrix, floatList, matrixList


def _eigs(Mat: Matrix) -> tuple:
    r"""
    Calculate eigenvalue and eigenvectors of a given matrix.

    Parameters
    ----------
    Mat : Matrix
        a matrix

    Returns
    -------
    tuple
        tuple containing (eigenvalues, eigenvectors)
    """
    if isinstance(Mat, spmatrix):
        Mat = Mat.A
    return lina.eig(Mat)

def _eigStat(Mat: Matrix, symp: bool = False) -> floatList:
    r"""
    Calculate amplitudes of eigenvalue entries for a given matrix.

    Parameters
    ----------
    Mat : Matrix
        a matrix
    symp : bool, optional
        If True (False)

    Returns
    -------
    floatList
        [description]
    """
    return (np.abs(_eigs(Mat)[1].flatten()))**2 if not symp else _eigStatSymp(Mat)

def _eigStatSymp(Mat: Matrix) -> floatList:
    vecsSymplectic = _eigs(Mat)[1]
    return _eigsStatEigSymp(vecsSymplectic)

def _eigStatEig(EigVecs: Matrix, symp=False) -> floatList:
    return (np.abs(EigVecs.flatten()))**2 if not symp else _eigsStatEigSymp(EigVecs)

def _eigsStatEigSymp(EigVecs: Matrix) -> floatList:
    componentsSymplectic = []
    dims = EigVecs.shape[0]
    for ind in range(dims):
        elSymplectic = 0
        for _ in range(int(dims/2)):
            p1Symplectic = (np.abs(EigVecs[:, ind][elSymplectic]))**2
            p2Symplectic = (np.abs(EigVecs[:, ind][elSymplectic+1]))**2
            elSymplectic += 2
            componentsSymplectic.append(p1Symplectic+p2Symplectic)
    return componentsSymplectic

# TODO create the function for the result of eigenvec calculation
def eigVecStatKet(basis: matrixList, ket: Matrix) -> floatList:
    r"""
    Calculates components of a `ket` in a basis.

    Main use is in eigenvector statistics.

    Parameters
    ----------
    basis : matrixList
        a complete basis
    ket : Matrix
        the ket state

    Returns
    -------
    floatList
        `list` of component values in the basis

    Examples
    --------
    >>> import qTools.QuantumToolbox.states as qStates
    >>> ket = qStates.basis(2, 1)
    >>> completeBasis = qStates.completeBasis(dimension=2)
    >>> components = eigVecStatKet(basis=completeBasis, ket=ket)
    [0, 1]
    """

    comps = []
    for basKet in basis:
        comps.append(fidelityPure(basKet, ket))
    return comps

def eigVecStatKetNB(ket: Matrix) -> float:
    r"""
    Calculates component amplitudes of a ket.

    Parameters
    ----------
    ket : Matrix
        a ket state or list of ket states

    Returns
    -------
    return: float
        list of components

    Examples
    --------
    >>> import qTools.QuantumToolbox.states as qStates
    >>> ket = qStates.basis(2, 1)
    >>> completeBasis = qStates.completeBasis(dimension=2)
    >>> components = eigVecStatKetNB(ket=ket)
    [0 1]
    """

    # TODO Find a way around this
    if isinstance(ket, spmatrix):
        ket = ket.A
    return np.real(ket.flatten())