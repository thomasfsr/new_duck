from app import extract, transform
import os

def pipeline(output:str='database',
             table_name:str='sales_table.parquet'
             ):
    extract.create_data_dir()
    extract.download_from_gdrive()
    passed = transform.validation('data')
    df = transform.concating(passed)
    df.to_parquet(os.path.join(output,table_name))

if __name__ == "__main__":
    pipeline()