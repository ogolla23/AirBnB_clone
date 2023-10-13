#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The base Model Module for the AirBnB project
"""

from datetime import datetime
import models
import uuid


class BaseModel:
    """
    The base Model Class


    Attributes:
        id (str): It's an UUID for when an instance is created.
        created_at (datetime): The current date and time that
            an instance is created.
        updated_at (datetime): The current date and time that
            an instance is created and it will be updated every
            time that the object changes.

    """

    def __init__(self, *args, **kwargs):
        """
        The base Model __init__ Method

        """
        if kwargs:
            for arg, val in kwargs.items():
                if arg in ('created_at', 'updated_at'):
                    val = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')

                if arg != '__class__':
                    setattr(self, arg, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Returns class string representation.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Updates instances update_at and saves to file
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Returns instance dictionary """
        map_objects = {
            key: value.isoformat() if isinstance(value, datetime)
            else value
            for key, value in self.__dict__.items()
        }
        map_objects["__class__"] = self.__class__.__name__
        return map_objects
