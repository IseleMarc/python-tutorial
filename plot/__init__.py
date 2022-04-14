"""Plots multiple data sets in one plot."""

import matplotlib.pyplot as plt
import matplotlib as mpl


def lines(ax, x, y, **kwargs):
    ax.plot(x, y, **kwargs)


def scatter(ax, x, y, **kwargs):
    ax.scatter(x, y, **kwargs)


def vlines(ax, x, y, origin=0, **kwargs):
    ax.vlines(x, origin, y, **kwargs)


def errorbar(ax, x, y, **kwargs):
    ax.errorbar(x, y, **kwargs)


plot_func = {
    'lines': lines,
    'scatter': scatter,
    'vlines': vlines,
    'errorbar': errorbar
}


class Plotdataset:
    """Datasets for the Plot class."""

    def __init__(self, x, y, plotcase='lines', **kwargs):
        self.x = x
        self.y = y
        self.plotcase = plotcase
        self.kwargs = kwargs


class Plot:
    """Plots multiple data sets in one plot.

    Aims to declutter matplotlib a bit and has a uniform layout.
    It's possible to give each instance of this class different
    properties and everything gets plotted via plot() in the end.

    Attributes:
    -----------
    grid (bool): Whether or not a grid is drawn (True by default).
    savename (str): If set, plot will be saved to this name.

    Methods:
    --------
    add_dataset: Add a dataset to be plotted and give necessary kwargs.
    clearplotlist: Clears all previously added datasets.
    plot: Plots everything.
    setax: Set properties of the Axes.
    """

    def __init__(self):
        self._plotlist = []
        self._labels = False
        self._axsetkwargs = None

        self._linewidth = 4
        self._fontsize = 24
        self._label_fontsize = 20
        self._label_linewidth = 4

        self.grid = True
        self.savename = None

        mpl.rcParams['lines.linewidth'] = self._linewidth
        mpl.rcParams['font.size'] = self._fontsize

        self.loc = 'upper left'
        self.bbox_to_anchor = (1, 1)
        self.borderaxespad = 0.1
        self.frameon = False

    def add_dataset(self, x, y, plotcase='lines', **kwargs):
        self._plotlist.append(Plotdataset(x, y, plotcase, **kwargs))
        if 'label' in kwargs:
            self._labels = True

    def clearplotlist(self):
        """Clears all previously added datasets."""
        self._plotlist = []

    def plot(self, close=False):
        """Plots everything"""
        # Create the figure and axes.
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plot all datasets.
        for pl in self._plotlist:
            plot_func[pl.plotcase](ax, pl.x, pl.y, **pl.kwargs)

        # Set the axes.
        if self._axsetkwargs:
            ax.set(**self._axsetkwargs)

        # Add distance between tick labels and graph.
        ax.tick_params(axis='x', which='major', pad=7)
        ax.grid(self.grid)

        # Set legend.
        if self._labels:
            leg = ax.legend(fontsize=self._label_fontsize, loc=self.loc,
                            bbox_to_anchor=self.bbox_to_anchor,
                            borderaxespad=self.borderaxespad,
                            frameon=self.frameon)
            # Set linewidth in legend.
            for legobj in leg.legendHandles:
                legobj.set_linewidth(self._label_linewidth)

        if self.savename:
            plt.savefig(self.savename, bbox_inches='tight')

        if close:
            plt.close(fig)

    def setax(self, **kwargs):
        """Sets the axes.
        Possible kwargs are e.g.: xlim, ylim, xlabel, ylabel, title"""
        self._axsetkwargs = kwargs
