"""solve a function"""
from __future__ import print_function
import sys, os
# Append SYSPATH in order to access different modules of the library
sys.path.insert(0, os.path.abspath('..'))
import environments
import backend.models as model_factory
import backend.algorithms as algorithm_factory
from solver import Solver

import argparse
import torch

def main():
    # Assumes CUDA is available
    parser = argparse.ArgumentParser(description='Func Solver')
    parser.add_argument('--pool_size', type=int, default=50, metavar='N',
                        help='number of samples in the pool (def: 50)')
    parser.add_argument('--nb_anchors', type=int, default=5, metavar='N',
                        help='number of anchors (def: 5)')
    parser.add_argument('--nb_probes', type=int, default=8, metavar='N',
                        help='number of probes per anchor (def: 8)')
    parser.add_argument('--iterations', type=int, default=500, metavar='N',
                        help='maximum number of optimization steps (def: 500)')
    args = parser.parse_args()

    precision = torch.half # Set precision

    # Make an MNIST Dataset environment
    env = environments.make_env("function",
                                "rastrigin",
                                nb_dimensions = 2,
                                plot = True
                                )

    # Make a pool
    pool = model_factory.make_pool("MNIST CNN MSN", args.pool_size, precision)

    # Make an algorithm --algorithm takes control of the pool--
    hyper_params = {
                    "pool size": args.pool_size,
                    "number of anchors": args.nb_anchors,
                    "number of probes per anchor": args.nb_probes,
                    "target": env.optimal_y,
                    "minimization mode": env.minimize
                    }
    alg = algorithm_factory.make_alg("MSN", pool, hyper_params)

    # Make a solver
    slv = Solver(env, alg)

    # Use solver to solve the problem
    #slv.train_dataset_with_validation(args.iterations)
    slv.repeated_batch_train_dataset_with_validation(args.iterations)

if __name__ == '__main__':
    main()
















#
