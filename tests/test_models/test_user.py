#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.user import User


class TestUserInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(User, type(User()))

    def test_new_instatance_stored_object(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(User().id))

    def test_email_string(self):
        self.assertEqual(str, type(User.email))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_password_string(self):
        self.assertEqual(str, type(User.password))

    def test_firstname_string(self):
        self.assertEqual(str, type(User.first_name))

    def test_lastname_string(self):
        self.assertEqual(str, type(User.last_name))

    def test_differnt_user_created_at(self):
        user1 = User()
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_unique_user_id(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_different_user_updated_at(self):
        user1 = User()
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        struser = user.__str__()
        self.assertIn("[User] (123456)", struser)
        self.assertIn("'id': '123456'", struser)
        self.assertIn("'created_at': " + dt_repr, struser)
        self.assertIn("'updated_at': " + dt_repr, struser)

    def test_unused_args(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        user = User(id="2bf3ebfd-a220-49ee-9ae6-b01c75f6f6a4", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "2bf3ebfd-a220-49ee-9ae6-b01c75f6f6a4")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)


class TestUser_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_correct_keys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        user = User()
        user.middle_name = "School"
        user.my_number = 98
        self.assertEqual("School", user.middle_name)
        self.assertIn("my_number", user.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), tdict)

    def test_contrast_to_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)

class TestUser_save(unittest.TestCase):
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
        user = User()
        f_updated_at = user.updated_at
        user.save()
        self.assertLess(f_updated_at, user.updated_at)

    def test_two_saves(self):
        user = User()
        f_updated_at = user.updated_at
        user.save()
        n_updated_at = user.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        user.save()
        self.assertLess(n_updated_at, user.updated_at)

    def test_save_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        user = User()
        user.save()
        userid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(userid, f.read())



if __name__ == "__main__":
    unittest.main()
