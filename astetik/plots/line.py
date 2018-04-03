import numpy as np
import matplotlib.pyplot as plt

from ..style.formats import _thousand_sep
from ..style.style import params
from ..style.titles import _titles
from ..style.template import _header, _footer
from ..utils.utils import _limiter, _scaler


def line(data,
         x,
         y=None,
         dropna=True,
         median_line=False,
         drawstyle='default',
         linestyle='solid',
         markerstyle='o',
         palette='default',
         style='astetik',
         dpi=72,
         title='',
         sub_title='',
         x_label='',
         y_label='',
         legend=False,
         x_scale='linear',
         y_scale=None,
         x_limit='None',
         y_limit='auto',
         save=False):

    '''TIMESERIES LINE PLOT

    A line plot for one or more columns all with a comparable
    value, in a time sequence.

    1.USE
    =====
    line_plot(data=ldata,
              x='value',
              linestyle='dashdot',
              palette='colorblind',
              title="The main title comes here",
              sub_title="Suptibtle comes here")

    Inputs: 1 or more continuous and an optional timestamp
    Features: Continuous and optional datetime format

    2. PARAMETERS
    =============
    2.1 INPUT PARAMETERS
    --------------------
    data :: pandas dataframe

    x :: one or more columns of data

    y :: a single timeseries column (no need to be dt)
         and if y is not defined, then a sequence will
         be automatically generated as time labels.

    --------------------
    2.2. PLOT PARAMETERS
    --------------------
    median_line :: If True, a median line will be drawn

    drawstyle :: 'default', 'steps', 'steps-pre','steps-mid' or 'steps-post'

    linestyle :: 'solid', 'dashed', 'dashdot' , 'dotted'

    markerstyle :: ".", ",", "o", "+", "x", "|", "_", "^", "v"

    ----------------------
    2.3. COMMON PARAMETERS
    ----------------------
    palette :: One of the hand-crafted palettes:
               'default'
               'colorblind'
               'blue_to_red'
               'blue_to_green'
               'red_to_green'
               'green_to_red'
               'violet_to_blue'
               'brown_to_green'
               'green_to_marine'

               Or use any cmap, seaborn or matplotlib
               color or palette code, or hex value.

    style :: Use one of the three core styles:
               'astetik'     # white
               '538'         # grey
               'solarized'   # sepia

             Or alternatively use any matplotlib or seaborn
             style definition.

    dpi :: the resolution of the plot (int value)

    title :: the title of the plot (string value)

    sub_title :: a secondary title to be shown below the title

    x_label :: string value for x-axis label

    y_label :: string value for y-axis label

    x_scale :: 'linear' or 'log' or 'symlog'

    y_scale :: 'linear' or 'log' or 'symlog'

    x_limit :: int or list with two ints

    y_limit :: int or list with two ints

    outliers :: Remove outliers using either 'zscore' or 'iqr'

    '''

    # START OF PLOT SPECIFIC >>>
    if type(x) != type([]):
        x = [x]

    lines = len(x)

    if dropna == True:
        data = data[data[x].isna() == False]

    x_data = []

    for i in range(len(x)):
        x_data.append(np.array(data[x[i]]))

    if y == None:
        y_data = range(len(data))
    else:
        y_data = data[y]

    markers = ["o", "+", "x", "|", "-", ",", ".", "^", "v"]
    # <<< END OF PLOT SPECIFIC

    # START OF HEADER >>>
    palette = _header(palette, style, n_colors=lines, dpi=dpi)
    # <<< END OF HEADER

    p, ax = plt.subplots(figsize=(params()['fig_width'],
                                  params()['fig_height']))

    # # # # PLOT STARTS # # # #
    for i in range(lines):
        p = plt.plot(y_data,
                     x_data[i],
                     marker=markers[i],
                     drawstyle=drawstyle,
                     linestyle=linestyle,
                     c=palette[i],
                     linewidth=2,
                     markersize=7,
                     markeredgewidth=2,
                     mfc='white',
                     rasterized=True,
                     aa=True,
                     alpha=1)
    # # # # PLOT ENDS # # # #
    if median_line:
        x_mean = x.mean()
        x_mean = np.full(len(data), x_mean)
        plt.plot(y, x_mean)

    # SCALING AND LIMITS STARTS >>>
    if x_scale != 'linear' or y_scale != 'linear':
        _scaler(p, x_scale, y_scale)

    if x_limit != None or y_limit != None:
        _limiter(data=data, x=x, y='_R_E_S_', x_limit=None, y_limit=y_limit)

    # HEADER
    _thousand_sep(p, ax)
    _titles(title, sub_title=sub_title)
    _footer(p, x_label, y_label, save=save)

    if legend != False:
        plt.legend(x, loc=1, ncol=lines)