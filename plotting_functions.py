import matplotlib.pyplot as plt
import pandas as pd

import aux_functions as aux


def pie_plot(df: pd.DataFrame, label, ax=None, show=True, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    counts = df[label].value_counts()

    pie = ax.pie(counts, **kwargs)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(pie[0], aux.break_labels(counts.keys()), fontsize=9,
              bbox_transform=ax.transAxes, bbox_to_anchor=(1, 0.5), loc="center left")

    ax.set_title(aux.break_label(counts.name, ['a ', 'do']))

    if show:
        plt.show()


def pie_subplots(df: pd.DataFrame, labels, nrows=2, show=True, title=None, fig_kwargs=None):
    fig_kwargs = fig_kwargs or {}

    ncols = len(labels) // nrows + int(bool(len(labels) % nrows))
    fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
    for i, label in enumerate(labels):
        pie_plot(df, label, ax=axes[i//nrows, i % nrows], show=False)

    plt.suptitle(title or "", fontsize=16)
    if show:
        plt.show()

    return fig
