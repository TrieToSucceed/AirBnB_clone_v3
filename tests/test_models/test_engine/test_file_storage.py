#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models import storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    def tearDown(self):
        """ teardown tests """
        all_objs = storage.all()
        all_objs.clear()
        storage.save()

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_get_state(self):
        """Test get method that retrieve one class object"""
        state = State()
        state.name = "ca"
        state.save()
        obj = storage.get("State", state.id)
        self.assertEqual(state, obj)

    def test_get_city(self):
        """Test get method that retrieve one class object"""
        city = City()
        city.name = "sf"
        city.save()
        obj = storage.get("City", city.id)
        self.assertEqual(city, obj)

    def test_get_user(self):
        """Test get method that retrieve one class object"""
        user = User()
        user.name = "ca"
        user.save()
        obj = storage.get("User", user.id)
        self.assertEqual(user, obj)

    def test_get_place(self):
        """Test get method that retrieve one class object"""
        new = Place()
        new.name = "ca"
        new.save()
        obj = storage.get("Place", new.id)
        self.assertEqual(new, obj)

    def test_get_review(self):
        """Test get method that retrieve one class object"""
        new = Review()
        new.name = "ca"
        new.save()
        obj = storage.get("Review", new.id)
        self.assertEqual(new, obj)

    def test_get_amenity(self):
        """Test get method that retrieve one class object"""
        new = Amenity()
        new.name = "ca"
        new.save()
        obj = storage.get("Amenity", new.id)
        self.assertEqual(new, obj)

    def test_count(self):
        """test count method that count the number of object of
        each class"""
        count = storage.count()
        self.assertEqual(count, 0)
        obj = State()
        obj.save()
        count = storage.count()
        count_obj = storage.count("State")
        self.assertEqual(count, 1)
        self.assertEqual(count_obj, 1)

        obj = City()
        obj.save()
        count = storage.count()
        count_obj = storage.count("City")
        self.assertEqual(count, 2)
        self.assertEqual(count_obj, 1)

        obj = User()
        obj.save()
        count = storage.count()
        count_obj = storage.count("User")
        self.assertEqual(count, 3)
        self.assertEqual(count_obj, 1)

        obj = Place()
        obj.save()
        count = storage.count()
        count_obj = storage.count("Place")
        self.assertEqual(count, 4)
        self.assertEqual(count_obj, 1)

        obj = Review()
        obj.save()
        count = storage.count()
        count_obj = storage.count("Review")
        self.assertEqual(count, 5)
        self.assertEqual(count_obj, 1)

        obj = Amenity()
        obj.save()
        count = storage.count()
        count_obj = storage.count("Amenity")
        self.assertEqual(count, 6)
        self.assertEqual(count_obj, 1)
