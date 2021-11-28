
import random

from scaleup_model import ScaleUpModel
from global_random_model import GlobalRandomModel

def shuffle(
        graph, model,
        num_claws=4,
        mf_dist_margin=4000,
        constant_dendrite_length=15000,
        seed=0,
        ):
    random.seed(seed)
    if model == 'scaleup':
        graph = ScaleUpModel(
            n_grcs=1211,
            n_mfs=487,
            input_graph=graph,
            seed=seed,
            )
    elif model == 'random':
        graph = GlobalRandomModel(
            n_grcs=1211,
            n_mfs=487,
            n_dendrites=[4, 4, 4, 4],
            seed=seed,
            )
    elif model == 'global_random':
        graph = GlobalRandomModel(
            n_grcs=1211,
            n_mfs=15000,
            n_dendrites=[4, 4, 4, 4],
            seed=seed,
            )
    elif model == 'constant_grc':
        graph.randomize_graph_by_grc(
            mf_dist_margin=mf_dist_margin,
            single_connection_per_pair=True,
            constant_grc_degree=num_claws,
            preserve_mf_degree=True,
        )
    elif model == 'constant_length':
        graph.randomize_graph_by_grc(
            mf_dist_margin=mf_dist_margin,
            single_connection_per_pair=True,
            constant_dendrite_length=constant_dendrite_length,
            preserve_mf_degree=True,
        )
    elif model == 'classic_random':
        graph.randomize_graph(
            random_model=True,
            constant_grc_degree=num_claws,
            )
    elif model == 'no_same_mf':
        graph.randomize_graph_by_grc(
            mf_dist_margin=mf_dist_margin,
            single_connection_per_pair=True,
            )
    elif model == 'naive_random_15':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            constant_dendrite_length=15000,
            mf_dist_margin=4000,
            )
    elif model == 'naive_random_17':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            constant_dendrite_length=17000,
            mf_dist_margin=4000,
            )
    elif model == 'naive_random_21':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            constant_dendrite_length=21700,
            mf_dist_margin=4000,
            )
    elif model == 'expanded_random_15':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            # constant_dendrite_length=constant_dendrite_length,
            # always_pick_closest_rosette=True,
            dendrite_range=(0, 15000),
            )
    elif model == 'expanded_random_30':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            # constant_dendrite_length=constant_dendrite_length,
            # always_pick_closest_rosette=True,
            dendrite_range=(0, 30000),
            )
    elif model == 'expanded_random_50':
        graph.randomize_graph_by_grc(
            single_connection_per_pair=True,
            constant_grc_degree=4,
            # constant_dendrite_length=constant_dendrite_length,
            # always_pick_closest_rosette=True,
            dendrite_range=(0, 50000),
            )
    else:
        assert model == 'data'
    return graph
