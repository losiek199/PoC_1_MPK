import pytest
import requests
from Confest import cities_mocked_row, routes_mocked_row
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


def test_post_flask_cities(cities_mocked_row):
    resp = client.post('/api/cities', data={"city_id": 1, "city_name": "Wrocław"})
    print(resp)
    assert resp.status_code == 200


def test_get_flask_routes_response(mocker, routes_mocked_row):
    mocker.patch('project.db_controller.select_routes_for_city',
                 return_value=routes_mocked_row)
    expected = routes_mocked_row
    resp = client.get('/api/routes/Wrocław')
    assert expected == json.loads(resp.data)


def test_post_flask_routes():
    client.post('/api/routes/Wrocław')
    assert pytest.raises(Exception)
