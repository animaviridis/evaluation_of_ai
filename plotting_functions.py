import matplotlib.pyplot as plt
import pandas as pd

import aux_functions as aux


def make_plot(df: pd.DataFrame, labels, nrows=2, show=True, title=None, fig_kwargs=None, **kwargs):
    fig_kwargs = fig_kwargs or {}

    ncols = len(labels) // nrows + int(bool(len(labels) % nrows))

    fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)

    for i, label in enumerate(labels):
        make_subplot(df, label, ax=axes[i//nrows, i % nrows], show=False, **kwargs)

    plt.suptitle(title or "", fontsize=16)

    if show:
        plt.show()

    return fig


def count(df: pd.DataFrame, label):
    return df[label].value_counts()


def make_subplot(df, label, type='pie', ax=None, show=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    counts = count(df, label)

    if type == 'pie':
        pie_subplot(counts, ax, **kwargs)
    else:
        raise ValueError(f"Plot type '{type}' not recognised")

    if show:
        plt.show()

    ax.set_title(aux.break_label(counts.name, ['a ', 'do']))


def pie_subplot(counts, ax, **kwargs):
    pie = ax.pie(counts, **kwargs)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(pie[0], aux.break_labels(counts.keys()), fontsize=10,
              bbox_transform=ax.transAxes, bbox_to_anchor=(1, 0.5), loc="center left")


