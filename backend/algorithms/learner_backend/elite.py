"""Base class for elite."""

import copy

class Elite(object):
    def __init__(self, hp):
        self.model = None
        self.elite_score = hp.initial_score
        self.minimizing = hp.minimizing

    def set_elite(self, model, analyzer):
        """Checks current top score and determines if there's a new elite. The
        elite is then either updated or set as is.
        """
        score = analyzer.score
        if self.replace(score):
            print ("------Setting new Elite-------")
            self.clone_model(model)
            self.elite_score = score
        print ("Elite Score: %f" %self.elite_score)

    def replace(self, score):
        """Assesses whether a new elite will replace the current one or not."""
        if self.minimizing:
            return score < self.elite_score
        else:
            return score > self.elite_score

    def clone_model(self, model):
        """We clone the elite in order to have our own copy of it, not just a
        pointer to the object. This will be important because we want to
        keep the elite outside of the pool. Only when backtracking do we insert
        the elite into the pool.
        """
        print("Cloning elite model")
        self.model = copy.deepcopy(model)

    def get_elite(self, observation):
        inference = self.model(observation)
        return inference
