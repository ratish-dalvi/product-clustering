import click

import pandas as pd
import numpy as np
from tokenizer import tokenize_text, product_id_parser
from core import create_distance_matrix, clustering


@click.command()
@click.option("--input-filepath", "-i", type=str, required=True, help="Absolute path of the input file")
@click.option("--output-filepath", "-o", type=str, required=True,  help="Absolute path of the output file")
@click.option("--importer-colname", "-im", type=str, required=True, help="Column name of the importer")
@click.option("--product-description-colname", "-p", type=str, required=True, default=None,
              help="Column name containing product descriptions")
def run(input_filepath, output_filepath, product_description_colname, importer_colname):
    # Load data
    df = pd.read_csv(input_filepath)
    x_train = df[product_description_colname]
    print("Total rows fetched: %d" % len(df))
    print("Total number of importers: %d" % df[importer_colname].nunique())

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
        importer_colname, product_description_colname,  'cluster',
        'best_match_product_id', 'detected_product_ids', 'num_product_ids_detected']
    df[output_columns].to_csv(output_filepath, index=False)


if __name__ == '__main__':
    run()
