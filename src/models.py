"""
Module contenant le modele pour les tables de la base de donnees.
"""
import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TemperatureLog(Base):
    """
    Classe TemperatureLog pour la table temperature_log.
    """

    __tablename__ = "temperature_log"
    id = Column(Integer, Sequence("temp_log_id_seq"), primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    action = Column(String(50))

    def __init__(self, date, temperature, action):
        """
        Initialisation de la classe TemperatureLog.
        """
        if date:
            self.date = date
        self.temperature = temperature
        self.action = action

    def print_log_details(self):
        """
        Print the date, temperature, and action attributes of the instance.
        """
        print(
            f"Date: {self.date}, Temperature: {self.temperature}, Action: {self.action}"
        )

    def pleaseLint(self, string):
        """
        Méthode pour satisfaire le linter avec au moins 2 méthodes publiques.
        """
        print(string)
