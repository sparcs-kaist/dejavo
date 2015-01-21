# -*- coding: utf-8 -*-

from functools import wraps

from django.utils.decorators import available_attrs
from django.http import HttpResponse


def require_accept_format(_format):
    # View decorator that sets a response header.
    # 
    # Example:
    # @header('X-Powered-By', 'Django')
    # def view(request, ...):
    #     ....
    #
    # For class-based views use:
    # @method_decorator(header('X-Powered-By', 'Django'))
    # def get(self, request, ...)
    #     ...
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if _format in request.HEADER_LIST:
                return func(request, *args, **kwargs)

            return HttpResponse(
                    status = 406,
                    content = 'Unsupported Accept type',
                    )
        return inner
    return decorator


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
