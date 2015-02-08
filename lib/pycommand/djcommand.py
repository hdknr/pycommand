# -*- coding: utf-8 -*-
import command

from django.core.management.base import BaseCommand


class SubCommand(command.SubCommand):
    pass


class Command(BaseCommand, command.Command):

    def run_from_argv(self, argv):
        return self.run(argv[1:])
