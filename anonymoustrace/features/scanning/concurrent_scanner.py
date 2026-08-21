"""Concurrent scanner with bounded worker pool."""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from anonymoustrace.models import ConfidenceLevel, Site, ScanResult
from anonymoustrace.features.detection import (
    build_detector,
    validate_username,
)
from anonymoustrace.features.scanning.http_client import HTTPClient

logger = logging.getLogger(__name__)


class ConcurrentScanner:
    """Bounded-thread-pool scanner for username enumeration."""

    def __init__(
        self,
        registry: dict[str, Site],
        http_client: HTTPClient,
        workers: int = 20,
        rate_limit: float | None = None,
        min_confidence: str = "unknown",
    ) -> None:
        self.registry = registry
        self.http_client = http_client
        self.workers = workers
        self.rate_limit = rate_limit
        self.min_confidence = min_confidence

    def _passes_confidence_filter(self, result: ScanResult) -> bool:
        levels = ["found", "likely", "unknown", "not_found"]
        threshold = levels.index(self.min_confidence)
        actual = levels.index(result.confidence.value)
        return actual <= threshold

    def scan_site(
        self, site: Site, username: str
    ) -> ScanResult | None:
        """Scan a single site for a single username."""
        if not validate_username(site, username):
            return ScanResult(
                username=username,
                site_name=site.name,
                detected=False,
                confidence=ConfidenceLevel.UNKNOWN,
                error="username failed regex validation",
            )

        if self.rate_limit:
            time.sleep(self.rate_limit)

        resp = self.http_client.request(site, username)
        if resp is None:
            return ScanResult(
                username=username,
                site_name=site.name,
                detected=False,
                confidence=ConfidenceLevel.UNKNOWN,
                error="request failed",
            )

        detector = build_detector(site.error_type.value, self.registry)
        result = detector.detect(site, username, resp)

        if result.detected and site.url:
            result.response_url = site.url.format(username)

        if not self._passes_confidence_filter(result):
            return ScanResult(
                username=username,
                site_name=site.name,
                detected=False,
                confidence=ConfidenceLevel.UNKNOWN,
                error=f"below confidence threshold ({result.confidence.value})",
                status_code=result.status_code,
            )

        return result

    def scan(
        self, usernames: list[str], sites: list[str] | None = None
    ) -> list[ScanResult]:
        """Scan usernames against sites concurrently."""
        if sites:
            registry_lower = {k.lower(): v for k, v in self.registry.items()}
            target_sites = [
                registry_lower[s.lower()]
                for s in sites
                if s.lower() in registry_lower
            ]
        else:
            target_sites = list(self.registry.values())

        results: list[ScanResult] = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {}
            for username in usernames:
                for site in target_sites:
                    future = executor.submit(
                        self.scan_site, site, username
                    )
                    futures[future] = (username, site.name)

            for future in as_completed(futures):
                username, site_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as exc:
                    logger.error(
                        "Scanner error for %s@%s: %s",
                        username, site_name, exc
                    )

        return results
