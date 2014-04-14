from inspect import signature, getmembers
import json
from functools import wraps
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.utils import trailing_slash


def is_action(obj):
    return getattr(obj, 'is_action', False)


def action(name=None, url=None, static=False, allowed=None, login_required=False, throttled=False):
    if callable(name):
        wrapped = name
        name = None
    else:
        wrapped = None

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if allowed is not None:
                self.method_check(request, allowed)

            if login_required:
                self.is_authenticated(request)

            if throttled:
                self.throttle_check(request)
                self.log_throttled_access(request)

            return func(self, request, *args, **kwargs)

        wrapper.is_action = True
        wrapper.action_is_static = static
        wrapper.action_name = name
        wrapper.action_url = url
        wrapper.allowed_methods = allowed
        wrapper.expected_data = list(signature(func).parameters.values())[2:]
        wrapper.responses = getattr(func, 'responses', {})
        return wrapper

    if wrapped is not None:
        return decorator(wrapped)
    return decorator


def response(http_response, description):
    def decorator(f):
        if getattr(f, 'responses', None) is None:
            f.responses = {}
        f.responses.update({http_response.status_code: description})
        return f
    return decorator


class ActionResourceMixin(object):
    def _get_actions(self):
        actions = []
        for name in dir(self):
            if name == 'urls':
                continue
            method = getattr(self, name)
            if is_action(method):
                actions.append((name, method))
        return actions

    def prepend_urls(self):
        urls = super().prepend_urls()
        action_methods = self._get_actions()

        for name, method in action_methods:
            action_name = method.action_name or name
            url_name = 'api_action_' + action_name
            action_url = method.action_url

            if action_url is not None:
                pattern = r'^{action_url}{slash}$'
                action_url = action_url.strip('/')

            elif method.action_is_static:
                pattern = r'^(?P<resource_name>{resource})/{name}{slash}$'
                url_name = 'api_action_static_' + action_name

            else:
                pattern = (r'^(?P<resource_name>{resource})/'
                           r'(?P<{detail_uri}>.*?)/{name}{slash}$')

            pattern = pattern.format(
                action_url=action_url,
                resource=self._meta.resource_name,
                detail_uri=self._meta.detail_uri_name,
                name=action_name, slash=trailing_slash()
            )
            urls.insert(0, url(pattern, self.json_args(self.wrap_view(name)), name=url_name))
        return urls

    @staticmethod
    def json_args(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            try:
                request.api = kwargs
                data = request.body.decode('utf-8')
                data = json.loads(data) if data else {}
                return view(request, **data)
            except ValueError:
                return HttpBadRequest()
        return wrapper

    def _handle_500(self, request, exception):
        if isinstance(exception, TypeError):
            return HttpBadRequest()

        return super()._handle_500(request, exception)

    def build_schema(self):
        data = super().build_schema()

        action_methods = self._get_actions()
        actions = []

        for name, method in action_methods:
            actions.append({name: {
                "allowed_http_methods": method.allowed_methods,
                "is_static": method.action_is_static,
                "expected_data": method.expected_data,
                "responses": method.responses
            }})

        data['actions'] = actions
        return data
