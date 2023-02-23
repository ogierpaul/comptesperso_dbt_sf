import os

import pandas as pd

from stagingfinanzgurutosf.src import set_env_variables_if_missing, latest_excel_as_df_prepared, query_database, formatname, upload_to_table



def verify_latest_transaction_date(df, stagename:tuple):
    q = f"""SELECT MAX(TO_DATE(DATE_ENREGISTREMENT)) as TRANSACTION_DATE\nFROM IDENTIFIER(%s)\n"""
    r = query_database(q, params=(formatname(stagename),))
    print('latest transaction date in database:', r['TRANSACTION_DATE'][0])
    print('latest transaction date in df:', df['DATE_ENREGISTREMENT'].max())
    return None

def get_destination() -> tuple:
    set_env_variables_if_missing()
    database = os.environ.get('SF_DATABASE')
    schema = os.environ.get('SF_SCHEMA')
    table = 'STG_FINANZGURU'
    destination = (database, schema, table)
    return destination

def read_latest_excel() ->pd.DataFrame:
    df = latest_excel_as_df_prepared().reset_index(drop=False)
    return df

def upload_to_stg(df:pd.DataFrame, destination:tuple):
    upload_to_table(df, destination)
    verify_latest_transaction_date(df, destination)


def main():
    destination = get_destination()
    df = read_latest_excel()
    upload_to_stg(df, destination)


if __name__ == '__main__':
    main()

