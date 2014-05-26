# -*- coding: utf-8 -*-
import sys
import inspect
import argparse


class SubCommand(object):
    name = ''
    description = ''
    args = []   # (tuple, dict)

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            prog=self.name, add_help=False,
            description=unicode(self.description))

        for a, k in self.args:
            self.parser.add_argument(*a, **k)

    def help(self):
        self.parser.print_help()

    def execute(self, *args, **options):
        params = self.parser.parse_args(args)
        self.run(params, **options)

    def run(self, params, **options):
        raise NotImplemented()


class Command(object):

    @classmethod
    def subcommands(cls):
        return dict(
            (v.name, v) for k, v in cls.__dict__.items()
            if inspect.isclass(v) and issubclass(v, SubCommand))

    @classmethod
    def subcommand(cls, name):
        return cls.subcommands().get(name, None)

    def run_from_argv(self, argv):
        ''' Django Management Command interface '''

        args = argv and argv[0] == 'manage.py' and argv[2:] or argv[1:]

        if len(args) < 1:
            for k, v in self.subcommands().items():
                print "\n\n*** Subcommand:", k
                v().help()

        elif len(args) > 1 and args[0] == 'help':
            command = self.subcommand(args[1])
            command and command().help()
        else:
            command = self.subcommand(args[0])
            if command:
                command().execute(*args[1:])
            else:
                print "ERROR ", args[0], "is not found."
                for k, v in self.subcommands().items():
                    print "----- ", k, ":",  v.description


if __name__ == '__main__':
    class MyCommand(Command):
        class Echo(SubCommand):
            name = 'echo'
            description = 'echo back arguments'
            args = [
                (('msg',), dict(nargs=1, help="Message String")),
            ]

            def run(self, param, **options):
                print param.msg[0]
    #: exec
    MyCommand().run_from_argv(sys.argv)