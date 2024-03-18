import os

import duckdb
from dotenv import load_dotenv

load_dotenv()

path = os.getenv("path_csvs")

os.makedirs("data", exist_ok=True)
for file in os.listdir(path):
    filename = file.split(".", 1)[0]
    parquetname = filename + ".parquet"
    duckdb.read_csv(os.path.join(path, file)).to_parquet(
        os.path.join("data", parquetname)
    )
