#!/usr/bin/python3
"""Module for storing data. manages serialization-deserialization"""

import json
import os
from models.base_model import BaseModel


class FileStorage:
    """serialize-deserialize instances to/from JSON file"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        # convert object values to serializable format
        objects = {}
        for key, val in self.__objects.items():
            objects[key] = val.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(objects, json_file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                objects = json.load(json_file)
            for key, val in objects.items():
                # remember dict["__class__"] = __class__.__name__
                # so eval(val['__class__']) will retrieve the class name
                # <class name>.id   = Classname(**val) (recreates object)
                self.__objects[key] = eval(val['__class__'])(**val)
