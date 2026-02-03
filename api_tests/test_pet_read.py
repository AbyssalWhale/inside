import pytest

from api_tests.config import BASE_URL, HTTP_OK, HTTP_NOT_FOUND, VALID_STATUSES
from api_tests.pet_builder import PetBuilder


@pytest.mark.api
class TestReadPetPositive:
    def test_get_pet_by_id(self, api_client, created_pet):
        pet_id = created_pet["id"]

        response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
        assert response.status_code == HTTP_OK

        body = response.json()
        assert body["id"] == pet_id
        assert body["name"] == created_pet["name"]
        assert body["status"] == created_pet["status"]

    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_find_pets_by_status(self, api_client, status):
        response = api_client.get(
            f"{BASE_URL}/pet/findByStatus", params={"status": status}
        )
        assert response.status_code == HTTP_OK

        body = response.json()
        assert isinstance(body, list)

    def test_find_pets_returns_created_pet(self, api_client, created_pet):
        status = created_pet["status"]
        pet_id = created_pet["id"]

        response = api_client.get(
            f"{BASE_URL}/pet/findByStatus", params={"status": status}
        )
        assert response.status_code == HTTP_OK

        body = response.json()
        pet_ids = [pet["id"] for pet in body]
        assert pet_id in pet_ids


@pytest.mark.api
class TestReadPetNegative:
    def test_get_pet_nonexistent_id(self, api_client):
        response = api_client.get(f"{BASE_URL}/pet/999999999")
        assert response.status_code == HTTP_NOT_FOUND

    def test_get_pet_invalid_id_format(self, api_client):
        response = api_client.get(f"{BASE_URL}/pet/invalid")
        assert response.status_code != HTTP_OK

    def test_find_pets_invalid_status(self, api_client):
        response = api_client.get(
            f"{BASE_URL}/pet/findByStatus", params={"status": "xyz"}
        )
        # Petstore accepts any status string and returns matching pets;
        # verify the response is a valid list
        assert response.status_code in (HTTP_OK, 400)
        if response.status_code == HTTP_OK:
            assert isinstance(response.json(), list)
