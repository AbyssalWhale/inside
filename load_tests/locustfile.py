import random
import logging

from locust import HttpUser, task, between, events

from config import ALL_SEARCH_TERMS, DEFAULT_HEADERS, SEARCH_PATH

logger = logging.getLogger(__name__)


class N11SearchUser(HttpUser):
    wait_time = between(2, 5)

    def on_start(self):
        self.client.headers.update(DEFAULT_HEADERS)

    @task
    def search_product(self):
        term = random.choice(ALL_SEARCH_TERMS)
        with self.client.get(
            SEARCH_PATH,
            params={"q": term},
            name="/arama?q=[search_term]",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 403:
                response.failure(
                    f"403 Forbidden for search term '{term}' — "
                    "the request was blocked (check headers/rate-limiting)"
                )
            else:
                response.failure(
                    f"Unexpected status {response.status_code} "
                    f"for search term '{term}'"
                )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Load test started against %s", environment.host)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Load test finished")
