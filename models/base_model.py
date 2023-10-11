#!/usr/bin/python3
"""Base Model, this is the parent class for all other classes"""
import uuid
from datetime import datetime


class BaseModel:
    """defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """initializes a new BaseModel instance
        Args:
        id (str): the id of the instance
        created_at (datetime): the creation date
        updated_at (datetime): the last update date
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """returns a string representation of the BaseModel instance"""
        return f"[{__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates updated_at with current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a __dict__ representation of the instance"""
        dict = self.__dict__.copy()
        dict["__class__"] = __class__.__name__
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        return dict
