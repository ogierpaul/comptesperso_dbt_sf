import pytest
import pandas as pd
from staging.src.read_finanzguru_extract import _hello_world
from staging.src import prepare_excel_for_upload, expected_columns
import os


@pytest.fixture
def dummy_export() -> pd.DataFrame:
    fd = os.path.dirname(os.path.abspath(__file__))
    fn = '20221210-Export-Alle_Buchungen.xlsx'
    fp = os.path.join(fd, fn)
    df = pd.read_excel(fp)
    return df


def test_hello_world():
    assert _hello_world() == 'Hello World'

def test_prepare_excel_for_upload(dummy_export):
    df = prepare_excel_for_upload(dummy_export)
    assert isinstance(df, pd.DataFrame)
    assert set(expected_columns) == set(df.columns)
