
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
