"""It is expected that the hyper_params object passed to the class is compatible
with the chosen algorithm. Thus, since MSN is chosen here, it is expected that
the hyper_params object will contain the expected information/params in the
expected locations.

We need to create an optimizer object. This object will be initialized with the
desired hyper parameters. An example of hyper params is the number of Anchors.
"""
import torch
from .msn_backend import optimizer as optim
from .algorithm import Algorithm

class MSN(Algorithm):
    def __init__(self, pool, hyper_params, optimizer):
        print ("Using MSN algorithm")
        self.pool_size = len(pool)
        super().__init__(pool_size)
        self.pool = pool
        if optimizer == None:
            self.optimizer = optim(hyper_params)
        else:
            self.optimizer = optimizer

    def optimize(self, env):
        pass
