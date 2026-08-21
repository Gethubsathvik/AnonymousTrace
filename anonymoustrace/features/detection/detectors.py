"""Concrete detection strategy implementations."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from anonymoustrace.models import ConfidenceLevel, Site

if TYPE_CHECKING:
    from anonymoustrace.models import ScanResult


class BaseDetector:
    """Abstract base for detection strategies."""

    def detect(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        raise NotImplementedError


class StatusCodeDetector(BaseDetector):
    """Detects based solely on HTTP status code."""

    def detect(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        from anonymoustrace.models import ScanResult

        detected = response.status_code == 200
        return ScanResult(
            username=username,
            site_name=site.name,
            detected=detected,
            confidence=(
                ConfidenceLevel.FOUND
                if detected
                else ConfidenceLevel.NOT_FOUND
            ),
            status_code=response.status_code,
            response_url=str(response.url),
        )


class MessageDetector(BaseDetector):
    """Detects based on presence of an error substring in the body."""

    def detect(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        from anonymoustrace.models import ScanResult

        error_msg = site.error_msg or ""
        detected = error_msg not in response.text
        return ScanResult(
            username=username,
            site_name=site.name,
            detected=detected,
            confidence=(
                ConfidenceLevel.FOUND
                if detected
                else ConfidenceLevel.NOT_FOUND
            ),
            status_code=response.status_code,
            response_url=str(response.url),
        )


class ResponseUrlDetector(BaseDetector):
    """Detects based on the final URL after redirects."""

    def detect(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        from anonymoustrace.models import ScanResult

        error_url = site.error_url or ""
        detected = response.url != error_url
        return ScanResult(
            username=username,
            site_name=site.name,
            detected=detected,
            confidence=(
                ConfidenceLevel.FOUND
                if detected
                else ConfidenceLevel.NOT_FOUND
            ),
            status_code=response.status_code,
            response_url=str(response.url),
        )


class HybridDetector(BaseDetector):
    """
    Confidence-scored hybrid strategy combining status, body, and size signals.

    Returns found | likely | unknown | not_found instead of a flat boolean.
    """

    def __init__(self, sites: dict[str, Site]) -> None:
        self.sites = sites

    def detect(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        from anonymoustrace.models import ScanResult

        score = 0
        signals: list[str] = []

        if response.status_code == 200:
            score += 1
            signals.append("status_200")
        elif response.status_code == 404:
            score -= 2
            signals.append("status_404")
        else:
            score -= 1
            signals.append(f"status_{response.status_code}")

        error_msg = site.error_msg or ""
        if error_msg and error_msg not in response.text:
            score += 2
            signals.append("msg_not_found")
        elif error_msg and error_msg in response.text:
            score -= 2
            signals.append("msg_found")

        error_url = site.error_url or ""
        if error_url and str(response.url) != error_url:
            score += 1
            signals.append("url_not_error")
        elif error_url and str(response.url) == error_url:
            score -= 2
            signals.append("url_error")

        body_len = len(response.text)
        if body_len < 500:
            score -= 1
            signals.append("small_body")

        if score >= 3:
            confidence = ConfidenceLevel.FOUND
        elif score >= 1:
            confidence = ConfidenceLevel.LIKELY
        elif score >= -1:
            confidence = ConfidenceLevel.UNKNOWN
        else:
            confidence = ConfidenceLevel.NOT_FOUND

        detected = confidence in (
            ConfidenceLevel.FOUND,
            ConfidenceLevel.LIKELY,
        )

        return ScanResult(
            username=username,
            site_name=site.name,
            detected=detected,
            confidence=confidence,
            status_code=response.status_code,
            response_url=str(response.url),
            response_size=body_len,
            metadata={"signals": signals, "score": score},
        )


def validate_username(site: Site, username: str) -> bool:
    """Check if a username matches the platform's regex constraint."""
    if not site.regex_check:
        return True
    return bool(re.match(site.regex_check, username))


def build_detector(error_type: str, registry: dict[str, Site]) -> BaseDetector:
    """Factory function for detection strategies."""
    if error_type == "status_code":
        return StatusCodeDetector()
    if error_type == "message":
        return MessageDetector()
    if error_type == "response_url":
        return ResponseUrlDetector()
    if error_type == "hybrid":
        return HybridDetector(registry)
    raise ValueError(f"Unknown errorType: {error_type}")
