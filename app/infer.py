import os

import duckdb
import pandas as pd
from pandera import infer_schema


def infer(df: pd.DataFrame, directory_path: str = "infered_schema"):
    """Infer the schema of the first file downloaded, in this case I already know that this file has now issues."""
    os.makedirs(directory_path, exist_ok=True)
    schema = infer_schema(df)
    file_path = os.path.join(directory_path, "schema_inferred.py")
    with open(file_path, "w", encoding="utf-8") as arquivo:
        arquivo.write(schema.to_script())


if __name__ == "__main__":
    df = duckdb.read_parquet("data/daily_sales_retail_0.parquet").fetchdf()
    infer(df)
