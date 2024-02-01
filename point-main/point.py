from sqlalchemy import Column, Integer
from base import Base


class Point(Base):
    """ 2D Point """

    __tablename__ = "point"

    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    def __init__(self, x, y):
        """ Constructor """

        if type(x) != int or x < 0:
            raise ValueError("X Coordinate is Invalid")

        if type(y) != int or y < 0:
            raise ValueError("Y Coordinate is Invalid")

        self.x = x
        self.y = y

    def to_dict(self):
        """ Dictionary Representation of a Point """
        dict = {}
        dict['id'] = self.id
        dict['x'] = self.x
        dict['y'] = self.y

        return dict

    def copy(self, object):
        """ Copies data from a Point object to this Point object """
        if isinstance(object, Point):
            self.x = object.x
            self.y = object.y
