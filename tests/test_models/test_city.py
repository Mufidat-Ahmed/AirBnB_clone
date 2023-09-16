#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.city import City


class TestCityInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(City, type(City()))

    def test_new_instatance_stored_object(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_differnt_user_created_at(self):
        city1 = City()
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_unique_user_id(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_different_user_updated_at(self):
        city1 = City()
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        strcity = city.__str__()
        self.assertIn("[City] (123456)", strcity)
        self.assertIn("'id': '123456'", strcity)
        self.assertIn("'created_at': " + dt_repr, strcity)
        self.assertIn("'updated_at': " + dt_repr, strcity)

    def test_unused_args(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        city = City(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "123")
        self.assertEqual(city.created_at, dt)
        self.assertEqual(city.updated_at, dt)


class TestCity_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_correct_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city = City()
        city.middle_name = "School"
        city.my_number = 98
        self.assertEqual("School", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.now()
        city = City()
        city.id = "12345"
        city.created_at = city.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_contrast_to_dict(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        city = City()
        f_updated_at = city.updated_at
        city.save()
        self.assertLess(f_updated_at, city.updated_at)

    def test_two_saves(self):
        city = City()
        f_updated_at = city.updated_at
        city.save()
        n_updated_at = city.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        city.save()
        self.assertLess(n_updated_at, city.updated_at)

    def test_save_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        city = City()
        city.save()
        cityid = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(cityid, f.read())


if __name__ == "__main__":
    unittest.main()
