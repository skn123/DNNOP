"""Base class for an Algorithm. The placeholder methods here are meant to guide
the developer, to make the class extendable intuitively.

This is a somewhat useless class, just like the model class. There is not much
that is shared among all algorithms to justify having a class.

Candidate for removal.
"""
import torch

class Interrogator(object):
    def __init__(self):
        self.inference = None
        self.chain = []

    def set_inference(self, model, env, test=False):
        """This method runs inference on the given environment using the models.
        I'm not sure, but I think there could be many ways to run inference. For
        that reason, I designate this function, to be a single point of contact
        for running inference, in whatever way the user/problem requires.
        """
        if not test:
            # Training
            self.inference = model(env.observation)
        else:
            # Testing
            model.eval()  # Turn on evaluation mode
            inferences = [model(x_t.cuda()) for x_t in env.test_data]
            self.inference = torch.cat(inferences)

    def set_inference_chain_(self, model, env, test=False):
        """This method runs inference on the given environment using the models.
        I'm not sure, but I think there could be many ways to run inference. For
        that reason, I designate this function, to be a single point of contact
        for running inference, in whatever way the user/problem requires.
        """
        if not test:
            # Training
            self.inference = model(env.observation)
            self.chain.append(self.inference)
        else:
            # Testing
            model.eval()  # Turn on evaluation mode
            self.inference = model(env.test_data)

    def get_var(self, chain=False):
        if chain:
            x = torch.cat(self.chain)
            var = x.var()
        else:
            var = self.inference.var()
        return var

    def get_mean(self, chain=False):
        if chain:
            x = torch.cat(self.chain)
            mean = x.mean()
        else:
            mean = self.inference.mean()
        return mean

    def print_inference(self):
        """Prints the inference of the neural networks. Attempts to extract
        the output items from the tensors.
        """
        if len(self.inference) == 1:
            x = self.inferences.item()
        elif len(self.inference) == 2:
            x = (self.inference[0].item(), self.inference[1].item())
        else:
            x = [a.item() for a in self.inference]
        print("Inference: ", x)

    def get_inference(self, model, observation):
        inference = model(observation)
        return inference

    def reset_state(self):
        self.inference = None
        self.chain = []
#
