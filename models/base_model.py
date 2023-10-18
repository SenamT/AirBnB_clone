#!/usr/bin/python3
"""this will define the Base Model class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """this will Represent the Base Model of the HBnB project"""

    def __init__(self, *args, **kwargs):
        """Start a new Base Model

        Arguments:
            *arguments: Unused
            **kwargs: this is the value pairs of attributes
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """this will update updated_at with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """R=this will return the dictionary of the Base Model instance
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """this will return the string representation of the Base Model instance"""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
