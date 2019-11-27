import pandas as pd


def break_label(label, breakwords=None):
    if not isinstance(label, str):
        return label

    if breakwords is None:
        breakwords = ['and']
    for breakword in breakwords:
        label = label.replace(f' {breakword}', f'\n{breakword}')
    return label


def break_labels(labels):
    return [break_label(label, ['and', 'not']) for label in labels]


def prepare_data(fname=None):
    data = pd.read_excel(fname or 'data/main_survey_relabelled.xlsx')

    # divide questions
    k = list(data.keys())
    keys = dict()
    keys['general'] = k[2:6]
    keys['search_engines'] = k[6:9]
    keys['phrase'] = k[9:10]
    keys['tasks'] = k[10:18]
    keys['clustering'] = k[18:20]
    keys['yippy'] = k[20:23] + k[25:26]
    keys['remarks_yippy'] = k[23:24]
    keys['remarks_eval'] = [k[26], k[28]]
    keys['eval'] = [k[27]]

    return data, keys
