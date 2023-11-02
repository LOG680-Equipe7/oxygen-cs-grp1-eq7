"""
Tests for main.py
"""
import pytest
from src.main import Main


# Fixtures
@pytest.fixture
def mock_environ(monkeypatch):
    """
    Fixture to mock environment variables
    """
    monkeypatch.setenv("HOST", "TEST_HOST")
    monkeypatch.setenv("TOKEN", "TEST_TOKEN")
    monkeypatch.setenv("T_MAX", "TEST_T_MAX")
    monkeypatch.setenv("T_MIN", "TEST_T_MIN")


# Tests
def test_environment_variables(mock_environ):
    """
    Test environment variables
    """
    print(mock_environ)
    # Given
    expected_host = "TEST_HOST"
    expected_token = "TEST_TOKEN"
    expected_t_max = "TEST_T_MAX"
    expected_t_min = "TEST_T_MIN"

    # When
    main_obj = Main()

    # Then
    assert main_obj.HOST == expected_host
    assert main_obj.TOKEN == expected_token
    assert main_obj.T_MAX == expected_t_max
    assert main_obj.T_MIN == expected_t_min
