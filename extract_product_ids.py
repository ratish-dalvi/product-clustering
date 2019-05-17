import pandas as pd

from tokenizer import product_id_parser

df = pd.read_csv("/Users/rdalvi/Downloads/parsed_product_ids_REVERTED - parsed_product_ids.csv")
df_prod = df.Description.apply(product_id_parser)
extracted_product_ids = df_prod.product_id

df_prod['old'] = df['Extracted product_id']
df_prod['comment'] = df['Group']
df_prod['description'] = df.Description.values
df_prod.to_csv('~/Downloads/parsed_product_ids.csv', index=False)

print(df_prod.head())
print("Counts of number of hits on product id: \n%s" % df_prod.num_matched.value_counts())
