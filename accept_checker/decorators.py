# -*- coding: utf-8 -*-

from functools import wraps

from django.utils.decorators import available_attrs
from django.http import HttpResponse, JsonResponse


def require_accept_formats(formats):
    # View decorator that sets multiple response headers.
    # 
    # Example:
    # @headers({'Connection': 'close', 'X-Powered-By': 'Django'})
    # def view(request, ...):
    #     ....
    #
    # For class-based views use:
    # @method_decorator(headers({'Connection': 'close',
    #                            'X-Powered-By': 'Django'})
    # def get(self, request, ...)
    #     ...
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            for header in request.HEADER_LIST:
                if header in formats:
                    return func(request, *args, **kwargs)

            return HttpResponse(
                    status = 406,
                    content = 'Unsupported Accept type',
                    )
        return inner
    return decorator


def check_authentication(func):
    def checker(request, *args, **kwargs):
        if not request.user.is_authenticated():
            if request.ACCEPT_FORMAT == 'html':
                return HttpResponse(
                        status = 401,
                        content = 'User does not authorized'
                        )
            elif request.ACCEPT_FORMAT == 'json':
                return JsonResponse(
                        status = 401,
                        data = {
                            'error' : 'User does not authorized'
                            },
                        )
            else:   # Set HttpResponse as default
                return HttpResponse(
                        status = 401,
                        content = 'User does not authorized'
                        )
        else:
            return func(request, *args, **kwargs)
    return checker
