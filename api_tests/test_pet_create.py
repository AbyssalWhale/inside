import pytest

from api_tests.config import BASE_URL, HTTP_OK, VALID_STATUSES
from api_tests.pet_builder import PetBuilder


@pytest.mark.api
class TestCreatePetPositive:
    def test_create_pet_with_all_fields(self, api_client):
        pet_data = (
            PetBuilder()
            .with_name("doggie")
            .with_category(1, "Dogs")
            .with_tags([(1, "friendly"), (2, "trained")])
            .with_photo_urls(["https://example.com/dog1.jpg", "https://example.com/dog2.jpg"])
            .with_status("available")
            .build()
        )

        response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
        assert response.status_code == HTTP_OK

        body = response.json()
        assert body["name"] == pet_data["name"]
        assert body["status"] == pet_data["status"]
        assert body["category"]["name"] == pet_data["category"]["name"]
        assert body["tags"][0]["name"] == pet_data["tags"][0]["name"]
        assert body["photoUrls"] == pet_data["photoUrls"]

        api_client.delete(f"{BASE_URL}/pet/{body['id']}")

    def test_create_pet_with_required_fields_only(self, api_client):
        pet_data = (
            PetBuilder()
            .with_name("minimal_pet")
            .with_photo_urls(["https://example.com/photo.jpg"])
            .build()
        )

        response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
        assert response.status_code == HTTP_OK

        body = response.json()
        assert body["name"] == "minimal_pet"

        api_client.delete(f"{BASE_URL}/pet/{body['id']}")

    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_create_pet_status_values(self, api_client, status):
        pet_data = PetBuilder().with_status(status).build()

        response = api_client.post(f"{BASE_URL}/pet", json=pet_data)
        assert response.status_code == HTTP_OK

        body = response.json()
        assert body["status"] == status

        api_client.delete(f"{BASE_URL}/pet/{body['id']}")


@pytest.mark.api
class TestCreatePetNegative:
    def test_create_pet_with_empty_body(self, api_client):
        response = api_client.post(f"{BASE_URL}/pet", json={})
        # Petstore accepts empty JSON and creates a pet with defaults;
        # verify response is still valid JSON with an id
        if response.status_code == HTTP_OK:
            body = response.json()
            assert "id" in body
            api_client.delete(f"{BASE_URL}/pet/{body['id']}")
        else:
            assert response.status_code in (400, 405, 500)

    def test_create_pet_with_invalid_json(self, api_client):
        response = api_client.post(
            f"{BASE_URL}/pet",
            data="this is not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code != HTTP_OK
