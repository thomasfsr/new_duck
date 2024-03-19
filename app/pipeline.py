import os

import streamlit as st
import transform

import app.extract_from_gdrive as extract_from_gdrive


def pipeline(output_dir: str = "database", table_name: str = "sales_table.parquet"):
    """* Initialize the pipeline of creating directory for the files in G-Drive;  
    * download the files from google drive;  
    * check if the files were already in the log of files already loaded;  
    * validate the file type;  
    * validate the data itself if there is no Null values or price less than 0;  
    * concat the files passed in the validation into a parquet files with only the relevant columns.
    """
    os.makedirs(output_dir, exist_ok=True)
    extract_from_gdrive.create_data_dir()
    extract_from_gdrive.download_from_gdrive()
    passed = transform.validation("data")
    if passed is not None:
        df = transform.concating(passed)
        df.to_parquet(os.path.join(output_dir, table_name))
    else:
        st.write("There is no file to update.")
        pass
