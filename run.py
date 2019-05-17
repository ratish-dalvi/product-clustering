import numpy as np
from tokenizer import tokenize_text, product_id_parser
from distances import create_distance_matrix, get_product_indicator_function, pprint, clustering

# Load data
df = pd.read_csv("~/Downloads/importers.csv")
x_train = df['PRODUCT_DESCRIPITION']
print("Total rows fetched: %d" % len(df))
print("Total number of importers: %d" % df['IMPORTER'].nunique())

tokenized_descriptions = x_train.apply(tokenize_text,
                                       punctuation_replacement='', remove_numbers=True)

df_prod = x_train.apply(product_id_parser)
print("Counts of number of hits on product id: \n%s" %
      df_prod.num_matched.value_counts())
df['best_match_product_id'] = df_prod.best_match_product_id
df['detected_product_ids'] = df_prod.detected_product_ids
df['num_product_ids_detected'] = df_prod.num_matched

mask_no_prod_id = (df_prod.best_match_product_id.apply(len) == 0)
mask_prod_id = (df_prod.best_match_product_id.apply(len) > 0)

X1 = create_distance_matrix(tokenized_descriptions[mask_no_prod_id], filter_extremes=True)
df.loc[mask_no_prod_id, 'cluster'] = clustering(X1, 0.05, 2)
print(df.cluster.value_counts())
max_cluster = int(df.cluster.max()) + 1
# print(X1)
# print(tokenized_descriptions[mask_no_prod_id])

X2 = create_distance_matrix(df_prod.best_match_product_id[mask_prod_id])
y = clustering(X2, 0.4, 2)
y = np.where(y == -1, y, y + max_cluster)
df.loc[mask_prod_id, 'cluster'] = y


# I = get_product_indicator_function(df_prod.best_match_product_id)

for i, x in enumerate(df.PRODUCT_DESCRIPITION[:1]):
    print(i, x)

# Print
cluster_counts = df.cluster.value_counts()
print("\nNumber of clusters: %d" % df.cluster.nunique())
print("Descriptions that do not belong to any cluster: %s" % (df.cluster == -1).sum())
print("\nSummary stats on cluster size:\n%s" %
      cluster_counts.describe(percentiles=[0.01, 0.1, 0.9, 0.99]))

# Output columns
output_columns = ['IMPORTER', 'SUPPLIER_NAME',  'PRODUCT_DESCRIPITION',  'cluster',
                  'best_match_product_id', 'detected_product_ids', 'num_product_ids_detected']
df[output_columns].to_csv('~/Downloads/importer_clusters.csv', index=False)
