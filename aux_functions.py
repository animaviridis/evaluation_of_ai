import pandas as pd
import nltk
from typing import Union

import misc

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
    keys['remarks_yippy'] = k[23:25] + k[26:27]
    keys['remarks_eval'] = [k[28]]
    keys['eval'] = [k[27]]

    return data, keys


def count_words(data: Union[pd.Series, pd.DataFrame], label=None):
    if isinstance(data, pd.DataFrame):
        data = data[label]

    merged_text = "".join(data.dropna()).lower()
    words = nltk.tokenize.word_tokenize(merged_text)

    stop_words = nltk.corpus.stopwords.words("english") + [',', '.', ';', ':', "'", '(', ')', "n't"]

    ps = nltk.stem.PorterStemmer()

    stemmed_words = misc.ListDict()

    for w in words:
        if w not in stop_words:
            w_stem = ps.stem(w)
            if w_stem not in stop_words:
                stemmed_words[w_stem].append(w)

    counts = {v[0]: len(v) for v in stemmed_words.values()}

    counts_pandas = pd.Series(counts, name=label or "Word counts")

    return counts_pandas
