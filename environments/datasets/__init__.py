"""This script allows making objects of different dataset classes"""

from .mnist import MNIST
from .cifar10 import CIFAR10

def make_dataset(name, data_path, batch_size, precision, loss):
    """Class factory method. This method takes the name of the desired
    dataset and returns an object of the corresponding class.
    """
    if name == 'mnist':
        return MNIST(data_path, batch_size, precision, loss)
    elif name == 'cifar10':
        return CIFAR10(data_path, batch_size, precision, loss)
