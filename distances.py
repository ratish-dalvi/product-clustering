import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN
from gensim import corpora, models, similarities


def create_distance_matrix(tokenized_texts, filter_extremes=False):
    # Create vectors (common words are penalized)
    dictionary = corpora.Dictionary(tokenized_texts, prune_at=None)  # dictionary
    if filter_extremes:
        dictionary.filter_extremes(no_below=5, no_above=0.5)

    corpus = [dictionary.doc2bow(d) for d in tokenized_texts]  # OHE vector
    tfidf = models.TfidfModel(corpus)  # TFIDF Model
    corpus = tfidf[corpus]  # Apply TFIDF

    # Compute distance matrix between descriptions
    index = similarities.MatrixSimilarity(corpus, num_features=len(dictionary))
    similarity_matrix = index[corpus]
    distance_matrix = 1 - similarity_matrix
    return distance_matrix


def get_product_indicator_function(product_ids):
    """ Matrix identifying whether a product ID was present in either
    of the pair.
    """
    prod_ids_found = product_ids.apply(len) > 0
    n = len(product_ids)
    I = np.ones((n, n))
    empty_indices = prod_ids_found[~prod_ids_found]
    for i in empty_indices:
        for j in empty_indices:
            I[i, j] = 0
    return I


def pprint(X1, X2, I, i, j):
    print("(%d, %d): DM1: %.3f, DM2: %.3f I: %d" %
          (i, j, X1[i, j], X2[i, j], I[i, j]))


def clustering(X, eps, num_samples):
    dbscan = DBSCAN(eps=eps, min_samples=num_samples, metric='precomputed')
    clusters = dbscan.fit(X)
    return clusters.labels_
