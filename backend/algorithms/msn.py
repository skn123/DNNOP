"""It is expected that the hyper_params object passed to the class is compatible
with the chosen algorithm. Thus, since MSN is chosen here, it is expected that
the hyper_params object will contain the expected information/params in the
expected locations.

We need to create an optimizer object. This object will be initialized with the
desired hyper parameters. An example of hyper params is the number of Anchors.
The optimizer object will own the pool.?
"""
import torch
import torch.nn.functional as F
from .msn_backend.optimizer import Optimizer

class MSN:
    def __init__(self, pool, hyper_params, optimizer):
        print ("Using MSN algorithm")
        self.pool = pool
        self.pool_size = len(pool)
        self.optim = optimizer
        self.train_loss = 0.
        self.test_loss = 0.
        self.train_acc = 0.
        self.test_acc = 0.
        self.correct_test_preds = 0
        self.hyper_params = hyper_params
        self.scores = []
        self.set_optimizer()

    def set_optimizer(self):
        """If the user gives an optimizer, then use it. Otherwise, use the
        default MSN optimizer.
        The given optimizer has to contain the required methods for the MSN
        algorithm to function, for example inference().
        """
        if self.optim == None:
            self.optim = Optimizer(self.pool, self.hyper_params)
        else:
            self.optim = self.optim

    def optimize(self, env):
        """This method takes in the environment, runs the models against it,
        obtains the scores and accordingly updates the models.
        """
        outputs = self.optim.inference(env.x)
        if env.loss:
            if env.loss_type == 'NLL loss':
                self.train_loss = F.nll_loss(outputs, env.y)
                print(self.train_loss)
                print("Loss: %f" %self.train_loss)
            else:
                print("Unknown loss type")
                exit()
            self.scores = self.optim.calculate_scores(self.train_loss)
        else:
            self.scores = self.optim.calculate_scores(outputs)
        self.optim.update(self.scores)

    def test(self, env):
        """This is a method for testing."""
        outputs = self.optim.inference(env.x_t, test=True)
        if env.loss:
            if env.loss_type == 'NLL loss':
                self.test_loss = F.nll_loss(outputs, env.y_t, reduction='sum').item()
                pred = predictions.max(1, keepdim=True)[1]
                self.correct_test_preds = pred.eq(env.y_t.view_as(pred)).sum().item()
            else:
                print("Unknown loss type")
                exit()
        else:
            self.scores = self.optim.calculate_scores(outputs)

    def achieved_target(self):
        if self.hyper_params.minimizing:
            return self.test_loss <= self.optim.hp.target_loss
        else:
            return self.test_loss >= self.optim.hp.target_loss





#
