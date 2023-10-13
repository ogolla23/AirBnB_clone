#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The File Storage Module
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import path


class FileStorage:
    """
    The File Storage Class
    Attributes:
        __file_path (str): This is the path of the JSON file in which
            the contents of the `__objects` variable will be stored.
        __objects (dict): This store all the instances data
    """
    __file_path = 'objects.json'
    __objects = {}

    def all(self):
        """
        gets the _objects info
        """
        return self.__objects

    def new(self, obj):
        """
        Saves a new object in the `__objects` class attribute
        Args:
            obj (inst): The object to adds in the `__objects` class attribute
        Sets in the `__objects` class attribute the instance data
        with a key as <obj class name>.id.
        """
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """
        serializes the JSON file
        """
        dict_to_store = {k: v.to_dict() for k, v in self.__objects.items()}
        try:
            with open(self.__file_path, 'w') as f:
                json.dump(dict_to_store, f)
        except IOError:
            print("An error occurred while trying to write to the file.")

    def reload(self):
        """
        deserializes the JSON file.
        """
        try:
            with open(self.__file_path, 'r') as f:
                dict = json.load(f)
                for key, value in dict.items():
                    cls = value["__class__"]
                    self.__objects[key] = eval(cls)(**value)
        except FileNotFoundError:
            pass
