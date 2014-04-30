from tastypie.authentication import SessionAuthentication


class SystemAuthentication(SessionAuthentication):
    def is_authenticated(self, request, check_csrf=True, **kwargs):
        return request.user.is_authenticated()