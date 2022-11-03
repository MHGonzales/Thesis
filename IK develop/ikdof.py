import numpy as np

# the robotics toolbox provides robotics specific functionality
import roboticstoolbox as rtb

# spatial math provides objects for representing transformations
import spatialmath as sm

# ansitable is a great package for printing tables in a terminal
from ansitable import ANSITable

# python mechanisms to create abstract classes
from abc import ABC, abstractmethod

# a package for creating dynamic progress bars
from progress.bar import Bar

# swift is a lightweight browser-based simulator which comes with the toolbox
from swift import Swift

# spatialgeometry is a utility package for dealing with geometric objects
import spatialgeometry as sg

# provides sleep functionaly
import time

class IK(ABC):
   

    def __init__(
        self,
        name: str = "IK Solver",
        ilimit: int = 30,
        slimit: int = 100,
        tol: float = 1e-6,
        we: np.ndarray = np.ones(6),
        problems: int = 1000,
    ):
        
        # Solver parameters
        self.name = name
        self.slimit = slimit
        self.ilimit = ilimit
        self.tol = tol
        self.We = np.diag(we)

        # Solver results
        self.success = np.zeros(problems)
        self.searches = np.zeros(problems)
        self.iterations = np.zeros(problems)

        # initialise with NaN
        self.searches[:] = np.nan
        self.iterations[:] = np.nan
        self.success[:] = np.nan

    def solve(self, ets: rtb.ETS, Tep: np.ndarray, q0: np.ndarray):
       
        # Iteration count
        i = 0
        total_i = 0

        for search in range(self.slimit):
            q = q0[search].copy()
            
            while i <= self.ilimit:
                i += 1

                # Attempt a step
                # try:
                E, q = self.step(ets, Tep, q)
                # except np.linalg.LinAlgError:
                #     i = np.nan
                #     break

                # Check if we have arrived
                if E < self.tol:
                    return q, True, total_i + i, search + 1, E

            total_i += i
            i = 0

        # If we make it here, then we have failed
        return q, False, np.nan, np.nan, E

    def error(self, Te: np.ndarray, Tep: np.ndarray):
       
        e = rtb.angle_axis(Te, Tep)
        E = 0.5 * e @ self.We @ e

        return e, E

    @abstractmethod
    def step(self, ets: rtb.ETS, Tep: np.ndarray, q: np.ndarray):
       
        pass

class NR(IK):
    def __init__(self, pinv=False, **kwargs):
        super().__init__(**kwargs)
        self.pinv = pinv

        self.name = f"NR (pinv={pinv})"

    def step(self, ets: rtb.ETS, Tep: np.ndarray, q: np.ndarray):
        Te = ets.eval(q)
        e, E = self.error(Te, Tep)

        J = ets.jacob0(q)

        if self.pinv:
            q += np.linalg.pinv(J) @ e
        else:
            q += np.linalg.inv(J) @ e

        return E, q