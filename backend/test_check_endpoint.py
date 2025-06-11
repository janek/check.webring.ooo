import asyncio
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app import app, get_redis


class _DummyRedis:
    """In-memory stub to replace Redis during tests."""

    def __init__(self):
        self._store: dict[str, Any] = {}

    async def get(self, key: str):  # type: ignore[override]
        return self._store.get(key)

    async def set(self, key: str, value: str, ex: int | None = None):  # type: ignore[override]
        self._store[key] = value


@pytest.fixture(autouse=True)
def _override_redis_dependency(monkeypatch):
    dummy = _DummyRedis()

    async def _override():  # noqa: WPS430 – inner async stub
        return dummy

    app.dependency_overrides[get_redis] = _override
    yield
    app.dependency_overrides.pop(get_redis, None)


client = TestClient(app)


taken_domains = ["webring.ooo", "janek.ooo"]
free_domain = "donotbuythisdomainormytestswillfail.ooo"


@pytest.mark.parametrize("domain", taken_domains)
def test_taken_domain(domain: str):
    resp = client.get(f"/check/{domain}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["domain"] == domain
    assert data["available"] is False


def test_free_domain():
    resp = client.get(f"/check/{free_domain}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["domain"] == free_domain
    assert data["available"] is True

    # second call should be cached
    resp2 = client.get(f"/check/{free_domain}")
    assert resp2.status_code == 200
    assert resp2.json()["cached"] is True
