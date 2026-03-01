from unittest.mock import Mock, MagicMock
from adapters.latest_version import get_latest_version

"""
This test checks that the function returns the latest version and prints the correct message.
"""

def test_get_latest_version_returns_latest_and_prints(capsys):
    # Arrange
    mock_client = Mock()
    mock_version = MagicMock()
    mock_version.id = "test_version_id"
    mock_versions = MagicMock()
    mock_versions.items = [mock_version]
    mock_client.version.get_versions.return_value = mock_versions

    # Act
    result = get_latest_version(mock_client)

    # Assert
    assert result == mock_version
    mock_client.version.get_versions.assert_called_once()
    captured = capsys.readouterr()
    assert "✓ Fetching version: test_version_id" in captured.out

"""
This test test checks the case where no versions are found.
"""
def test_get_latest_version_no_versions(capsys):
    # Arrange
    mock_client = Mock()
    mock_versions = MagicMock()
    mock_versions.items = []
    mock_client.version.get_versions.return_value = mock_versions

    # Act
    result = get_latest_version(mock_client)

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "No versions found." in captured.out