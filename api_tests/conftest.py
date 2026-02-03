import pytest
import requests

from api_tests.config import BASE_URL, HEADERS
from api_tests.pet_builder import PetBuilder


@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(HEADERS)
    yield session
    session.close()


@pytest.fixture()
def created_pet(api_client):
    pet_data = PetBuilder().build()
    response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
    assert response.status_code == 200
    pet_json = response.json()
    yield pet_json
    api_client.delete(f"{BASE_URL}/pet/{pet_json['id']}")


@pytest.fixture()
def pet_data():
    return PetBuilder().build()
