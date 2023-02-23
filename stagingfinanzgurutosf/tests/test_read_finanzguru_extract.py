import pytest
import pandas as pd
from stagingfinanzgurutosf.src.read_finanzguru_extract import _hello_world
from stagingfinanzgurutosf.src import prepare_excel_for_upload, global_expected_columns
from importlib import resources as pkg_resources
import os

global_fn  = '20221210-Export-Alle_Buchungen.xlsx'

@pytest.fixture
def dummy_export() -> pd.DataFrame:
    fd = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(fd, global_fn)
    df = pd.read_excel(fp)
    return df


def test_hello_world():
    assert _hello_world() == 'Hello World'

def test_prepare_excel_for_upload(dummy_export):
    df = prepare_excel_for_upload(dummy_export, global_fn)
    assert isinstance(df, pd.DataFrame)
    assert set(global_expected_columns) == set(df.columns)
    assert df.index.name == 'TRANSACTION_ID'
    assert df.index.is_unique
