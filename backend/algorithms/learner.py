"""It is expected that the hyper_params object passed to the class is compatible
with the chosen algorithm. Thus, since Learner is chosen here, it is expected that
the hyper_params object will contain the expected information/params in the
expected locations.

We need to create an optimizer object. This object will be initialized with the
desired hyper parameters. An example of hyper params is the number of Anchors.
The optimizer object will own the pool.?
"""
from __future__ import division
import torch
import numpy as np
from .learner_backend.hyper_parameters import Hyper_Parameters
from .learner_backend.pool import Pool
from .learner_backend.optimizer import Optimizer
import time

class LEARNER(object):
    def __init__(self, models, alg_params):
        print ("Using Learner algorithm")
        self.hyper_params = Hyper_Parameters(alg_params) # Create a hyper parameters object
        self.pool = Pool(models, self.hyper_params) # Create a pool object
        self.optim = Optimizer(self.pool, self.hyper_params)  # Optimizer object
        self.pool_size = alg_params["pool size"]
        self.inferences = []
        self.scores = []
        self.correct_test_preds = 0

    def set_environment(self, env):
        """Sets the environment attribute."""
        self.env = env
        assert self.env is not None  # Sanity check
        if self.env.loss:
            self.scoring = "loss"
        if self.env.acc:
            self.scoring = "accuracy"
        if self.env.score:
            self.scoring = "score"
        if self.env.error:
            self.scoring = "error"
        self.optim.set_environment(env)

    def optimize(self):
        """This method takes in the environment, runs the models against it,
        obtains the scores and accordingly updates the models.
        """
        self.inference()
        self.optim.reset_state()
        if self.scoring == "loss":
            self.optim.calculate_losses(self.inferences)
        elif self.scoring == "accuracy":
            self.optim.calculate_correct_predictions(self.inferences, acc=True)
        elif self.scoring == "score" or self.scoring == "error":
            self.optim.calculate_scores(self.inferences)
        else:
            self.optim.set_scores(self.inferences)
        self.optim.step()

    def inference(self, test=False, silent=True):
        """This method runs inference on the given environment using the models.
        I'm not sure, but I think there could be many ways to run inference. For
        that reason, I designate this function, to be a single point of contact
        for running inference, in whatever way the user/problem requires.
        """
        with torch.no_grad():
            if not test:
                # Training
                inferences = []
                for model in self.pool.models:
                    inference = model(self.env.observation)
                    inferences.append(inference)
            else:
                # Testing
                model = self.pool.models[self.pool.anchors.anchors_idxs[0]]
                model.eval()  # Turn on evaluation mode
                inferences = model(self.env.test_data)
        self.inferences = inferences
        if not silent:
            self.print_inferences()

    def print_inferences(self):
        """Prints the inference of the neural networks. Attempts to extract
        the output items from the tensors.
        """
        print (self.inferences[0])
        print (len(self.inferences[0]))
        if len(self.inferences[0]) == 1:
            x = [a.item() for a in self.inferences]
        elif len(self.inferences[0]) == 2:
            x = [[a[0].item(), a[1].item()] for a in self.inferences]
        else:
            x = [[tensor_.item() for tensor_ in output_] for output_ in self.inferences]
        print("Inference: ", x)

    def test(self):
        """This is a method for testing."""
        assert self.env.test_data is not None  # Sanity check
        self.inference(test=True)
        self.optim.calculate_correct_predictions(self.inferences, test=True)
        self.correct_test_preds = self.optim.scores

    def print_test_accuracy(self):
        """Prints the accuracy figure for the test/validation case/set."""
        test_size = len(self.env.test_data)
        correct = self.correct_test_preds
        self.test_acc = 100.*correct/test_size
        if self.env.loss:
            loss = self.optim.test_loss  # Assuming minizming loss
            loss /= test_size  # Not really sure what this does
            print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)'.format(
                                    loss, correct, test_size, self.test_acc))
        else:
            print('\nTest set: Accuracy: {}/{} ({:.0f}%)'.format(
                                    correct, test_size, self.test_acc))

    def achieved_target(self):
        """Determines whether the algorithm achieved its target or not."""
        best = self.optim.pool.elite.elite_score
        if self.hyper_params.minimizing:
            return best <= (self.hyper_params.target + self.hyper_params.tolerance)
        else:
            return best >= (self.hyper_params.target - self.hyper_params.tolerance)

    def save_weights(self, path):
        for i, sample in enumerate(self.pool):
            fn = path+"model_"+str(i)+".pth"
            torch.save(sample.state_dict(), fn)
        fn = path+"model_elite.pth"
        torch.save(self.pool.elite.model.state_dict(), fn)












#
