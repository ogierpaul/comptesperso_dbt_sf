import os
import pandas as pd
import snowflake
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import SnowflakeConnection
from stagingfinanzgurutosf.src import set_env_variables_if_missing

def sf_connection() -> SnowflakeConnection:
    set_env_variables_if_missing()
    con = snowflake.connector.connect(
        user=os.environ.get('SF_USER'),
        password=os.environ.get('SF_PASSWORD'),
        account=os.environ.get('SF_ACCOUNT'),
        database=os.environ.get('SF_DATABASE'),
        schema=os.environ.get('SF_SCHEMA'),
        role=os.environ.get('SF_ROLE'),
        warehouse=os.environ.get('SF_WAREHOUSE'),
        paramstyle="pyformat"
    )
    return con



def clean_token(s: str, max_length=32) -> str:
    assert isinstance(s, str)
    bad_chars = [';', ' ', '-', ',', '=', '/', "\\", "'", '"']
    for b in bad_chars:
        s = s.split(b)[0]
    s = s[:max_length]
    return s

def clean_object_triple(object_triple:tuple) -> tuple:
    assert len(object_triple) == 3
    return tuple([clean_token(s) for s in object_triple])

def formatname(object_triple:tuple) -> str:
    object_triple = clean_object_triple(object_triple)
    return f"""{object_triple[0]}.{object_triple[1]}.{object_triple[2]}"""

def run_sql_statement(q: str, params) -> None:
    q = q.strip().split(';')[0]
    with sf_connection() as con:
        con.cursor().execute(q, params)
        con.close()
    return None

def query_database(q: str, params) -> pd.DataFrame:
    q = q.strip().split(';')[0]
    with sf_connection() as con:
        r = con.cursor().execute(q, params).fetch_pandas_all()
        con.close()
    return r


def table_exists(object_triple:tuple) -> bool:
    object_triple = clean_object_triple(object_triple)
    information_schema_tables = formatname((object_triple[0], 'INFORMATION_SCHEMA', 'TABLES'))
    q = f"""SELECT TABLE_SCHEMA, TABLE_NAME\nFROM IDENTIFIER(%s) as i\nWHERE\ni.TABLE_SCHEMA = (%s) and i.TABLE_NAME = (%s)\n"""
    params = (information_schema_tables, object_triple[1], object_triple[2])
    r = query_database(q, params)
    return r.shape[0] > 0


def get_columns_info(object_triple:tuple) -> list:
    object_triple = clean_object_triple(object_triple)
    information_schema_columns = formatname((object_triple[0], 'INFORMATION_SCHEMA', 'COLUMNS'))
    q = f"""SELECT COLUMN_NAME\nFROM IDENTIFIER(%s) as i\nWHERE\ni.TABLE_SCHEMA = (%s) and i.TABLE_NAME = (%s)\nORDER BY i.ORDINAL_POSITION ASC"""
    params = (information_schema_columns, object_triple[1], object_triple[2])
    r = query_database(q, params)
    r = r['COLUMN_NAME'].values
    return r


def compare_columns_info(df: list, db: list) -> bool:
    df = [c.upper() for c in df]
    db = [c.upper() for c in db]
    same_cols = ( tuple(df) == tuple(db))
    if same_cols is False:
        raise KeyError(f"""Different columns mapping between df and database: {df} vs {db}""")
    return same_cols

def create_table_if_not_exists(object_triple:tuple, columns: list):
    columns = [clean_token(c).upper() for c in columns]
    objectname = formatname(object_triple)
    col_list = ",\n".join([f"""{c} VARCHAR""" for c in columns])
    params = (objectname, )
    q = f"""CREATE TABLE IF NOT EXISTS IDENTIFIER(%s) (\n {col_list} , \n PRIMARY KEY (TRANSACTION_ID))"""
    run_sql_statement(q, params)
    pass

def truncate_table(object_triple:tuple):
    objectname = formatname(object_triple)
    q = f"""TRUNCATE TABLE IDENTIFIER(%s)"""
    params = (objectname, )
    run_sql_statement(q, params)
    pass


def prepare_table(df, object_triple:tuple):
    df_cols = df.columns.tolist()
    if table_exists(object_triple):
        print('table exists')
        db_cols = get_columns_info(object_triple)
        assert compare_columns_info(df_cols, db_cols)
        print('column matches')
        truncate_table(object_triple)
        print('truncate_table')
    else:
        print('create table')
        create_table_if_not_exists(object_triple, df_cols)


def append_with_pandas(df, destination:tuple):
    destination = clean_object_triple(destination)
    with sf_connection() as conn:
        r = write_pandas(df=df, conn=conn, database=destination[0], schema=destination[1], table_name=destination[2], overwrite=False,
                         auto_create_table=False, quote_identifiers=False, create_temp_table=False)
    print('write_pandas: ', r)
    conn.close()

def upload_to_table(df, destination:tuple):
    prepare_table(df, destination)
    append_with_pandas(df, destination)
    return None