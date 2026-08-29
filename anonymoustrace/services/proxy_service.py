"""Proxy and Tor routing services."""

from __future__ import annotations

import logging
import socket
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ProxyService:
    """Resolves and validates proxy URLs."""

    def __init__(self, proxy_url: str | None = None) -> None:
        self.proxy_url = proxy_url
        self._validate()

    def _validate(self) -> None:
        if not self.proxy_url:
            return
        try:
            parsed = urlparse(self.proxy_url)
            if parsed.scheme not in ("http", "https", "socks4", "socks5"):
                raise ValueError(f"Unsupported proxy scheme: {parsed.scheme}")
            socket.gethostbyname(parsed.hostname or "127.0.0.1")
        except Exception as exc:
            raise ValueError(f"Invalid proxy configuration: {exc}") from exc

    def get_proxy_dict(self) -> dict[str, str]:
        """Get proxy dictionary."""
        if not self.proxy_url:
            return {}
        return {"http": self.proxy_url, "https": self.proxy_url}


class TorService:
    """Manages Tor connectivity and circuit management."""

    def __init__(self, control_port: int = 9051, socks_port: int = 9050) -> None:
        self.control_port = control_port
        self.socks_port = socks_port

    def is_running(self) -> bool:
        """Check if Tor SOCKS proxy is reachable."""
        try:
            with socket.create_connection(("127.0.0.1", self.socks_port), timeout=2):
                return True
        except OSError:
            return False

    def new_circuit(self) -> None:
        """Request a new Tor circuit."""
        try:
            from stem import Signal
            from stem.control import Controller

            with Controller.from_port(port=self.control_port) as ctrl:
                ctrl.authenticate()
                ctrl.signal(Signal.NEWNYM)
        except Exception as exc:
            logger.warning("Failed to request new Tor circuit: %s", exc)
