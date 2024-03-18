from schema_class import schema
import duckdb
import os
import streamlit as st

def validation(data_folder:str='data'):
    passed = []
    for file in os.listdir(data_folder):
        filename = file.split('.',1)[0]
        filepath = os.path.join(data_folder,file)
        df = duckdb.read_parquet(filepath).fetchdf()
        try:
            schema.validate(df)
            passed.append(filepath)
            print(f"File {filename} is okay!")
            st.write(f"File {filename} is okay!")
        except Exception as e:
            print(f"File {filename} has a problem")
            st.write(f"File {filename} has a problem")
            continue
    return passed

def concating(passed:list):
    df = duckdb.sql(f"SELECT product_name, transaction_time, price, store FROM read_parquet({passed})").fetchdf()
    return df

def pipeline():
    passed = validation('data')
    df = concating(passed)