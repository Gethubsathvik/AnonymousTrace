"""Resilience layer: retry with exponential backoff + jitter."""

from __future__ import annotations

import logging
import random
import time
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    jitter: bool = True,
) -> Callable[[F], F]:
    """Decorator factory for exponential backoff with jitter."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = base_delay
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s",
                        attempt + 1, max_retries, func.__name__, exc,
                    )
                    if attempt < max_retries - 1:
                        sleep_time = delay + (random.uniform(0, delay) if jitter else 0)
                        time.sleep(min(sleep_time, max_delay))
                        delay *= 2
            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator
