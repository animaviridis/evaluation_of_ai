import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm

import aux_functions as aux


def count(df: pd.DataFrame, label):
    return df[label].value_counts()


def gauss(df: pd.DataFrame, label):
    data = df[label]
    mean = data.mean()
    std = data.std()
    return mean, std


def pie_subplot(counts, ax, **kwargs):
    pie = ax.pie(counts, **kwargs)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(pie[0], aux.break_labels(counts.keys()), fontsize=10,
              bbox_transform=ax.transAxes, bbox_to_anchor=(1, 0.5), loc="center left")


def bar_subplot(counts, ax, gauss_params=None, bar_color='lightslategray', gauss_color='crimson', **kwargs):
    keys = counts.keys()

    ax.bar(keys, counts, color=bar_color, **kwargs, label='Counts')

    if gauss_params is not None:
        x = np.linspace(0, keys.max(), 100)
        y = norm.pdf(x, *gauss_params)
        y = y / y.max() * counts.max()

        mean, std = gauss_params
        ax.plot(x, y, zorder=5, color=gauss_color, lw=3, label='Distribution')
        ax.axvline(mean, color=gauss_color, linestyle='--', label=f'Mean: {mean:.1f}')

    ax.legend(fancybox=True, framealpha=0.5)


PLOTS_REGISTRY = {'pie': pie_subplot,
                  'bar': bar_subplot}


def make_subplot(df, label, type='pie', ax=None, show=True, break_labels=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    counts = count(df, label)
    if counts.keys().is_numeric():
        kwargs['gauss_params'] = gauss(df, label)

    PLOTS_REGISTRY[type](counts, ax, **kwargs)

    if show:
        plt.show()

    ax.set_title(aux.break_label(counts.name, ['a ', 'do']) if break_labels else counts.name)


def make_plot(df: pd.DataFrame, labels, nrows=2, show=True, title=None, fig_kwargs=None, **kwargs):
    fig_kwargs = fig_kwargs or {}

    ncols = len(labels) // nrows + int(bool(len(labels) % nrows))

    fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
    axes = axes.reshape(nrows, -1)  # make sure the axes array is 2D

    for i, label in enumerate(labels):
        make_subplot(df, label, ax=axes[i//ncols, i % ncols], show=False, **kwargs)

    plt.suptitle(title or "", fontsize=16)

    if show:
        plt.show()

    return fig
