#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_state(self):
        """Test get method that retrieve one class object"""
        state = State()
        state.name = "ca"
        state.save()
        obj = storage.get("State", state.id)
        self.assertEqual(state, obj)
        storage.delete(obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_city(self):
        """Test get method that retrieve one class object"""
        city = City()
        city.name = "sf"
        city.save()
        obj = storage.get("City", city.id)
        self.assertEqual(city, obj)
        storage.delete(obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_user(self):
        """Test get method that retrieve one class object"""
        user = User()
        user.name = "ca"
        user.save()
        obj = storage.get("User", user.id)
        self.assertEqual(user, obj)
        storage.delete(obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_place(self):
        """Test get method that retrieve one class object"""
        new = Place()
        new.name = "ca"
        new.save()
        obj = storage.get("Place", new.id)
        self.assertEqual(new, obj)
        storage.delete(obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_review(self):
        """Test get method that retrieve one class object"""
        new = Review()
        new.name = "ca"
        new.save()
        obj = storage.get("Review", new.id)
        self.assertEqual(new, obj)
        storage.delete(obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_amenity(self):
        """Test get method that retrieve one class object"""
        new = Amenity()
        new.name = "ca"
        new.save()
        obj = storage.get("Amenity", new.id)
        self.assertEqual(new, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """test count method that count the number of object of each class"""
        count = storage.count()
        self.assertEqual(count, 0)
        obj = State()
        obj.save()
        count = storage.count()
        count_obj = storage.count("State")
        self.assertEqual(count, 1)
        self.assertEqual(count_obj, 1)

        obj1 = City()
        obj1.save()
        count = storage.count()
        count_obj = storage.count("City")
        self.assertEqual(count, 2)
        self.assertEqual(count_obj, 1)

        obj2 = User()
        obj2.save()
        count = storage.count()
        count_obj = storage.count("User")
        self.assertEqual(count, 3)
        self.assertEqual(count_obj, 1)

        obj3 = Place()
        obj3.save()
        count = storage.count()
        count_obj = storage.count("Place")
        self.assertEqual(count, 4)
        self.assertEqual(count_obj, 1)

        obj4 = Review()
        obj4.save()
        count = storage.count()
        count_obj = storage.count("Review")
        self.assertEqual(count, 5)
        self.assertEqual(count_obj, 1)

        obj5 = Amenity()
        obj5.save()
        count = storage.count()
        count_obj = storage.count("Amenity")
        self.assertEqual(count, 6)
        self.assertEqual(count_obj, 1)

        storage.delete(obj)
        storage.delete(obj1)
        storage.delete(obj2)
        storage.delete(obj3)
        storage.delete(obj4)
        storage.delete(obj5)
