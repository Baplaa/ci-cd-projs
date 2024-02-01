from car import Car

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CarManager:
    """ Manager of car records """

    def __init__(self, db_name):

        if db_name is None or db_name == "":
            raise ValueError("DB Name cannot be undefined")

        engine = create_engine(db_name)
        self._db_session = sessionmaker(bind=engine)

    def add_car(self, make, model, year, price):
        """ Adds a single car """

        # TODO - need validation
        if make is None or make == "":
            raise ValueError("Make must be defined")

        if model is None or model == "":
            raise ValueError("Model must be defined")

        if year is None or type(year) != int:
            raise ValueError("Year must be defined and valid")

        if year < 1980 or year > 2019:
            raise ValueError("Year must be between 1980 and 2019")

        if price is None or type(price) != float:
            raise ValueError("Price must be defined and valid")

        if price < 0.0:
            raise ValueError("Price must be a positive value")


        session = self._db_session()

        car = Car(make, model, year, price)

        session.add(car)
        session.commit()

        session.close()

    def delete_car(self, id):
        """ Deletes a single car based on the id """

        # TODO - need validation
        if id is None or type(id) != int:
            raise ValueError("Id must be defined")

        if id < 0:
            raise ValueError("Id must be positive")

        session = self._db_session()

        car = session.query(Car).filter(Car.id == id).first()

        if car is None:
            session.close()
            raise ValueError("Car does not exist")

        session.delete(car)
        session.commit()

        session.close()


    def get_all_cars(self):
        """ Returns a list of all cars """

        session = self._db_session()

        cars = session.query(Car).all()

        session.close()

        return cars
