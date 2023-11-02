"""
This module contains tests for the main application logic, primarily focusing on
the interaction with environment variable configuration.
"""

import pytest

from src.main import Main


# Fixtures
@pytest.fixture
def mock_environ(monkeypatch):
    """
    Mock environment variables for testing purposes.
    """
    monkeypatch.setenv("HOST", "TEST_HOST")
    monkeypatch.setenv("TOKEN", "TEST_TOKEN")
    monkeypatch.setenv("T_MAX", "TEST_T_MAX")
    monkeypatch.setenv("T_MIN", "TEST_T_MIN")


# Tests
def test_environment_variables():
    """
    Tests if the application correctly reads the environment variables.
    """
    # Given
    expected_host = "https://hvac-simulator-a23-y2kpq.ondigitalocean.app"
    expected_token = "9vXWwTEL39"
    expected_t_max = 50
    expected_t_min = 0

    # When
    main_obj = Main()

    # Then
    assert main_obj.HOST == expected_host
    assert main_obj.TOKEN == expected_token
    assert main_obj.T_MAX == expected_t_max
    assert main_obj.T_MIN == expected_t_min
