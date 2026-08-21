"""Service layer: scan orchestration."""

from __future__ import annotations

import logging
from typing import Any

from anonymoustrace.models import Site, ScanResult
from anonymoustrace.features.scanning.http_client import HTTPClient
from anonymoustrace.features.scanning.concurrent_scanner import ConcurrentScanner
from anonymoustrace.features.scanning.registry_loader import RegistryLoader
from anonymoustrace.services.detection_service import DetectionService
from anonymoustrace.services.export_service import ExportService
from anonymoustrace.services.proxy_service import ProxyService, TorService

logger = logging.getLogger(__name__)


class ScanService:
    """High-level scan orchestrator wiring all services together."""

    def __init__(
        self,
        registry: dict[str, Site],
        http_client: HTTPClient,
        workers: int = 20,
        rate_limit: float | None = None,
        min_confidence: str = "unknown",
        export_service: ExportService | None = None,
    ) -> None:
        self.registry = registry
        self.http_client = http_client
        self.detection_service = DetectionService(registry)
        self.scanner = ConcurrentScanner(
            registry=registry,
            http_client=http_client,
            workers=workers,
            rate_limit=rate_limit,
            min_confidence=min_confidence,
        )
        self.export_service = export_service

    def execute(
        self,
        usernames: list[str],
        sites: list[str] | None = None,
        export_format: str | None = None,
        username_for_export: str | None = None,
    ) -> list[ScanResult]:
        """Run the full scan pipeline."""
        results = self.scanner.scan(usernames, sites)

        if export_format and self.export_service and username_for_export:
            if export_format == "json":
                self.export_service.export_json(results, username_for_export)
            elif export_format == "csv":
                self.export_service.export_csv(results, username_for_export)
            elif export_format == "xlsx":
                self.export_service.export_xlsx(results, username_for_export)
            elif export_format == "txt":
                self.export_service.export_txt(results, username_for_export)

        return results

    def close(self) -> None:
        self.http_client.close()
