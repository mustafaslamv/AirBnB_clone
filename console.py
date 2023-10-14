#!/usr/bin/python3
"""simple command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import re
import sys


class HBNBCommand(cmd.Cmd):
    """the entry point of the command interpreter"""

    classes_dict = {
        'User': User,
        'BaseModel': BaseModel,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
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

    def do_count(self, line):
        """Display count of instances specified"""
        if line in HBNBCommand.classes_dict:
            count = 0
            for key, objs in storage.all().items():
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """Handle Cmd methods."""
        line_vector = line.split('.')
        class_argument = line_vector[0]

        if line_vector == []:
            print("*** Unknown syntax: {}".format(line))
            return

        try:
            line_vector = line_vector[1].split('(')
            command = line_vector[0]

            if command == 'all':  # <class name>.all
                HBNBCommand.do_all(self, class_argument)  # all BaseModel

            elif command == 'count':  # <class name>.count()
                HBNBCommand.do_count(self, class_argument)

            elif command == 'show':  # <class name>.show(<id>)
                line_vector = line_vector[1].split(')')
                id_argument = line_vector[0].strip("'\"")
                argument = class_argument + ' ' + id_argument
                HBNBCommand.do_show(self, argument)  # show BaseModel 123

            elif command == 'destroy':  # <class name>.destroy(<id>)
                line_vector = line_vector[1].split(')')
                id_argument = line_vector[0].strip("'\"")
                argument = class_argument + ' ' + id_argument
                HBNBCommand.do_destroy(self, argument)  # destroy BaseModel 122

            elif command == 'update':
                line_vector = line_vector[1].split(',')
                id_argument = line_vector[0].strip("'\"")
                name_argument = line_vector[1].strip(',')
                if "{" not in line:
                    value_argument = line_vector[2]
                    name_argument = name_argument.strip(" '\"")
                    value_argument = value_argument.strip(' )')
                if "{" in line:

                    b1 = line.index('{')
                    b2 = line.index('}')
                    value_dict = line[b1 + 1: b2].replace(" ", "")
                    value_dict_list = value_dict.split(",")

                    for s in value_dict_list:
                        s = s.split(":")
                        argument = class_argument + ' ' + id_argument + \
                            ' ' + s[0][1:-1] + ' ' + s[1]
                        HBNBCommand.do_update(self, argument)
                        key = class_argument + '.' + id_argument
                        if key not in storage.all().keys():
                            return
                else:
                    # If eval fails, use the attribute and value pattern
                    argument = class_argument + ' ' + id_argument + \
                        ' ' + name_argument + ' ' + value_argument
                    HBNBCommand.do_update(self, argument)

            else:
                print("*** Unknown syntax: {}".format(line))
                return

        except IndexError:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            if line:
                HBNBCommand().onecmd(line)
    else:
        HBNBCommand().cmdloop()
