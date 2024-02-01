from sqlalchemy import Column, Integer, Float, String, DateTime
from base import Base

import datetime

class Car(Base):
    """ Car Class """

    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    make = Column(String(250))
    model = Column(String(250))
    year = Column(Integer())
    price = Column(Float())

    def __init__(self, make, model, year, price):
        """ Creates a new Car record """

        self.make = make
        self.model = model
        self.year = year
        self.price = price

    def to_dict(self):
        """ Converts the Car record to a Python dictionary """

        new_dict = { "id" : self.id,
                     "timestamp" : self.timestamp.strftime("%Y-%m-%d"),
                     "make" : self.make,
                     "model" : self.model,
                     "year" : self.year,
                     "price" : self.price }

        return new_dict
