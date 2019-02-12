"""Base class for functions"""

import numpy as np
import torch
from .plotter import Plotter
from ..environment import Environment

class Function(Environment):
    def __init__(self, plot, precision):
        super().__init__(precision)
        self.plot = plot
        self.optimal_x = 0  # Location
        self.resolution = 50
        self.x_low = [0, 0]
        self.x_high = [0, 0]
        self.domain = []  # Matrix of coordinate vectors
        self.range = []  # Matrix of function values
        self.score = True

    def init_plot(self):
        if self.plot:
            self.plotter = Plotter(self)

    def set_observation(self):
        self.observation = [torch.tensor(
                            np.random.uniform(self.x_low, self.x_high, 2),
                            dtype=self.precision,
                            device = self.device),
                            self.x_low,
                            self.x_high]

    def set_domain(self):
        x1 = np.linspace(self.x_low[0], self.x_high[0], self.resolution)
        x2 = np.linspace(self.x_low[1], self.x_high[1], self.resolution)
        m1, m2 = np.meshgrid(x1, x2)
        self.domain = [m1, m2]

    def set_range(self):
        self.x = self.domain
        self.range = self.get_func()

    def construct_base(self):
        pass

    def evaluate(self, position):
        x1 = position[0].cpu().numpy()
        x2 = position[1].cpu().numpy()
        self.x = [x1, x2]
        self.z = self.get_func()
        return self.z

    def step(alg=None):
        #
        if alg is not None and self.plot:
            elite = alg.optim.pool.elite.query_elite(self.observation[0])
            elite_score = alg.optim.pool.elite.elite_score
            anchors = alg.inferences[alg.optim.pool.anchors.anchors_idxs]
            anchors_scores = alg.scores[alg.optim.pool.anchors.anchors_idxs]
            probes = alg.inferences[alg.optim.pool.probes.probes_idxs]
            probes_scores = alg.scores[alg.optim.pool.probes.probes_idxs]
            blends = alg.inferences[alg.optim.pool.blends.blends_idxs]
            blends_scores = alg.scores[alg.optim.pool.blends.blends_idxs]
            positions = {
                        "elite": elite,
                        "anchors": anchors,
                        "probes":probes,
                        "blends":blends}
            scores = {
                        "elite": elite,
                        "anchors": anchors,
                        "probes":probes,
                        "blends":blends}

    def plot(self, positions, scores):
        pass


#
