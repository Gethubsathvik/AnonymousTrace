"""JSON registry loader with validation."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import requests

from anonymoustrace.models import Site

logger = logging.getLogger(__name__)


class RegistryLoader:
    """Loads and validates the site registry from JSON."""

    def __init__(self, registry_path: Path | str | None = None) -> None:
        if registry_path is None:
            registry_path = (
                Path(__file__).resolve().parent.parent.parent
                / "data"
                / "registry.json"
            )
        self.registry_path = registry_path

    def _is_url(self, path: Path | str) -> bool:
        """Check if the given path is a URL."""
        if isinstance(path, str):
            return path.startswith("http://") or path.startswith("https://")
        return False

    def _load_from_url(self, url: str) -> dict:
        """Load JSON from a URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            raise ValueError(f"Failed to load registry from URL {url}: {exc}") from exc

    def load(self) -> dict[str, Site]:
        """Load the registry JSON and return a name -> Site mapping."""
        if self._is_url(self.registry_path):
            raw = self._load_from_url(str(self.registry_path))
        else:
            path = Path(self.registry_path)
            if not path.exists():
                raise FileNotFoundError(
                    f"Registry not found at {path}"
                )
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)

        registry: dict[str, Site] = {}
        for name, entry in raw.items():
            try:
                site = Site.from_dict(name, entry)
                registry[name] = site
            except Exception as exc:
                logger.warning("Skipping invalid site %s: %s", name, exc)

        logger.info("Loaded %d sites from registry", len(registry))
        return registry

    def list_sites(self) -> list[str]:
        """Return all site names without loading full objects."""
        if self._is_url(self.registry_path):
            raw = self._load_from_url(str(self.registry_path))
        else:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        return list(raw.keys())
