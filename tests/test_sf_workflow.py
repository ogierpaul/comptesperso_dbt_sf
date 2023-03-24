import pytest
from upload2sf import sf_connection, set_env_variables_if_missing


@pytest.fixture(scope="module")
def cursor():
    set_env_variables_if_missing(project_name='comptesperso_dbt_sf', target_name='dev')
    con = sf_connection()
    curs = con.cursor()
    yield curs
    curs.close()
    con.close()
    pass

def test_connection_is_working(cursor):
    assert cursor.execute("SELECT 1").fetchone()[0] == 1


