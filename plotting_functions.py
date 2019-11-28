import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from collections.abc import Iterable

import aux_functions as aux


def count(df: pd.DataFrame, label):
    values = df[label]
    if isinstance(values[0], str):
        values_split = []
        for value in values:
            values_split.extend(value.split(';'))
        values = pd.Series(values_split, name=label)

    return values.value_counts()


def gauss(df: pd.DataFrame, label):
    data = df[label]
    mean = data.mean()
    std = data.std()
    return mean, std


def pie_subplot(counts, ax, **kwargs):
    s = sum(counts)
    pie = ax.pie(counts, autopct=lambda p: str(int(round(p*s/100))), **kwargs)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(pie[0], aux.break_labels(counts.keys()), fontsize=10,
              bbox_transform=ax.transAxes, bbox_to_anchor=(1, 0.5), loc="center left")


def bar_subplot(counts, ax, gauss_params=None, bar_color='lightslategray', gauss_color='crimson', **kwargs):
    keys = counts.keys()

    if isinstance(keys[0], str):
        cmap = plt.get_cmap('tab10')
        bar_color = [cmap(i) for i in range(len(keys))]
        label = None
        ax.set_ylabel('Counts')
        plt.xticks(rotation=30, ha='right')
    else:
        label = 'Counts'

    ax.bar(keys, counts, color=bar_color, **kwargs, label=label)


    if gauss_params is not None:
        x = np.linspace(0, keys.max(), 100)
        y = norm.pdf(x, *gauss_params)
        y = y / y.max() * counts.max()

        mean, std = gauss_params
        ax.plot(x, y, zorder=5, color=gauss_color, lw=3, label='Distribution')
        ax.axvline(mean, color=gauss_color, linestyle='--', label=f'Mean ({mean:.1f} +/- {std:.1f})')

    if label is not None:
        ax.legend(fancybox=True, framealpha=0.5)


PLOTS_REGISTRY = {'pie': pie_subplot,
                  'bar': bar_subplot}


def make_subplot(df, label, kind='pie', ax=None, show=True, break_labels=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    counts = count(df, label)
    if counts.keys().is_numeric():
        kwargs['gauss_params'] = gauss(df, label)

    PLOTS_REGISTRY[kind](counts, ax, **kwargs)

    if show:
        plt.show()

    ax.set_title(aux.break_label(counts.name, ['a ', 'do']) if break_labels else counts.name)


def make_plot(df: pd.DataFrame, labels, nrows=2, show=False, title=None, fig_kwargs=None, kind='pie', **kwargs):
    fig_kwargs = fig_kwargs or {}

    n = len(labels)
    ncols = n // nrows + int(bool(n % nrows))

    same_kind = False
    if isinstance(kind, str):
        kind = n * [kind]
        same_kind = True
    elif not isinstance(kind, Iterable) or len(kind) != n:
        raise ValueError(f"'kind' should be a string or an iterable of {n} strings")

    fig, axes = plt.subplots(nrows, ncols,
                             sharex='all' if same_kind else 'none',
                             sharey='row' if same_kind else 'none',
                             **fig_kwargs)

    # make sure the axes array is 2D
    if n < 2:
        axes = np.array([axes])
    axes = axes.reshape(nrows, -1)

    for i, label in enumerate(labels):
        make_subplot(df, label, ax=axes[i//ncols, i % ncols], show=False, kind=kind[i], **kwargs)

    plt.suptitle(title or "", fontsize=16)

    if show:
        plt.show()

    return fig
