import pytest

import datetime
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker

from src.main import Main


# Database configuration
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ORM Model
class TemperatureLog(Base):
    __tablename__ = "temperature_log"
    id = Column(Integer, Sequence("temp_log_id_seq"), primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    action = Column(String(50))


# Fixtures
@pytest.fixture
def mock_environ(monkeypatch):
    monkeypatch.setenv("HOST", "TEST_HOST")
    monkeypatch.setenv("TOKEN", "TEST_TOKEN")
    monkeypatch.setenv("T_MAX", "TEST_T_MAX")
    monkeypatch.setenv("T_MIN", "TEST_T_MIN")
    
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def valid_temperature():
    valid_temperature = TemperatureLog(
        temperature=200,
        action="Heat"
    )
    return valid_temperature

# Tests
def test_environment_variables(mock_environ):
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
    

class TestTempoeratureLog:
    def test_send_event_to_database(self, db_session):
        # Add a new temperature log entry to the session
        temperature = 200
        action = "Heat"
        temperature_log_entry = TemperatureLog(temperature=temperature, action=action)
        db_session.add(temperature_log_entry)
        
        log = db_session.query(TemperatureLog).filter_by(temperature=temperature).first()
        assert log.temperature == 200
        assert log.action == "Heat"
