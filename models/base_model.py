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
        f = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(kwargs[key], f)
                if key != '__class__':
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def save(self):
        """updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def __str__(self):
        """returns class name, id and attribute dictionary
        """
        class_name = "[" + self.__class__.__name__ + "]"
        dct = {k: v for (k, v) in self.__dict__.items() if (not v) is False}
        return class_name + " (" + self.id + ") " + str(dct)

    def to_dict(self):
        """to create a new dictionary, adding a key and returning
        datemtimes converted to strings
        """
        new_dict = {
                key: value.isoformat() if isinstance(value, datetime)
                else value
                for key, value in self.__dict__.items() if value is not None
                }
        new_dict['__class__'] = self.__class__.__name__

        return new_dict
