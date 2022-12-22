import pytest
import project.tests.Confest as conf


db = conf.db_client

@pytest.fixture(autouse=True)
def mandatory_tables():
    return ['cities', 'routes', 'trips', 'stop_times', 'stops', 'vehicle_types']

def test_select_city_id(mocker, cities_mocked_row):
    mocker.patch('project.db_controller.get_city_id',
                 return_value=cities_mocked_row)
    expected = 1
    session = db.Session()
    assert db.get_city_id(session, 'Wrocław') == expected
