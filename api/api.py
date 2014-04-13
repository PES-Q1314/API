from tastypie.api import Api
from tastypie.resources import ModelResource


def resource_discover():
    from django.conf import settings
    from django.utils.importlib import import_module
    import inspect

    resources = []
    for app in settings.INSTALLED_APPS:
        if app.startswith('apps'):
            try:
                module = import_module('%s.resources' % app)
                members = inspect.getmembers(module,
                                             # Get only members defined in the module
                                             # i.e. avoid imported stuff
                                             lambda x: inspect.getmodule(x) == module)
            except ImportError as e:
                members = []

            for name, member in members:
                if name.endswith('Resource') and issubclass(member, ModelResource):
                    resources.append(member)

    return resources


resources = resource_discover()
api = Api(api_name="api")
for resource in resources:
    api.register(resource())