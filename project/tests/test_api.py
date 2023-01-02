import pytest
from unittest import mock
import requests
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
    mocker.patch('project.api_handler.select_cities', return_value=cities_mocked_row)
    expected = {"cities": [{"city_id": 1, "city_name": "Wrocław"}]}
    resp = client.get('/api/cities')
    assert expected == json.loads(resp.data)

def test_post_flask_cities_success(mocker):
    mocker.patch('project.api_handler.insert_city_row', return_value=1)
    json_data = {"city_id": 1, "city_name": "Wrocław"}
    resp = client.post('/api/cities', json=json_data)
    assert resp.status_code == 200
    assert json.loads(resp.data) == json_data
    assert resp.request.method == 'POST'


def test_post_flask_cities_failed(mocker):
    mocker.patch('project.api_handler.insert_city_row', return_value=0)
    json_data = {"city_id": 1, "city_name": "Wrocław"}
    resp = client.post('/api/cities', json=json_data)
    assert resp.status_code == 409
    assert resp.data.decode(encoding='UTF-8') == f'{json_data} already exists'
    assert resp.request.method == 'POST'


def test_get_flask_routes_response(mocker, routes_mocked_row):
    mocker.patch('project.api_handler.select_routes_for_city',
                 return_value=routes_mocked_row)
    mocker.patch('project.api_handler.select_count_from_city_trips',
                 return_value=1)
    expected = {'count': 1, 'routes': routes_mocked_row}
    resp = client.get('/api/routes/Wrocław')
    assert resp.status_code == 200
    assert expected == json.loads(resp.data)


def test_get_flask_trips_response(mocker, trips_mocked_row):
    mocker.patch('project.api_handler.select_city_trips',
                 return_value=trips_mocked_row, autospec=True)
    mocker.patch('project.api_handler.select_count_from_city_trips',
                 return_value=1)
    expected = {'page': 0, 'page_count': 1, 'per_page': 100, 'trips': trips_mocked_row}
    resp = client.get('/api/trips/Wrocław/0')
    assert resp.status_code == 200
    assert expected == json.loads(resp.data)
