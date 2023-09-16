#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.state import State


class TestStateInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(State, type(State()))

    def test_new_instatance_stored_object(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_public_attribute(self):
        state = State()
        self.assertEqual(str, type(state.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_differnt_user_created_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_unique_user_id(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_different_user_updated_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        strstate = state.__str__()
        self.assertIn("[State] (123456)", strstate)
        self.assertIn("'id': '123456'", strstate)
        self.assertIn("'created_at': " + dt_repr, strstate)
        self.assertIn("'updated_at': " + dt_repr, strstate)

    def test_unused_args(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        state = State(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "123")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)


class TestState_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_correct_keys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        state = State()
        state.middle_name = "School"
        state.my_number = 98
        self.assertEqual("School", state.middle_name)
        self.assertIn("my_number", state.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.now()
        state = State()
        state.id = "12345"
        state.created_at = state.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), tdict)

    def test_contrast_to_dict(self):
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


class TestState_save(unittest.TestCase):
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
        state = State()
        f_updated_at = state.updated_at
        state.save()
        self.assertLess(f_updated_at, state.updated_at)

    def test_two_saves(self):
        state = State()
        f_updated_at = state.updated_at
        state.save()
        n_updated_at = state.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        state.save()
        self.assertLess(n_updated_at, state.updated_at)

    def test_save_with_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self):
        state = State()
        state.save()
        stateid = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(stateid, f.read())


if __name__ == "__main__":
    unittest.main()
