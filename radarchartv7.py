import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import xarray
from mplsoccer import Radar, FontManager

# as input files you need .nc output files from the pypam create_dataset progra
# to use this and adapt it to your use you need to change loc_1 and 2 in ~ l17-18, and the titles in ~ l168-180
# and filename
# no need to add a file_extension to your name, it does it automatically (.png)
# if you want to use more (or less) parameters you need to change to number in ~ l99 (round_int=[False]*5)
#
start = time.time()
filename = 'gotit'


def get_data():
    # loc_1 and 2 should be the paths to your .nc you wanna compare
    loc_1 = r'C:\Users\Jonas Bousquet\Desktop\pyhy3\Code\data_exploration\deployments\0_DW.nc'
    loc_2 = r'C:\Users\Jonas Bousquet\Desktop\pyhy3\Code\data_exploration\deployments\1_Hst001.nc'
    lc1 = xarray.open_dataset(loc_1)
    lc2 = xarray.open_dataset(loc_2)
    vars1 = ['name']
    loc1 = ['loc1']
    loc2 = ['loc2']

    for data_var in lc1.data_vars:
        vars1.append(data_var)
        loc1.append(lc1[data_var].mean('id').values[0])
        loc2.append(lc2[data_var].mean('id').values[0])

    array = np.array([loc1, loc2])

    # index_values = [0,1]
    column_val = vars1

    df1 = pd.DataFrame(data = array,
                       # index = index_values,
                       columns = column_val)
    return df1


# Function call
df = get_data()

params = list(df.columns)
params = params[1:]
min_range = []
max_range = []
a_values = []
b_values = []

for x in params:
    a = min(df[params][x])
    a = float(a)
    a = a - (a*.25)
    a = round(a, 4)
    min_range.append(a)

    b = max(df[params][x])
    b = float(b)
    b = b + (b * .25)
    b = round(b, 4)
    max_range.append(b)

for x in range(len(df['name'])):

    if df.loc[x]['name'] == 'loc1':

        a_values = df.iloc[x].values.tolist()
    if df.loc[x]['name'] == 'loc2':
        b_values = df.iloc[x].values.tolist()

a_values = a_values[1:]
b_values = b_values[1:]
a_val = []
for item in a_values:
    a_val.append(float(item))
b_val = []
for item in b_values:
    b_val.append(float(item))

# Fonts
URL1 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
        'fonts/SourceSerifPro-Regular.ttf?raw=true')
serif_regular = FontManager(URL1)
URL2 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
        'fonts/SourceSerifPro-ExtraLight.ttf?raw=true')
serif_extra_light = FontManager(URL2)
URL3 = ('https://github.com/google/fonts/blob/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf?raw=true')
rubik_regular = FontManager(URL3)
URL4 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Thin.ttf?raw=true'
robotto_thin = FontManager(URL4)
URL5 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
robotto_regular = FontManager(URL5)
URL6 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Bold.ttf?raw=true'
robotto_bold = FontManager(URL6)

# init
numb = int(len(params))
radar = Radar(params, min_range, max_range,
              round_int=[False]*numb,
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)

# def Mosaic for Title and subtitle


def radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14):

    """ Create a Radar chart flanked by a title and endnote axes.

    Parameters
    ----------
    radar_height: float, default 0.915
        The height of the radar axes in fractions of the figure height (default 91.5%).
    title_height: float, default 0.06
        The height of the title axes in fractions of the figure height (default 6%).
    figheight: float, default 14
        The figure height in inches.

    Returns
    -------
    fig : matplotlib.figure.Figure
    axs : dict[label, Axes]
    """
    if title_height + radar_height > 1:
        error_msg = 'Reduce one of the radar_height or title_height so the total is ≤ 1.'
        raise ValueError(error_msg)
    endnote_height = 1 - title_height - radar_height
    figwidth = figheight * radar_height
    figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                      gridspec_kw={'height_ratios': [title_height, radar_height,
                                                                     endnote_height],
                                                   # the grid takes up the whole of the figure 0-1
                                                   'bottom': 0, 'left': 0, 'top': 1,
                                                   'right': 1, 'hspace': 0},
                                      figsize=(figwidth, figheight))
    axes['title'].axis('off')
    axes['endnote'].axis('off')
    return figure, axes


# Data input
# creating the figure using the function defined above:
fig, axs = radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14)

# plot radar
radar.setup_axis(ax=axs['radar'])  # format axis as a radar
rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffffff', edgecolor='#000000')
radar_output = radar.draw_radar_compare(a_val, b_val, ax=axs['radar'],
                                        kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.5},
                                        kwargs_compare={'facecolor': '#d80499', 'alpha': 0.5})
radar_poly, radar_poly2, vertices1, vertices2 = radar_output
range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_regular.prop)
axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                     c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                     c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
endnote_text = axs['endnote'].text(0.99, 0.5, 'Recordings by Mayanna / Analysis with pypam / Chart by jonasbousquet', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
# Title left
title1_text = axs['title'].text(0.01, 0.65, 'Pair 2', fontsize=25, color='#01c49d',
                                fontproperties=robotto_bold.prop, ha='left', va='center')
# subtitle left
title2_text = axs['title'].text(0.01, 0.25, 'OFF-site', fontsize=20,
                                fontproperties=robotto_regular.prop,
                                ha='left', va='center', color='#01c49d')
# title right
title3_text = axs['title'].text(0.99, 0.65, 'Pair 2', fontsize=25,
                                fontproperties=robotto_bold.prop,
                                ha='right', va='center', color='#d80499')
# subtitle right
title4_text = axs['title'].text(0.99, 0.25, 'ON-site', fontsize=20,
                                fontproperties=robotto_regular.prop,
                                ha='right', va='center', color='#d80499')

plt.savefig('{filename}.png'.format(filename=filename))
print('saved figure under {filename}.png'.format(filename=filename))

end = time.time()
zeit = end - start
if zeit > 60:
    minutes = int(zeit / 60)
    sec = zeit % 60
    sec = round(sec, 2)
    print(f'\nscript run in {minutes} m and {sec} s')
else:
    zeit = round(zeit, 2)
    print(f'\nscript run in {zeit} s')