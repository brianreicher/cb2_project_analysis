import random
import copy
import logging
import sys
import compress_pickle

# from run_tests_201204 import *
from run_tests_201210 import *
from spatial_model import SpatialModel


mf_size_dist = compress_pickle.load(
    '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/'
    'rosette_size_db_210116.gz'
    )

grc_dendrite_count_dist = compress_pickle.load(
    '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/'
    'grc_dendrite_count_dist_db_210225.gz'
    )

grc_dendrite_len_dist = compress_pickle.load(
    '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/'
    'grc_dendrite_len_dist_db_201109.gz'
    )


random.seed(0)
input_graph = SpatialModel(
    n_grcs=100000,
    actual_n_grcs=1211,
    n_mfs=10000,
    n_boutons=28550,
    size_xyz=(160, 80, 3680),
    dendrite_count_dist=[4, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    dendrite_len_dist=[17, 17, 17, 17],
    mf_size_dist=[15, 15],
    # x_expansion=80,
    x_expansion=0,
    box_size=80,
    )

'''Load data'''
# fname = '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114.gz'
# input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114_restricted_z.gz')
# input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114_xlim_320_560_zlim_10_40.gz')
# input_graph = compress_pickle.load(fname)


num_claws = 4
if '--num_claws' in sys.argv:
    num_claws = int(sys.argv[2])

if '--constant_grc' in sys.argv:
    input_graph.randomize_graph_by_grc(
        mf_dist_margin=4000,
        single_connection_per_pair=True,
        constant_grc_degree=num_claws,
        preserve_mf_degree=True,
    )

if '--constant_length' in sys.argv:
    input_graph.randomize_graph_by_grc(
        mf_dist_margin=4000,
        single_connection_per_pair=True,
        constant_dendrite_length=15000,
        preserve_mf_degree=True,
    )

if '--classic_random' in sys.argv:
    input_graph.randomize_graph(
        random_model=True,
        constant_grc_degree=num_claws,
        )

if '--no_same_mf' in sys.argv:
    input_graph.randomize_graph_by_grc(
        mf_dist_margin=4000,
        single_connection_per_pair=True,
        )

if '--naive_random' in sys.argv:
    input_graph.randomize_graph_by_grc(
        single_connection_per_pair=True,
        constant_grc_degree=4,
        # constant_dendrite_length=15000,
        constant_dendrite_length=25000,
        always_pick_closest_rosette=True,
        )

# if '--naive_random' in sys.argv:
#     input_graph.randomize_graph_by_grc(
#         single_connection_per_pair=True,
#         constant_grc_degree=4,
#         # constant_dendrite_length=20000,
#         # constant_dendrite_length=,
#         always_pick_closest_rosette=True,
#         )


# run_tests_201204(input_graph)
# test_dim_similar_input(input_graph)
# test_hamming_distance_similar_input_201204(input_graph)
# test_dim_201205(input_graph, print_output=True)

test_similarity_by_activation_level(
    input_graph,
    print_output=True,
    test_len=4096,
    activation_levels=[20],
    noise_probs=[10, 20, 40, 90, 95, 100],
    seed=0,
    )

