"""Test registry loader and scanner functionality."""

from unittest.mock import Mock, patch

from anonymoustrace.models import ErrorType
from anonymoustrace.features.detection import build_detector
from anonymoustrace.features.detection.detectors import (
    StatusCodeDetector,
    MessageDetector,
    ResponseUrlDetector,
    HybridDetector,
)
from anonymoustrace.features.scanning.concurrent_scanner import ConcurrentScanner
from anonymoustrace.features.scanning.http_client import HTTPClient
from anonymoustrace.features.scanning.registry_loader import RegistryLoader


def test_registry_loader_loads_json(tmp_path):
    """Test that registry loader can load JSON file."""
    # Create a temporary registry file
    registry_data = {
        "test_site": {
            "errorType": "status_code",
            "url": "https://example.com/{}",
            "urlMain": "https://example.com/",
            "username_claimed": "testuser",
            "username_unclaimed": "noonewouldeverusethisxyz123",
        }
    }
    registry_file = tmp_path / "registry.json"
    registry_file.write_text(__import__('json').dumps(registry_data))

    loader = RegistryLoader(registry_file)
    registry = loader.load()

    assert "test_site" in registry
    site = registry["test_site"]
    assert site.name == "test_site"
    assert site.error_type == ErrorType.STATUS_CODE
    assert site.url == "https://example.com/{}"
    assert site.username_claimed == "testuser"
    assert site.username_unclaimed == "noonewouldeverusethisxyz123"


def test_registry_loader_list_sites(tmp_path):
    """Test listing site names."""
    registry_data = {
        "site1": {"errorType": "status_code", "url": "https://example1.com/{}", "urlMain": "https://example1.com/"},
        "site2": {"errorType": "status_code", "url": "https://example2.com/{}", "urlMain": "https://example2.com/"},
    }
    registry_file = tmp_path / "registry.json"
    registry_file.write_text(__import__('json').dumps(registry_data))

    loader = RegistryLoader(registry_file)
    sites = loader.list_sites()

    assert "site1" in sites
    assert "site2" in sites
    assert len(sites) == 2


def test_build_detector_factory(sample_sites):
    """Test detector factory function."""
    registry = {name: site for name, site in sample_sites.items()}

    # Test status_code detector
    detector = build_detector("status_code", registry)
    assert isinstance(detector, StatusCodeDetector)

    # Test message detector
    detector = build_detector("message", registry)
    assert isinstance(detector, MessageDetector)

    # Test response_url detector
    detector = build_detector("response_url", registry)
    assert isinstance(detector, ResponseUrlDetector)

    # Test hybrid detector
    detector = build_detector("hybrid", registry)
    assert isinstance(detector, HybridDetector)


@patch('anonymoustrace.features.scanning.http_client.HTTPClient.request')
def test_concurrent_scanner_scans_sites(mock_request, sample_sites):
    """Test that concurrent scanner works correctly."""
    # Mock successful responses
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Welcome testuser"
    mock_response.url = "https://example.com/testuser"
    mock_request.return_value = mock_response

    registry = {name: site for name, site in sample_sites.items()}
    http_client = HTTPClient(timeout=5)
    scanner = ConcurrentScanner(registry=registry, http_client=http_client, workers=2)

    results = scanner.scan(["testuser"], ["test_status"])

    assert len(results) == 1
    result = results[0]
    assert result.username == "testuser"
    assert result.site_name == "test_status"
    assert result.detected is True
    assert mock_request.called


@patch('anonymoustrace.features.scanning.http_client.HTTPClient.request')
def test_concurrent_scanner_handles_errors(mock_request, sample_sites):
    """Test that scanner handles request failures gracefully."""
    # Mock failed request
    mock_request.return_value = None

    registry = {name: site for name, site in sample_sites.items()}
    http_client = HTTPClient(timeout=5)
    scanner = ConcurrentScanner(registry=registry, http_client=http_client, workers=2)

    results = scanner.scan(["testuser"], ["test_status"])

    assert len(results) == 1
    result = results[0]
    assert result.username == "testuser"
    assert result.site_name == "test_status"
    assert result.detected is False
    assert result.confidence.value == "unknown"
    assert result.error == "request failed"
