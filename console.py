#!/usr/bin/python3
"""simple command interpreter"""
import cmd
import models


class HBNBCommand(cmd.Cmd):
    """the entry point of the command interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, args):
        """Exit the interpreter using 'quit'"""
        return True

    def do_EOF(self, args):
        """EOF (CTRL+D) exits the interpreter"""
        return True

    def emptyline(self):
        """do nothing when newline entered"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
