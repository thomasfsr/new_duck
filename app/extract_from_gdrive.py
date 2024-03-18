import io

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st
import duckdb

import log

import os

load_dotenv()

def create_data_dir(data_folder:str='data'):
    "Creates a data folder to keep the parquet tables from Google Drive"
    os.makedirs(data_folder, exist_ok=True)


def download_from_gdrive(data_folder:str='data'):
    "Downloads from the google drive folder the parquet files"
    data_folder = "data"
    folder_id = os.environ.get("folder_id")
    credentials = service_account.Credentials.from_service_account_file(
        "credentials/api_key.json"
    )

    drive_service = build("drive", "v3", credentials=credentials)

    files = (
        drive_service.files()
        .list(q=f"'{folder_id}' in parents and mimeType='application/octet-stream'")
        .execute()
    )

    con = log.connect_db()
    log.table_init(con)
    list_of_files = con.execute("SELECT filename FROM historical_files").fetchall()
    list_of_files = [row[0] for row in list_of_files]
    
    for file in files.get("files", []):
        file_id = file["id"]
        filename = file["name"]
        path_plus_filename = os.path.join(data_folder, filename)

        if not os.path.isfile(path_plus_filename) \
            and filename not in list_of_files:
            type = filename.split('.')[-1]
            if type == 'parquet':
                request = drive_service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = io.BytesIO(request.execute())
                with open(os.path.join(data_folder, filename), "wb") as f:
                    f.write(downloader.read())
                    filename_without_type = filename.split('.')[0]
                    st.write(f'File **{filename_without_type}** downloaded.')
            else:
                print(f"File type **{type}** not supported.")
                st.write(f"File type **{type}** not supported.")
        else:
            st.write(f"File **{filename}** is already loaded in the dataframe.")
    con.close()