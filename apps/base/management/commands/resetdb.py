from django.core.management import call_command
from os import remove
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from api.settings import DATABASES

        try:
            remove(DATABASES['default']['NAME'])
        except FileNotFoundError:
            pass

        call_command('syncdb', interactive=False)
        call_command('populate')
