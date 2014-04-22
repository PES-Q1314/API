from django.conf import settings
from django.middleware.csrf import _sanitize_token
from django.utils.crypto import constant_time_compare
from tastypie.authentication import SessionAuthentication


class SystemAuthentication(SessionAuthentication):
    def is_authenticated(self, request, check_csrf=True, **kwargs):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return request.user.is_authenticated()

        if not check_csrf or getattr(request, '_dont_enforce_csrf_checks', False):
            return request.user.is_authenticated()

        csrf_token = _sanitize_token(request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))
        request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

        if not constant_time_compare(request_csrf_token, csrf_token):
            return False

        return request.user.is_authenticated()