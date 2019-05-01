"""base class for pool
The pool object will contain the models under optimization.
"""
import torch

class Converter(object):
    def __init__(self, weights):
        self.model = model
        self.hp = hyper_params
        self.state_dict = {} # Weights dictionary
        self.vector = None # Parameter vector
        self.nb_layers = 0
        self.shapes = []
        self.num_elems = []
        self.keys = []
        self.set_state_dict()
        self.set_shapes(self.state_dict)
        self.set_vector()

    def convert(self, weights, mode):
        """It is always assumed that the dict and the vector belong to the same
        model.
        """
        if mode == 'dict2vec':
            self.set_shapes(weights)
            self.set_vector()
        elif mode == 'vec2dict':
            pass
        else:
            print("Unknown conversion mode, exiting!")
            exit()

    def set_shapes(self, dict):
        """We only call this method once since all the pool models are the same
        shape.
        Traverse the dictionary and acquire the shapes.
        """
        self.nb_layers = len(dict)
        for i, key in enumerate(dict):
            x = dict[key]  # Get tensor of parameters
            self.shapes.append(x.size())
            self.num_elems.append(x.numel())
            self.keys.append(key)

    def set_vector(self):
        """Changes the dictionary of weights into a vector."""
        dict = self.state_dict
        mylist = []
        for i, key in enumerate(dict):
            x = dict[key]  # Get tensor of parameters
            mylist.append(x.reshape(x.numel()))  # Flatten tensor
        self.vector = torch.cat(mylist)  # Flatten all tensors in model

    def update_model(self, vector):
        """Updates the weight dictionaries of the models."""
        param_list = self.vec_to_tensor(vector)  # Restore shape
        self.update_dict(param_list)
        # Update model's state dictionary
        self.model.load_state_dict(self.state_dict)

    def vec_to_tensor(self, vec):
        """Changes a vector into a tensor using the original network shapes."""
        a = vec.split(self.num_elems)  # Split parameter tensors
        b = [None]*self.nb_layers
        for i in range(self.nb_layers):
            b[i] = a[i].reshape(self.shapes[i])  # Reconstruct tensor shape
        return b

    def update_dict(self, param_list):
        """Updates the state dictionary class attribute."""
        for i, key in enumerate(self.keys):
            self.state_dict[key] = param_list[i]






#