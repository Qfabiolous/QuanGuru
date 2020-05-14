import numpy as np
import qTools.QuantumToolbox.evolution as lio
from qTools.QuantumToolbox.operators import identity
from qTools.classes.computeBase import _parameter, qBaseSim
from qTools.classes.updateBase import updateBase
from qTools.classes.QUni import qUniversal

# under construction

class genericProtocol(qBaseSim):
    instances = 0
    label = 'genericProtocol'
    numberOfExponentiations = 0

    @classmethod
    def _increaseExponentiationCount(cls):
        cls.numberOfExponentiations += 1

    __slots__ = ['__lastState', '__inProtocol', '__fixed', '__ratio', '__updates', '_funcToCreateUnitary']

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None), _internal=kwargs.pop('_internal', False))
        self.__lastState = _parameter()
        self.__inProtocol = False
        self.__fixed = False
        self.__ratio = 1
        self.__updates = []
        self._funcToCreateUnitary = None
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    @property
    def lastState(self):
        return self._genericProtocol__lastState.value

    @lastState.setter
    def lastState(self, inp):
        self._genericProtocol__lastState.value = inp

    @property
    def initialState(self):
        if self.simulation._stateBase__initialState.value is None: # pylint: disable=protected-access
            try:
                self.simulation._stateBase__initialState.value =\
                    self.superSys._initialState(self.simulation._initialStateInput) # pylint: disable=W0212, E1101
            except: # pylint: disable=bare-except
                self.simulation._stateBase__initialState.value = self.superSys.initialState # pylint:disable=W0212,E1101
        return self.simulation._stateBase__initialState.value # pylint: disable=protected-access

    @initialState.setter # pylint: disable=no-member
    def initialState(self, inp):
        self.simulation._stateBase__initialStateInput.value = inp # pylint: disable=protected-access
        self.simulation._stateBase__initialState.value = self.superSys._initialState(inp) # pylint:disable=W0212,E1101

    def save(self):
        saveDict = super().save()
        stepsDict = {}
        for sys in self.subSys.values():
            stepsDict[sys.name] = sys.save()
        saveDict['steps'] = stepsDict
        return saveDict

    def _runCreateUnitary(self):
        pass

    def getUnitary(self, callAfterUpdate=_runCreateUnitary):
        for update in self._genericProtocol__updates:
            update.setup()
        callAfterUpdate(self)
        for update in self._genericProtocol__updates:
            update.setback()

    def createUpdate(self, **kwargs):
        update = Update(**kwargs)
        self.addUpdate(update)
        return update

    def addUpdate(self, *args):
        for update in args:
            self._genericProtocol__updates.append(update) # pylint: disable=no-member

    @property
    def updates(self):
        return self._genericProtocol__updates

    @property
    def ratio(self):
        return self._genericProtocol__ratio

    @ratio.setter
    def ratio(self, val):
        self._genericProtocol__ratio = val # pylint: disable=assigning-non-slot

    @property
    def system(self):
        return self.superSys

    @system.setter
    def system(self, supSys):
        self.superSys = supSys # pylint: disable=no-member

    def prepare(self):
        if self.fixed is True:
            self.getUnitary()

        for step in self.subSys.values():
            if isinstance(step, genericProtocol):
                step.prepare()

    @property
    def fixed(self):
        return self._genericProtocol__fixed

    @fixed.setter
    def fixed(self, boolean):
        self._genericProtocol__fixed = boolean # pylint: disable=assigning-non-slot

    @qBaseSim.superSys.setter # pylint: disable=no-member
    def superSys(self, supSys):
        qBaseSim.superSys.fset(self, supSys) # pylint: disable=no-member
        supSys._paramBoundBase__paramBound[self.name] = self # pylint: disable=protected-access
        self.simulation._bound(supSys.simulation) # pylint: disable=protected-access
        self.simulation._qUniversal__subSys[self] = self.superSys # pylint: disable=protected-access

    @property
    def unitary(self):
        if self._paramBoundBase__matrix is not None: # pylint: disable=no-member
            if ((self.fixed is True) or (self._paramUpdated is False)):
                unitary = self._paramBoundBase__matrix # pylint: disable=no-member
            else:
                unitary = self.getUnitary() # pylint: disable=assignment-from-no-return
                self._paramBoundBase__paramUpdated = False  # pylint: disable=assigning-non-slot
        else:
            self._paramBoundBase__paramUpdated = False  # pylint: disable=assigning-non-slot
            unitary = self.getUnitary() # pylint: disable=assignment-from-no-return
        return unitary

