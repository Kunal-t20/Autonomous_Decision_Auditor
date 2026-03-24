"""Redis LLM cache helpers (uses fakeredis; no real Redis required)."""
import pytest
import fakeredis

from services import redis_cache as rc


@pytest.fixture
def fake_redis_enabled():
    """Enable Redis with an in-memory fake client; restore globals after test."""
    old_enabled = rc.REDIS_ENABLED
    rc.reset_redis_client_for_tests()
    rc.REDIS_ENABLED = True
    fake = fakeredis.FakeRedis(decode_responses=True)
    rc.set_redis_client(fake)
    yield fake
    rc.REDIS_ENABLED = old_enabled
    rc.reset_redis_client_for_tests()


def test_llm_cache_key_stable():
    k1 = rc.llm_cache_key("openai/gpt-oss-20b", 0.0, "same prompt")
    k2 = rc.llm_cache_key("openai/gpt-oss-20b", 0.0, "same prompt")
    assert k1 == k2
    assert k1.startswith(rc.LLM_CACHE_KEY_PREFIX)


def test_llm_cache_roundtrip(fake_redis_enabled):
    key = rc.llm_cache_key("m", 0.0, "prompt text")
    assert rc.llm_cache_get(key) is None
    rc.llm_cache_set(key, "cached body")
    assert rc.llm_cache_get(key) == "cached body"


def test_redis_ping_with_fake(fake_redis_enabled):
    assert rc.redis_ping() is True


def test_rate_limit_window(fake_redis_enabled):
    rc.RATE_LIMIT_ENABLED = True
    old_limit = rc.RATE_LIMIT_PER_MINUTE
    rc.RATE_LIMIT_PER_MINUTE = 2
    try:
        assert rc.rate_limit_exceeded("client-a") is False
        assert rc.rate_limit_exceeded("client-a") is False
        assert rc.rate_limit_exceeded("client-a") is True
    finally:
        rc.RATE_LIMIT_ENABLED = False
        rc.RATE_LIMIT_PER_MINUTE = old_limit
