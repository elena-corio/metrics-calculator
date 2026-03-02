from unittest.mock import Mock, MagicMock
from adapters.new_version import create_version

def test_create_version_prints_and_calls_create(monkeypatch):
    # Arrange
    mock_client = Mock()
    mock_version = MagicMock()
    mock_version.id = "test_version_id"
    mock_client.version.create.return_value = mock_version

    # Act
    create_version(mock_client, "test_object_id")

    # Assert
    mock_client.version.create.assert_called_once()
    # Optionally, check the print output
    # (pytest's capsys fixture can capture print output)