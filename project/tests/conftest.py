import tempfile
import pytest
import os
import project.db_controller as db
import project.api_handler as ah

@pytest.fixture(autouse=True)
def client():
    db_fd, ah.app.config['DATABASE'] = tempfile.mkstemp()
    ah.app.config['TESTING'] = True
    yield client

    os.close(db_fd)
    os.unlink(ah.app.config['DATABASE'])


@pytest.fixture(autouse=True)
def db_client():
    return db


@pytest.fixture(autouse=True)
def cities_mocked_row():
    return [{'city_id': 1, 'city_name': 'Wrocław'}]

@pytest.fixture(autouse=True)
def routes_mocked_row():
    return [
                {"agency_id": 2,
                "city_id": 1,
                "route_desc": "KOZANÓW - Kozanowska - Popowicka - Kozanowska - KOZANÓW",
                "route_id": "C",
                "route_long_name": None,
                "route_short_name": "C ",
                "route_type": 3,
                "route_type2_id": 35,
                "valid_from": "2022-11-26",
                "valid_until": "2999-01-01"}
            ]

@pytest.fixture(autouse=True)
def trips_mocked_row():
    return [{'city_id': '1',
             'trip_id': '8_11600331',
             'trip_headsign': 'LEŚNICA',
             'route_id': '923',
             'arrival_time': '05:05:00',
             'stop_id': '4201',
             'stop_code': 18388,
             'stop_name': 'LEŚNICA',
             'vehicle_type_id': 1}]

