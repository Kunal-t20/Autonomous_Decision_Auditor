"""
Redis client and LLM response cache helpers.

When REDIS_ENABLED is false or connection fails, callers behave as no-cache / no rate limit.
"""
from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path
from typing import Optional

import redis
from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_env_path, override=True)

REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
LLM_CACHE_TTL_SECONDS = int(os.getenv("LLM_CACHE_TTL_SECONDS", "86400"))
LLM_CACHE_KEY_PREFIX = os.getenv("LLM_CACHE_KEY_PREFIX", "llm:v1:")
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

_client: Optional[redis.Redis] = None


def get_redis() -> Optional[redis.Redis]:
    """Return a shared Redis client, or None if caching/rate-limit is disabled."""
    global _client
    if not REDIS_ENABLED:
        return None
    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)
    return _client


def reset_redis_client_for_tests() -> None:
    """Clear singleton (used by tests with fakeredis)."""
    global _client
    _client = None


def set_redis_client(client: Optional[redis.Redis]) -> None:
    """Inject client (e.g. fakeredis) for tests."""
    global _client
    _client = client


def redis_ping() -> bool:
    """True if Redis is enabled and responds to PING."""
    r = get_redis()
    if r is None:
        return False
    try:
        return bool(r.ping())
    except Exception:
        return False


def llm_cache_key(model: str, temperature: float, prompt: str) -> str:
    digest = hashlib.sha256(f"{model}|{temperature}|{prompt}".encode()).hexdigest()
    return f"{LLM_CACHE_KEY_PREFIX}{digest}"


def llm_cache_get(key: str) -> Optional[str]:
    r = get_redis()
    if r is None:
        return None
    try:
        return r.get(key)
    except Exception:
        return None


def llm_cache_set(key: str, value: str) -> None:
    r = get_redis()
    if r is None:
        return
    try:
        r.setex(key, LLM_CACHE_TTL_SECONDS, value)
    except Exception:
        pass


def rate_limit_exceeded(client_id: str) -> bool:
    """
    Fixed-window counter per minute. Returns True if over limit.
    No-op (returns False) when rate limiting or Redis is disabled.
    """
    if not RATE_LIMIT_ENABLED:
        return False
    r = get_redis()
    if r is None:
        return False
    window = int(time.time() // 60)
    key = f"rl:audit:{client_id}:{window}"
    try:
        n = r.incr(key)
        if n == 1:
            r.expire(key, 120)
        return n > RATE_LIMIT_PER_MINUTE
    except Exception:
        return False
