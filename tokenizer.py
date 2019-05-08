import re

import numpy as np
import pandas as pd

regex_alpha_numeric_only = re.compile(r'[^a-zA-Z0-9\s]+', re.UNICODE)


def remove_punctuation(x: str, replacement: str) -> str:
    """ Replace/remove punctuation from text
    :param replacement: character to replace the punctuation by
    :return: `x` without punctuations
    """
    return regex_alpha_numeric_only.sub(replacement, x)


def tokenize_text(txt: str, prefix: str = None, punctuation_replacement: str = None) -> list:
    """ Tokenize a scalar into a list of tokens

    :param x: scalar to tokenize
    :return: list of tokens created from x
    """
    if pd.isnull(txt):
        return []
    if not np.isscalar(txt):
        raise TypeError('Input must be a scalar')

    txt = str(txt).lower()
    if punctuation_replacement is not None:
        txt = remove_punctuation(txt, punctuation_replacement)

    tokens = txt.split()
    clean_tokens = [x for x in tokens if not is_null(x)]
    if prefix is not None:
        clean_tokens = ["%s:%s" % (prefix, x) for x in clean_tokens]

    return clean_tokens


def is_null(x: str) -> bool:
    """ Check if x is null

    :param x: scalar
    :return: boolean, indicating whether the token is null or not
    """
    return pd.isnull(x) or (x.strip() == '')


# Regexes for product ID in the decreaseing order of priority
product_regexes = [
    re.compile(r'\b[a-zA-Z]{1,2}[\s]?[-]?[\s]?[0-9]{2,4}\b', re.UNICODE),
    re.compile(r'\b[0-9]{3,5}\b', re.UNICODE)
]


def id_cleanup(x):
    return x.replace(" ", "").replace("-", "").upper()


def product_id_parser(x):
    for reg in product_regexes:
        matches = reg.findall(x)
        standardised_matches = set([id_cleanup(match) for match in matches])
        unique_matches = set(standardised_matches)
        if len(unique_matches) > 0:
            return pd.Series({'product_id': unique_matches,
                              'num_matched': len(unique_matches)})
    return pd.Series({'num_matched': 0})
