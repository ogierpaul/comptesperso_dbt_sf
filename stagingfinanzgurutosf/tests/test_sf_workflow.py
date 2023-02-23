import pytest
from stagingfinanzgurutosf.src.sf_utils import sf_connection, clean_token, clean_object_triple, query_database

@pytest.fixture(scope="module")
def cursor():
    con = sf_connection()
    curs = con.cursor()
    yield curs
    curs.close()
    con.close()
    pass

def test_connection_is_working(cursor):
    assert cursor.execute("SELECT 1").fetchone()[0] == 1


def test_clean_token():
    assert "DROP TABLE USERS" not in clean_token("INSERT INTO USERS FOO; DROP TABLE USERS;")

def test_remove_bad_chars_from_namespace():
    namespace = ("DROP TABLE USERS", "foo", "bar")
    namespace = clean_object_triple(namespace)
    assert "DROP TABLE USERS" not in namespace[0]

