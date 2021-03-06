"""It is expected that the hyper_params object passed to the class is compatible
with the chosen algorithm. Thus, since Learner is chosen here, it is expected that
the hyper_params object will contain the expected information/params in the
expected locations.

We need to create an optimizer object. This object will be initialized with the
desired hyper parameters. An example of hyper params is the number of Anchors.
The optimizer object will own the pool.?
"""
from __future__ import division
from .algorithm import Algorithm
from .neuro1_backend.hyper_parameters import Hyper_Parameters
from .neuro1_backend.engine import Engine

class NEURO1(Algorithm):
    def __init__(self, model, alg_params):
        print ("Using Learner8 algorithm")
        super(NEURO1, self).__init__()
        self.model = model
        self.hyper_params = Hyper_Parameters(alg_params)
        self.engine = Engine(self.model.parameters(), self.hyper_params)
        self.populations = False
        self.grad = False
        self.minimizing = self.hyper_params.minimizing
        self.initial_score = self.hyper_params.initial_score
        self.top_score = self.initial_score
        self.target = None
        self.set_target()

    def set_target(self):
        if self.minimizing:
            self.target = self.hyper_params.target + self.hyper_params.tolerance
        else:
            self.target = self.hyper_params.target - self.hyper_params.tolerance

    def step(self, feedback):
        """This method takes in the environment, runs the models against it,
        obtains the scores and accordingly updates the models.
        """
        inference, score = feedback
        #print(inference)
        print(score.item())
        #score = self.regularize(score)
        self.engine.analyze(score, self.top_score)
        self.engine.set_elite()
        #self.engine.update_state()
        self.engine.update(self.model)
        self.update_top_score(score)

    def regularize(self, score):
        norm = self.engine.vector.norm()
        score = score+(0.01*norm)
        return score

    def update_top_score(self, score):
        """Analysis is still needed even if there's no improvement,
        so other modules know that this as well. Hence, can't "return" after
        initial condition.
        """
        if self.engine.jumped:
            self.top_score = score
        else:
            v = 0.00
            if self.minimizing and self.top_score>0.:
                self.top_score = self.top_score*(1.+v)
            elif self.minimizing and self.top_score<0.:
                self.top_score = self.top_score*(1.-v)
            elif not self.minimizing and self.top_score>0.:
                self.top_score = self.top_score*(1.-v)
            elif not self.minimizing and self.top_score<0.:
                self.top_score = self.top_score*(1.+v)

    def print_state(self):
        if self.engine.analyzer.replace:
            print ("------Setting new Elite-------")
        if self.engine.frustration.jump:
            print("------WOOOOOOHHOOOOOOOO!-------")
        if self.engine.analyzer.improved:
            print("Improved!")
        print ("Top Score: %f" %self.top_score)
        print("Memory: %d" %self.engine.frustration.count)
        print("Frustration: %f" %self.engine.frustration.tau)
        print("Integrity: %f" %self.engine.integrity.value)
        #print("Bin: ", self.engine.integrity.step_size.bin)
        #print("Step size: %f" %self.engine.integrity.step_size.value)
        #print("Selections: %d" %self.engine.noise.num_selections)





#
