from apps.cuentas.models import SystemUser
from core.action import ActionResourceMixin, action, response
from core.http import HttpOK
from django.contrib import auth
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpCreated
from tastypie.resources import ModelResource


class SystemUserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(pk=bundle.request.user.pk)

    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized()

    def create_detail(self, object_list, bundle):
        raise Unauthorized()

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user



class SystemUserResource(ActionResourceMixin, ModelResource):

    class Meta:
        queryset = SystemUser.objects.all()
        excludes = ['password']
        authentication = SessionAuthentication()
        authorization = SystemUserAuthorization()

        # Only registering features are allowed for lists
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put', 'delete', 'patch']

    @action(allowed=('post',), static=True)
    @response(HttpOK, "Login successful")
    @response(HttpUnauthorized, "Login failed")
    @response(HttpForbidden, "User is inactive")
    def login(self, request, username, password):
        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise ImmediateHttpResponse(HttpUnauthorized())
        if not user.is_active:
            raise ImmediateHttpResponse(HttpForbidden())

        auth.login(request, user)
        return self.create_response(request, self._serialize_user(request, user))

    @action(allowed=('post',), static=True)
    @response(HttpCreated, "Registration successful")
    def register(self, request, username, email, password):
        user = SystemUser.objects.create_user(username=username, email=email, password=password)
        return self.create_response(request, self._serialize_user(request, user), response_class=HttpCreated)

    @action(allowed=('post',), static=True, login_required=True)
    @response(HttpOK, "Logout successful")
    @response(HttpUnauthorized, "User is not logged in")
    def logout(self, request):
        auth.logout(request)
        return self.create_response(request, {})

    @action(allowed=('get',), static=True, login_required=True)
    @response(HttpOK, "User is logged in")
    @response(HttpUnauthorized, "User is not logged in")
    def logincheck(self, request):
        return self.create_response(request, self._serialize_user(request, request.user))
