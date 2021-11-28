import argparse
import random
import copy
import logging
import sys
import os

from random_patterns import generate_patterns, add_noise_to_patterns

script_n = os.path.basename(__file__).split('.')[0]

from run_tests_210603 import *

# from shuffle_210404 import shuffle
from global_random_model2 import GlobalRandomModel

'''
python3 batch_210607_redundancy_vs_small_features.py --mode act --model random
python3 batch_210607_redundancy_vs_small_features.py --mode act --model global_random
python3 batch_210607_redundancy_vs_small_features.py --mode act --model data
python3 batch_210607_redundancy_vs_small_features.py --mode act --model naive_random_15
python3 batch_210607_redundancy_vs_small_features.py --mode act --model naive_random_17
python3 batch_210607_redundancy_vs_small_features.py --mode act --model naive_random_21
'''

os.makedirs(script_n, exist_ok=True)


ap = argparse.ArgumentParser()
# ap.add_argument("--n_random", type=int, help='', default=1)
ap.add_argument("--n_random", type=int, help='', default=40)
ap.add_argument("--pattern_len", type=int, help='', default=128*2)
# ap.add_argument("--pattern_len", type=int, help='', default=8)
# ap.add_argument("--activation_levels", type=float, help='', nargs='+', default=None)
ap.add_argument("--activation_level", type=float, help='', default=0.3)
# ap.add_argument("--noise_scale", type=float, help='', default=0.05)
ap.add_argument("--noise_level", type=float, help='', default=0.05)
# ap.add_argument("--grc_pcts", type=float, help='', nargs='+', default=None)
ap.add_argument("--variation_sizes", type=float, help='', nargs='+', default=None)
# ap.add_argument("--noise_prob", type=float, help='', default=1)
ap.add_argument("--model", type=str, help='', default='global_random')
ap.add_argument("--n_grcs", type=int, help='', default=1400)
ap.add_argument("--n_mfs", type=int, help='', default=400)
ap.add_argument("--redundant_factor", type=float, help='', default=2)
ap.add_argument("--n_share", type=int, help='', default=2)
ap.add_argument("--pattern_type", type=str, help='', default='binary')
ap.add_argument("--valence_dir", type=str, help='', default='0')
config = ap.parse_args()

# grc_pcts = config.grc_pcts
# if grc_pcts is None:
#     # grc_pcts = [k/1000 for k in range(25, 1025, 25)]
#     grc_pcts = [k/1000 for k in range(50, 1050, 50)]
#     # grc_pcts = [k/1000 for k in range(1000, 1050, 50)]
# print(grc_pcts)

variation_sizes = config.variation_sizes
if variation_sizes is None:
    # variation_sizes = [.1]
    # variation_sizes = [k/1000 for k in range(10, 210, 10)]
    variation_sizes = [k/1000 for k in range(800, 1000, 10)]
print(variation_sizes)


make_weights_fn = functools.partial(get_optimal_weights_same,
                                    valence_dir=config.valence_dir,
                                    )


n_grcs = config.n_grcs
n_mfs = config.n_mfs
model = config.model
model_desc = None
assert model is not None

def make_graph(model, seed):
    global model_desc
    if model == 'global_random':
        input_graph = GlobalRandomModel(
            n_grcs=n_grcs,
            n_mfs=n_mfs,
            seed=seed,
            )
        input_graph = input_graph.make_redundant(config.redundant_factor, config.n_share)
        model_desc = f'{model}_redundant_{config.redundant_factor}_nshare_{config.n_share}'
    else:
        assert False
    return input_graph

# model = Simulation(model)


# '''Load data'''
# import compress_pickle
# if config.model == 'scaleup4':
#     input_graph = compress_pickle.load(f'models/scaleup4_{n_grcs}_{n_mfs}_f_300_seed_0_calibrated_full.gz')
# elif config.model == 'naive_random4':
#     input_graph = compress_pickle.load(f'models/naive_random4_{n_grcs}_{n_mfs}_f_300_seed_0_calibrated_full.gz')
# elif config.model == 'random':
#     input_graph = compress_pickle.load(f'models/global_random_{n_grcs}_{n_mfs}_f_300_seed_0_calibrated_full.gz')
# else:
#     assert False

# pattern_type = 'uniform'
pattern_type = config.pattern_type

pattern_generator = functools.partial(generate_patterns, type=pattern_type)
variation_generator = functools.partial(add_noise_to_patterns, type=pattern_type)
noise_generator = functools.partial(add_noise_to_patterns, type=pattern_type, invert_noise_mask=True)

def test(model, seed):

    graph = make_graph(model, seed=seed)
    sim = make_sim(graph)
    if pattern_type == 'binary':
        sim.set_binary_mode()
        pass
    return test_consistency_across_variations(
        sim,
        pattern_generator=pattern_generator,
        variation_generator=variation_generator,
        noise_generator=noise_generator,
        print_output=True,
        test_len=config.pattern_len,
        activation_level=config.activation_level,
        variation_sizes=variation_sizes,
        # noise_scaling=config.noise_scale,
        noise_level=config.noise_level,
        make_weights_fn=make_weights_fn,
        seed=seed,
        )


print(f'Running {model}')
ress = []
for n in range(config.n_random):
    print(f'Pass {n}')
    res = test(model, seed=n)
    ress.append(res)
    compress_pickle.dump((
        ress,
        ), f"{script_n}/{script_n}_{model_desc}_"
           f"{pattern_type}_{config.n_grcs}_{config.n_mfs}_"
           f"dir_{config.valence_dir}_noise_{config.noise_level}_"
           f"{config.activation_level}_{config.pattern_len}_{config.n_random}.gz")
    print()
