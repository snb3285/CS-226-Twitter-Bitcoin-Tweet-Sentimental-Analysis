from pathlib import Path
import pandas as pd


data_dir = Path('/Users/admin/PycharmProjects/SentimentPipeline/parc')
full_df = pd.concat(
    pd.read_parquet(parquet_file)
    for parquet_file in data_dir.glob('*.parquet')
)
full_df.to_csv('combinedparquetscores.csv')
print(full_df)

