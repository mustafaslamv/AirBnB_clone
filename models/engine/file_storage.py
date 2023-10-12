#!/usr/bin/python3
"""Module for storing data. manages serialization-deserialization"""

import json
import os
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """serialize-deserialize instances to/from JSON file"""

    __file_path = "file.json"
    __objects = {}
    classes_dict = {
        'User': User,
        'BaseModel': BaseModel,
        # 'State': State,
        # 'City': City,
        # 'Amenity': Amenity,
        # 'Place': Place,
        # 'Review': Review
    }

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
            json.dump(objects, json_file, indent=4)

    def reload(self):
        """deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                try:
                    objects = json.load(json_file)
                except json.JSONDecodeError:
                    objects = {}
            for key, val in objects.items():
                class_name = val['__class__']
                if class_name in self.classes_dict:
                    cls = self.classes_dict[class_name]
                    instance = cls(**val)
                    self.__objects[key] = instance
