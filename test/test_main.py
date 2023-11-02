"""
This module contains tests for the main application logic, primarily focusing on
the interaction with the database and environment variable configuration.
"""

import datetime
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.main import Main
from src.models import TemperatureLog


# Database configuration
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


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


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a new database session for testing, ensuring that any changes
    are rolled back afterwards.
    """
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def valid_temperature():
    """
    Provides a valid temperature log instance for testing.
    """
    current_date = datetime.datetime.now()
    valid_temperature = TemperatureLog(
        date=current_date, temperature=200, action="Heat"
    )
    return valid_temperature


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


class TestTempoeratureLog:
    """Tests for the TemperatureLog model and its interactions."""

    def test_send_event_to_database(self, db_session):
        """
        Tests if the event data is correctly sent and stored in the database.
        """
        # Add a new temperature log entry to the session
        current_date = datetime.datetime.now()
        temperature = 200
        action = "Heat"
        temperature_log_entry = TemperatureLog(
            date=current_date, temperature=temperature, action=action
        )
        db_session.add(temperature_log_entry)

        log = (
            db_session.query(TemperatureLog).filter_by(temperature=temperature).first()
        )
        assert log.temperature == 200
        assert log.action == "Heat"
