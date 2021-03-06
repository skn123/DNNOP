"""Class factory for different models, also ensures that the desired precision
is chosen.
"""

from .cnn_mnist import Net as MNIST_CNN
from .cnn_fashionMNIST import Net as FashionMNIST_CNN
from .cnn_cifar10 import Net as CIFAR10_CNN
from .mnist_cnn_msn import Net as MNIST_CNN_MSN
from .func_fc import Net as FUNC_FC
from .nao_fc import Net as NAO_FC
from .dqn import Net as DQN
from .dqn_ram import Net as DQN_RAM
from .dqn_ram2 import Net as DQN_RAM2
from .dqn_ram3 import Net as DQN_RAM3
from .dqn_lstm_ram import Net as DQN_LSTM_RAM
from .dqn_spiking_ram import Net as DQN_SPIKING_RAM
from .roboschool_fc import Net as ROBOSCHOOL_FC
from .roboschool_simple_fc import Net as ROBOSCHOOL_SIMPLE_FC
from .neural_fc import Net as NEURAL_FC
from .sar_model import Net as SAR_MODEL

import torch
import torch.nn as nn
import numpy as np

def make_model(name, model_params={}):
    """Makes a single model."""
    model_params = ingest_params(model_params)
    if model_params["grad"]:
        model = pick_model(name, model_params)
    else:
        with torch.no_grad():
            model = pick_model(name, model_params)
    model.cuda()  # sends the model to GPU
    model.to(model_params["precision"])
    init_weights(model, model_params["weight initialization scheme"])
    if model_params["pre-trained"]:
        load_weights(model, model_params["elite path"])
    return model

def make_pool(name, model_params={}):
    """Makes a pool of models, without the "grad" parameters since no gradient
    is calculated when a pool is used (ie. evolutionary algorithms don't need
    to calculate gradients).
    """
    model_params = ingest_params(model_params)
    pool = []
    for _ in range(model_params["pool size"]):
        with torch.no_grad():
            model = pick_model(name, model_params)
            model.cuda().to(model_params["precision"])
            init_weights(model, model_params["weight initialization scheme"])
            pool.append(model)
    assert len(pool) == model_params["pool size"]  # Sanity check
    return pool

def ingest_params(user_params):
    """Creates a default parameters dictionary, overrides it if necessary
    with user selections and then returns the result.
    """
    default_params = {
                    "pool size": 50,
                    "precision": torch.float,
                    "weight initialization scheme": "Default",
                    "pre-trained": False,
                    "elite path": 'C:/model_elite.pth',
                    "grad": False
                    }
    default_params.update(user_params)  # Override with user choices
    return default_params

def pick_model(name, model_params):
    """Defines which class of models to pick, based on user input."""
    if name == "MNIST CNN":
        model = MNIST_CNN(model_params)
    elif name == "MNIST CNN MSN":
        model = MNIST_CNN_MSN(model_params)
    elif name == "FashionMNIST CNN":
        model = FashionMNIST_CNN(model_params)
    elif name == "CIFAR10 CNN":
        model = CIFAR10_CNN(model_params)
    elif name == "Function FC model":
        model = FUNC_FC(model_params)
    elif name == "NAO FC model":
        model = NAO_FC(model_params)
    elif name == "DQN RAM model":
        model = DQN_RAM(model_params)
    elif name == "DQN RAM2 model":
        model = DQN_RAM2(model_params)
    elif name == "DQN RAM3 model":
        model = DQN_RAM3(model_params)
    elif name == "DQN LSTM RAM model":
        model = DQN_LSTM_RAM(model_params)
    elif name == "DQN Spiking RAM model":
        model = DQN_SPIKING_RAM(model_params)
    elif name == "DQN model":
        model = DQN(model_params)
    elif name == "Roboschool FC":
        model = ROBOSCHOOL_FC(model_params)
    elif name == "Roboschool Simple FC":
        model = ROBOSCHOOL_SIMPLE_FC(model_params)
    elif name == "NEURAL FC":
        model = NEURAL_FC(model_params)
    elif name == "SAR model":
        model = SAR_MODEL(model_params)
    else:
        print("Unknown model selected")
        exit()
    return model

def init_weights(model, scheme):
    """Initializes the weights of the model according to a defined scheme."""
    if scheme == 'Uniform':
        model.apply(init_uniform)
    elif scheme == 'Normal':
        model.apply(init_normal)
    elif scheme == 'Integer':
        model.apply(init_integer)
    elif scheme == 'Identical':
        model.apply(init_eye)
    elif scheme == 'Constant':
        model.apply(init_constant)
    elif scheme == 'He':
        model.apply(init_he)
    elif scheme == 'Sparse':
        model.apply(init_sparse)
    elif scheme == 'Spiking':
        model.apply(init_uniform)
        model.apply(init_spiking)
    else:
        return  # Default initialization scheme

def init_uniform(m):
    """Initializes weights according to a Uniform distribution."""
    a = -0.5
    b = 0.5
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.uniform_(m.weight, a=a, b=b)
        nn.init.constant_(m.bias, 0.)

def init_integer(m):
    """Initializes weights according to a Uniform distribution."""
    a = -1.
    b = 1.
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.uniform_(m.weight, a=a, b=b)
        nn.init.uniform_(m.bias, a=a, b=b)
        m.weight.data.ceil_()
        m.bias.data.ceil_()

def init_normal(m):
    """Initializes weights according to a Normal distribution."""
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        limit = 0.15
        origin = 0.
        nn.init.normal_(m.weight, mean=origin, std=limit)
        nn.init.constant_(m.bias, 0.)

def init_eye(m):
    """Initializes weights according to an Identity matrix. This special case
    allows the initial input(s) to be reflected in the output of the model.
    """
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.eye_(m.weight)

def init_constant(m):
    """Initializes weights according to an Identity matrix. This special case
    allows the initial input(s) to be reflected in the output of the model.
    """
    val = 0.5
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.constant_(m.weight, val)
        nn.init.constant_(m.bias, 0.)

def init_he(m):
    """Initializes weights according to an Identity matrix. This special case
    allows the initial input(s) to be reflected in the output of the model.
    """
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.kaiming_normal_(m.weight)

def init_sparse(m):
    """Initializes weights according to an Identity matrix. This special case
    allows the initial input(s) to be reflected in the output of the model.
    """
    ratio = 0.9
    if type(m) == nn.Linear:
        nn.init.sparse_(m.weight, sparsity=ratio)
        nn.init.constant_(m.bias, 0.)

def init_spiking(m):
    """Initializes weights according to an Identity matrix. This special case
    allows the initial input(s) to be reflected in the output of the model.
    """
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        m.weight.data.round_()
        m.bias.data.round_()

def load_weights(model, path):
    model.load_state_dict(torch.load(path))
