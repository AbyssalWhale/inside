import pytest

from api_tests.config import BASE_URL, HTTP_OK
from api_tests.pet_builder import PetBuilder


@pytest.mark.api
class TestUpdatePetPositive:
    def test_update_pet_name(self, api_client, created_pet):
        created_pet["name"] = "updated_name"

        response = api_client.put(f"{BASE_URL}/pet", json=created_pet)
        assert response.status_code == HTTP_OK

        get_response = api_client.get(f"{BASE_URL}/pet/{created_pet['id']}")
        assert get_response.status_code == HTTP_OK
        assert get_response.json()["name"] == "updated_name"

    def test_update_pet_status(self, api_client, created_pet):
        created_pet["status"] = "sold"

        response = api_client.put(f"{BASE_URL}/pet", json=created_pet)
        assert response.status_code == HTTP_OK

        get_response = api_client.get(f"{BASE_URL}/pet/{created_pet['id']}")
        assert get_response.status_code == HTTP_OK
        assert get_response.json()["status"] == "sold"

    def test_update_pet_with_form_data(self, api_client, created_pet):
        pet_id = created_pet["id"]

        response = api_client.post(
            f"{BASE_URL}/pet/{pet_id}",
            data={"name": "form_updated_name", "status": "pending"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == HTTP_OK

        get_response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
        assert get_response.status_code == HTTP_OK
        body = get_response.json()
        assert body["name"] == "form_updated_name"
        assert body["status"] == "pending"


@pytest.mark.api
class TestUpdatePetNegative:
    def test_update_pet_invalid_id(self, api_client):
        pet_data = PetBuilder().build()
        pet_data["id"] = 999999999

        response = api_client.put(f"{BASE_URL}/pet", json=pet_data)

        get_response = api_client.get(f"{BASE_URL}/pet/999999999")
        if response.status_code == HTTP_OK:
            api_client.delete(f"{BASE_URL}/pet/999999999")
        else:
            assert get_response.status_code == 404

    def test_update_pet_with_empty_body(self, api_client):
        response = api_client.put(f"{BASE_URL}/pet", json={})
        # Petstore accepts empty JSON on PUT; verify response is valid
        if response.status_code == HTTP_OK:
            body = response.json()
            assert "id" in body
            api_client.delete(f"{BASE_URL}/pet/{body['id']}")
        else:
            assert response.status_code in (400, 405, 500)
