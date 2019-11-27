import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def break_label(label, breakwords=None):
    if breakwords is None:
        breakwords = ['and']
    for breakword in breakwords:
        label = label.replace(f' {breakword}', f'\n{breakword}')
    return label


def break_labels(labels):
    return [break_label(label, ['and', 'not']) for label in labels]


def pie_plot(df, label, ax=None, show=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    counts = df[label].value_counts()

    pie = ax.pie(counts, **kwargs)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(pie[0], break_labels(counts.keys()), fontsize=9,
              bbox_transform=ax.transAxes, bbox_to_anchor=(1, 0.5), loc="center left")

    ax.set_title(break_label(counts.name, ['a ', 'do']))

    if show:
        plt.show()


def pie_subplots(df, labels, nrows=2, show=True, title=None, fig_kwargs=None):
    fig_kwargs = fig_kwargs or {}

    ncols = len(labels) // nrows + int(bool(len(labels) % nrows))
    fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
    for i, label in enumerate(labels):
        pie_plot(df, label, ax=axes[i//nrows, i % nrows], show=False)

    plt.suptitle(title or "", fontsize=16)
    if show:
        plt.show()

    return fig
