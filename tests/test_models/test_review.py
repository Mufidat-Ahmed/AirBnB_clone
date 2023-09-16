#!/usr/bin/python3
"""models.user unittest defination"""
import os
import models
import unittest
from datetime import datetime
from models.review import Review


class TestReviewInstantation(unittest.TestCase):
    """unittest for User class"""
    def test_no_args(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instatance_stored_object(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_string(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_publicdate_time(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_public_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_public_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_public_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_differnt_user_created_at(self):
        review1 = Review()
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_unique_user_id(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_different_user_updated_at(self):
        review1 = Review()
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        strreview = review.__str__()
        self.assertIn("[Review] (123456)", strreview)
        self.assertIn("'id': '123456'", strreview)
        self.assertIn("'created_at': " + dt_repr, strreview)
        self.assertIn("'updated_at': " + dt_repr, strreview)

    def test_unused_args(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        review = Review(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "123")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)


class TestReview_to_dict(unittest.TestCase):
    """Unittests for to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_correct_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        review = Review()
        review.middle_name = "School"
        review.my_number = 98
        self.assertEqual("School", review.middle_name)
        self.assertIn("my_number", review.to_dict())

    def test_to_dict_datetime_attributes_string(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.now()
        review = Review()
        review.id = "12345"
        review.created_at = review.updated_at = dt
        tdict = {
            'id': '12345',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), tdict)

    def test_contrast_to_dict(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_to_dict_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


class TestReview_save(unittest.TestCase):
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
        review = Review()
        f_updated_at = review.updated_at
        review.save()
        self.assertLess(f_updated_at, review.updated_at)

    def test_two_saves(self):
        review = Review()
        f_updated_at = review.updated_at
        review.save()
        n_updated_at = review.updated_at
        self.assertLess(f_updated_at, n_updated_at)
        review.save()
        self.assertLess(n_updated_at, review.updated_at)

    def test_save_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        review = Review()
        review.save()
        reviewid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(reviewid, f.read())


if __name__ == "__main__":
    unittest.main()
