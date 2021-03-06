import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from collections.abc import Iterable
from typing import Union, List

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


def bar_subplot(counts, ax, gauss_params=None, bar_color=None, gauss_color='crimson', limit: int=None, **kwargs):

    keys = counts.keys()

    if isinstance(keys[0], str):
        counts = counts.sort_values(ascending=False)

        if limit is not None:
            counts = counts[:limit]
            keys = counts.keys()

        if bar_color is None:
            n = len(counts)
            if n <= 20:
                cmap = plt.get_cmap('tab20')
                bar_color = [cmap(i) for i in range(n)]
            else:
                bar_color = [tuple(np.random.rand(3)) for _ in range(n)]

        label = None
        ax.set_ylabel('Counts')
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
    else:
        bar_color = bar_color or 'lightslategray'
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


def make_subplot(df, label, kind='pie', counted=False, ax=None, show=True, break_labels=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    if counted:
        counts = df[label]
    else:
        counts = count(df, label)

    if counts.keys().is_numeric():
        kwargs['gauss_params'] = gauss(df, label)

    PLOTS_REGISTRY[kind](counts, ax, **kwargs)

    if show:
        plt.show()

    ax.set_title(aux.break_label(counts.name, ['a ', 'do']) if break_labels else counts.name)


def make_plot(df: Union[pd.DataFrame, List[pd.Series]], labels=None, nrows=2, show=False, title=None,
              fig_kwargs=None, kind='pie', sharex=True, sharey=True, **kwargs):
    fig_kwargs = fig_kwargs or {}

    if isinstance(df, Iterable):
        df = {dfi.name: dfi for dfi in df}
    elif not isinstance(df, pd.DataFrame):
        raise TypeError(f"Data should be in the form of pandas DataFrame or list of Series (got {type(df)})")

    labels = labels or df.keys()

    n = len(labels)
    nrows = min(n, nrows)
    ncols = n // nrows + int(bool(n % nrows))

    same_kind = False
    if isinstance(kind, str):
        kind = n * [kind]
        same_kind = True
    elif not isinstance(kind, Iterable) or len(kind) != n:
        raise ValueError(f"'kind' should be a string or an iterable of {n} strings")

    fig, axes = plt.subplots(nrows, ncols,
                             sharex='all' if (same_kind and sharex) else 'none',
                             sharey='row' if (same_kind and sharey) else 'none',
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
