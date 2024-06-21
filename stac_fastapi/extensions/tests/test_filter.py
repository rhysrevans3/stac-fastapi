from typing import Iterator

import pytest
from starlette.testclient import TestClient

from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import create_get_request_model, create_post_request_model
from stac_fastapi.extensions.core import FilterExtension
from stac_fastapi.types.config import ApiSettings
from stac_fastapi.types.core import BaseCoreClient


class DummyCoreClient(BaseCoreClient):
    def all_collections(self, *args, **kwargs):
        raise NotImplementedError

    def get_collection(self, *args, **kwargs):
        raise NotImplementedError

    def get_item(self, *args, **kwargs):
        raise NotImplementedError

    def get_search(self, *args, **kwargs):
        raise NotImplementedError

    def post_search(self, *args, **kwargs):
        return args[0].model_dump()

    def item_collection(self, *args, **kwargs):
        raise NotImplementedError


@pytest.fixture
def client() -> Iterator[TestClient]:
    settings = ApiSettings()
    extensions = [FilterExtension()]
    api = StacApi(
        settings=settings,
        client=DummyCoreClient(),
        extensions=extensions,
        search_get_request_model=create_get_request_model(extensions),
        search_post_request_model=create_post_request_model(extensions),
    )
    with TestClient(api.app) as client:
        yield client


def test_search_filter_post_filter_lang_default(client: TestClient):
    """Test search POST endpoint with filter ext."""
    response = client.post(
        "/search",
        json={
            "collections": ["test"],
            "filter": {"op": "=", "args": [{"property": "test_property"}, "test-value"]},
        },
    )
    assert response.is_success, response.json()
    response_dict = response.json()
    assert response_dict["filter_lang"] == "cql2-json"


def test_search_filter_post_filter_lang_non_default(client: TestClient):
    """Test search POST endpoint with filter ext."""
    filter_lang_value = "cql2-text"
    response = client.post(
        "/search",
        json={
            "collections": ["test"],
            "filter": {"op": "=", "args": [{"property": "test_property"}, "test-value"]},
            "filter-lang": filter_lang_value,
        },
    )
    assert response.is_success, response.json()
    response_dict = response.json()
    assert response_dict["filter_lang"] == filter_lang_value
