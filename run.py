import pandas as pd
from gensim import corpora, models, similarities
from sklearn.cluster import DBSCAN
from tokenizer import tokenize_text, product_id_parser

# Load data
df = pd.read_csv("~/Downloads/importers.csv")
X_train = df['PRODUCT_DESCRIPITION']
print("Total rows fetched: %d" % len(df))
print("Total number of importers: %d" % df['IMPORTER'].nunique())

# Tokenize data
descriptions = X_train.apply(tokenize_text, punctuation_replacement='')
df_prod = X_train.apply(product_id_parser)
print("Counts of number of hits on product id: \n%s" % df_prod.num_matched.value_counts())
df_prod['description'] = X_train.values
df_prod.to_csv('~/Downloads/parsed_product_ids.csv', index=False)

# Create vectors (common words are penalized)
dictionary = corpora.Dictionary(descriptions, prune_at=None)  # dictionary
corpus = [dictionary.doc2bow(d) for d in descriptions]  # OHE vector
tfidf = models.TfidfModel(corpus)  # TFIDF Model
corpus = tfidf[corpus]  # Apply TFIDF

# Compute distance matrix between descriptions
index = similarities.MatrixSimilarity(corpus, num_features=len(dictionary))
similarity_matrix = index[corpus]
distance_matrix = 1 - similarity_matrix
# print(distance_matrix)

# Apply clustering
dbscan = DBSCAN(eps=0.3, min_samples=3, metric='precomputed')
clusters = dbscan.fit(distance_matrix)
df['cluster'] = clusters.labels_

# Print
cluster_counts = df.cluster.value_counts()
print("\nNumber of clusters: %d" % df.cluster.nunique())
print("Descriptions that do not belong to any cluster: %s" % (df.cluster == -1).sum())
print("\nSummary stats on cluster size:\n%s" %
      cluster_counts.describe(percentiles=[0.01, 0.1, 0.9, 0.99]))

# Output columns
output_columns = ['IMPORTER', 'SUPPLIER_NAME',  'PRODUCT_DESCRIPITION',  'cluster']
df[output_columns].to_csv('~/Downloads/importer_clusters.csv', index=False)
