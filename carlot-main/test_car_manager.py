from unittest import TestCase

from car_manager import CarManager

import sqlite3
import unittest
import os
import inspect
import xmlrunner


class TestCarManager(TestCase):
    """ Tests the CarManager class """

    TEST_DB = 'test_carlot.sqlite'

    def setUp(self):
        """ Set up test environment """
        self.logPoint()

        conn = sqlite3.connect(TestCarManager.TEST_DB)

        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS cars
                  (id INTEGER PRIMARY KEY ASC,
                   timestamp DATETIME NOT NULL,
                   make VARCHAR(250) NOT NULL,
                   model VARCHAR(250) NOT NULL,           
                   year INTEGER NOT NULL,
                   price REAL NOT NULL
                  )
                  ''')

        conn.commit()
        conn.close()

        self.car_mgr = CarManager("sqlite:///" + TestCarManager.TEST_DB)


    def tearDown(self):
        """ call log message for test"""
        self.logPoint()
        os.remove(TestCarManager.TEST_DB)

    def logPoint(self):
        """ Log out testing information """
        current_test = self.id().split('.')[-1]
        calling_function = inspect.stack()[1][3]
        print('in %s - %s()' % (current_test, calling_function))

    def test_add_car_success(self):
        """ TP-01 - Success test on add_car """

        cars_before = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_before), 0)

        self.car_mgr.add_car("Honda", "Civic", 2010, 5999.0)
        self.car_mgr.add_car("Ford", "Explorer", 2017, 32500.99)

        cars_after = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_after), 2)

    def test_add_car_invalid(self):
        """ TP-02 - Validation test on add_car """

        with self.assertRaisesRegex(ValueError, "Make must be defined"):
            self.car_mgr.add_car("", "civic", 2010, 5999.0)

        with self.assertRaisesRegex(ValueError, "Model must be defined"):
            self.car_mgr.add_car("honda", "", 2010, 5999.0)

        with self.assertRaisesRegex(ValueError, "Year must be defined"):
            self.car_mgr.add_car("honda", "civic", "2010", 5999.0)

        with self.assertRaisesRegex(ValueError, "Price must be defined"):
            self.car_mgr.add_car("honda", "civic", 2010, "5999.0")

        with self.assertRaisesRegex(ValueError, "Make must be defined"):
            self.car_mgr.add_car(None, "civic", 2010, 5999.0)

        with self.assertRaisesRegex(ValueError, "Model must be defined"):
            self.car_mgr.add_car("honda", None, 2010, 5999.0)

        with self.assertRaisesRegex(ValueError, "Year must be defined"):
            self.car_mgr.add_car("honda", "civic", None, 5999.0)

        with self.assertRaisesRegex(ValueError, "Price must be defined"):
            self.car_mgr.add_car("honda", "civic", 2010, None)

        with self.assertRaisesRegex(ValueError, "Year must be between 1980 and 2019"):
            self.car_mgr.add_car("honda", "civic", 1979, 5999.0)

        with self.assertRaisesRegex(ValueError, "Year must be between 1980 and 2019"):
            self.car_mgr.add_car("honda", "civic", 2020, 5999.0)

        with self.assertRaisesRegex(ValueError, "Price must be a positive value"):
            self.car_mgr.add_car("Vancouver", "Edmonton", 2010, -9999.99)


    def test_delete_car_success(self):
        """ TP-04 - Success test on delete_car """

        cars_before = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_before), 0)

        self.car_mgr.add_car("Honda", "Civic", 2010, 5999.0)
        self.car_mgr.add_car("Ford", "Explorer", 2017, 32500.99)

        cars_between = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_between), 2)

        for car in cars_between:
            self.car_mgr.delete_car(car.id)

        cars_after = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_after), 0)

    def test_delete_cart_invalid(self):
        """ TP-05 - Validation test on delete_car """

        with self.assertRaisesRegex(ValueError, "Id must be defined"):
            self.car_mgr.delete_car(None)

        with self.assertRaisesRegex(ValueError, "Id must be defined"):
            self.car_mgr.delete_car("")

        with self.assertRaisesRegex(ValueError, "Id must be positive"):
            self.car_mgr.delete_car(-100)

    def test_get_all_cars_success(self):
        """ TP-06 - Success test on get_all_cars """

        cars_before = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_before), 0)

        self.car_mgr.add_car("Honda", "Civic", 2010, 5999.0)

        cars_between = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_between), 1)

        self.car_mgr.add_car("Ford", "Explorer", 2017, 32500.99)

        cars_after = self.car_mgr.get_all_cars()
        self.assertEqual(len(cars_after), 2)




if __name__ == "__main__":
    runner = xmlrunner.XMLTestRunner(output='car-test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
