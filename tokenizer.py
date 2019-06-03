import re

import numpy as np
import pandas as pd

regex_alpha_numeric_only = re.compile(r'[^a-zA-Z0-9\s]+', re.UNICODE)
regex_alpha_numeric_only_no_space = re.compile(r'[^a-zA-Z0-9]+', re.UNICODE)

regex_numeric = re.compile(r'[0-9]+', re.UNICODE)


# Regexes for product ID in the decreasing order of priority
product_regexes = [
    re.compile(r'\b'
               r'[a-zA-Z]{1,3}'
               r'[\s]?[-]?[\s]?'
               r'[0-9]{1,5}'
               r'[\s]?[-]?[\s]?'
               r'[a-zA-Z]{0,2}'
               r'\b', re.UNICODE),

    re.compile(r'\s'
               r'[0-9]{2,5}'
               r'[-]?'
               r'[a-zA-Z]{0,3}'
               r'\s', re.UNICODE),

    re.compile(r'\b'                        # Similar to the first one, but allows for longer words
               r'[a-zA-Z]{4,5}'
               r'[\s]?-[\s]?'
               r'[0-9]{1,5}'
               r'\b', re.UNICODE),
    ]

irrelevant_numbers_regexes = [
    re.compile(r'[0-9]+[\s]?X[\s]?[0-9]+[\s]?(KGS)?(KG)?(LT)?(G)?', re.UNICODE),  # eg. 30 X 400
    re.compile(r'[0-9]+[\s]?KG[S]?', re.UNICODE),  # eg. 300 KG
    re.compile(r'QTY[\s]?[0-9]+', re.UNICODE),  # eg. QTY 344
    re.compile(r'[0-9]+LT', re.UNICODE),  # eg. 2 LT
    re.compile(r'^20[12][0-9]$', re.UNICODE),  # eg. year 2019, 2018 etc
]


def remove_punctuation(x: str, replacement: str) -> str:
    """ Replace/remove punctuation from text
    :param replacement: character to replace the punctuation by
    :return: `x` without punctuations
    """
    return regex_alpha_numeric_only.sub(replacement, x)


def tokenize_text(txt: str, prefix: str = None, punctuation_replacement: str = None,
                  remove_numbers=False) -> list:
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

    if remove_numbers:
        txt = regex_numeric.sub(' ', txt)

    tokens = txt.split()
    clean_tokens = [x for x in tokens if not is_null(x)]
    if prefix is not None:
        clean_tokens = ["%s:%s" % (prefix, x) for x in clean_tokens]

    return clean_tokens


def remove_irrelevant_numbers(txt):
    for reg_tmp in irrelevant_numbers_regexes:
        txt = reg_tmp.sub(' ', txt)
    return txt


def is_null(x: str) -> bool:
    """ Check if x is null

    :param x: scalar
    :return: boolean, indicating whether the token is null or not
    """
    return pd.isnull(x) or (x.strip() == '') or len(x) <= 2


def id_cleanup(x):
    # return x.replace(" ", "").replace("-", "").upper()
    return regex_alpha_numeric_only_no_space.sub('', x)


def is_false_positive(x):
    if len(x) <= 2:
        return True
    return False


def duplicate_match(new_match, current_matches):
    for x in current_matches:
        if new_match in x and new_match != x:
            return True


def product_id_parser(x):
    x = remove_irrelevant_numbers(x)
    all_matches = []
    for reg in product_regexes:
        matches = reg.finditer(x)
        matches = [(match.group(), match.span()) for match in matches]
        standardised_matches = [(id_cleanup(match), span) for (match, span) in matches]
        all_matches.extend(standardised_matches)

    lst_all_matches = [match for (match, span) in all_matches]

    final_matches = [
        (match, span) for (match, span) in all_matches
        if not (is_false_positive(match) or duplicate_match(match, lst_all_matches))
        ]

    # Pick the best match. Span is a tuple, so we pick the first one
    if final_matches:
        best_match = [sorted(final_matches, key=lambda x: x[1][0])[0][0]]
    else:
        best_match = []

    return pd.Series({'detected_product_ids': final_matches,
                      'best_match_product_id': best_match,
                      'num_matched': len(final_matches)})
