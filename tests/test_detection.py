"""Test detection strategies."""

from anonymoustrace.models import ConfidenceLevel
from anonymoustrace.features.detection.detectors import (
    StatusCodeDetector,
    MessageDetector,
    ResponseUrlDetector,
    HybridDetector,
)


def test_status_code_detector(sample_sites, mock_response):
    """Test status code detector."""
    detector = StatusCodeDetector()
    site = sample_sites["test_status"]

    # Test found (200 status)
    response = mock_response(status_code=200)
    result = detector.detect(site, "testuser", response)
    assert result.detected is True
    assert result.confidence == ConfidenceLevel.FOUND
    assert result.status_code == 200

    # Test not found (404 status)
    response = mock_response(status_code=404)
    result = detector.detect(site, "testuser", response)
    assert result.detected is False
    assert result.confidence == ConfidenceLevel.NOT_FOUND
    assert result.status_code == 404


def test_message_detector(sample_sites, mock_response):
    """Test message detector."""
    detector = MessageDetector()
    site = sample_sites["test_message"]

    # Test found (message not in text)
    response = mock_response(status_code=200, text="Welcome testuser!")
    result = detector.detect(site, "testuser", response)
    assert result.detected is True
    assert result.confidence == ConfidenceLevel.FOUND
    assert result.status_code == 200

    # Test not found (message in text)
    response = mock_response(status_code=200, text="Not Found")
    result = detector.detect(site, "testuser", response)
    assert result.detected is False
    assert result.confidence == ConfidenceLevel.NOT_FOUND
    assert result.status_code == 200


def test_response_url_detector(sample_sites, mock_response):
    """Test response URL detector."""
    detector = ResponseUrlDetector()
    site = sample_sites["test_response_url"]

    # Test found (different URL)
    response = mock_response(status_code=200, url="https://example.com/testuser")
    result = detector.detect(site, "testuser", response)
    assert result.detected is True
    assert result.confidence == ConfidenceLevel.FOUND
    assert result.status_code == 200
    assert result.response_url == "https://example.com/testuser"

    # Test not found (same as error URL)
    response = mock_response(status_code=200, url="https://example.com/404")
    result = detector.detect(site, "testuser", response)
    assert result.detected is False
    assert result.confidence == ConfidenceLevel.NOT_FOUND
    assert result.status_code == 200
    assert result.response_url == "https://example.com/404"


def test_hybrid_detector(sample_sites, mock_response):
    """Test hybrid detector."""
    detector = HybridDetector({name: site for name, site in sample_sites.items()})
    site = sample_sites["test_hybrid"]

    # Test found (strong signals)
    response = mock_response(status_code=200, text="Welcome testuser!", url="https://example.com/testuser")
    result = detector.detect(site, "testuser", response)
    assert result.detected is True
    assert result.confidence in [ConfidenceLevel.FOUND, ConfidenceLevel.LIKELY]
    assert result.status_code == 200
    assert result.response_url == "https://example.com/testuser"
    assert result.response_size > 0

    # Test not found (weak signals)
    response = mock_response(status_code=404, text="Not Found", url="https://example.com/404")
    result = detector.detect(site, "testuser", response)
    assert result.detected is False
    assert result.confidence == ConfidenceLevel.NOT_FOUND
    assert result.status_code == 404
    assert result.response_url == "https://example.com/404"
    assert result.response_size > 0
