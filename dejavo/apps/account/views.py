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

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def post(self, request, format=None):
        # handle login process
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

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        logout(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JWTLoginHandler(APIView):

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def get(self, request, format=None):
        return self.post(request, format)

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

    def post(self, request, format=None):

        serializer = UpdateUserSerializer(request.user, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
