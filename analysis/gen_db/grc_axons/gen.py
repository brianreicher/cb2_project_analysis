import collections
from collections import defaultdict
import sys
import json
import random
from jsmin import jsmin
from io import StringIO
import numpy as np
import copy
import importlib
from functools import partial
import daisy
import compress_pickle

sys.path.insert(0, '/n/groups/htem/Segmentation/shared-dev/cb2_segmentation/segway.graph.tmn7')
import segway.graph.synapse_graph

sys.path.insert(0, '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc')
from tools import to_ng_coord

seg_file = "/n/f810/htem/Segmentation/cb2_v4/output.zarr"
seg = daisy.open_ds(seg_file, 'volumes/super_1x2x2_segmentation_0.500_mipmap/s2')

# config_f = "../../config_pf_200925.json"
config_f = "/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/config_grc_201207.json"
with open(config_f) as js_file:
    minified = jsmin(js_file.read())
    config = json.load(StringIO(minified))

syn_score_threshold = 20

overwrite = True
if len(sys.argv) == 2:
    syn_score_threshold = int(sys.argv[1])

graph = segway.graph.synapse_graph.SynapseGraph(config_f, overwrite=overwrite,
    db_name='cb2_v4_synapse_pred_setup22_synapsedb_0p6_threshold_5',
    # syn_score_threshold=100)
    syn_score_threshold=syn_score_threshold)

def get_segment_id(seg, loc):
    loc = daisy.Coordinate((loc[2], loc[1], loc[0]))
    return int(seg[loc])

grcs = []
grcs_locs = defaultdict(lambda: defaultdict(list))
locs_to_sid = {}
locs_to_sid = compress_pickle.load('setup22_locs_to_sid.gz')
# locs_to_sid, _ = locs_to_sid

f = '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/completed_neurons_with_axons_201208'
with open(f) as fin:
    for line in fin:
        line = line.strip()
        if 'grc' in line:
            grcs.append(line)

for grc in grcs:
    print(f'Processing {grc}...')
    syns = graph.get_synapses(grc, type='pre')
    for syn in syns:
        post_loc = syn['post_loc']
        # print(post_loc)
        if post_loc in locs_to_sid:
            sid = locs_to_sid[post_loc]
        else:
            sid = get_segment_id(seg, post_loc)
            locs_to_sid[post_loc] = sid
        assert sid is not None
        nid = graph.neuron_db.find_neuron_with_segment_id(sid)
        if nid:
             if (('pc' in nid and 'pcl' not in nid) or
                    'purkinje' in nid):
                nid = nid.split('.')[0]
                pre_loc = syn['pre_loc']
                syn_loc = syn['syn_loc']
                loc = (pre_loc, syn_loc, post_loc)
                grcs_locs[grc][nid].append(loc)

compress_pickle.dump((
    dict(grcs_locs)
    ), f"setup22_thr_{syn_score_threshold}.gz")

