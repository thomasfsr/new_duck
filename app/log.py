import duckdb
import os
from datetime import datetime

def conectar_banco(file_path:str='log'):
    """Connect to a existing database"""
    os.makedirs(file_path, exist_ok=True)
    return duckdb.connect(database=f'{file_path}/files_log.db', read_only=False)

def table_init(con):
    """Create table of log"""
    con.execute("""
        CREATE TABLE IF NOT EXISTS historical_files (
            filename VARCHAR,
            processed_time TIMESTAMP
        )
    """)

def register_files(con, filename):
    """Register the filename with the time of the processing"""
    con.execute("""
        INSERT INTO historical_files (filename, processed_time)
        VALUES (?, ?)
    """, (filename, datetime.now()))

def arquivos_processados(con):
    """Return the name of all processed files"""
    return set(row[0] for row in con.execute("SELECT filename FROM historical_files").fetchall())