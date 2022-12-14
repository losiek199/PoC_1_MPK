import pytest
import project.tests.Confest as conf
from collections import Counter


db = conf.db_client

@pytest.fixture(autouse=True)
def db_table_list():
    return db.meta.tables

@pytest.fixture(autouse=True)
def mandatory_tables():
    return ['cities', 'routes', 'trips', 'stop_times', 'stops', 'vehicle_types']

def test_db_connection_error():
    with pytest.raises(Exception) as e:
        db.initialize_connection('qlite:///bad_host.db')

def test_db_tables_present():
    assert len(db.meta.tables) > 0

def test_db_tables():
    assert len(db_table_list()) > 0
    assert [key for key, cnt in Counter(db_table_list())] == 1
    assert len(mandatory_tables()) == len([tab for tab in mandatory_tables() if tab in db_table_list])

def test_select_city_id():
    assert db.get_city_id('Wrocław') == 1
