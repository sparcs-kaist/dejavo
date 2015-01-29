# -*- coding: utf-8 -*-

from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
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

def user_passes_auth(test_func, redirect=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            if request.ACCEPT_FORMAT == 'json':
                return JsonResponse(
                        status = 401,
                        data = {
                            'error' : 'User does not authorized'
                            },
                        )
            elif request.ACCEPT_FORMAT == 'html':
                if not redirect:
                    return HttpResponse(
                            status = 401,
                            content = 'User does not authorized'
                            )
                else:
                    path = request.build_absolute_uri()
                    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                    # If the login url is the same scheme and net location then just
                    # use the path as the "next" url.
                    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                    current_scheme, current_netloc = urlparse(path)[:2]
                    if ((not login_scheme or login_scheme == current_scheme) and
                            (not login_netloc or login_netloc == current_netloc)):
                        path = request.get_full_path()
                    from django.contrib.auth.views import redirect_to_login
                    return redirect_to_login(
                        path, resolved_login_url, redirect_field_name)
            else:
                return HttpResponse(
                        status = 401,
                        content = 'User does not authorized'
                        )
        return _wrapped_view
    return decorator

def auth_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, redirect=True, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_auth(
        lambda u: u.is_authenticated(),
        redirect=redirect,
        redirect_field_name=redirect_field_name,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
