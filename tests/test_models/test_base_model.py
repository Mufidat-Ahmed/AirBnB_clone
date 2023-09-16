#!/usr/bin/python3
"""models.basem unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModelInstantation(unittest.TestCase):
    """unittest for BaseModel class"""
    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instatance_stored_object(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_differnt_basem_created_at(self):
        basem1 = BaseModel()
        basem2 = BaseModel()
        self.assertLess(basem1.created_at, basem2.created_at)

    def test_unique_basem_id(self):
        basem1 = BaseModel()
        basem2 = BaseModel()
        self.assertNotEqual(basem1.id, basem2.id)

    def test_different_basem_updated_at(self):
        basem1 = BaseModel()
        basem2 = BaseModel()
        self.assertLess(basem1.updated_at, basem2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = dt
        strbasem = basem.__str__()
        self.assertIn("[BaseModel] (123456)", strbasem)
        self.assertIn("'id': '123456'", strbasem)
        self.assertIn("'created_at': " + dt_repr, strbasem)
        self.assertIn("'updated_at': " + dt_repr, strbasem)

    def test_unused_args(self):
        basem = BaseModel(None)
        self.assertNotIn(None, basem.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        basem = BaseModel(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(basem.id, "123")
        self.assertEqual(basem.created_at, dt)
        self.assertEqual(basem.updated_at, dt)


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(BaseModel().to_dict()))

    def test_to_dict_correct_keys(self):
        basem = BaseModel()
        self.assertIn("id", basem.to_dict())
        self.assertIn("created_at", basem.to_dict())
        self.assertIn("updated_at", basem.to_dict())
        self.assertIn("__class__", basem.to_dict())

    def test_to_dict_contains_added_attributes(self):
        basem = BaseModel()
        basem.middle_name = "School"
        basem.my_number = 98
        self.assertEqual("School", basem.middle_name)
        self.assertIn("my_number", basem.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        basem = BaseModel()
        basem_dict = basem.to_dict()
        self.assertEqual(str, type(basem_dict["id"]))
        self.assertEqual(str, type(basem_dict["created_at"]))
        self.assertEqual(str, type(basem_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(basem.to_dict(), tdict)

    def test_contrast_to_dict(self):
        basem = BaseModel()
        self.assertNotEqual(basem.to_dict(), basem.__dict__)

    def test_to_dict_with_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.to_dict(None)


class TestBaseModel_save(unittest.TestCase):
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
        basem = BaseModel()
        f_updated_at = basem.updated_at
        basem.save()
        self.assertLess(f_updated_at, basem.updated_at)

    def test_two_saves(self):
        basem = BaseModel()
        f_updated_at = basem.updated_at
        basem.save()
        n_updated_at = basem.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        basem.save()
        self.assertLess(n_updated_at, basem.updated_at)

    def test_save_with_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.save(None)

    def test_save_updates_file(self):
        basem = BaseModel()
        basem.save()
        basemid = "BaseModel." + basem.id
        with open("file.json", "r") as f:
            self.assertIn(basemid, f.read())


if __name__ == "__main__":
    unittest.main()
