#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import uuid
from datetime import datetime
import inspect
import models
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


class TestImproveStorage(unittest.TestCase):
    """Test the Improve Stoage Task"""

    @classmethod
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def setUpClass(cls):
        """Setup functionality to be used for the whole class"""
        cls.storage = models.storage

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_return_object(self):
        """Test that get returns object"""
        new_id = str(uuid.uuid4())
        name = "Oyo"
        new_state = State(id=new_id, name=name)
        self.storage.new(new_state)
        self.assertEqual(self.storage.get(State, new_id).id, new_id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_without_id(self):
        """Test no id supplied"""
        with self.assertRaises(TypeError):
            new_state = State(id=str(uuid.uuid4()), name="Ogbomoso")
            models.storage.get(new_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_return_none_id_not_present(self):
        """Test return none when id not present"""
        new_id = str(uuid.uuid4())
        self.assertEqual(self.storage.get(State, new_id), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_storage_count_is_integer(self):
        """Test the count method of the db_storage"""
        self.assertTrue(isinstance(
            self.storage.count(),
            int))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_storage_count_correct(self):
        """Test that the number of count return is correct
        """
        storage = self.storage
        state_count = storage.count(State)
        new_state = State(id=str(uuid.uuid4()), name="Lagos")
        storage.new(new_state)
        count_after_update = storage.count(State)
        self.assertEqual(state_count + 1, count_after_update)

        new_city = City(state_id=new_state.id, name="Ikorodu")
        total_count = storage.count()
        city_count = storage.count(City)
        storage.new(new_city)
        self.assertEqual(total_count + 1, storage.count())
        self.assertEqual(city_count + 1, storage.count(City))
