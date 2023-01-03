import pytest
import requests
import os
import zipfile


"""Fixtures and configuration"""
mpk_source_url = 'https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data'
mpk_source_file_url = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'


"""Test methods"""
@pytest.mark.parametrize('url_to_test', [mpk_source_url, mpk_source_file_url])
def test_check_source_urls(url_to_test):
    assert requests.get(url_to_test).status_code == 200
