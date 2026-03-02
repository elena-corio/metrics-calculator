import logging
from unittest.mock import Mock, MagicMock
from adapters.latest_version import get_latest_version

def test_get_latest_version_returns_latest_and_prints(caplog):
    # Arrange
    mock_client = Mock()
    mock_version = MagicMock()
    mock_version.id = "test_version_id"
    mock_versions = MagicMock()
    mock_versions.items = [mock_version]
    mock_client.version.get_versions.return_value = mock_versions

    # Act
    with caplog.at_level(logging.INFO):
        result = get_latest_version(mock_client)

    # Assert
    assert result == mock_version
    mock_client.version.get_versions.assert_called_once()
    assert "✓ Fetching version: test_version_id" in caplog.text

def test_get_latest_version_no_versions(caplog):
    # Arrange
    mock_client = Mock()
    mock_versions = MagicMock()
    mock_versions.items = []
    mock_client.version.get_versions.return_value = mock_versions

    # Act
    with caplog.at_level(logging.WARNING):
        result = get_latest_version(mock_client)

    # Assert
    assert result is None
    assert "No versions found." in caplog.text