import pytest
from collections import Counter
from project import db_controller

@pytest.fixture(autouse=True)
def db_table_list():
    return db_controller.meta.tables

@pytest.fixture(autouse=True)
def mandatory_tables():
    return ['cities', 'routes', 'trips', 'stop_times', 'stops', 'vehicle_types']

def test_db_connection_error():
    with pytest.raises(Exception) as e:
        db_controller.initialize_connection('qlite:///bad_host.db')

def test_db_tables_present():
    assert len(db_controller.meta.tables) > 0

def test_db_tables():
    assert len(db_controller.meta.tables) > 0
    assert [key for key, cnt in Counter(db_table_list())] == 1

def test_db_tables():
    assert len(db_controller.meta.tables) > 0
    assert len(mandatory_tables) == len([tab for tab in mandatory_tables() if tab in db_table_list])

def test_city_id():
    assert db_controller.get_city_id('Wrocław') == 1
