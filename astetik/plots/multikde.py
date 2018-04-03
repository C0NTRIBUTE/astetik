import seaborn as sns
import matplotlib.pyplot as plt

from ..style.template import _header


def multikde(data,
             x,
             label_col,
             sort=None,
             transform=None,
             transform_func='sum',
             palette='default',
             style='astetik',
             dpi=72,
             title='',
             sub_title='',
             x_label='',
             y_label='',
             legend=False,
             x_scale='linear',
             y_scale='linear',
             x_limit='auto',
             y_limit='auto',
             save=False):

    '''MULTI KDE

    Creates a plot with several kde style histograms
    one on top of each other. Great for comparing categorical
    features against continuous features.

    Inputs: 2
    Features: 1 continuous and 1 categorical

    1. USE
    ======
    ast.multikde(data=patients,
             x='age',
             label_col='insurance')

    2. PARAMETERS
    =============
    2.1 INPUT PARAMETERS
    --------------------
    data :: pandas dataframe

    x :: x-axis data (continuous)

    y :: x-axis overlap data (continuous)

    label_col :: the column with the label values

    --------------------
    2.2. PLOT PARAMETERS
    --------------------
    sort :: either True or False for ascending sort based on the
            x-axis data.

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

    palette = _header(palette,
                      style,
                      n_colors=1,
                      dpi=dpi,
                      fig_height=None,
                      fig_width=None)
    # <<< HEADER ENDS

    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    g = sns.FacetGrid(data,
                      row=label_col,
                      hue=label_col,
                      aspect=15,
                      size=1,
                      palette=palette)

    g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2,
                label,
                fontweight="bold",
                fontsize=14,
                color=color,
                ha="left",
                va="center",
                transform=ax.transAxes)

    g.map(label, x)

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play will with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True);
