"""Integration tests for the OSINT reconnaissance framework."""

from unittest.mock import Mock, patch

from anonymoustrace.models import Site, ErrorType
from anonymoustrace.features.detection.detectors import validate_username
from anonymoustrace.services.scan_service import ScanService
from anonymoustrace.services.export_service import ExportService
from anonymoustrace.features.scanning.http_client import HTTPClient


def test_validate_username():
    """Test username validation against site regex."""
    site = Site(
        name="test",
        error_type=ErrorType.STATUS_CODE,
        url="https://example.com/{}",
        url_main="https://example.com/",
        regex_check=r"^[a-zA-Z0-9_]{3,20}$",
    )

    # Valid usernames
    assert validate_username(site, "abc") is True
    assert validate_username(site, "test_user123") is True
    assert validate_username(site, "a" * 20) is True

    # Invalid usernames
    assert validate_username(site, "ab") is False  # too short
    assert validate_username(site, "a" * 21) is False  # too long
    assert validate_username(site, "test-user") is False  # hyphen not allowed
    assert validate_username(site, "test.user") is False  # dot not allowed


@patch('anonymoustrace.features.scanning.http_client.HTTPClient.request')
def test_scan_service_end_to_end(mock_request):
    """Test full scan service execution."""
    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Welcome testuser"
    mock_response.url = "https://example.com/testuser"
    mock_request.return_value = mock_response

    # Create registry with one site
    registry = {
        "test_site": Site(
            name="test_site",
            error_type=ErrorType.STATUS_CODE,
            url="https://example.com/{}",
            url_main="https://example.com/",
            username_claimed="testuser",
            username_unclaimed="nonexistentuser123",
        )
    }

    # Create services
    http_client = HTTPClient(timeout=5)
    export_service = ExportService()
    scan_service = ScanService(
        registry=registry,
        http_client=http_client,
        workers=2,
        export_service=export_service,
    )

    # Execute scan
    results = scan_service.execute(
        usernames=["testuser"],
        sites=["test_site"],
        export_format=None,
        username_for_export=None,
    )

    # Verify results
    assert len(results) == 1
    result = results[0]
    assert result.username == "testuser"
    assert result.site_name == "test_site"
    assert result.detected is True
    assert result.status_code == 200

    # Cleanup
    scan_service.close()
