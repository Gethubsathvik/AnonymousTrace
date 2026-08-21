"""Data models for the OSINT reconnaissance framework.

This module contains the core data structures for sites and scan results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ErrorType(str, Enum):
    """Supported detection strategies."""

    STATUS_CODE = "status_code"
    MESSAGE = "message"
    RESPONSE_URL = "response_url"
    HYBRID = "hybrid"


class ConfidenceLevel(str, Enum):
    """Confidence levels for hybrid detection."""

    FOUND = "found"
    LIKELY = "likely"
    UNKNOWN = "unknown"
    NOT_FOUND = "not_found"


@dataclass
class Site:
    """Represents a platform/site definition from the registry."""

    name: str
    error_type: ErrorType
    url: str
    url_main: str
    url_probe: str | None = None
    error_msg: str | None = None
    error_url: str | None = None
    regex_check: str | None = None
    username_claimed: str | None = None
    username_unclaimed: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    request_method: str = "GET"
    request_payload: dict[str, Any] | None = None
    request_url: str | None = None

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> Site:
        """Construct a Site from a registry JSON entry."""
        return cls(
            name=name,
            error_type=ErrorType(data.get("errorType", "status_code")),
            url=data.get("url", ""),
            url_main=data.get("urlMain", ""),
            url_probe=data.get("urlProbe"),
            error_msg=data.get("errorMsg"),
            error_url=data.get("errorUrl"),
            regex_check=data.get("regexCheck"),
            username_claimed=data.get("username_claimed"),
            username_unclaimed=data.get("username_unclaimed"),
            headers=data.get("headers", {}),
            request_method=data.get("request_method", "GET"),
            request_payload=data.get("request_payload"),
            request_url=data.get("request_url"),
        )


@dataclass
class ScanResult:
    """Result of scanning a single username against a single site."""

    username: str
    site_name: str
    detected: bool
    confidence: ConfidenceLevel
    status_code: int | None = None
    response_url: str | None = None
    response_size: int | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "site": self.site_name,
            "detected": self.detected,
            "confidence": self.confidence.value,
            "status_code": self.status_code,
            "response_url": self.response_url,
            "response_size": self.response_size,
            "error": self.error,
            "metadata": self.metadata,
        }
