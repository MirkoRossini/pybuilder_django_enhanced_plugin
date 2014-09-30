__author__ = 'Mirko Rossini'

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Command that fails'

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=str)

    def handle(self, *args, **options):
        raise CommandError("Command failed")