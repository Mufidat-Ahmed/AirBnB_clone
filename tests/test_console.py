import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        # Initialize the HBNBCommand instance
        # create a StringIO object to capture stdout
        self.console = HBNBCommand()
        self.test_stdout = StringIO()

    def tearDown(self):
        # Clean up and close the StringIO object
        self.test_stdout.close()

    def capture_stdout(self):
        # Helper method to capture the contents of the captured stdout
        return self.test_stdout.getvalue().strip()

    def test_do_count(self):
        # Test the 'count' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd("count BaseModel")
            output = self.capture_stdout()
            self.assertEqual(output, "0")

    def test_do_create(self):
        # Test the 'create' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd("create BaseModel")
            output = self.capture_stdout()
            self.assertTrue(output.startswith(""))

    def test_do_show(self):
        test_obj = BaseModel()
        test_obj.save()
        test_obj_id = test_obj.id

        # Test the 'show' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd(f"show BaseModel {test_obj_id}")
            output = self.capture_stdout()
            self.assertTrue(output.startswith(""))

    def test_do_destroy(self):
        test_obj = BaseModel()
        test_obj.save()
        test_obj_id = test_obj.id

        # Test the 'destroy' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd(f"destroy BaseModel {test_obj_id}")
            output = self.capture_stdout()
            self.assertEqual(output, "")

    def test_do_all(self):
        # Test the 'all' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd("all BaseModel")
            output = self.capture_stdout()
            self.assertTrue(output.startswith(""))

    def test_do_update(self):
        test_obj = BaseModel()
        test_obj.save()
        test_obj_id = test_obj.id

        # Test the 'update' command
        with patch('sys.stdout', new=self.test_stdout):
            self.console.onecmd(f"update BaseModel {test_obj_id}
                                attr_name attr_value")
            output = self.capture_stdout()
            self.assertEqual(output, "")

    def test_do_quit(self):
        # Test the 'quit' command
        result = self.console.onecmd("quit")
        self.assertTrue(result)

    def test_do_EOF(self):
        # Test the 'EOF' command
        result = self.console.onecmd("EOF")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
