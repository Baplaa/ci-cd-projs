import unittest
import xmlrunner
from point import Point
from point_manager import PointManager
import inspect
import os

from sqlalchemy import create_engine
from base import Base


class TestPointManager(unittest.TestCase):
    """ Tests PointManager Class """

    def setUp(self):
        engine = create_engine('sqlite:///test_points.sqlite')

        # Creates all the tables
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.points_mgr = PointManager('test_points.sqlite')

        self.logPoint()

    def tearDown(self):
        os.remove('test_points.sqlite')
        self.logPoint()

    def logPoint(self):
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def test_add_point(self):
        point = Point(5,5)
        self.points_mgr.add_point(point)

        all_points = self.points_mgr.get_all_points()
        self.assertEqual(len(all_points), 1)

    def test_add_point_invalid(self):
        self.assertRaisesRegex(ValueError, "Invalid Point Object", self.points_mgr.add_point, None)
        self.assertRaisesRegex(ValueError, "Invalid Point Object", self.points_mgr.add_point, [])

    def test_update_point(self):
        point1 = Point(5, 5)
        point1_id = self.points_mgr.add_point(point1)

        retrieved_point = self.points_mgr.get_point(point1_id)
        self.assertEqual(retrieved_point.x, 5)
        self.assertEqual(retrieved_point.y, 5)

        retrieved_point.x = 6
        retrieved_point.y = 7
        self.points_mgr.update_point(retrieved_point)

        retrieved_updated_point = self.points_mgr.get_point(point1_id)
        self.assertEqual(retrieved_updated_point.x, 6)
        self.assertEqual(retrieved_updated_point.y, 7)

    def test_update_point_invalid(self):
        self.assertRaisesRegex(ValueError, "Invalid Point Object", self.points_mgr.update_point, None)
        self.assertRaisesRegex(ValueError, "Invalid Point Object", self.points_mgr.update_point, [])

    def test_delete_point(self):
        point1 = Point(5, 5)
        point1_id = self.points_mgr.add_point(point1)

        retreived_point1 = self.points_mgr.get_point(point1_id)
        self.assertIsNotNone(retreived_point1)

        self.points_mgr.delete_point(point1_id)

        retreived_point1 = self.points_mgr.get_point(point1_id)
        self.assertIsNone(retreived_point1)

    def test_delete_point_invalid(self):
        self.assertRaisesRegex(ValueError, "Invalid Point ID", self.points_mgr.delete_point, None)
        self.assertRaisesRegex(ValueError, "Invalid Point ID", self.points_mgr.delete_point, "1")

    def test_get_point(self):
        point1 = Point(5, 5)
        point2 = Point(6, 6)

        point1_id = self.points_mgr.add_point(point1)
        point2_id = self.points_mgr.add_point(point2)

        retrieved_point1 = self.points_mgr.get_point(point1_id)
        self.assertIsNotNone(retrieved_point1)
        self.assertEqual(retrieved_point1.x, 5)
        self.assertEqual(retrieved_point1.y, 5)

        retrieved_point2 = self.points_mgr.get_point(point2_id)
        self.assertIsNotNone(retrieved_point2)
        self.assertEqual(retrieved_point2.x, 6)
        self.assertEqual(retrieved_point2.y, 6)

    def test_get_point_invalid(self):
        self.assertRaisesRegex(ValueError, "Invalid Point ID", self.points_mgr.get_point, None)
        self.assertRaisesRegex(ValueError, "Invalid Point ID", self.points_mgr.get_point, "1")


    def test_get_all(self):
        all_points = self.points_mgr.get_all_points()
        self.assertEqual(len(all_points), 0)

        point1 = Point(5, 5)
        point2 = Point(6, 6)

        point1_id = self.points_mgr.add_point(point1)
        point2_id = self.points_mgr.add_point(point2)

        all_points = self.points_mgr.get_all_points()
        self.assertEqual(len(all_points), 2)



if __name__ == "__main__":
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
