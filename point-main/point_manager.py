from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from point import Point


class PointManager:

    def __init__(self, db_filename):
        """ Initializes the list of points """

        if db_filename is None or db_filename == "":
            raise ValueError("Invalid Database File")

        engine = create_engine('sqlite:///' + db_filename)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self._db_session = sessionmaker(bind=engine)

    def add_point(self, point):
        """ Adds a new point"""

        if point is None or not isinstance(point, Point):
            raise ValueError("Invalid Point Object")

        session = self._db_session()

        session.add(point)
        session.commit()

        point_id = point.id

        session.close()

        return point_id

    def update_point(self, point):
        """ Updates an existing point """

        if point is None or not isinstance(point, Point):
            raise ValueError("Invalid Point Object")

        session = self._db_session()

        existing_point = session.query(Point).filter(Point.id == point.id).first()

        if existing_point is None:
            raise ValueError("Point does not exist")

        existing_point.copy(point)

        session.commit()
        session.close()

    def get_point(self, point_id):
        """ Gets an existing point """

        if (point_id is None or type(point_id) != int):
            raise ValueError("Invalid Point ID")

        session = self._db_session()

        existing_point = session.query(Point).filter(Point.id == point_id).first()

        session.close()

        return existing_point

    def delete_point(self, point_id):
        """ Deletes an existing point """

        if (point_id is None or type(point_id) != int):
            raise ValueError("Invalid Point ID")

        session = self._db_session()

        existing_point = session.query(Point).filter(Point.id == point_id).first()

        if existing_point is None:
            raise ValueError("Point does not exist")

        session.delete(existing_point)
        session.commit()

        session.close()

    def get_all_points(self):
        """ Gets all existing points """

        session = self._db_session()

        existing_points = session.query(Point).all()

        session.close()

        return existing_points
