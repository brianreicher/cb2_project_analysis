import random
import copy
import logging
import sys

from run_tests_201204 import *

'''Load data'''
import compress_pickle
# fname = '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114.gz'
# input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114_restricted_z.gz')
input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114_xlim_320_560_zlim_10_40.gz')
# input_graph = compress_pickle.load(fname)

random.seed(0)

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
test_voi_similar_input_201204(input_graph)

