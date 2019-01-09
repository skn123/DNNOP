"""Base class for an Algorithm. The placeholder methods here are meant to guide
the developer, to make the class extendable intuitively.
"""
class Algorithm:
    def __init__(self, nb_models):
        self.nb_models = nb_models

    def optimize(self):
        """Placeholder method for performing an optimization step."""
        pass

    def test(self):
        """Placeholder method to perform tests/validation.
        """
        pass

    def reset_state(self):
        """Placeholder method in case the solver has need to reset its internal
        state.
        """
        pass