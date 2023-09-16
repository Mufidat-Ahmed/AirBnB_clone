#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.place import Place


class TestPlaceInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instatance_stored_object(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_public_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)

    def test_user_id_public_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)

    def test_name_public_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)

    def test_description_public_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place))
        self.assertNotIn("desctiption", place.__dict__)

    def test_number_rooms_public_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)

    def test_number_bathrooms_public_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)

    def test_max_guest__public_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)

    def test_price_by_night__public_attribute(self):
        place = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)

    def test_latitude_public_attribute(self):
        place = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)

    def test_longitude_public__attribute(self):
        place = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)

    def test_amenity_ids_public_attribute(self):
        place = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def test_differnt_user_created_at(self):
        place1 = Place()
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_unique_user_id(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_different_user_updated_at(self):
        place1 = Place()
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        strplace = place.__str__()
        self.assertIn("[Place] (123456)", strplace)
        self.assertIn("'id': '123456'", strplace)
        self.assertIn("'created_at': " + dt_repr, strplace)
        self.assertIn("'updated_at': " + dt_repr, strplace)

    def test_unused_args(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        place = Place(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "123")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_correct_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        place = Place()
        place.middle_name = "School"
        place.my_number = 98
        self.assertEqual("School", place.middle_name)
        self.assertIn("my_number", place.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.now()
        place = Place()
        place.id = "12345"
        place.created_at = place.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def test_contrast_to_dict(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def test_to_dict_with_arg(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


class TestPlace_save(unittest.TestCase):
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
        place = Place()
        f_updated_at = place.updated_at
        place.save()
        self.assertLess(f_updated_at, place.updated_at)

    def test_two_saves(self):
        place = Place()
        f_updated_at = place.updated_at
        place.save()
        n_updated_at = place.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        place.save()
        self.assertLess(n_updated_at, place.updated_at)

    def test_save_with_arg(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_save_updates_file(self):
        place = Place()
        place.save()
        placeid = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(placeid, f.read())


if __name__ == "__main__":
    unittest.main()
