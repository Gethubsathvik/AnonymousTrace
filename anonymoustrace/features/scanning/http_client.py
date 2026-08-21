"""HTTP client with session pooling, timeouts, and proxy support."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from anonymoustrace.models import Site

logger = logging.getLogger(__name__)


class HTTPClient:
    """Manages HTTP sessions with pooling, retries, and proxy support."""

    def __init__(
        self,
        timeout: int = 10,
        proxy: str | None = None,
        tor: bool = False,
        unique_tor: bool = False,
        dump_response: bool = False,
    ) -> None:
        self.timeout = timeout
        self.proxy = proxy
        self.tor = tor
        self.unique_tor = unique_tor
        self.dump_response = dump_response
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "HEAD"],
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        if self.proxy:
            session.proxies = {"http": self.proxy, "https": self.proxy}

        if self.tor or self.unique_tor:
            session.proxies = {
                "http": "socks5://127.0.0.1:9050",
                "https": "socks5://127.0.0.1:9050",
            }

        return session

    def new_circuit(self) -> None:
        """Request a new Tor circuit (requires stem control port)."""
        if not (self.tor or self.unique_tor):
            return
        try:
            from stem import Signal
            from stem.control import Controller

            with Controller.from_port(port=9051) as ctrl:
                ctrl.authenticate()
                ctrl.signal(Signal.NEWNYM)
        except Exception as exc:
            logger.warning("Failed to request new Tor circuit: %s", exc)

    def build_url(self, site: Site, username: str) -> str:
        """Construct the probe URL for a given site and username."""
        if site.url_probe:
            return site.url_probe.format(username)
        return site.url.format(username)

    def request(self, site: Site, username: str) -> requests.Response | None:
        """Execute a single HTTP request with error isolation."""
        url = self.build_url(site, username)
        method = site.request_method.upper()
        payload = site.request_payload
        headers = {**site.headers}

        try:
            if method == "GET":
                resp = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
            elif method == "POST":
                resp = self.session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
            elif method == "HEAD":
                resp = self.session.head(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
            else:
                logger.warning("Unsupported method %s for %s", method, site.name)
                return None

            if self.dump_response:
                logger.info("Response for %s (%s): status=%s, body=%s", site.name, url, resp.status_code, resp.text[:500])

            return resp
        except requests.exceptions.Timeout:
            logger.warning("Timeout on %s (%s)", site.name, url)
        except requests.exceptions.ConnectionError:
            logger.warning("Connection error on %s (%s)", site.name, url)
        except requests.exceptions.SSLError:
            logger.warning("SSL error on %s (%s)", site.name, url)
        except requests.exceptions.TooManyRedirects:
            logger.warning("Redirect loop on %s (%s)", site.name, url)
        except Exception as exc:
            logger.warning("Unexpected error on %s: %s", site.name, exc)
        return None

    def close(self) -> None:
        self.session.close()
