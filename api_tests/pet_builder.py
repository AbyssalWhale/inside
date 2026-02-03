import random


class PetBuilder:
    def __init__(self):
        self._id = random.randint(100_000, 999_999)
        self._name = f"test_pet_{random.randint(1000, 9999)}"
        self._photo_urls = ["https://example.com/photo.jpg"]
        self._status = "available"
        self._category = None
        self._tags = None
        self._include_name = True
        self._include_photo_urls = True

    def with_name(self, name):
        self._name = name
        self._include_name = True
        return self

    def with_status(self, status):
        self._status = status
        return self

    def with_category(self, category_id, category_name):
        self._category = {"id": category_id, "name": category_name}
        return self

    def with_tags(self, tags):
        self._tags = [{"id": t[0], "name": t[1]} for t in tags]
        return self

    def with_photo_urls(self, urls):
        self._photo_urls = urls
        self._include_photo_urls = True
        return self

    def without_name(self):
        self._include_name = False
        return self

    def without_photo_urls(self):
        self._include_photo_urls = False
        return self

    def build(self):
        pet = {"id": self._id}

        if self._category:
            pet["category"] = self._category

        if self._include_name:
            pet["name"] = self._name

        if self._include_photo_urls:
            pet["photoUrls"] = self._photo_urls

        if self._tags:
            pet["tags"] = self._tags

        pet["status"] = self._status

        return pet
