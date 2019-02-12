"""Class that defines all blend operations."""

from __future__ import division
from random import choices
import torch
import numpy as np

class Blends:
    def __init__(self, hp):
        self.hp = hp
        self.nb_blends = self.hp.pool_size-((self.hp.nb_anchors*self.hp.nb_probes))
        self.nb_anchors = 0  # State not hyperparameter
        self.models = []
        self.blends_idxs = []
        self.blend_type = "crisscross"  # Or "random choice"
        self.anchors = None
        self.analyzer = None
        self.vectors = []
        self.vec_length = 0
        self.compounds1 = []
        self.compounds2 = []
        self.indices = []

    def set_blends(self, anchors, vectors, analyzer, perturb):
        self.update_state(anchors, vectors, analyzer, perturb)
        if self.nb_blends>0:
            self.set_indices()
            self.set_compounds1()
            self.set_compounds2()
            self.blend()

    def update_state(self, anchors, vectors, analyzer, perturb):
        self.models = [] # Reset state
        self.anchors = anchors
        self.vectors = vectors
        self.analyzer = analyzer
        self.perturb = perturb
        self.vec_length = torch.numel(anchors.models[0])
        self.nb_anchors = len(anchors.models)
        self.nb_blends = self.hp.pool_size-(self.nb_anchors+(
                                    self.nb_anchors * self.hp.nb_probes))

    def set_indices(self):
        # In case I wanted a variable blending method
        #indices = random.sample(range(self.vec_length), self.analyzer.num_selections)
        #self.indices = random.sample(range(self.vec_length), self.vec_length/2)
        # I can select/determine a random sequence, and keep it for the iteration
        self.indices = np.arange(start=0, stop=self.vec_length, step=2)
        self.indices = torch.tensor(self.indices).cuda().long()

    def set_compounds1(self):
        # From anchors
        idxs = choices(range(self.nb_anchors), k=self.nb_blends)
        self.compounds1 = [self.anchors.models[i] for i in idxs]

    def set_compounds2(self):
        # From pool, i.e. vectors
        idxs = choices(range(self.hp.pool_size), k=self.nb_blends)
        self.compounds2 = [self.vectors[i] for i in idxs]

    def blend(self):
        for i in range(self.nb_blends):
            c1 = self.compounds1[i]
            c2 = self.compounds2[i]
            c1[self.indices] = c2[self.indices]
            blend = c1
            #p2 = torch.take(p2, self.indices)
            #p1.put_(self.indices, p2)  # Accumulate false
            self.perturb.apply(blend)
            self.models.append(blend)
