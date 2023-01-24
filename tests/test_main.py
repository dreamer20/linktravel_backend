import requests
import pytest


@pytest.fixture
def mock_response(monkeypatch):
    def get_mock(*args, **kwargs):
        with open('tests/test_index.html', 'rb') as f:
            html = f.read()
        class MockResponse:
            text = html
            status_code = 200
        return MockResponse

    monkeypatch.setattr(requests, 'get', get_mock)


def test_main(client):
    response = client.get('/')
    assert response.status_code == 200, response.text


def test_get_links(client, mock_response):
    """ Should return list of URL """
    url = 'http://example.com'
    response = client.post('/', json={'url': url})
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert len(response_json) == 6


def test_get_links_only_root(client, mock_response):
    """ Should return list of URL with hostname only """
    url = 'http://example.com'
    response = client.post('/', json={'url': url, 'only_root': True})
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert  {'url': 'https://sub.test.com.ua', 'links': []} in response_json


def test_get_links_without_subdomain(client, mock_response):
    """ Should return list of URL without subdomain """
    url = 'http://example.com'
    response = client.post('/', json={'url': url, 'only_root': True , 'without_subdomain': True})
    assert response.status_code == 200, response.text
    response_json = response.json()
    assert {'url': 'https://test.com.ua', 'links': []} in response_json
    assert len(response_json) == 3
