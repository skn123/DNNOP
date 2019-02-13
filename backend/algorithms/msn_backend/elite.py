"""base class for elite"""

import copy

class Elite:
    def __init__(self, hp):
        self.model = []
        self.elite_score = hp.initial_score
        self.minimizing = hp.minimizing
        self.elite_idx = 0

    def set_elite(self, pool, analyzer):
        idx = analyzer.top_idx
        pool_top_score = analyzer.new_top
        if self.replace(pool_top_score):
            print ("------Setting new Elite-------")
            elite = pool[idx]
            self.clone_model(elite)
            self.elite_score = pool_top_score
            self.elite_idx = idx
        print ("Elite Score: %f" %self.elite_score)

    def replace(self, pool_top_score):
        if self.minimizing:
            return pool_top_score < self.elite_score
        else:
            return pool_top_score > self.elite_score

    def clone_model(self, elite):
        """We clone the elite in order to have our own copy of it, not just a
        pointer to the object. This will be important because we want to
        keep the elite outside of the pool. Only when backtracking do we insert
        the elite into the pool.
        """
        print("Cloning elite model")
        self.model = copy.deepcopy(elite)
