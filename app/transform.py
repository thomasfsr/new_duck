from schema_class import schema
import duckdb
import os
import streamlit as st
import log

def validation(data_folder:str='data'):
    passed = []
    con = log.connect_db()
    log.table_init(con)
    list_of_files = con.execute("SELECT filename FROM historical_files").fetchall()
    list_of_files = [row[0] for row in list_of_files]

    for file in os.listdir(data_folder):
        if file not in list_of_files:
            filename = file.split('.',1)[0]
            filepath = os.path.join(data_folder,file)
            df = duckdb.read_parquet(filepath).fetchdf()
            try:
                schema.validate(df)
                passed.append(filepath)
                st.write(f"File {filename} is okay!")
                log.register_files(con, file)
            except Exception as e:
                st.write(f"File {filename} has a problem")
                continue
        else:
                st.write(f"File {filename} is already loaded in the dataframe")
                continue

    return passed

def concating(passed:list):
    df = duckdb.sql(f"SELECT product_name, transaction_time, price, store FROM read_parquet({passed})")
    return df