#!/usr/bin/python3
"""Basemodel class defination"""
import models
from datetime import datetime
import uuid


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initializes new instance of basemodel
        Args:
            *args: Arguments
            **kwargs: keyword arguments
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)

    def save(self):
        """updated_at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def __str__(self):
        """Returns a string rep of basemodel"""
        classname = self.__class__.__name__
        return "[{}], ({}), {}".format(classname, self.id, self.__dict__)

    def to_dict(self):
        """ converts basemodel instance to dictionary
        Return: dictionary containing all keys/values
        """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
