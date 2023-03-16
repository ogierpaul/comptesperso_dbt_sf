import pandas as pd
from stagingfinanzgurutosf.src.read_finanzguru_extract import latest_excel_as_df_prepared
from upload2sf import upload_df_to_sf, run_single_sql_statement, get_destination, set_env_variables_if_missing, format_triple_to_identifier

_table_name = 'STG_FINANZGURU'

def verify_latest_transaction_date(df, stagename:tuple):
    stagename_as_str = format_triple_to_identifier(stagename)
    q = f"""SELECT MAX(TO_DATE(DATE_ENREGISTREMENT)) as TRANSACTION_DATE\nFROM IDENTIFIER(%s)\n"""
    r = run_single_sql_statement(q, params=(stagename_as_str,), df_output=True)
    print('latest transaction date in database:', r['TRANSACTION_DATE'][0])
    print('latest transaction date in df:', df['DATE_ENREGISTREMENT'].max())
    return None




def upload_latest_excel_to_sf():
    set_env_variables_if_missing(project_name='comptesperso_dbt_sf', target_name='dev')
    destination = get_destination(table=_table_name)
    df = latest_excel_as_df_prepared()
    upload_df_to_sf(df, table=_table_name)
    verify_latest_transaction_date(df, destination)


if __name__ == '__main__':
    upload_latest_excel_to_sf()

