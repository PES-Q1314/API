from urllib.parse import urlparse
from api import settings
from django import http
try:
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
    XS_SHARING_ALLOW_CREDENTIALS = settings.XS_SHARING_ALLOW_CREDENTIALS
except:
    XS_SHARING_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['X-CSRFToken']
    XS_SHARING_ALLOW_CREDENTIALS = 'true'


class CORSMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            return self.process_response(request, http.HttpResponse())

        return None

    def process_response(self, request, response):
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        allow_origin = XS_SHARING_ALLOWED_ORIGINS[0]
        try:
            url = urlparse(request.META['HTTP_REFERER'])
            origin = "%s://%s" % (url.scheme, url.netloc)

            if settings.DEBUG or origin in XS_SHARING_ALLOWED_ORIGINS:
                allow_origin = origin
        except KeyError:
            pass

        response['Access-Control-Allow-Origin'] = allow_origin
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
        response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
        response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOW_CREDENTIALS

        return response
