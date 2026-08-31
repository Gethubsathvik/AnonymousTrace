"""Test configuration and fixtures."""

import pytest
from anonymoustrace.models import ErrorType, Site
from anonymoustrace.features.detection.detectors import BaseDetector

@pytest.fixture
def sample_sites():
    """Create sample sites for testing."""
    return {
        "test_status": Site(
            name="test_status",
            error_type=ErrorType.STATUS_CODE,
            url="https://example.com/{}",
            url_main="https://example.com/",
            username_claimed="testuser",
            username_unclaimed="nonexistentuser123",
        ),
        "test_message": Site(
            name="test_message",
            error_type=ErrorType.MESSAGE,
            url="https://example.com/{}",
            url_main="https://example.com/",
            error_msg="Not Found",
            username_claimed="testuser",
            username_unclaimed="nonexistentuser123",
        ),
        "test_response_url": Site(
            name="test_response_url",
            error_type=ErrorType.RESPONSE_URL,
            url="https://example.com/{}",
            url_main="https://example.com/",
            error_url="https://example.com/404",
            username_claimed="testuser",
            username_unclaimed="nonexistentuser123",
        ),
        "test_hybrid": Site(
            name="test_hybrid",
            error_type=ErrorType.HYBRID,
            url="https://example.com/{}",
            url_main="https://example.com/",
            error_msg="Not Found",
            error_url="https://example.com/404",
            username_claimed="testuser",
            username_unclaimed="nonexistentuser123",
        ),
    }


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    class MockResponse:
        def __init__(self, status_code=200, text="", url="https://example.com/testuser"):
            self.status_code = status_code
            self.text = text
            self.url = url

    return MockResponse
