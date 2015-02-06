# -*- coding: utf-8 -*-
import command

from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models


class Command(BaseCommand, command.Command):

    def run_from_argv(self, argv):
        return self.run(argv[1:])


class SubCommand(command.SubCommand):

    def module(self, package):
        return package.replace('.management.commands', '')

    def app(self, package):
        return get_app(self.module(package))

    def models(self, package):
        return get_models(self.app(package))
