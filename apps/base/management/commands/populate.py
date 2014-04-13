import importlib
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from api.settings import INSTALLED_APPS

        for app in INSTALLED_APPS:
            if not app.startswith('apps'):
                continue

            print("Populating app: %s" % app)
            try:
                importlib.import_module("%s.%s" % (app, 'populate'))
            except ImportError:
                pass
            except Exception as e:
                print("Error populating the database of application: %s" % app)
                print("%s" % e)
                raise RuntimeError("Be sure to define the correct dependency order in settings.INSTALLED_APPS")
