from subprocess import CalledProcessError
from unittest.mock import MagicMock, mock_open, patch

import pytest

from mockup.exercises import (
    execute_command,
    fetch_data_from_api,
    perform_action_based_on_time,
    read_data_from_file,
)


@patch("mockup.exercises.requests.get")
def test_fetch_data_from_api_success(mock_get):
    mock_get.return_value.json.return_value = {"key": "value"}

    result = fetch_data_from_api("https://api.example.com/data")

    assert result == {"key": "value"}
    mock_get.assert_called_once_with("https://api.example.com/data", timeout=10)


def test_read_data_from_file_success():
    with patch(
        "builtins.open", mock_open(read_data="mock file content")
    ) as mocked_open:
        result = read_data_from_file("data.txt")

    assert result == "mock file content"
    mocked_open.assert_called_once_with("data.txt", encoding="utf-8")


def test_read_data_from_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_data_from_file("missing.txt")


@patch("mockup.exercises.subprocess.run")
def test_execute_command_success(mock_run):
    mock_run.return_value = MagicMock(stdout="command output")

    result = execute_command(["ls"])

    assert result == "command output"
    mock_run.assert_called_once_with(
        ["ls"], capture_output=True, check=False, text=True
    )


@patch("mockup.exercises.subprocess.run")
def test_execute_command_raises_called_process_error(mock_run):
    mock_run.side_effect = CalledProcessError(returncode=1, cmd=["ls"])

    with pytest.raises(CalledProcessError):
        execute_command(["ls"])


@patch("mockup.exercises.time.time")
def test_perform_action_based_on_time_action_a(mock_time):
    mock_time.return_value = 5

    assert perform_action_based_on_time() == "Action A"


@patch("mockup.exercises.time.time")
def test_perform_action_based_on_time_action_b(mock_time):
    mock_time.return_value = 15

    assert perform_action_based_on_time() == "Action B"
