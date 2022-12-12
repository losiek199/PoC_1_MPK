import pytest
import requests
import project.api_handler as ah

"""Fixtures"""
@pytest.fixture(autouse=True)
def source_file_response():
    return requests.get('https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data')

mpk_source_url = 'https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data'
local_source_url = 'http://127.0.0.1:5000/'
test_city = 'Wrocław'

"""Test methods"""
@pytest.mark.parametrize("config", [local_source_url, mpk_source_url])
def test_connection_to_host(config):
    resp = requests.get(config)
    assert resp.status_code == 200

@pytest.mark.parametrize("config",[(local_source_url.join(url)).replace('<city_name>', test_city) for url in ah.app.url_map.iter_rules()])
def test_get_flask_defined_urls(config):
    resp = requests.get(config)
    assert resp.status_code == 200

