"""A script that defines a simple CNN, used in the PyTorch example to solve
MNIST problem
"""
import torch.nn as nn
import torch

class Net(nn.Module):
    def __init__(self, model_params):
        print("Creating basic CNN MNIST model for MSN")
        super(Net, self).__init__()
        self.act = nn.ReLU()
        #self.act = nn.Tanh()
        self.drop = nn.Dropout(0.05)
        self.maxpool = nn.MaxPool2d(2, 2)
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        #self.softmax = nn.LogSoftmax(dim=1)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        """Forward pass over the model."""
        x = self.conv1(x)
        x = self.act(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.act(x)
        x = self.maxpool(x)
        (_, C, H, W) = x.data.size()
        x = x.view(-1, C*H*W)
        #print(C*H*W)
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x
