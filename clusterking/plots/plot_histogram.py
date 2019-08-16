#!/usr/bin/env python3

# std

# 3rd party
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_histogram(ax, edges, contents, normalize=False, *args, **kwargs):
    """
    Plot a histogram.

    Args:
        ax: Instance of `matplotlib.axes.Axes` to plot on. If ``None``, a new
            figure will be initialized.
        edges: Edges of the bins or None (to use bin numbers on the x axis)
        contents: bin contents
        normalize (bool): Normalize histogram. Default False.
        *args: passed on to `matplotlib.pyplot.step`
        **kwargs: passed on to `matplotlib.pyplot.step`

    Returns:
        Instance of `matplotlib.axes.Axes`
    """

    if not ax:
        fig, ax = plt.subplots()

    # "flatten" contents
    _contents = contents
    contents = np.array(contents)
    contents = contents.squeeze()
    if not len(contents.shape) == 1:
        raise ValueError(
            "The supplied contents array of shape {} can't be squeezed"
            "into a one dimensional array.".format(_contents.shape)
        )

    # bin numbers for the x axis if no x values are supplied
    if edges:
        edges = np.array(edges)
        assert len(edges.shape) == 1
        if not len(edges) == (len(contents) + 1):
            raise ValueError(
                "Invalid number of bin edges ({}) supplied for "
                "{} bins.".format(len(edges), len(contents))
            )
    else:
        edges = np.arange(len(contents) + 1)
        # force to have only integers on the x axis
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Normalize contents?
    if normalize:
        bin_widths = edges[:-1] - edges[1:]
        norm = sum(contents * bin_widths)
        contents /= norm

    # We need to repeat the last entry of the contents
    # because we use the 'post' plotting method for matplotlib.pyplot.step
    contents = np.append(contents, contents[-1])

    ax.step(edges, contents, where="post", *args, **kwargs)

    return ax


def plot_histogram_fill(ax, edges, content_low, content_high, **kwargs):
    """
    Plot two histograms with area shaded in between.

    Args:
        ax: Instance of `matplotlib.axes.Axes` to plot on. If ``None``, a new
            figure will be initialized.
        edges: Edges of the bins or None (to use bin numbers on the x axis)
        content_low: Bin contents of lower histogram
        content_high: Bin contents of higher histogram
        **kwargs: Keyword argumenets to `matplotlib.pyplot.fill_between`

    Returns:
        Instance of `matplotlib.axes.Axes`
    """

    if not ax:
        fig, ax = plt.subplots()

    content_low = np.squeeze(np.array(content_low))
    content_high = np.squeeze(np.array(content_high))

    if not len(content_high) == len(content_low) == len(edges) - 1:
        raise ValueError(
            "Lenghts don't match: content_high: {}, content_low: {}, "
            "edges -1: {}".format(
                len(content_high), len(content_low), len(edges) - 1
            )
        )

    content_low = np.concatenate((content_low, np.atleast_1d(content_low[-1])))
    content_high = np.concatenate(
        (content_high, np.atleast_1d(content_high[-1]))
    )

    fb_kwargs = dict(step="post", linewidth=0)
    fb_kwargs.update(kwargs)

    ax.fill_between(edges, content_low, content_high, **fb_kwargs)

    return ax