class qProtocol(genericProtocol):
    instances = 0
    label = 'qProtocol'

    __slots__ = []
    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None))
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    @property
    def steps(self):
        return self._qUniversal__subSys # pylint: disable=no-member

    @steps.setter
    def steps(self, stps):
        self.addStep(*stps)

    def addStep(self, *args):
        '''
            Copy step ensures the exponentiation
        '''
        for step in args:
            self._paramBoundBase__paramBound[step.name] = step # pylint: disable=no-member
            if step._genericProtocol__inProtocol:
                super().addSubSys(copyStep(step))
            else:
                super().addSubSys(step)
                step._genericProtocol__inProtocol = True
                step._genericProtocol__lastState._bound = self._genericProtocol__lastState #pylint:disable=W0212,E1101
                step.simulation._bound(self.simulation, re=True) # pylint: disable=protected-access
                if step.superSys is None:
                    step.superSys = self.superSys

    def createStep(self, n=1):
        newSteps = []
        for _ in range(n):
            newSteps.append(super().createSubSys(Step()))
        return newSteps if n > 1 else newSteps[0]

    def _runCreateUnitary(self):
        super()._runCreateUnitary()
        unitary = identity(self.superSys.dimension) # pylint: disable=no-member
        for step in self.steps.values():
            unitary = step.getUnitary() @ unitary
        self._paramBoundBase__matrix = unitary # pylint: disable=assigning-non-slot

    def getUnitary(self, callAfterUpdate=_runCreateUnitary):
        super().getUnitary(callAfterUpdate=callAfterUpdate)
        return self._paramBoundBase__matrix # pylint: disable=no-member


class Step(genericProtocol):
    instances = 0
    label = 'Step'

    __slots__ = []

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None), _internal=kwargs.pop('_internal', False))
        self._funcToCreateUnitary = None
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    def _runCreateUnitary(self):
        super()._runCreateUnitary()
        self.createUnitary() # pylint: disable=assigning-non-slot

    def getUnitary(self, callAfterUpdate=_runCreateUnitary):
        if ((self.fixed is True) and (self._paramBoundBase__matrix is None)): # pylint: disable=no-member
            super().getUnitary(callAfterUpdate=callAfterUpdate)
        elif ((self.fixed is False) and ((self._paramUpdated is True) or (self._paramBoundBase__matrix is None))): # pylint: disable=no-member, line-too-long
            super().getUnitary(callAfterUpdate=callAfterUpdate)
        self._paramBoundBase__paramUpdated = False # pylint: disable=assigning-non-slot
        return self._paramBoundBase__matrix # pylint: disable=no-member

    def createUnitary(self):
        if not callable(self._funcToCreateUnitary):
            raise TypeError('?')
        self._paramBoundBase__matrix = self._funcToCreateUnitary() # pylint: disable=assigning-non-slot
        return self._paramBoundBase__matrix # pylint: disable=no-member

class copyStep(qUniversal):
    instances = 0
    label = 'copyStep'

    __slots__ = []

    def __init__(self, superSys, **kwargs):
        super().__init__(name=kwargs.pop('name', None))
        self.superSys = superSys
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    def save(self):
        saveDict = super().save()
        saveDict['superSys'] = self.superSys.name
        return saveDict

    def getUnitary(self):
        return self.superSys.unitary

class freeEvolution(Step):
    instances = 0
    _nonInternalInstances = 0
    _internalInstances = 0
    label = 'freeEvolution'

    __slots__ = []

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None), _internal=kwargs.pop('_internal', False))
        self._funcToCreateUnitary = self.matrixExponentiation
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    def matrixExponentiation(self):
        self._increaseExponentiationCount()
        unitary = lio.LiouvillianExp(2 * np.pi * self.superSys.totalHam, # pylint: disable=no-member
                                     timeStep=((self.simulation.stepSize*self.ratio)/self.simulation.samples))
        self._paramBoundBase__matrix = unitary # pylint: disable=assigning-non-slot
        return unitary

class Gate(Step):
    instances = 0
    label = 'Gate'

    __slots__ = ['__implementation']

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None))
        self.__implementation = None
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    @Step.superSys.setter # pylint: disable=no-member
    def superSys(self, supSys):
        Step.superSys.fset(self, supSys) # pylint: disable=no-member
        self.addSubSys(supSys)

    @property
    def system(self):
        return list(self.subSys.values())

    @system.setter
    def system(self, sys):
        if not isinstance(sys, list):
            sys = [sys]
        for s in tuple(*[sys]):
            self.addSubSys(s)
        self.superSys = tuple(sys)[0]

    def addSys(self, sys):
        self.system = sys

    @property
    def implementation(self):
        return self._Gate__implementation

    @implementation.setter
    def implementation(self, typeStr):
        self._Gate__implementation = typeStr # pylint: disable=assigning-non-slot

class Update(updateBase):
    instances = 0
    label = 'Update'

    toBeSaved = qUniversal.toBeSaved.extendedCopy(['value'])

    __slots__ = ['value', '__memoryValue', 'setup', 'setback']

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.pop('name', None))
        self.value = None
        self.setup = self._setup
        self.setback = self._setback
        self.__memoryValue = None
        self._qUniversal__setKwargs(**kwargs) # pylint: disable=no-member

    @property
    def memoryValue(self):
        return self._Update__memoryValue

    @memoryValue.setter
    def memoryValue(self, value):
        self._Update__memoryValue = value # pylint: disable=assigning-non-slot

    def _setup(self):
        self._Update__memoryValue = getattr(list(self.subSys.values())[0], self.key) # pylint:disable=assigning-non-slot
        for sys in self.subSys.values():
            if self._Update__memoryValue != getattr(sys, self.key): # pylint: disable=assigning-non-slot
                raise ValueError('?')

        if self.value != self.memoryValue:
            super()._runUpdate(self.value)

    def _setback(self):
        if self.value != self.memoryValue:
            super()._runUpdate(self._Update__memoryValue)
