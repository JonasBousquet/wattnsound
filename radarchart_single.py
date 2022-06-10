import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import xarray
from mplsoccer import Radar, FontManager

'''The only things you have to change are path, filename and color. 
            path is the path to your .nc file
                filename explains itself
            and color is the color of the chart
    i proposed some colors but you can also add every hex color you want'''

# >----------------------------------------------------------------------------------------------------------------<
path = r'C:\Users\Jonas Bousquet\Desktop\pyhy3\Code\data_exploration\deployments\0_DW.nc'
filename = 'orange'
color = '#FE9B02'
# green : #06B408
# red : #E61F1F
# lightblue : #29DFEE
# darkblue : #0A1FF5
# orange : #FE9B02
# >----------------------------------------------------------------------------------------------------------------<


def get_data(inpath):
    loc_1 = inpath
    lc1 = xarray.open_dataset(loc_1)
    vars1 = ['name']
    loc1 = ['loc1']

    for data_var in lc1.data_vars:
        vars1.append(data_var)
        loc1.append(lc1[data_var].mean('id').values[0])

    array = np.array([loc1])
    column_val = vars1

    df1 = pd.DataFrame(data = array,
                       # index = index_values,
                       columns = column_val)
    return df1


# Function call
df = get_data(path)

params = list(df.columns)
params = params[1:]
min_range = []
max_range = []
a_values = []

# for x in params:
#     a = min(df[params][x])
#     a = float(a)
#     a = a - (a*.25)
#     a = round(a, 4)
#     min_range.append(a)
#
#     b = max(df[params][x])
#     b = float(b)
#     b = b + (b * .25)
#     b = round(b, 4)
#     max_range.append(b)

min_range = [54.1602, 75.2036, -6.0213, 0.2293, 0]
max_range = [103.1124, 115.951, -10.3288, 1.4115, 0]
for x in range(len(df['name'])):

    if df.loc[x]['name'] == 'loc1':

        a_values = df.iloc[x].values.tolist()
a_values = a_values[1:]
a_val = []
for item in a_values:
    a_val.append(float(item))

# Radarchart
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

# Chart
numb = int(len(params))
radar = Radar(params, min_range, max_range,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*numb,
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
fig, ax = radar.setup_axis()  # format axis as a radar
rings_inner = radar.draw_circles(ax=ax, facecolor='#ffffff', edgecolor='#000000')  # draw circles
radar_output = radar.draw_radar(a_val, ax=ax,
                                kwargs_radar={'facecolor': color, 'alpha': 0.7},
                                kwargs_rings={'facecolor': '#ffffff', 'alpha': 0})  # draw the radar
radar_poly, radar_poly2, vertices1 = radar_output
range_labels = radar.draw_range_labels(ax=ax, fontsize=15,
                                       fontproperties=robotto_thin.prop)  # draw the range labels
param_labels = radar.draw_param_labels(ax=ax, fontsize=20,
                                       fontproperties=robotto_regular.prop)  # draw the param labels
ax.scatter(vertices1[:, 0], vertices1[:, 1],
                     c=color, edgecolors=color, marker='o', s=150, zorder=2)

plt.savefig('{filename}.png'.format(filename=filename))
print('saved figure under {filename}.png'.format(filename=filename))
