import io

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

import os

import duckdb
load_dotenv()

def create_data_dir():
    "Creates a data folder to keep the parquet tables from Google Drive"
    os.makedirs("data", exist_ok=True)


def download_from_gdrive():
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

    for file in files.get("files", []):
        file_id = file["id"]
        file_name = file["name"]
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = io.BytesIO(request.execute())
        with open(os.path.join(data_folder, file_name), "wb") as f:
            f.write(downloader.read())
