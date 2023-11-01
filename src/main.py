"""
Main module for the application.
"""

import logging
import os
import time
import json
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, TemperatureLog


class Main:
    """
    Main class for the application.
    """

    def __init__(self):
        """
        Initializes the Main class with required environment variables and default values.
        """
        self._hub_connection = None
        self.HOST = os.environ.get("HOST")
        self.TOKEN = os.environ.get("TOKEN")
        self.engine = None
        self.session = None
        self.TICKETS = 2
        self.T_MAX = os.environ.get("T_MAX")
        self.T_MIN = os.environ.get("T_MIN")

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """
        Sets up the environment for the application.
        """
        self.setup_database()
        self.set_sensorhub()

    def setup_database(self):
        """
        Sets up the database connection using SQLAlchemy.
        """
        DATABASE_URL = (
            "postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/mydb"
        )
        self.engine = create_engine(DATABASE_URL, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def start(self):
        """
        Starts the application.
        """
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """
        Configures the hub connection and subscribes to sensor data events.
        """
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
            lambda data: print(f"||| An exception was thrown: {data.error}", flush=True)
        )

    def on_sensor_data_received(self, data):
        """
        Handles sensor data on reception.
        """
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            print(date)
            temperature = float(data[0]["data"])
            action = self.take_action(temperature)
            self.send_event_to_database(date, temperature, action)

        except requests.exceptions.RequestException as err:
            print(f"Error: {err}", flush=True)

    def take_action(self, temperature):
        """
        Takes action based on the current temperature.
        """
        action = None
        if float(temperature) >= float(self.T_MAX):
            action = "TurnOnAc"
            self.send_action_to_hvac(action)
        elif float(temperature) <= float(self.T_MIN):
            action = "TurnOnHeater"
            self.send_action_to_hvac(action)
        return action

    def send_action_to_hvac(self, action):
        """
        Sends an action query to the HVAC service.
        """
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, temperature, action):
        """
        Saves sensor data into the database
        """
        try:
            new_log = TemperatureLog(
                date=timestamp, temperature=temperature, action=action
            )
            self.session.add(new_log)
            self.session.commit()

        except requests.exceptions.RequestException as e:
            print(f"Error saving to database: {e}", flush=True)
            self.session.rollback()
            # test


if __name__ == "__main__":
    main = Main()
    main.start()
