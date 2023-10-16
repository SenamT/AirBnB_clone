#!/usr/bin/env python3
"""
This is the module for the Air BnB clone console
"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
from typing import get_type_hints
import json
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class

    This is the command-line for the interpreter which manages the objects which are inside the HBNB data storage system

    Attributes:
        prompt: This is the string for the command prompt
        cls: these are available class names for object management which were put into a class
    """

    prompt = "(hbnb) "
    cls = ["BaseModel", "User", "Place", "State", "City", "Amenity", "Review"]

    def do_EOF(self, line):
        """
        This will exit the command interpreter on end-of-file
        """
        print()
        return True

    def help_EOF(self):
        """
        This will display help info for the EOF command
        """
        print("\nUsage: EOF\n")
        print("This command allows you to exit the command", end=" ")
        print("interpreter gracefully by pressing Ctrl+D (EOF).\n")

    def do_quit(self, arg):
        """
        This will exit the command interpreter
        """
        return True

    def help_quit(self):
        """
        This will display help information for the quit command
        """
        print("\nUsage: quit\n")
        print("This command allows you to exit the command", end=" ")
        print("interpreter gracefully.\n")

    def emptyline(self):
        """
        nothing will be done when an empty line is entered
        """
        pass

    def is_valid(self, line, line_arr, instances, flag):
        """
        This will check the input based on specified conditions validity
        """
        if flag >= 1 and len(line_arr) == 0:
            print("** class name missing **")
        elif flag >= 1 and line_arr[0] not in self.cls:
            print("** class doesn't exist **")
        elif flag >= 2 and len(line_arr) == 1:
            print("** instance id missing **")
        elif flag >= 2 and line not in instances:
            print("** no instance found **")
        elif flag >= 3 and len(line_arr) == 2:
            print("** attribute name missing **")
        elif flag >= 3 and len(line_arr) == 3:
            print("** value missing **")
        else:
            return True
        return False

    def value_type(self, attr, line, obj):
        """
        This will convert a string to an integer or a float if it is possible
        """
        if (hasattr(obj, attr)):
            attr_type = type(getattr(obj, attr))
            try:
                return attr_type(line)
            except ValueError:
                pass
        if re.match(r"^\d+$", line):
            return int(line)
        elif re.match(r"^\d+\.\d+$", line):
            return float(line)
        else:
            return line

    def do_create(self, line):
        """
        This will create a new instance of a specified class and then save it to storage
        """
        line_arr = shlex.split(line)
        if self.is_valid("", line_arr, {}, 1):
            my_model = eval(line_arr[0])()
            my_model.save()
            print(my_model.id)

    def help_create(self):
        """
        This will display help information for the create command
        """
        print("\nUsage: create <class_name>\n")
        print("This command creates a new instance of", end=" ")
        print("the specified class and assigns it a unique identifier.\n")

    def do_show(self, line):
        """
        This will display an instance in string representation
        """
        instances = storage.all()
        line_arr = shlex.split(line)
        if len(line_arr) >= 2:
            line = "{}.{}".format(line_arr[0], line_arr[1])
        if self.is_valid(line, line_arr, instances, 2):
            print(instances[line])

    def help_show(self):
        """
        This will display help information for the show command
        """
        print("\nUsage: show <class_name> <id>\n")
        print("This command displays an instance's string representation.\n")

    def do_destroy(self, line):
        """
        This will delete an instance by class name and instance ID
        """
        instances = storage.all()
        line_arr = shlex.split(line)
        if len(line_arr) >= 2:
            line = "{}.{}".format(line_arr[0], line_arr[1])
        if self.is_valid(line, line_arr, instances, 2):
            del instances[line]
            storage.save()

    def help_destroy(self):
        """
        This will display help for the destroy command
        """
        print("\nUsage: help destroy\n")
        print("Destroy command deletes an instance by class", end=' ')
        print("name and instance ID.\n")

    def do_all(self, line=None):
        """
        This will display string representations of all the instances
        """
        instances = storage.all()
        line_arr = shlex.split(line)
        if len(line_arr) == 1 and line_arr[0] not in self.cls:
            print("** class doesn't exist **")
            return
        print_model = []
        for inst in instances:
            if len(line_arr) == 0 or (
                len(line_arr) >= 1
                and line_arr[0] == instances[inst].to_dict()["__class__"]
            ):
                print_model.append(str(instances[inst]))
        print(print_model)

    def help_all(self):
        """
        This will display help for the all command
        """
        print("\nUsage: help all\n")
        print("All command displays string representations of all instances.")
        print("Optionally, provide a class name to filter instances", end=' ')
        print("of a specific class.\n")

    def count(self, line):
        """
        This will count the amount of instances of a specified class
        """
        instances = storage.all()
        count = 0
        if line not in self.cls:
            print("** class doesn't exist **")
            return
        for inst in instances:
            if line == instances[inst].to_dict()["__class__"]:
                count += 1
        print(count)

    def do_update(self, line, flag=0):
        """
        This will update an instance attribute's value by its class name and instance ID
        """
        instances = storage.all()
        if not flag:
            l_arr = shlex.split(line)
        else:
            l_arr = line
        if len(l_arr) >= 2:
            line = "{}.{}".format(l_arr[0], l_arr[1])
        if self.is_valid(line, l_arr, instances, 3):
            l_arr[3] = self.value_type(l_arr[2], l_arr[3], instances[line])
            setattr(instances[line], l_arr[2], l_arr[3])
            instances[line].save()

    def help_update(self):
        """
        This will display help for the update command
        """
        print("\nUsage: help update\n")
        print("Update command modifies an instance's attribute value", end=" ")
        print("by class name, instance ID, attribute name, and value.")
        print("Provide required arguments to update.\n")

    def default(self, line):
        """
        This will handle behavior for the commands of format: <cls>.<cmd>(<additionnal_args>)
        """
        instances = storage.all()
        line_arr = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if line_arr:
            line_arr = list(line_arr.groups())
            line_arr[2] = line_arr[2].replace(",", "")
            line_args = shlex.split(line_arr[2])
            for i in range(len(line_args)):
                line_args[i] = line_args[i].strip("{}:")
        cmd = {
            "all": self.do_all,
            "count": self.count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": None
        }
        if (
            line_arr
            and len(line_arr) >= 2
            and line_arr[1] in cmd
        ):
            if len(line_arr) >= 3 and (
                line_arr[1] == "show" or line_arr[1] == "destroy"
            ):
                arg = line_arr[0] + " " + line_arr[2]
                cmd[line_arr[1]](arg)
            elif len(line_arr) >= 3 and line_arr[1] == "update":
                if len(line_args) == 1:
                    args = [line_arr[0], line_args[0]]
                    self.do_update(args, 1)
                for i in range(1, len(line_args), 2):
                    args = [line_arr[0], line_args[0], line_args[i]]
                    if i + 1 < len(line_args):
                        args.append(line_args[i + 1])
                    self.do_update(args, 1)
            else:
                arg = line_arr[0]
                cmd[line_arr[1]](arg)
        else:
            super().default(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
