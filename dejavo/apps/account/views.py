from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_decode_handler

from dejavo.apps.account.serializers import UserSerializer, UpdateUserSerializer, \
                                            UserSessionSerializer

from datetime import datetime


def main(request):
    return HttpResponse("<p>apps.account.views.main</p><p>/account/</p>")


class SessionLoginHandler(APIView):
    """**SessionLoginHandler** class create sessions for users who try to login with
    common browsers.

    ## Note ##
    + Only **POST** method is allowed for login process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/login.json"
                -d '{"username" : "elaborate", "password" : "1234"}'
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "elaborate",
            "email": "a@c.com",
            "last_name" : "Ahn",
            "first_name" : "Beunguk"
        }
        /* Invalid ID or password - 401 */
        {
            "non_field_errors": ["Unable to login with provided credentials."]
        }
        /* Bad request - 400 */
        {
            "username": ["This field is required."],
            "password": ["This field is required."]
        }
    """

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def post(self, request, format=None):
        serializer = UserSessionSerializer(data=request.DATA)

        if serializer.is_valid():
            user = serializer.object
            user_serializer = UserSerializer(user)
            login(request, user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)


class SessionLogoutHandler(APIView):
    """**SessionLogoutHandler** class destroy sessions for users who request.

    ## Note ##
    + Only **GET** method is allowed for logout process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/logout.json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "elaborate",
            "email": "a@c.com",
            "last_name" : "Ahn",
            "first_name" : "Beunguk"
        }
        /* User is not logged in - 403 */
        {
            "detail" : "Authentication credentials were not provided."
        }
    """

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        logout(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JWTLoginHandler(APIView):
    """**JWTLoginHandler** class auth token (Javascript Web Token) for user
    login.

    ## Note ##
    + Only **POST** method is allowed for logout process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/auth_token.json"
                -d '{"username" : "elaborate", "password" : "1234"}'
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On Success - 200 */
        {
            "token" : "{token_string}",
            "expire" : "2014-11-20T19:16:52"
        }
        /* Invalid ID or Password - 401 */
        {
            "non_field_errors": ["Unable to login with provided credentials."]
        }
    """

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def post(self, request, format=None):

        serializer = JSONWebTokenSerializer(data=request.DATA)

        if serializer.is_valid():
            token = serializer.object['token']
            pay_load = jwt_decode_handler(token)

            return Response({
                'token' : token,
                'expire' : datetime.fromtimestamp(pay_load['exp'])
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordHandler(APIView):
    """**PasswordHandler** class handles password change request
    login.

    ## Note ##
    + Only **POST** method is allowed for changing password.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/change_password.json"
                -d '{"password" : "{new_password}"',
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "elaborate",
            "email": "a@c.com",
            "last_name" : "Ahn",
            "first_name" : "Beunguk"
        }
        /* User is not logged in - 403 */
        {
            "detail" : "Authentication credentials were not provided."
        }
    """

    def post(self, request, format=None):

        serializer = UpdateUserSerializer(request.user, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
