#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.amenity import Amenity


class TestAmenityInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instatance_stored_object(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_public_attribute(self):
        amenity = Amenity()
        self.assertEqual(str, type(amenity.name))
        self.assertIn("name", dir(amenity))
        self.assertNotIn("name", amenity.__dict__)

    def test_differnt_user_created_at(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_unique_user_id(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_different_user_updated_at(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        stramenity = amenity.__str__()
        self.assertIn("[Amenity] (123456)", stramenity)
        self.assertIn("'id': '123456'", stramenity)
        self.assertIn("'created_at': " + dt_repr, stramenity)
        self.assertIn("'updated_at': " + dt_repr, stramenity)

    def test_unused_args(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "123")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_correct_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenity = Amenity()
        amenity.middle_name = "School"
        amenity.my_number = 98
        self.assertEqual("School", amenity.middle_name)
        self.assertIn("my_number", amenity.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.now()
        amenity = Amenity()
        amenity.id = "12345"
        amenity.created_at = amenity.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), tdict)

    def test_contrast_to_dict(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def test_to_dict_with_arg(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


class TestAmenity_save(unittest.TestCase):
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
        amenity = Amenity()
        f_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(f_updated_at, amenity.updated_at)

    def test_two_saves(self):
        amenity = Amenity()
        f_updated_at = amenity.updated_at
        amenity.save()
        n_updated_at = amenity.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        amenity.save()
        self.assertLess(n_updated_at, amenity.updated_at)

    def test_save_with_arg(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_save_updates_file(self):
        amenity = Amenity()
        amenity.save()
        amenityid = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenityid, f.read())


if __name__ == "__main__":
    unittest.main()
