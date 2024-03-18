import extract, transform
import os

def pipeline(output_dir:str='database',
             table_name:str='sales_table.parquet'
             ):
    os.makedirs(output_dir, exist_ok=True )
    extract.create_data_dir()
    extract.download_from_gdrive()
    passed = transform.validation('data')
    df = transform.concating(passed)
    df.to_parquet(os.path.join(output_dir,table_name))