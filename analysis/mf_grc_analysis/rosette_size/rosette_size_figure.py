
import os
import sys
import importlib
import seaborn as sns
sys.path.insert(0, '/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc')

import my_plot
importlib.reload(my_plot)
from my_plot import MyPlotData, my_box_plot

def to_ng_coord(coord):
    return (
        int(coord[0]/4),
        int(coord[1]/4),
        int(coord[2]/40),
        )


import compress_pickle
# input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114_restricted_z.gz')
input_graph = compress_pickle.load('/n/groups/htem/Segmentation/shared-nondev/cb2_segmentation/analysis_mf_grc/mf_grc_model/input_graph_201114.gz')
grcs = [k for k in input_graph.grcs.keys()]

rosette_loc_size = {}
for mf_id, mf in input_graph.mfs.items():
    mf.get_all_mf_locs_size(rosette_loc_size)


# z_min = 15
# z_max = 35
z_min = 20
z_max = 30
mpd = MyPlotData()

averages = []
for rosette_loc, size in rosette_loc_size.items():
    x, y, z = rosette_loc
    if x < 360000 or x > 520000:
        continue
    if z < z_min*1000 or z > z_max*1000:
        continue
    averages.append(size)
    mpd.add_data_point(
        rosette_loc=rosette_loc,
        size=size,
        type='Rosette'
        )

print(f'Average: {sum(averages)/len(averages)}')
script_n = os.path.basename(__file__).split('.')[0]

importlib.reload(my_plot); my_plot.my_displot(
    mpd,
    x='size',
    kind='hist',
    context='paper',
    kde=True,
    stat='density',
    height=4,
    aspect=2,
    x_axis_label='# of GrC partners per MF',
    y_axis_label='Normalized Frequency',
    save_filename=f'{script_n}_{z_min}_{z_max}_hist.svg',
    )

importlib.reload(my_plot); my_plot.my_displot(
    mpd,
    x='size',
    kind='kde',
    context='paper',
    # kde=True,
    height=4,
    aspect=2,
    x_axis_label='# of GrC partners per MF',
    y_axis_label='Normalized Frequency',
    save_filename=f'{script_n}_{z_min}_{z_max}_kde.svg',
    )

importlib.reload(my_plot); my_plot.my_displot(
    mpd,
    x='size',
    kind='ecdf',
    context='paper',
    # ecdf=True,
    height=4,
    aspect=2,
    y_axis_label='Cumulative Distribution',
    x_axis_label='# of GrC partners per MF',
    save_filename=f'{script_n}_{z_min}_{z_max}_ecdf.svg',
    )

for c in ['lightsalmon', 'darksalmon', 'salmon', 'coral', 'tomato']:
    importlib.reload(my_plot); my_plot.my_catplot(
        mpd,
        # x="size",
        y="size",
        # hue="type",
        # hue_order=['All', 'Per PC', 'Per pf'],
        # hue_order=['All', 'Per PC'],
        # y_lims=[.25, .75],
        context='paper',
        kind='violin',
        # palette=sns.color_palette("mako_r", as_cmap=True),
        # palette=sns.color_palette("rocket"),
        color=c,
        # font_scale=1.5,
        height=4,
        # width=2,
        aspect=.75,
        y_axis_label='# of GrC partners per MF',
        # x_axis_label='# of GrCs per MF',
        save_filename=f'{script_n}_{z_min}_{z_max}_violin_{c}.svg',
        )











# sns.jointplot(data=mpd.to_dataframe(), x="x_dis", y="y_dis", hue='kind')
# plt.show()

# for num_claws in range(max_claws+1):
#     if num_claws == 0:
#         continue
#     mpd.add_data_point(
#         kind='Data',
#         num_claws=num_claws,
#         count=true_count[num_claws],
#         )

# for i, random_count in enumerate(random_counts):
#     for num_claws in range(max_claws+1):
#         if num_claws == 0:
#             continue
#         mpd.add_data_point(
#             kind='Shuffle',
#             num_claws=num_claws,
#             count=random_count[num_claws],
#             shuffle_i=i,
#             )


# importlib.reload(my_plot); my_plot.my_relplot(
#     mpd, y='count', x='num_claws', hue='kind',
#     kind='line',
#     # y='ratio', y_lims=[.25, .75],
#     context='paper',
#     # kind='violin',
#     # font_scale=1.5,
#     width=4,
#     aspect=1,
#     y_axis_label='Count',
#     x_axis_label='GrCs per Mossy Fiber',
#     save_filename='claws_per_mf_201109_plot.svg',
#     )
