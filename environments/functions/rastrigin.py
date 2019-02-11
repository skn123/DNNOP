"""Implementation of the Rastrigin function as in the link below. The number of
problem dimensions is arbitrary, as well as the bounds.
https://www.sfu.ca/~ssurjano/rastr.html
"""
from .function import Function
import numpy as np

class Rastrigin(Function):
    def __init__(self, plot):
        super().__init__(plot)
        self.x = None  # NP array
        self.symmetrical = True  # Symmetrical function about the X1,X2 axes
        self.x_low = -5.12
        self.x_high = 5.12
        self.optimal_x = [0, 0]  # Location
        self.resolution = 250
        self.z = None  # Function evaluation
        self.set_observation()
        self.set_domain()
        self.set_range()
        self.init_plot()

    def get_func(self):
        a = 10*2
        b = np.square(self.x[0]) - 10*np.cos(2*np.pi*self.x[0])
        c = np.square(self.x[1]) - 10*np.cos(2*np.pi*self.x[1])
        d = b + c
        return a + d

    def evaluate(self, x):
        self.x = x
        self.z = self.get_func()

    def step(self):
        pass

    def plot(self, elite, anchors, probes, blends):
        pass








        #
