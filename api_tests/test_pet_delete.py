import pytest

from api_tests.config import BASE_URL, HTTP_OK, HTTP_NOT_FOUND
from api_tests.pet_builder import PetBuilder


@pytest.mark.api
class TestDeletePetPositive:
    def test_delete_pet_verify_removed(self, api_client):
        pet_data = PetBuilder().build()
        create_response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
        assert create_response.status_code == HTTP_OK
        pet_id = create_response.json()["id"]

        delete_response = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
        assert delete_response.status_code == HTTP_OK

        get_response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
        assert get_response.status_code == HTTP_NOT_FOUND


@pytest.mark.api
class TestDeletePetNegative:
    def test_delete_pet_nonexistent_id(self, api_client):
        response = api_client.delete(f"{BASE_URL}/pet/999999999")
        assert response.status_code == HTTP_NOT_FOUND

    def test_delete_pet_twice(self, api_client):
        pet_data = PetBuilder().build()
        create_response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
        assert create_response.status_code == HTTP_OK
        pet_id = create_response.json()["id"]

        first_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
        assert first_delete.status_code == HTTP_OK

        second_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
        assert second_delete.status_code == HTTP_NOT_FOUND
