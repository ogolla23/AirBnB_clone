#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A custom console module that controls instances.
"""


from datetime import datetime
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """A custom command processor."""
    prompt = '(hbnb) '
    allowed_classes = ['BaseModel', 'User', 'State', 'City',
                       'Amenity', 'Place', 'Review']

    def do_quit(self, line):
        """
        command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, line):
        """
        Creates a new instance.
        """
        args = shlex.split(line)
        if len(args) == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        else:
            new_obj = eval(args[0])()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """
        Prints an instance
        """
        args = shlex.split(line)
        inst_data = None
        if len(args) == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            inst_data = models.storage.all().get(key)
        if inst_data is None:
            print('** no instance found **')
        else:
            print(inst_data)

    def do_destroy(self, line):
        """
        Deletes an instance.
        """
        args = shlex.split(line)
        key = None
        if len(args) == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
        if key in models.storage.all():
            del models.storage.all()[key]
            models.storage.save()
        else:
            print('** no instance found **')

    def do_all(self, line):
        """
        Prints all instances.
        """
        args = shlex.split(line)
        objs = models.storage.all()
        if len(args) == 0:
            for obj in objs.values():
                print(obj)
        elif args[0] in self.allowed_classes:
            for key, obj in objs.items():
                if key.startswith(args[0]):
                    print(obj)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
        Adds an updating attribute ona instance.
        """
        args = shlex.split(line)
        key = None
        if len(args) == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print('** instance id missing **')
        elif len(args) == 2:
            print('** attribute name missing **')
        elif len(args) == 3:
            print('** value missing **')
        else:
            key = args[0] + '.' + args[1]
        if key in models.storage.all():
            setattr(models.storage.all()[key], args[2], args[3])
            models.storage.save()
        else:
            print('** no instance found **')

    def analyze_parameter_value(self, value):
        """
        Converts a string to a float or int
        Args:
            value: The value to analyze

        """
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)

        return value

    def get_objects(self, instance=''):
        """It gets the elements created by the console

        Args:
            instance (:obj:`str`, optional): The instance to finds into
                the objects.

        Returns:
            list: If the `instance` argument is not empty, it will search
            only for objects that match the instance. Otherwise, it will show
            all instances in the file where all objects are stored.

        """
        objects = models.storage.all()

        if instance:
            keys = objects.keys()
            return [str(val) for key, val in objects.items()
                    if key.startswith(instance)]

        return [str(val) for key, val in objects.items()]

    def default(self, line):
        """
        Links an unrecognized command to its coresponding method.
        """
        if '.' in line:
            splitted = re.split(r'\.|\(|\)', line)
            class_name = splitted[0]
            method_name = splitted[1]

            if class_name in self.allowed_classes:
                if method_name == 'all':
                    print(self.get_objects(class_name))
                elif method_name == 'count':
                    print(len(self.get_objects(class_name)))
                elif method_name == 'show':
                    class_id = splitted[2][1:-1]
                    self.do_show(class_name + ' ' + class_id)
                elif method_name == 'destroy':
                    class_id = splitted[2][1:-1]
                    self.do_destroy(class_name + ' ' + class_id)

    def emptyline(self):
        """
        prevents repeating previous command when empty command
        is used.
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
