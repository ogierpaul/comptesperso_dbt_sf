import pytest
import pandas as pd
from stagingfinanzgurutosf import prepare_excel_for_upload, _global_expected_columns
from importlib import resources as pkg_resources
import os

global_fn  = '20221210-Export-Alle_Buchungen.xlsx'

@pytest.fixture
def dummy_export() -> pd.DataFrame:
    fd = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(fd, global_fn)
    df = pd.read_excel(fp)
    return df



def test_prepare_excel_for_upload(dummy_export):
    df = prepare_excel_for_upload(dummy_export, global_fn)
    assert isinstance(df, pd.DataFrame)
    if set(_global_expected_columns) != set(df.columns):
        columns_not_in_expected = set(df.columns) - set(_global_expected_columns)
        columns_not_in_df = set(_global_expected_columns) - set(df.columns)
        raise ValueError(f"""Columns do not match.\n\
        Columns in df that are not in _global_expected_columns: {columns_not_in_expected}\
        Columns in _global_expected_columns that are not in df: {columns_not_in_df}""")
    assert df['TRANSACTION_ID'].is_unique
