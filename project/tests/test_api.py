import pytest
import requests
from Confest import cities_mocked_row, routes_mocked_row, trips_mocked_row
import json

import project.api_handler as ah

"""Fixtures and configuration"""
mpk_source_url = 'https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data'
local_source_url = 'http://127.0.0.1:5000/'
test_city = 'Wrocław'
app = ah.app
client = ah.app.test_client()

@pytest.fixture(autouse=True)
def source_file_response():
    return requests.get('https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data')


"""Test methods"""
def test_get_flask_defined_urls():
    resp = client.get('/')
    assert resp.status_code == 200


def test_get_flask_cities_response(mocker, cities_mocked_row):
    mocker.patch('project.db_controller.select_from_table',
                 return_value=cities_mocked_row)
    expected = {"cities":[{"city_id": 1, "city_name": "Wrocław"}]}
    resp = client.get('/api/cities')
    assert expected == json.loads(resp.data)


def test_post_flask_cities(mocker):
    mocker.patch('project.db_controller.insert_data_row', return_value=1)
    json_data = {"city_id": 1, "city_name": "Wrocław"}
    resp = client.post('/api/cities', json=json_data)
    assert resp.status_code == 200
    assert json.loads(resp.data) == json_data


def test_get_flask_routes_response(mocker, routes_mocked_row):
    mocker.patch('project.db_controller.select_routes_for_city',
                 return_value=routes_mocked_row)
    expected = routes_mocked_row
    resp = client.get('/api/routes/Wrocław')
    assert expected == json.loads(resp.data)
    assert resp.status_code == 200


def test_get_flask_trips_response(mocker, trips_mocked_row ):
    mocker.patch('project.db_controller.select_city_trips',
                 return_value=trips_mocked_row)
    expected = trips_mocked_row
    resp = client.get('/api/trips/Wrocław')
    assert resp.status_code == 200
    assert expected == json.loads(resp.data)
