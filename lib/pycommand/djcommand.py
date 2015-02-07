# -*- coding: utf-8 -*-
import command

from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models


class SubCommand(command.SubCommand):

    def module(self, package):
        return package.replace('.management.commands', '')

    def app(self, package):
        return get_app(self.module(package))

    def models(self, package):
        return get_models(self.app(package))


class Command(BaseCommand, command.Command):

    def run_from_argv(self, argv):
        return self.run(argv[1:])

    class ModelDoc(SubCommand):
        name = "model_doc"
        description = "Create Model Documentation for Sphinx"
        args = []

        def header(self, text, level=0):
            c = ['=', '=', '-', '^', '~', '#', ]
            if level == 0:
                print len(text) * 2 * c[level]
            print text.encode('utf8')
            print len(text) * 2 * c[level]
            print

        def ref(self, name):
            print ".. _{0}:\n".format(name)

        def autoclass(self, name):
            print ".. autoclass:: {0}".format(name)
            print "    :members:".encode('utf8')
            print

        def run(self, params, **options):
            title = (self.app(__package__).__doc__ or "Model").split('\n')[0]
            self.header(title, 0)

            module = self.module(__package__)

            for m in self.models(__package__):
                fullname = "{0}.models.{1}".format(module, m.__name__)
                self.ref(fullname)
                title = u"{0}:{1}".format(
                    m.__name__,
                    (m.__doc__ or '').split(u'\n')[0],
                )
                self.header(title, 1)
                self.autoclass(fullname)

    class SearchField(SubCommand):
        name = "search_field"
        description = "Search Model Field"
        args = [
            (('fields',), dict(nargs='+', help="Field Name")),
        ]

        def run(self, params, **options):
            for m in self.models(__package__):
                for f in params.fields:
                    try:
                        fld = m._meta.get_field(f)
                        print m.__name__, ":",  fld.deconstruct()
                    except:
                        pass
