from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q

from accept_checker.decorators import require_accept_formats, auth_required 
from jwt_auth.token import generate_jwt, refresh_jwt
from social.apps.django_app.utils import psa

from dejavo.apps.account.models import UserProfile
from dejavo.apps.zabo.models import Article

import json

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
def login_view(request):

    if request.user.is_authenticated():
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'Already logged in'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Already logged in'}
                    )

    if request.method == 'GET':
        # TODO create login page
        return HttpResponse('Login page')

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    if not username or not password:
        # invalid format
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'Invalid format'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(status = 400,
                    data = {'error' : 'Invalid format'}
                    )

    user = authenticate(username = username, password = password)

    if user is None:
        # login fail page. wrong password, username
        if request.ACCEPT_FORMAT == 'html':
            # TODO login fail page
            return HttpResponse(
                    status = 400,
                    content = 'Failed to login'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Failed to login'}
                    )

    if not user.is_active:
        # user inactive
        if request.ACCEPT_FORMAT == 'html':
            # XXX user blocked page??
            return HttpResponse(
                    status = 403,
                    content = 'User is blocked'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 403,
                    data = {'error' : 'User is blocked'}
                    )
    else:
        login(request, user)
        # login success
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponseRedirect(request.GET.get(REDIRECT_FIELD_NAME, '/')
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 200,
                    data = user.as_json()
                    )

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def logout_view(request):
    logout(request)
    if request.ACCEPT_FORMAT == 'html':
        return HttpResponse(
                status = 200,
                content = 'Successfully logout'
                )
    elif request.ACCEPT_FORMAT == 'json':
        return JsonResponse(
                status = 200,
                data = {'msg' : 'Successfully logout'}
                )

@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@csrf_exempt
def jwt_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if not username or not password:
        # invalid format
        return JsonResponse(status = 400, data = {'error' : 'Invalid format'})

    user = authenticate(username = username, password = password)

    if user is None:
        # login fail page. wrong password, username
        return JsonResponse(status = 400, data = {'error' : 'Failed to login'})

    if not user.is_active:
        # user inactive
        return JsonResponse(status = 403, data = {'error' : 'User is blocked'})
    
    try:
        user_token = generate_jwt(user)
        return JsonResponse(status = 200, data = user_token)
    except:
        return JsonReponse(status = 500, data = {'error' : 'Internal server error'})


@require_accept_formats(['application/json'])
@require_http_methods(['POST'])
@csrf_exempt
def jwt_refresh(request):
    user_token = request.POST.get('token', None)

    if user_token is None:
        return JsonResponse(status = 400, data = {'error' : 'Invalid format'})

    try:
        new_user_token = refresh_jwt(request.user, user_token)
        return JsonResponse(status = 200, data = new_user_token)
    except:
        return JsonReponse(status = 500, data = {'error' : 'Internal server error'})


@require_accept_formats(['application/json'])
@psa()
def auth_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(request.GET.get('access_token'))

    if user:
        login(request, user)
        return JsonResponse(status = 200, data = user.as_json())
    else:
        return JsonResponse(
                status = 401,
                data = { 'error' : 'User cannot be authorized' }
                )


@require_accept_formats(['text/html'])
@require_http_methods(['GET'])
@auth_required
def main(request):
    # User notification, owning article, history, else else else...
    # TODO create user page
    return HttpResponse(
            status = 200,
            content = 'User page'
            )

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
def create(request):
    # User creation page
    if request.user.is_authenticated():
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'User is already logged in'
                    )
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    content = 'User is already logged in'
                    )

    if request.method == 'GET':
        return HttpResponse(
                status = 200,
                content = 'User creating page'
                )

    # create user
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if not username or not email or not password:
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 400,
                    content = 'Invalid format'
                    )
        
        elif request.ACCEPT_FORMAT == 'json':
            return JsonResponse(
                    status = 400,
                    data = {'error' : 'Invalid format'}
                    )

    new_user  = get_user_model().objects.create_user(username, email, password)

    last_name = request.POST.get('lastname', '')
    first_name = request.POST.get('firstname', '')

    profile = new_user.profile
    profile.phone = request.POST.get('phone', '')
    profile.bio = request.POST.get('bio', '')

    profile.save()
    new_user.save()

    user = authenticate(username = username, password = password)
    login(request, user)

    if request.ACCEPT_FORMAT == 'html':
        response = HttpResponse(
                status = 201,
                content = 'User create complete')
        response['Location'] = '/account/edit/'
        return response

    elif request.ACCEPT_FORMAT == 'json':
        response = JsonResponse(
                status = 201,
                data = user.as_json()
                )
        response['Location'] = '/account/edit/'
        return response

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['POST', 'GET'])
@auth_required
def edit(request):
    # User profile editing page
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    if requset.method == 'GET':
        return HttpResponse(
                status = 200,
                content = 'User editing page'
                )
    # TODO
    # password
    # email
    # profile bio
    # profile image
    # profile phone

    return HttpResponse(__name__ + '.' + sys._getframe().f_code.co_name) 

@require_accept_formats(['text/html', 'application/json'])
@require_http_methods(['GET'])
def show_user(request, username):

    try:
        user_info = get_user_model().objects.get(username = username).as_json()
        if request.ACCEPT_FORMAT == 'html':
            # TODO Create user page
            return HttpResponse(
                    status = 200,
                    content = 'Show user page'
                    )
        else:
            # TODO add user's other information such as articles
            return JsonResponse(
                    status = 200,
                    data = user_info
                    )
    except get_user_model().DoesNotExist:
        if request.ACCEPT_FORMAT == 'html':
            return HttpResponse(
                    status = 404,
                    content = 'User does not exist'
                    )
        else:
            return JsonResponse(
                    status = 404,
                    data = {'error' : 'User does not exist'}
                    )

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def search_user(request):

    query = request.GET.get('q', None)
    page = int(request.GET.get('page', 0))
    count = int(request.GET.get('count', 10))

    start = page * count
    end = start + count

    if not query:
        return JsonResponse(
                status = 400,
                data = { 'error' : 'Parameter \'q\' should be given' }
                )

    _User = get_user_model()
    user_list = _User.objects.filter(Q(username__icontains = query) |
            Q(first_name__icontains = query) | Q(last_name__icontains = query))[start:end]
    user_list_json = map(lambda x : x.as_json(), user_list)

    return JsonResponse(
        status = 200,
        data = { 'result' : user_list_json }
        )


@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def participate(request, article_id):

    try:
        article = Article.objects.get(id = article_id)
        check = UserProfile.objects.filter(user = request.user,
                participation__exact = article).exists()

        if check:
            return JsonResponse(status = 400,
                    data = { 'error' : 'User already participate the article' }
                    )

        request.user.profile.participation.add(article)
        request.user.profile.save()
        return JsonResponse(status = 200, data = request.user.as_json())

    except Article.DoesNotExist:
        return JsonResponse(
            status = 400,
            data = { 'error' : 'Article does not exist' }
            )

@require_accept_formats(['application/json'])
@require_http_methods(['GET'])
@auth_required
def unparticipate(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
        check = UserProfile.objects.filter(user = request.user,
                participation__exact = article).exists()

        if check:
            request.user.profile.participation.remove(article)
            request.user.profile.save()
            return JsonResponse(status = 200, data = request.user.as_json())

        return JsonResponse(status = 400,
                data = { 'error' : 'User is not participating the article' }
                )

    except Article.DoesNotExist:
        return JsonResponse(
            status = 400,
            data = { 'error' : 'Article does not exist' }
            )
