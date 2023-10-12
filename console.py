#!/usr/bin/python3
"""simple command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
import re
import sys


class HBNBCommand(cmd.Cmd):
    """the entry point of the command interpreter"""

    classes_dict = {
        'User': User,
        'BaseModel': BaseModel,
        # 'State': State,
        # 'City': City,
        # 'Amenity': Amenity,
        # 'Place': Place,
        # 'Review': Review
    }
    prompt = "(hbnb) "

    def do_quit(self, args):
        """
        Exit the interpreter using 'quit'
        """
        return True

    def do_EOF(self, args):
        """
        EOF (CTRL+D) exits the interpreter
        """
        return True

    def emptyline(self):
        """do nothing when newline entered"""
        pass

    def do_create(self, args):
        """
        Creates a new instance of BaseModel.

        usage: create <class name>
        """
        if args == "":
            print("** class name missing **")
            return
        else:
            try:
                new_instance = eval(args)()
                new_instance.save()
                print(new_instance.id)
            except Exception:
                print("** class doesn't exist **")
                return

    def do_show(self, args):
        """
        Prints the string representation of an instance.

        usage: show <class name> <id>
        """
        new_list = args.split()
        if new_list == []:
            print("** class name missing **")
            return
        elif len(new_list) == 1:
            print("** instance id missing **")
            return
        elif new_list[0] not in self.classes_dict:
            print("** class doesn't exist **")
            return
        class_name = new_list[0]
        instance_id = new_list[1]
        key = f"{class_name}.{instance_id}"
        objects = storage.all()
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")

    def do_all(self, args):
        """
        Prints all string representation of all instances

        usage: all <class name> or all
        """
        new_list = args.split()
        result = []
        if not new_list:
            objects = storage.all()
            for key, val in objects.items():
                result.append(str(val))
            print(result)
        elif new_list[0] not in self.classes_dict:
            print("** class doesn't exist **")
            return
        else:
            objects = storage.all()
            class_name = new_list[0]
            for key, val in objects.items():
                if val.__class__.__name__ == class_name:
                    result.append(str(val))
            print(result)

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id

        usage: destroy <class name> <id>
        """
        new_list = args.split()
        if new_list == []:
            print("** class name missing **")
            return
        elif len(new_list) == 1:
            print("** instance id missing **")
            return
        elif new_list[0] not in self.classes_dict:
            print("** class doesn't exist **")
            return
        else:
            class_name = new_list[0]
            instance_id = new_list[1]
            key = f"{class_name}.{instance_id}"
            objects = storage.all()
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_update(self, line):
        """
        Updates an instance based on the class name and id

        usage: update <class name> <id> <attribute name> <attribute value>
        """
        line_vector = line.split()
        vector_len = len(line_vector)
        if line_vector == []:
            print("** class name missing **")
            return
        elif line_vector[0] not in self.classes_dict:
            print("** class doesn't exist **")
            return
        elif vector_len < 2:
            print("** instance id missing **")
            return
        else:
            objects = storage.all()
            key = line_vector[0] + "." + line_vector[1]

            if key not in objects.keys():
                print("** no instance found **")
                return
            elif vector_len < 3:
                print("** attribute name missing **")
                return
            elif vector_len < 4:
                print("** value missing **")
                return
            else:
                setattr(objects[key],
                        line_vector[2],  eval(line_vector[3]))
                objects[key].save()


if __name__ == '__main__':
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            if line:
                HBNBCommand().onecmd(line)
    else:
        HBNBCommand().cmdloop()
