"""Service layer: detection orchestration."""

from __future__ import annotations

import logging
from typing import Any

from anonymoustrace.models import Site, ScanResult
from anonymoustrace.features.detection import (
    build_detector,
    validate_username,
)

logger = logging.getLogger(__name__)


class DetectionService:
    """Orchestrates detection strategy selection and execution."""

    def __init__(self, registry: dict[str, Site]) -> None:
        self.registry = registry

    def validate(self, site: Site, username: str) -> bool:
        """Check username against site regex."""
        return validate_username(site, username)

    def run_detection(
        self, site: Site, username: str, response: Any
    ) -> ScanResult:
        """Run the appropriate detector for the site."""
        detector = build_detector(site.error_type.value, self.registry)
        return detector.detect(site, username, response)
