from django.http import HttpResponse


class HttpOK(HttpResponse):
    status_code = 200