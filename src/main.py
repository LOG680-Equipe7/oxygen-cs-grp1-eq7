from signalrcore.hub_connection_builder import HubConnectionBuilder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import requests
import json
import time
import os
from models import Base, TemperatureLog


class Main:
    def __init__(self):
        """Setup environment variables and default values."""
        self._hub_connection = None
        # self.HOST = "https://hvac-simulator-a23-y2kpq.ondigitalocean.app"  # Setup your host here
        # self.TOKEN = "9vXWwTEL39"  # Setup your token here
        # self.TICKETS = 2  # Setup your tickets here
        # self.T_MAX = 100  # Setup your max temperature here
        # self.T_MIN = 0  # Setup your min temperature here

        # Retrieve environment variables (when using Docker)
        self.HOST = os.environ.get("HOST")
        self.TOKEN = os.environ.get("TOKEN")
        self.TICKETS = 2
        self.T_MAX = os.environ.get("T_MAX")
        self.T_MIN = os.environ.get("T_MIN")

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS."""
        self.setup_database()
        self.set_sensorhub()

    def setup_database(self):
        # Setup your database connection with SQLAlchemy
        DATABASE_URL = (
            "postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/mydb"
        )
        self.engine = create_engine(DATABASE_URL, echo=True)

        # Create session factory
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # This will create tables defined in models.py if they don't exist
        Base.metadata.create_all(self.engine)

    def start(self):
        """Start Oxygen CS."""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(
            lambda: print("||| Connection opened.", flush=True)
        )
        self._hub_connection.on_close(
            lambda: print("||| Connection closed.", flush=True)
        )
        self._hub_connection.on_error(
            lambda data: print(
                f"||| An exception was thrown closed: {data.error}", flush=True
            )
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            print(date)
            temperature = float(data[0]["data"])
            action = self.take_action(temperature)

            self.send_event_to_database(date, temperature, action)

        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        action = None

        if float(temperature) >= float(self.T_MAX):
            action = "TurnOnAc"
            self.send_action_to_hvac(action)
        elif float(temperature) <= float(self.T_MIN):
            action = "TurnOnHeater"
            self.send_action_to_hvac(action)

        return action

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, temperature, action):
        """Save sensor data into database."""
        try:
            new_log = TemperatureLog(
                date=timestamp, temperature=temperature, action=action
            )
            # Add the instance to the session and commit
            self.session.add(new_log)
            self.session.commit()

        except requests.exceptions.RequestException as e:
            print(f"Error saving to database: {e}", flush=True)
            self.session.rollback()


if __name__ == "__main__":
    main = Main()
    main.start()
