#!/usr/bin/python3
"""Filestorage class defination"""
import json
from models.base_model import BaseModel


class FileStorage:
    """storage engine representation"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        objdict = FileStorage.__objects
        objectdict = {obj: objdict[obj].to_dict() for obj in objdict.keys()}
        with open(FileStorage.____file_path, "w") as f:
            json.dumps(objectdict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.____file_path) as f:
                objectdict = json.load(f)
                for m in objectdict.values():
                    clssname = m["__class__"]
                    del m["__class__"]
                    self.new(eval(clssname)(**m))
        except FileNotFoundError:
            return
