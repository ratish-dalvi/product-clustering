import pandas as pd
import numpy as np
from tokenizer import tokenize_text, product_id_parser
from distances import create_distance_matrix, get_product_indicator_function, pprint, clustering

# EDIT

INUPT_FILENAME = "~/Downloads/2018Finaltry.csv"
OUTPUT_FILENAME = '~/Downloads/2018Finaltry_output.csv'
DESCRIPTION_COLNAME = 'PRODUCT_DESCRIPTION'
IMPORTER_COLNAME = 'INDIAN_IMPORTER_NAME'

# Load data
df = pd.read_csv(INUPT_FILENAME)
x_train = df[DESCRIPTION_COLNAME]
print("Total rows fetched: %d" % len(df))
print("Total number of importers: %d" % df[IMPORTER_COLNAME].nunique())

# Extract product IDs from text
df_prod = x_train.apply(product_id_parser)
print("Counts of number of hits on product id: \n%s" % df_prod.num_matched.value_counts())
df['best_match_product_id'] = df_prod.best_match_product_id
df['detected_product_ids'] = df_prod.detected_product_ids
df['num_product_ids_detected'] = df_prod.num_matched

mask_no_prod_id = (df_prod.best_match_product_id.apply(len) == 0)
mask_prod_id = (df_prod.best_match_product_id.apply(len) > 0)

# Clustering Part 1: on texts without product ids
tokenized_descriptions = x_train.apply(
    tokenize_text, punctuation_replacement='', remove_numbers=True)
X1 = create_distance_matrix(tokenized_descriptions[mask_no_prod_id], filter_extremes=True)
df.loc[mask_no_prod_id, 'cluster'] = clustering(X1, 0.05, 2)
max_cluster = int(df.cluster.max()) + 1

# Clustering Part 2: on texts with product ids
X2 = create_distance_matrix(df_prod.best_match_product_id[mask_prod_id])
y = clustering(X2, 0.4, 2)
y = np.where(y == -1, y, y + max_cluster)
df.loc[mask_prod_id, 'cluster'] = y


# Describe the clusters formed
cluster_counts = df.cluster.value_counts()
print("\nNumber of clusters: %d" % df.cluster.nunique())
print("Descriptions that do not belong to any cluster: %s" % (df.cluster == -1).sum())
print("\nSummary stats on cluster size:\n%s" %
      cluster_counts.describe(percentiles=[0.01, 0.1, 0.9, 0.99]))

# Output columns
output_columns = [
    IMPORTER_COLNAME, DESCRIPTION_COLNAME,  'cluster',
    'best_match_product_id', 'detected_product_ids', 'num_product_ids_detected']
df[output_columns].to_csv(OUTPUT_FILENAME, index=False)
