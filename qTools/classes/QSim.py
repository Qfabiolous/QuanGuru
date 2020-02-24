import numpy as np
import scipy.sparse as sp
import qTools.QuantumToolbox.states as qSt
from qTools.classes.QSys import QuantumSystem, qSystem
from qTools.classes.QUni import qUniversal
from qTools.classes.exceptions import sweepInitError
from qTools.classes.extensions.timeEvolve import runSimulation

""" under construction be careful """
class Sweep(qUniversal):
    instances = 0
    label = 'Sweep'
    __slots__ = ['sweepKey', 'sweepMax', 'sweepMin', 'sweepPert', '__sweepList', 'logSweep', '__lCount', 'sweepFunction']
    # TODO write exceptions if gone keep
    # FIXME enable this
    #@sweepInitError
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO make these properties so that sweepList is dynamic
        self.sweepKey = None
        self.sweepMax = None
        self.sweepMin = None
        self.sweepPert = None
        self.__sweepList = None
        self.logSweep = False
        self.__lCount = 0
        self.sweepFunction = None
        self._qUniversal__setKwargs(**kwargs)

    @property
    def sweepList(self):
        return self._Sweep__sweepList

    @sweepList.setter
    def sweepList(self, sList):
        if sList is None:
            if self.logSweep is False:
                self._Sweep__sweepList = np.arange(self.sweepMin, self.sweepMax + self.sweepPert, self.sweepPert)
            elif self.logSweep is True:
                self._Sweep__sweepList = np.logspace(self.sweepMin, self.sweepMax, num=self.sweepPert, base=10.0)
        else:
            self._Sweep__sweepList = sList

    @property
    def lCounts(self):
        self._Sweep__lCount += 1
        return self._Sweep__lCount-1

    @lCounts.setter
    def lCounts(self,val):
        self._Sweep__lCount = val

    def runSweep(self, ind):
        if self.sweepFunction is None:
            val = self.sweepList[ind]
            setattr(self.subSystems, self.sweepKey, val)
        else:
            self.sweepFunction(self, self.superSys.superSys)

    @qUniversal.subSystems.setter
    def subSystems(self, subS):
        self._qUniversal__subSys = subS


class qSequence(qUniversal):
    instances = 0
    label = '_sweep'
    __slots__ = ['__Sweeps', '__swCount']
    # TODO Same as previous 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__Sweeps = []
        self.__swCount = 0
        self._qUniversal__setKwargs(**kwargs)

    @property
    def sweeps(self):
        return self._qSequence__Sweeps

    @sweeps.setter
    def sweeps(self, sysDict):
        self._qSequence__Sweeps = {}
        for key, val in sysDict.items():
            self.addSweep(val, key)

    # TODO Change name to create
    def addSweep(self, sys, sweepKey, **kwargs):
        newSweep = Sweep(superSys=self, subSystems=sys, sweepKey=sweepKey, **kwargs)
        self._qSequence__Sweeps.append(newSweep)
        return newSweep

    @property
    def lCount(self):
        self._qSequence__swCount += 1
        return self._qSequence__swCount - 1

    @lCount.setter
    def lCount(self,val):
        self._qSequence__swCount = val


class Simulation(qUniversal):
    instances = 0
    label = 'Simulation'
    __compute = 0
    __slots__ = ['__qSys', '__stepSize', '__finalTime', 'states', 'beforeLoop', 'Loop', 'whileLoop', 'compute', '__sample', '__step', 'delState']
    # TODO Same as previous 
    def __init__(self, system=None, **kwargs):
        super().__init__(**kwargs)
        self.__qSys = None

        self.beforeLoop = qSequence(superSys=self)
        self.Loop = qSequence(superSys=self)
        self.whileLoop = qSequence(superSys=self)
        
        self.delState = False

        self.__finalTime = None
        self.__stepSize = 0.02
        self.__sample = 1
        self.__step = 1

        self.compute = None

        if ((system is not None) and ('qSys' in kwargs.keys())):
            print('Two qSys given')
        elif ((system is not None) and ('qSys' not in kwargs.keys())):
            kwargs['qSys'] = system
        self._qUniversal__setKwargs(**kwargs)
        if self.__qSys is None:
            self.__qSys = QuantumSystem()

    def __computeDel(self, qSys, state):
        if self.compute is not None:
            results = self.compute(self, state)
        del(state)
        return results

    def __compute(self, qSys, state):
        if self.compute is not None:
            results = self.compute(self, state)
        return results

    @property
    def finalTime(self):
        self.__finalTime

    @finalTime.setter
    def finalTime(self, fTime):
        self.steps = int(round(self.finalTime/self.stepSize))+1

    @property
    def steps(self):
        if len(self.whileLoop.sweeps) > 0:
            return len(self.whileLoop.sweeps[0].sweepList)
        else:
            return self._Simulation__step

    @steps.setter
    def steps(self, num):
        self._Simulation__step = num

    @property
    def samples(self):
        return self._Simulation__sample

    @samples.setter
    def samples(self, num):
        self._Simulation__sample = num

    def __del__(self):
        class_name = self.__class__.__name__

    @property
    def qSys(self):
        self._Simulation__qSys.superSys = self
        return self._Simulation__qSys

    @qSys.setter
    def qSys(self, val):
        """if isinstance(val, QuantumSystem):
            QuantumSystem.constructCompSys(val)"""
        self._Simulation__qSys = val

    @property
    def stepSize(self):
        return self._Simulation__stepSize

    @stepSize.setter
    def stepSize(self, stepsize):
        self._Simulation__stepSize = stepsize
    
    def run(self, p=None):
        if isinstance(self.qSys, QuantumSystem):
            # TODO Check first if constructed
            self.qSys.constructCompSys()
        
        self._Simulation__res(self.beforeLoop)
        self._Simulation__res(self.Loop)
        self._Simulation__res(self.whileLoop)
        '''statesList = [] 
        resultsList = []'''
        res = runSimulation(self, p)
        if self.delState is True:
            return res
        else:
            return res[0], res[1]

    @staticmethod
    def __res(seq):
        seq.lCount = 0
        for ind in range(len(seq.sweeps)):
            seq.sweeps[ind].lCounts = 0
