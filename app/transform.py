import os

import duckdb
import streamlit as st
from schema_class import schema

import log


def validation(data_folder: str = "data"):
    """Validation of the data with pandera"""
    passed = []
    con = log.connect_db()
    log.table_init(con)
    list_of_files = con.execute("SELECT filename FROM historical_files").fetchall()
    list_of_files = [row[0] for row in list_of_files]

    for file in os.listdir(data_folder):
        if file not in list_of_files:
            filename = file.split(".", 1)[0]
            filepath = os.path.join(data_folder, file)
            df = duckdb.read_parquet(filepath).fetchdf()
            try:
                schema.validate(df)
                passed.append(filepath)
                st.write("File {filename} is okay!")
                log.register_files(con, file)
            except Exception as e:
                st.write(f"File **{file}** has a problem.")
                continue
        else:
            st.write(f"File **{file}** is already loaded in the dataframe.")
            continue
    con.close()
    if passed:
        return passed
    else:
        return None


def concating(passed: list):
    """ Concat all files that passed the validation"""
    df = duckdb.sql(
        f"SELECT product_name, transaction_time, price, store FROM read_parquet({passed})"
    )
    return df
